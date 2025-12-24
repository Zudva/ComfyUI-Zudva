# ComfyUI Development Guide

## 🚀 Quick Start

### Virtual Environment Setup

**IMPORTANT**: All ComfyUI development and execution **MUST** use the project's local virtual environment located at:

```
/media/zudva/git/git/ComfyUI/.venv
```

### Initial Setup

1. **Create and activate virtual environment:**
   ```bash
   cd /media/zudva/git/git/ComfyUI
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **For development with Rich UI:**
   ```bash
   pip install rich
   ```

## 🔧 Running ComfyUI

### Method 1: Standard Launcher (recommended)
```bash
./run_comfy.sh                    # Dual GPU (0,1)
./run_comfy.sh --single 0         # Single GPU
./run_comfy.sh --cpu              # CPU only
./run_comfy.sh --port 8190        # Custom port
```

### Method 2: Beautiful Output (with Rich)
```bash
./run_comfy_beautiful.sh          # Same options as run_comfy.sh
```

### Method 3: Direct Python
```bash
# Always use the venv Python!
.venv/bin/python main.py --port 8188
```

## 📝 VS Code Configuration

### Python Interpreter
The workspace is pre-configured to use `.venv/bin/python`. 

- **Select Interpreter**: `Ctrl/Cmd+Shift+P` → "Python: Select Interpreter" → Choose `.venv/bin/python`

### Integrated Terminal
All integrated terminals automatically activate the `.venv` environment. You don't need to run `source .venv/bin/activate` manually.

### Available Tasks
Press `Ctrl/Cmd+Shift+P` → "Tasks: Run Task":

- **ComfyUI: Start Server (Dual GPU)** - Launch with 2 GPUs
- **ComfyUI: Start Server (Single GPU 0)** - Launch with GPU 0
- **ComfyUI: Start with Beautiful Output** - Launch with Rich UI
- **ComfyUI: Install Dependencies** - Install/update packages
- **ComfyUI: Run Tests** - Run test suite

### Debug Configurations
Press `F5` or go to Run and Debug panel:

- **ComfyUI: Launch Server** - Debug server with dual GPU
- **ComfyUI: Single GPU** - Debug with single GPU
- **ComfyUI: CPU Only** - Debug CPU-only mode
- **Python: Current File** - Debug current Python file

## 🔍 Important Paths

All scripts and tools expect these paths:

| Component | Path |
|-----------|------|
| Python Interpreter | `/media/zudva/git/git/ComfyUI/.venv/bin/python` |
| Pip | `/media/zudva/git/git/ComfyUI/.venv/bin/pip` |
| Project Root | `/media/zudva/git/git/ComfyUI` |
| Main Entry | `/media/zudva/git/git/ComfyUI/main.py` |

## 🐛 Debugging

### Always Use venv Python
```bash
# ✅ Correct
/media/zudva/git/git/ComfyUI/.venv/bin/python script.py

# ❌ Wrong
python script.py
python3 script.py
/usr/bin/python script.py
```

### Installing Packages
```bash
# ✅ Correct
/media/zudva/git/git/ComfyUI/.venv/bin/pip install package_name

# Or if venv is activated:
pip install package_name

# ❌ Wrong
pip3 install package_name  # May install to wrong Python
sudo pip install package_name  # Never use sudo
```

## 🔐 Environment Variables

### GPU Configuration
```bash
# Dual GPU (default)
export CUDA_VISIBLE_DEVICES=0,1

# Single GPU
export CUDA_VISIBLE_DEVICES=0

# CPU only
unset CUDA_VISIBLE_DEVICES
```

### Python Path
The workspace root is automatically added to PYTHONPATH in VS Code configurations.

## 📦 Custom Nodes Development

When developing custom nodes:

1. Place your node in `custom_nodes/your_node_name/`
2. Use the venv Python for any dependencies
3. Import ComfyUI modules as usual:
   ```python
   import comfy
   from nodes import NODE_CLASS_MAPPINGS
   ```

## 🧪 Testing

```bash
# Run all tests
.venv/bin/python -m pytest tests/

# Run specific test
.venv/bin/python -m pytest tests/test_specific.py

# Run with coverage
.venv/bin/pip install pytest-cov
.venv/bin/python -m pytest --cov=comfy tests/
```

## 🚨 Common Issues

### "Module not found" errors
Make sure you're using the venv Python:
```bash
which python  # Should show: /media/zudva/git/git/ComfyUI/.venv/bin/python
```

### Permission errors with pip
Never use `sudo`. Always install in venv:
```bash
.venv/bin/pip install --user package_name
```

### VS Code not finding modules
1. Reload window: `Ctrl/Cmd+Shift+P` → "Developer: Reload Window"
2. Check Python interpreter: Should be `.venv/bin/python`
3. Check PYTHONPATH includes workspace root

## 📚 Additional Resources

- [Contributing Guide](../CONTRIBUTING.md)
- [VS Code Python Settings](.vscode/settings.json)
- [Launch Configurations](.vscode/launch.json)
- [Tasks](.vscode/tasks.json)

## 💡 Tips

1. **Always activate venv** before any Python operations
2. **Use VS Code tasks** instead of manual commands
3. **Check CUDA_VISIBLE_DEVICES** if GPU not detected
4. **Use `run_comfy_beautiful.sh`** for better visual feedback
5. **Keep dependencies updated**: `pip install -r requirements.txt --upgrade`
