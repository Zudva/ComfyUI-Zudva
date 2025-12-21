#!/usr/bin/env bash
set -euo pipefail

# Запуск ComfyUI из локального venv с выбором одного или двух GPU.
# Примеры:
#   ./run_comfy.sh                    # использовать две GPU 0,1 (по умолчанию)
#   ./run_comfy.sh --single 0         # только GPU 0
#   ./run_comfy.sh --single 1         # только GPU 1
#   ./run_comfy.sh --dual             # GPU 0 и 1
#   ./run_comfy.sh --gpus 0,1,2       # произвольный список устройств
#   ./run_comfy.sh --cpu              # запуск на CPU
#   ./run_comfy.sh --manager          # включить ComfyUI-Manager
#   ./run_comfy.sh --port 8190        # другой порт

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="$ROOT_DIR/.venv/bin/python"

usage() {
  cat <<EOF
Использование: ./run_comfy.sh [опции] [-- дополнительные_аргументы_для_ComfyUI]

Опции:
  --single GPU_ID     Использовать один GPU (например, 0 или 1)
  --dual              Использовать два GPU 0 и 1 (по умолчанию)
  --gpus LIST         Явно указать CUDA_VISIBLE_DEVICES (например, "0,1" или "1")
  --cpu               Запуск только на CPU (CUDA не используется)
  --port PORT         Порт HTTP (по умолчанию 8188)
  --manager           Включить ComfyUI-Manager (--enable-manager)
  -h, --help          Показать эту справку

Все аргументы после "--" передаются напрямую в main.py.
EOF
}

if [[ ! -x "$VENV_PY" ]]; then
  echo "[ERROR] Не найден Python в venv: $VENV_PY" >&2
  echo "Создайте окружение: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
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
        echo "[ERROR] Для --single нужно указать номер GPU (например, 0)." >&2
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
        echo "[ERROR] Для --gpus нужно указать список, например: 0,1" >&2
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
        echo "[ERROR] Для --port нужно указать номер порта." >&2
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
      # Всё остальное — напрямую в ComfyUI
      while [[ $# -gt 0 ]]; do
        EXTRA_ARGS+=("$1")
        shift
      done
      ;;
    *)
      # Любой другой аргумент прокидываем дальше в main.py
      EXTRA_ARGS+=("$1")
      shift
      ;;
  esac
done

cd "$ROOT_DIR"

if [[ "$USE_CPU" == true ]]; then
  unset CUDA_VISIBLE_DEVICES
  echo "[INFO] Запуск на CPU (без CUDA)."
else
  export CUDA_VISIBLE_DEVICES="$GPUS"
  echo "[INFO] CUDA_VISIBLE_DEVICES=$GPUS"
fi

echo "[INFO] Порт: $PORT"

if [[ "$ENABLE_MANAGER" == true ]]; then
  EXTRA_ARGS+=("--enable-manager")
fi

exec "$VENV_PY" main.py --port "$PORT" "${EXTRA_ARGS[@]}"