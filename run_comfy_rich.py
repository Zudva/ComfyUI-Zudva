#!/usr/bin/env python3
"""
ComfyUI Rich Launcher - красивый запуск с форматированным выводом
"""
import os
import sys
import subprocess
import re
import signal
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich import box
except ImportError:
    print("❌ Rich library не установлена. Устанавливаю...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich import box

console = Console()

# Состояние загрузки
loading_state = {
    "vram": None,
    "ram": None,
    "pytorch": None,
    "device": None,
    "python": None,
    "comfyui": None,
    "frontend": None,
    "port": None,
    "cuda_devices": None,
    "custom_nodes": [],
    "warnings": [],
    "errors": [],
    "server_started": False
}


def parse_log_line(line):
    """Парсинг строк лога ComfyUI"""
    # VRAM info
    if "Total VRAM" in line:
        match = re.search(r"Total VRAM (\d+) MB, total RAM (\d+) MB", line)
        if match:
            loading_state["vram"] = int(match.group(1))
            loading_state["ram"] = int(match.group(2))
    
    # PyTorch version
    elif "pytorch version:" in line:
        match = re.search(r"pytorch version: ([\d.+\w]+)", line)
        if match:
            loading_state["pytorch"] = match.group(1)
    
    # Device info
    elif "Device:" in line:
        match = re.search(r"Device: (.+)", line)
        if match:
            loading_state["device"] = match.group(1).strip()
    
    # Python version
    elif "Python version:" in line:
        match = re.search(r"Python version: (.+)", line)
        if match:
            loading_state["python"] = match.group(1).strip()
    
    # ComfyUI version
    elif "ComfyUI version:" in line:
        match = re.search(r"ComfyUI version: ([\d.]+)", line)
        if match:
            loading_state["comfyui"] = match.group(1)
    
    # Frontend version
    elif "ComfyUI frontend version:" in line:
        match = re.search(r"ComfyUI frontend version: ([\d.]+)", line)
        if match:
            loading_state["frontend"] = match.group(1)
    
    # CUDA devices
    elif "CUDA_VISIBLE_DEVICES" in line:
        match = re.search(r"CUDA_VISIBLE_DEVICES[=:]?\s*(\S+)", line)
        if match:
            loading_state["cuda_devices"] = match.group(1)
    
    # Port
    elif "Порт:" in line or "http://127.0.0.1:" in line:
        match = re.search(r"(\d{4,5})", line)
        if match:
            loading_state["port"] = match.group(1)
    
    # Server started
    elif "To see the GUI go to:" in line:
        loading_state["server_started"] = True
    
    # Custom nodes
    elif re.match(r"\s+[\d.]+ seconds: .+custom_nodes", line):
        match = re.search(r"([\d.]+) seconds: (.+)", line)
        if match:
            loading_state["custom_nodes"].append({
                "time": float(match.group(1)),
                "path": match.group(2).strip()
            })
    
    # Warnings
    elif "WARNING" in line or "Warning:" in line:
        loading_state["warnings"].append(line.strip())
    
    # Errors (но не критичные)
    elif "ERROR" in line and "DEPRECATION" not in line:
        loading_state["errors"].append(line.strip())


def create_header_panel():
    """Создание заголовка"""
    title = Text()
    title.append("🎨 ", style="bold magenta")
    title.append("ComfyUI", style="bold cyan")
    title.append(" Launcher", style="bold white")
    
    subtitle = Text(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
    
    header = Text.assemble(title, "\n", subtitle)
    return Panel(header, box=box.DOUBLE, border_style="cyan")


def create_system_info_table():
    """Создание таблицы с системной информацией"""
    table = Table(title="System Information", box=box.ROUNDED, border_style="green")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")
    
    if loading_state["python"]:
        table.add_row("🐍 Python", loading_state["python"])
    
    if loading_state["pytorch"]:
        table.add_row("🔥 PyTorch", loading_state["pytorch"])
    
    if loading_state["comfyui"]:
        table.add_row("🎨 ComfyUI", loading_state["comfyui"])
    
    if loading_state["frontend"]:
        table.add_row("🌐 Frontend", loading_state["frontend"])
    
    if loading_state["device"]:
        table.add_row("🎮 Device", loading_state["device"])
    
    if loading_state["cuda_devices"]:
        table.add_row("🔢 CUDA GPUs", loading_state["cuda_devices"])
    
    if loading_state["vram"]:
        vram_gb = loading_state["vram"] / 1024
        table.add_row("💾 VRAM", f"{vram_gb:.2f} GB ({loading_state['vram']} MB)")
    
    if loading_state["ram"]:
        ram_gb = loading_state["ram"] / 1024
        table.add_row("🧠 RAM", f"{ram_gb:.2f} GB ({loading_state['ram']} MB)")
    
    if loading_state["port"]:
        url = f"http://127.0.0.1:{loading_state['port']}"
        table.add_row("🌐 Server URL", url)
    
    return table


def create_custom_nodes_table():
    """Создание таблицы с загруженными custom nodes"""
    if not loading_state["custom_nodes"]:
        return None
    
    table = Table(title="Custom Nodes", box=box.SIMPLE, border_style="blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Time", style="magenta", justify="right", width=8)
    table.add_column("Path", style="cyan")
    
    for idx, node in enumerate(loading_state["custom_nodes"][:10], 1):  # Показываем первые 10
        time_str = f"{node['time']:.1f}s"
        path = node['path'].replace('/media/zudva/git/git/ComfyUI/custom_nodes/', '')
        table.add_row(str(idx), time_str, path)
    
    if len(loading_state["custom_nodes"]) > 10:
        table.add_row("...", "...", f"... and {len(loading_state['custom_nodes']) - 10} more")
    
    return table


def create_warnings_panel():
    """Создание панели с предупреждениями"""
    if not loading_state["warnings"]:
        return None
    
    text = Text()
    for warning in loading_state["warnings"][:5]:  # Первые 5 предупреждений
        # Сокращаем длинные пути
        warning = warning.replace('/media/zudva/git/git/ComfyUI/', '')
        text.append("⚠️  ", style="yellow")
        text.append(warning[:100] + "...\n" if len(warning) > 100 else warning + "\n", style="dim")
    
    if len(loading_state["warnings"]) > 5:
        text.append(f"\n... and {len(loading_state['warnings']) - 5} more warnings", style="dim italic")
    
    return Panel(text, title="⚠️  Warnings", border_style="yellow", box=box.ROUNDED)


def create_status_panel():
    """Создание панели статуса"""
    if loading_state["server_started"]:
        status = Text("✅ Server is RUNNING", style="bold green")
        url = f"http://127.0.0.1:{loading_state['port']}" if loading_state["port"] else "http://127.0.0.1:8188"
        status.append(f"\n\n🌐 Open: {url}", style="cyan underline")
        status.append("\n\n💡 Press Ctrl+C to stop", style="dim")
        return Panel(status, title="Status", border_style="green", box=box.HEAVY)
    else:
        status = Text("⏳ Loading ComfyUI...", style="bold yellow")
        return Panel(status, title="Status", border_style="yellow", box=box.HEAVY)


def display_dashboard():
    """Отображение полной панели управления"""
    console.clear()
    console.print(create_header_panel())
    console.print()
    
    # Системная информация
    console.print(create_system_info_table())
    console.print()
    
    # Custom nodes
    nodes_table = create_custom_nodes_table()
    if nodes_table:
        console.print(nodes_table)
        console.print()
    
    # Warnings
    warnings_panel = create_warnings_panel()
    if warnings_panel:
        console.print(warnings_panel)
        console.print()
    
    # Статус
    console.print(create_status_panel())


def run_comfyui(args):
    """Запуск ComfyUI с перехватом вывода"""
    root_dir = Path(__file__).parent
    venv_python = root_dir / ".venv" / "bin" / "python"
    
    if not venv_python.exists():
        console.print("[red]❌ Python venv не найден![/red]")
        console.print(f"Ожидался: {venv_python}")
        sys.exit(1)
    
    # Формируем команду
    cmd = [str(venv_python), "main.py"] + args
    
    # Запускаем процесс
    console.print("[cyan]🚀 Starting ComfyUI...[/cyan]\n")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=str(root_dir),
        env=os.environ.copy()
    )
    
    def signal_handler(sig, frame):
        console.print("\n[yellow]⏹️  Stopping ComfyUI...[/yellow]")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    last_update = datetime.now()
    dashboard_shown = False
    
    try:
        for line in process.stdout:
            line = line.rstrip()
            if not line:
                continue
            
            # Парсим строку
            parse_log_line(line)
            
            # Обновляем дашборд после старта сервера или раз в секунду
            now = datetime.now()
            if loading_state["server_started"] and not dashboard_shown:
                display_dashboard()
                dashboard_shown = True
            elif (now - last_update).total_seconds() > 1:
                if loading_state["python"]:  # Если уже есть данные
                    display_dashboard()
                last_update = now
            
            # Также выводим сырой лог в файл для отладки
            # Можно раскомментировать если нужно
            # console.print(f"[dim]{line}[/dim]")
        
        process.wait()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Interrupted by user[/yellow]")
        process.terminate()
        sys.exit(0)


def main():
    """Главная функция"""
    # Показываем стартовую заставку
    console.print(create_header_panel())
    console.print()
    
    # Передаем аргументы в ComfyUI
    args = sys.argv[1:]
    
    run_comfyui(args)


if __name__ == "__main__":
    main()
