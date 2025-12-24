# GPU Configuration Modes для ComfyUI

## Обзор

ComfyUI с Rich launcher поддерживает три режима работы с видеокартами:
- **Dual GPU** - использование двух GPU одновременно
- **Single GPU** - использование одной GPU
- **CPU Only** - работа только на CPU

---

## 🎮 Dual GPU Mode (Рекомендуется)

### Описание
Использует обе видеокарты (RTX 3090) для распределенной обработки через ComfyUI-MultiGPU (DisTorch).

### Преимущества
- ✅ **48 GB VRAM** - суммарная память двух карт
- ✅ **Параллельная обработка** - разные слои модели на разных GPU
- ✅ **Меньше OOM ошибок** - большие модели помещаются в память
- ✅ **Faster processing** - некоторые операции быстрее

### Запуск

```bash
# Через .env (по умолчанию)
CUDA_VISIBLE_DEVICES=0,1
./run_comfy_beautiful.sh

# Явно через флаг
./run_comfy_beautiful.sh --dual

# Через стандартный скрипт
./run_comfy.sh
```

### Как работает

```
┌─────────────────────────────────────────┐
│         ComfyUI Main Process            │
│                                         │
│  ┌─────────────┐    ┌─────────────┐   │
│  │   GPU 0     │    │   GPU 1     │   │
│  │ RTX 3090    │    │ RTX 3090    │   │
│  │ 24GB VRAM   │    │ 24GB VRAM   │   │
│  └─────────────┘    └─────────────┘   │
│         │                   │          │
│         └──── DisTorch ─────┘          │
│       (Layer Offloading)               │
└─────────────────────────────────────────┘
```

**DisTorch** автоматически распределяет:
- Разные слои моделей на разные GPU
- VAE encoding/decoding между картами
- Attention layers для оптимизации памяти

### Отображение в Rich UI

```
╭──────────────────────── 🎮 GPU Configuration ────────────────────────╮
│ 🎮 Dual GPU Mode                                                     │
│ Using 2 GPUs for distributed processing                              │
│                                                                      │
│ CUDA_VISIBLE_DEVICES: 0,1                                            │
│                                                                      │
│ Detected GPUs:                                                       │
│   GPU 0: NVIDIA GeForce RTX 3090                                     │
│          23.56 GB VRAM                                               │
│   GPU 1: NVIDIA GeForce RTX 3090                                     │
│          23.56 GB VRAM                                               │
╰──────────────────────────────────────────────────────────────────────╯
```

---

## 🎮 Single GPU Mode

### Описание
Использует только одну видеокарту для всех операций.

### Преимущества
- ✅ **Простота** - нет overhead от межкарточной коммуникации
- ✅ **Стабильность** - меньше вероятность конфликтов драйверов
- ✅ **Debugging** - проще отлаживать проблемы

### Недостатки
- ❌ **24 GB VRAM лимит** - большие модели могут не поместиться
- ❌ **Slower** - нет распределения нагрузки

### Запуск

```bash
# GPU 0
./run_comfy_beautiful.sh --single 0

# GPU 1
./run_comfy_beautiful.sh --single 1

# Через .env
CUDA_VISIBLE_DEVICES=0
./run_comfy_beautiful.sh
```

### Когда использовать

- 🔧 **Debugging** - изоляция проблем с GPU
- 🧪 **Testing** - проверка работы на одной карте
- 📊 **Benchmarking** - сравнение производительности
- ⚡ **Simple workflows** - легкие модели не требующие много VRAM

### Отображение в Rich UI

```
╭──────────────────────── 🎮 GPU Configuration ────────────────────────╮
│ 🎮 Single GPU Mode                                                   │
│ Using 1 GPU for processing                                           │
│                                                                      │
│ CUDA_VISIBLE_DEVICES: 0                                              │
│                                                                      │
│ Detected GPUs:                                                       │
│   GPU 0: NVIDIA GeForce RTX 3090                                     │
│          23.56 GB VRAM                                               │
╰──────────────────────────────────────────────────────────────────────╯
```

---

## 🖥️ CPU Only Mode

### Описание
Работает только на CPU, без использования CUDA.

### Преимущества
- ✅ **No GPU needed** - работает на любом компьютере
- ✅ **Testing** - проверка логики без GPU

### Недостатки
- ❌ **ОЧЕНЬ МЕДЛЕННО** - 10-100x медленнее GPU
- ❌ **Не для продакшена** - только для разработки/тестирования

### Запуск

```bash
./run_comfy_beautiful.sh --cpu

# Через .env
CUDA_VISIBLE_DEVICES=
./run_comfy.sh
```

### Когда использовать

- 🔧 **Development** - тестирование custom nodes без GPU
- 🐛 **Debugging** - изоляция CUDA-специфичных проблем
- 📝 **Workflow editing** - создание/редактирование workflows

### Отображение в Rich UI

```
╭──────────────────────── 🎮 GPU Configuration ────────────────────────╮
│ 🖥️  CPU Mode                                                         │
│ No CUDA devices configured                                           │
╰──────────────────────────────────────────────────────────────────────╯
```

---

## Сравнение режимов

| Характеристика | Dual GPU | Single GPU | CPU Only |
|----------------|----------|------------|----------|
| **VRAM** | 48 GB | 24 GB | RAM only |
| **Скорость** | Fastest* | Fast | Very Slow |
| **Стабильность** | Good | Best | Good |
| **Сложность** | Medium | Low | Low |
| **Use Case** | Production | Testing/Simple | Development |

*\* Зависит от workflow и модели*

---

## MultiGPU vs FSDP Sharding

### ComfyUI-MultiGPU (DisTorch)
- **Layer offloading** - разные слои на разных GPU
- **Automatic distribution** - DisTorch решает что куда
- **Dynamic loading** - модели загружаются по требованию
- **Node-based control** - можно выбрать GPU через ноды

### Wan 2.2 FSDP Sharding
- **Full model sharding** - модель разбита на shards
- **ZeRO optimization** - эффективное использование памяти
- **Gradient accumulation** - обучение больших моделей
- **Для training/inference** - не только inference

**Это РАЗНЫЕ системы:**
- ComfyUI-MultiGPU - для inference в ComfyUI
- Wan 2.2 FSDP - для training/inference в Wan

---

## Как выбрать режим?

### Используй **Dual GPU** если:
- ✅ Работаешь с большими моделями (SDXL, Flux, etc.)
- ✅ Нужна максимальная VRAM
- ✅ Production workflows
- ✅ Batch processing

### Используй **Single GPU** если:
- ✅ Debugging проблем
- ✅ Простые модели (SD 1.5)
- ✅ Testing новых nodes
- ✅ Хочешь оставить вторую GPU для другой задачи

### Используй **CPU** если:
- ✅ Development без GPU
- ✅ Тестирование логики
- ✅ GPU занята другими процессами
- ✅ Создание workflows

---

## Переключение между режимами

### Через .env файл (Рекомендуется)

```bash
# Редактировать .env
nano .env

# Установить режим
CUDA_VISIBLE_DEVICES=0,1  # Dual GPU
CUDA_VISIBLE_DEVICES=0    # Single GPU 0
CUDA_VISIBLE_DEVICES=1    # Single GPU 1
CUDA_VISIBLE_DEVICES=     # CPU Only

# Запустить
./run_comfy_beautiful.sh
```

### Через command line аргументы

```bash
# Override .env настройки
./run_comfy_beautiful.sh --dual    # Dual GPU
./run_comfy_beautiful.sh --single 0  # Single GPU
./run_comfy_beautiful.sh --cpu     # CPU Only

# Кастомная конфигурация
./run_comfy_beautiful.sh --gpus "1,0"  # Reverse order
```

---

## Monitoring GPU Usage

### Во время работы ComfyUI

```bash
# Watch GPU utilization
watch -n 1 nvidia-smi

# Детальная информация
nvidia-smi dmon -s u
```

### Проверка конфигурации

```bash
# Какие GPU видны
.venv/bin/python check_gpus.py

# Из Python
.venv/bin/python -c "import torch; print(torch.cuda.device_count())"
```

---

## Troubleshooting

### Проблема: "Only one GPU showing"

**Решение:** ComfyUI показывает только primary device (cuda:0) в UI, но обе GPU доступны:

```bash
# Проверить
.venv/bin/python check_gpus.py
# Должно показать: Number of CUDA devices: 2
```

### Проблема: "CUDA out of memory"

**Решения:**
1. Используй Dual GPU mode
2. Уменьши batch size
3. Включи `--lowvram` или `--medvram`

```bash
# В .env
COMFYUI_ARGS="--lowvram"
```

### Проблема: "GPU not detected"

**Проверки:**
```bash
# CUDA доступна?
nvidia-smi

# PyTorch видит CUDA?
.venv/bin/python -c "import torch; print(torch.cuda.is_available())"

# .env правильно загружен?
cat .env
```

---

## Best Practices

1. **Default to Dual GPU** - максимум производительности
2. **Use .env для постоянных настроек** - не нужно помнить флаги
3. **Command line для экспериментов** - быстрое переключение
4. **Monitor VRAM usage** - понять когда нужен dual mode
5. **Test на Single GPU first** - изоляция проблем

---

## Примеры использования

### Production Workflow

```bash
# .env
CUDA_VISIBLE_DEVICES=0,1
COMFYUI_PORT=8188
COMFYUI_ARGS="--preview-method auto --highvram"

# Запуск
./run_comfy_beautiful.sh
```

### Development/Testing

```bash
# Single GPU для debugging
./run_comfy_beautiful.sh --single 0 --port 8189

# CPU для тестирования логики
./run_comfy_beautiful.sh --cpu --port 8190
```

### Batch Processing

```bash
# Dual GPU с maximum VRAM
export CUDA_VISIBLE_DEVICES=0,1
.venv/bin/python batch_processor.py
```

---

## Дополнительная информация

- **VS Code Configuration**: [.vscode/README.md](../.vscode/README.md)
- **Development Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)
- **Environment Config**: [ENV_CONFIG.md](ENV_CONFIG.md)
- **Repository**: https://github.com/Zudva/ComfyUI-Zudva
