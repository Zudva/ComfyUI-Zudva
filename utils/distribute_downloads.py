import argparse
import fnmatch
import shutil
from pathlib import Path

import yaml

try:
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Confirm
    from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn
except Exception:  # Rich не обязателен — при отсутствии просто используем print
    Console = None
    Table = None
    Confirm = None
    Progress = None


DEFAULT_DOWNLOADS = Path.home() / "Downloads"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODELS_DIR = PROJECT_ROOT / "models"
TEMPLATE_PATH = PROJECT_ROOT / "model_paths_template.yaml"


# Простые эвристики по имени файла
CHECKPOINT_HINTS = {"sd", "sdxl", "stable-diffusion", "checkpoint", "model", "unet", "flux", "aura", "sd3"}
VAE_HINTS = {"vae", "decoder"}
LORA_HINTS = {"lora", "locon", "loha"}
EMB_HINTS = {"embedding", "emb", "ti_"}
CONTROLNET_HINTS = {"controlnet", "t2i"}
UPSCALE_HINTS = {"esrgan", "upscale", "swin", "real-esrgan", "4x"}


console = Console() if Console is not None else None

_TEMPLATE_CACHE: dict[str, list[str]] | None = None


def load_template_mapping() -> dict[str, list[str]]:
    """Загрузка шаблона путей из YAML.

    Структура файла: {subdir: [pattern1, pattern2, ...]}.
    """

    global _TEMPLATE_CACHE
    if _TEMPLATE_CACHE is not None:
        return _TEMPLATE_CACHE

    if not TEMPLATE_PATH.exists():
        _TEMPLATE_CACHE = {}
        return _TEMPLATE_CACHE

    try:
        data = yaml.safe_load(TEMPLATE_PATH.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # pragma: no cover - защитный код
        print(f"[WARN] Не удалось прочитать {TEMPLATE_PATH}: {exc}")
        _TEMPLATE_CACHE = {}
        return _TEMPLATE_CACHE

    if not isinstance(data, dict):
        _TEMPLATE_CACHE = {}
        return _TEMPLATE_CACHE

    # нормализуем к виду dict[str, list[str]]
    mapping: dict[str, list[str]] = {}
    for subdir, patterns in data.items():
        if isinstance(patterns, str):
            mapping[str(subdir)] = [patterns]
        elif isinstance(patterns, (list, tuple)):
            mapping[str(subdir)] = [str(p) for p in patterns]
    _TEMPLATE_CACHE = mapping
    return _TEMPLATE_CACHE


def guess_from_template(path: Path) -> str | None:
    """Определить целевую подпапку по YAML-шаблону (имя файла по glob-паттернам)."""

    mapping = load_template_mapping()
    if not mapping:
        return None

    name = path.name
    for subdir, patterns in mapping.items():
        for pattern in patterns:
            if fnmatch.fnmatch(name, pattern):
                return subdir
    return None


def guess_target_subdir(path: Path) -> str | None:
    """Грубое определение типа модели по имени файла.

    Возвращает относительный путь в `models/` или None, если не удалось угадать.
    """

    # Сначала пробуем явно указанный шаблон
    template_sub = guess_from_template(path)
    if template_sub is not None:
        return template_sub

    name = path.stem.lower()
    suffix = path.suffix.lower()

    # Embeddings — обычно маленькие .pt / .bin
    if suffix in {".pt", ".bin", ".safetensors"}:
        if any(h in name for h in EMB_HINTS):
            return "embeddings"

    # VAE
    if suffix in {".pt", ".pth", ".safetensors"}:
        if any(h in name for h in VAE_HINTS):
            return "vae"

    # LoRA
    if suffix == ".safetensors":
        if any(h in name for h in LORA_HINTS):
            return "loras"

    # ControlNet / T2I Adapter
    if suffix == ".safetensors":
        if any(h in name for h in CONTROLNET_HINTS):
            return "controlnet"

    # Upscale модели
    if suffix in {".pth", ".safetensors"}:
        if any(h in name for h in UPSCALE_HINTS):
            return "upscale_models"

    # Чекпоинты (основные SD/SDXL/Flux и т.п.)
    if suffix in {".safetensors", ".ckpt"}:
        if any(h in name for h in CHECKPOINT_HINTS):
            return "checkpoints"
        # по умолчанию все крупные .safetensors считаем чекпоинтом
        return "checkpoints"

    return None


def iter_downloaded_files(downloads_dir: Path):
    for p in downloads_dir.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".safetensors", ".ckpt", ".pt", ".pth", ".bin"}:
            continue
        yield p


def _iter_models(models_dir: Path):
    """Итерировать все файлы внутри models/."""

    for p in models_dir.rglob("*"):
        if p.is_file():
            yield p


def _print_plan(actions: list[tuple[Path, Path]], move: bool) -> None:
    if console and Table is not None:
        table = Table(title="План раскладки моделей", show_lines=True)
        table.add_column("#", justify="right", style="cyan", no_wrap=True)
        table.add_column("Действие", style="magenta")
        table.add_column("Из", style="yellow")
        table.add_column("В", style="green")

        op = "MOVE" if move else "COPY"
        for idx, (src, dst) in enumerate(actions, start=1):
            table.add_row(str(idx), op, str(src), str(dst))

        console.print(table)
    else:
        print("План действий:")
        for src, dst in actions:
            op = "MOVE" if move else "COPY"
            print(f"  [{op}] {src} -> {dst}")


def _interactive_filter_actions(actions: list[tuple[Path, Path]], move: bool) -> list[tuple[Path, Path]]:
    """Интерактивно выбрать, какие действия применять.

    Возвращает отфильтрованный список действий.
    """

    if not actions:
        return actions

    if console is None or Confirm is None:
        # Rich недоступен — просто возвращаем всё как есть
        return actions

    console.print("[bold cyan]Интерактивный режим[/bold cyan]: выберите, что делать с файлами.")
    console.print(
        "[dim]Варианты ответа:[/dim]\n"
        "  [green]a[/green] — сразу применить ко всем файлам\n"
        "  [red]s[/red] — пропустить все файлы\n"
        "  [cyan]Enter[/cyan] — перейти к пофайловому выбору (по умолчанию)"
    )

    choice = console.input("[bold yellow]Режим ([a] / [s] / Enter): [/bold yellow]").strip().lower()
    if choice == "s":
        return []
    if choice == "a":
        return actions

    # По-умолчанию — спрашиваем по каждому
    filtered: list[tuple[Path, Path]] = []
    op = "переместить" if move else "скопировать"
    apply_all = False

    for src, dst in actions:
        if apply_all:
            filtered.append((src, dst))
            continue

        console.print(f"\n[cyan]{src.name}[/cyan]")
        console.print(f"  из: [yellow]{src}[/yellow]")
        console.print(f"  в:  [green]{dst}[/green]")
        console.print(
            "[dim]Варианты:[/dim] "
            "[green]y[/green] — да, "
            "[red]n[/red] — нет, "
            "[green]a[/green] — да для всех оставшихся, "
            "[red]s[/red] — пропустить остальные и закончить"
        )

        answer = console.input(
            f"[bold yellow]{op.capitalize()} этот файл? ([y]/n/a/s): [/bold yellow]"
        ).strip().lower()

        if answer in {"", "y", "yes"}:
            filtered.append((src, dst))
        elif answer == "a":
            filtered.append((src, dst))
            apply_all = True
        elif answer == "s":
            break
        else:
            # Любой другой ответ трактуем как "нет" для этого файла
            continue

    return filtered


def _fix_existing_models(models_dir: Path, dry_run: bool) -> None:
    """Переложить уже существующие файлы в models/ согласно шаблону.

    Ищет файлы во всех подпапках `models/`, сверяет их имя с
    `model_paths_template.yaml` и при необходимости переносит в целевую
    подпапку. Уже лежащие "правильно" файлы не трогаются.
    """

    mapping = load_template_mapping()
    if not mapping:
        print("[INFO] Шаблон model_paths_template.yaml не найден или пуст, фиксировать нечего.")
        return

    models_dir = models_dir or DEFAULT_MODELS_DIR
    models_dir.mkdir(parents=True, exist_ok=True)

    planned: list[tuple[Path, Path]] = []

    for src in _iter_models(models_dir):
        rel = src.relative_to(models_dir)
        # пропускаем служебные файлы-заглушки
        if rel.name.startswith("put_"):
            continue

        sub_from_template = guess_from_template(src)
        if sub_from_template is None:
            continue

        target_dir = models_dir / sub_from_template
        dst = target_dir / src.name

        # уже на правильном месте
        if src == dst:
            continue

        # если по какой-то причине файл уже лежит в целевом месте — не трогаем
        if dst.exists():
            print(f"[SKIP] Целевой файл уже существует и будет сохранён: {dst}")
            continue

        planned.append((src, dst))

    if not planned:
        print("[INFO] Несогласованных файлов, подпадающих под шаблон, не найдено.")
        return

    print("План переноса существующих файлов по шаблону:")
    for src, dst in planned:
        print(f"  MOVE {src} -> {dst}")

    if dry_run:
        print("[DRY-RUN] Ничего не изменено. Запустите без --dry-run для применения.")
        return

    for src, dst in planned:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

    print(f"[DONE] Переложено файлов: {len(planned)}")


def distribute(downloads_dir: Path, models_dir: Path, move: bool, dry_run: bool, interactive: bool) -> None:
    # Отладочная информация по путям
    if console:
        console.print(f"[bold]Downloads:[/bold] [cyan]{downloads_dir}[/cyan]")
        console.print(f"[bold]Models:[/bold]    [green]{models_dir}[/green]")
    else:
        print(f"Downloads: {downloads_dir}")
        print(f"Models:    {models_dir}")

    if not downloads_dir.exists():
        print(f"[WARN] Downloads dir not found: {downloads_dir}")
        return

    models_dir.mkdir(parents=True, exist_ok=True)

    actions: list[tuple[Path, Path]] = []

    for src in iter_downloaded_files(downloads_dir):
        sub = guess_target_subdir(src)
        if sub is None:
            print(f"[SKIP] Не удалось определить тип: {src}")
            continue

        target_dir = models_dir / sub
        target_dir.mkdir(parents=True, exist_ok=True)
        dst = target_dir / src.name

        if dst.exists():
            print(f"[SKIP] Уже существует: {dst}")
            continue

        actions.append((src, dst))

    if not actions:
        print("[INFO] Подходящих новых файлов не найдено.")
        return

    _print_plan(actions, move)

    if interactive and not dry_run:
        actions = _interactive_filter_actions(actions, move)
        if not actions:
            print("[INFO] Все действия были пропущены в интерактивном режиме.")
            return

    if dry_run:
        print("[DRY-RUN] Ничего не изменено. Запустите без --dry-run, чтобы применить.")
        return

    total = len(actions)

    if console and Progress is not None and total > 0:
        op_label = "Перемещение" if move else "Копирование"
        progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        )

        with progress:
            task_id = progress.add_task(f"{op_label} файлов", total=total)
            for src, dst in actions:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if move:
                    shutil.move(str(src), str(dst))
                else:
                    shutil.copy2(src, dst)
                progress.update(task_id, advance=1, description=f"{op_label}: {src.name}")
    else:
        # Простой текстовый прогресс без rich
        for idx, (src, dst) in enumerate(actions, start=1):
            print(f"[{idx}/{total}] {src} -> {dst}")
            dst.parent.mkdir(parents=True, exist_ok=True)
            if move:
                shutil.move(str(src), str(dst))
            else:
                shutil.copy2(src, dst)

    print(f"[DONE] Обработано файлов: {len(actions)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Автоматически разложить скачанные веса из каталога Downloads "
            "по подпапкам в ComfyUI/models"),
    )
    parser.add_argument(
        "--downloads-dir",
        type=Path,
        default=DEFAULT_DOWNLOADS,
        help=f"Папка с загрузками (по умолчанию: {DEFAULT_DOWNLOADS})",
    )
    parser.add_argument(
        "--models-dir",
        type=Path,
        default=DEFAULT_MODELS_DIR,
        help=f"Папка models ComfyUI (по умолчанию: {DEFAULT_MODELS_DIR})",
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Перемещать файлы (по умолчанию копируем)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать, что будет сделано, без изменений",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Интерактивный режим с подтверждением (rich)",
    )
    parser.add_argument(
        "--fix-existing",
        action="store_true",
        help=(
            "Переложить уже существующие файлы внутри models/ согласно "
            "model_paths_template.yaml, без использования Downloads"
        ),
    )

    args = parser.parse_args()

    if args.fix_existing:
        # Фиксация расположения уже разложенных файлов по шаблону
        _fix_existing_models(args.models_dir, dry_run=args.dry_run)
    else:
        distribute(
            downloads_dir=args.downloads_dir,
            models_dir=args.models_dir,
            move=bool(args.move),
            dry_run=bool(args.dry_run),
            interactive=bool(args.interactive),
        )


if __name__ == "__main__":
    main()
