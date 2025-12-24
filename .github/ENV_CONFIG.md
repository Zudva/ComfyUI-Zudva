# Environment Configuration Guide

## Overview

ComfyUI launcher scripts support configuration via `.env` file for easy customization without modifying scripts directly.

## Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` to your preferences:**
   ```bash
   nano .env  # or use your favorite editor
   ```

## Configuration Options

### GPU Configuration

**CUDA_VISIBLE_DEVICES** - Controls which GPUs to use

```bash
# Dual GPU (default)
CUDA_VISIBLE_DEVICES=0,1

# Single GPU
CUDA_VISIBLE_DEVICES=0

# Different GPU
CUDA_VISIBLE_DEVICES=1

# Three GPUs
CUDA_VISIBLE_DEVICES=0,1,2

# CPU only (leave empty or comment out)
# CUDA_VISIBLE_DEVICES=
```

### Server Configuration

**COMFYUI_PORT** - HTTP server port (default: 8188)

```bash
COMFYUI_PORT=8188

# Custom port
COMFYUI_PORT=8190
```

### Optional Features

**ENABLE_COMFYUI_MANAGER** - Enable ComfyUI Manager

```bash
# Disabled (default)
# ENABLE_COMFYUI_MANAGER=true

# Enabled
ENABLE_COMFYUI_MANAGER=true
```

**COMFYUI_ARGS** - Additional command-line arguments

```bash
# Example: preview method and attention optimization
COMFYUI_ARGS="--preview-method auto --use-split-cross-attention"

# Example: disable metadata
COMFYUI_ARGS="--disable-metadata"

# Multiple arguments
COMFYUI_ARGS="--preview-method auto --highvram --fast"
```

### Memory Management

**PYTORCH_ALLOC_CONF** - PyTorch memory allocation settings

```bash
# Expandable memory segments (recommended for large models)
PYTORCH_ALLOC_CONF=expandable_segments:True

# Max split size (in MB)
PYTORCH_ALLOC_CONF=max_split_size_mb:512
```

### Python Settings

**PYTHONUNBUFFERED** - Disable Python output buffering

```bash
PYTHONUNBUFFERED=1
```

**PYTHONDONTWRITEBYTECODE** - Don't create .pyc files

```bash
PYTHONDONTWRITEBYTECODE=1
```

## Priority Order

Settings are applied in this order (later overrides earlier):

1. **.env file** - Default configuration
2. **Command-line arguments** - Override .env settings

### Example

```bash
# .env file
CUDA_VISIBLE_DEVICES=0,1
COMFYUI_PORT=8188

# Command line overrides port
./run_comfy.sh --port 8190
# Result: Uses GPU 0,1 from .env, but port 8190 from command line
```

## Usage Examples

### Basic Setup

```bash
# .env
CUDA_VISIBLE_DEVICES=0,1
COMFYUI_PORT=8188
```

Then simply run:
```bash
./run_comfy.sh
```

### Development Setup

```bash
# .env
CUDA_VISIBLE_DEVICES=0
COMFYUI_PORT=8190
ENABLE_COMFYUI_MANAGER=true
PYTHONUNBUFFERED=1
COMFYUI_ARGS="--preview-method auto"
```

### Production Setup

```bash
# .env
CUDA_VISIBLE_DEVICES=0,1
COMFYUI_PORT=8188
PYTORCH_ALLOC_CONF=expandable_segments:True
COMFYUI_ARGS="--highvram --preview-method auto"
```

### CPU-Only Setup

```bash
# .env
# CUDA_VISIBLE_DEVICES=  # Comment out or leave empty
COMFYUI_PORT=8188
```

Or use command line:
```bash
./run_comfy.sh --cpu
```

## Troubleshooting

### Changes not taking effect

1. **Restart the server** - Changes require restart
2. **Check file location** - `.env` must be in project root
3. **Check syntax** - No spaces around `=`
   ```bash
   # ✅ Correct
   COMFYUI_PORT=8188
   
   # ❌ Wrong
   COMFYUI_PORT = 8188
   ```

### GPU not detected

1. **Check CUDA_VISIBLE_DEVICES**:
   ```bash
   echo $CUDA_VISIBLE_DEVICES
   ```

2. **Verify GPU availability**:
   ```bash
   nvidia-smi
   ```

3. **Test with explicit setting**:
   ```bash
   ./run_comfy.sh --gpus 0,1
   ```

### Port already in use

Change port in `.env`:
```bash
COMFYUI_PORT=8190
```

Or override via command line:
```bash
./run_comfy.sh --port 8190
```

## Best Practices

1. **Never commit `.env`** - It's in `.gitignore` by default
2. **Use `.env.example`** - Document all available options
3. **Keep it simple** - Only set what you need to change
4. **Comment options** - Explain non-obvious settings
5. **Test changes** - Restart server after modifications

## Security Notes

- `.env` file is excluded from git (in `.gitignore`)
- Don't put sensitive data in `.env.example`
- `.env.example` is committed to repository for documentation
- Each user should create their own `.env` from `.env.example`

## Related Documentation

- [DEVELOPMENT.md](DEVELOPMENT.md) - Full development guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [README.md](../README.md) - Project overview
