#!/usr/bin/env bash
set -euo pipefail

# Запуск ComfyUI с красивым выводом через Rich library
# Использование точно такое же как run_comfy.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="$ROOT_DIR/.venv/bin/python"
RICH_LAUNCHER="$ROOT_DIR/run_comfy_rich.py"

usage() {
  cat <<EOF
🎨 ComfyUI Beautiful Launcher
Использование: ./run_comfy_beautiful.sh [опции]

Опции:
  --single GPU_ID     Использовать один GPU (например, 0 или 1)
  --dual              Использовать два GPU 0 и 1 (по умолчанию)
  --gpus LIST         Явно указать CUDA_VISIBLE_DEVICES (например, "0,1" или "1")
  --cpu               Запуск только на CPU (CUDA не используется)
  --port PORT         Порт HTTP (по умолчанию 8188)
  --manager           Включить ComfyUI-Manager (--enable-manager)
  -h, --help          Показать эту справку

Этот скрипт использует Rich library для красивого форматированного вывода.
EOF
}

if [[ ! -x "$VENV_PY" ]]; then
  echo "❌ Не найден Python в venv: $VENV_PY" >&2
  echo "Создайте окружение: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

# Проверяем наличие rich (через python -m pip, чтобы обойти битые shebang'и pip)
if ! "$VENV_PY" - <<'PY' 2>/dev/null; then
import importlib.util
import sys
sys.exit(0 if importlib.util.find_spec("rich") else 1)
PY
then
  echo "📦 Installing rich library..."
  "$VENV_PY" -m pip install rich -q
fi

MODE="dual"
GPUS="0,1"
PORT="8188"
USE_CPU=false
EXTRA_ARGS=()
ENABLE_MANAGER=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --single)
      MODE="single"
      if [[ $# -lt 2 ]]; then
        echo "❌ Для --single нужно указать номер GPU (например, 0)." >&2
        exit 1
      fi
      GPUS="$2"
      shift 2
      ;;
    --dual)
      MODE="dual"
      GPUS="0,1"
      shift
      ;;
    --gpus)
      if [[ $# -lt 2 ]]; then
        echo "❌ Для --gpus нужно указать список, например: 0,1" >&2
        exit 1
      fi
      MODE="custom"
      GPUS="$2"
      shift 2
      ;;
    --cpu)
      USE_CPU=true
      shift
      ;;
    --port)
      if [[ $# -lt 2 ]]; then
        echo "❌ Для --port нужно указать номер порта." >&2
        exit 1
      fi
      PORT="$2"
      shift 2
      ;;
    --manager)
      ENABLE_MANAGER=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        EXTRA_ARGS+=("$1")
        shift
      done
      ;;
    *)
      EXTRA_ARGS+=("$1")
      shift
      ;;
  esac
done

cd "$ROOT_DIR"

# Устанавливаем переменные окружения
if [[ "$USE_CPU" == true ]]; then
  unset CUDA_VISIBLE_DEVICES
  echo "🖥️  Запуск на CPU (без CUDA)"
else
  export CUDA_VISIBLE_DEVICES="$GPUS"
fi

if [[ "$ENABLE_MANAGER" == true ]]; then
  EXTRA_ARGS+=("--enable-manager")
fi

# Запускаем через Rich launcher
exec "$VENV_PY" "$RICH_LAUNCHER" --port "$PORT" "${EXTRA_ARGS[@]}"
