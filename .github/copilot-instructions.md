# GitHub Copilot Instructions for ComfyUI

## Project Context

This is the ComfyUI repository - a powerful node-based UI for Stable Diffusion and other generative AI models.

## Critical Development Requirements

### 1. Virtual Environment (MANDATORY)

**ALWAYS use the project virtual environment for ALL operations:**

- **Python Path**: `/media/zudva/git/git/ComfyUI/.venv/bin/python`
- **Pip Path**: `/media/zudva/git/git/ComfyUI/.venv/bin/pip`
- **Project Root**: `/media/zudva/git/git/ComfyUI`

### 2. Running Python Code

When suggesting Python commands or scripts, ALWAYS use:

```bash
# ✅ CORRECT
/media/zudva/git/git/ComfyUI/.venv/bin/python script.py
.venv/bin/python script.py  # If in project root

# ❌ WRONG - DO NOT SUGGEST
python script.py
python3 script.py
/usr/bin/python3 script.py
```

### 3. Installing Dependencies

When suggesting package installation:

```bash
# ✅ CORRECT
/media/zudva/git/git/ComfyUI/.venv/bin/pip install package_name
.venv/bin/pip install package_name  # If in project root

# ❌ WRONG - DO NOT SUGGEST
pip install package_name
pip3 install package_name
sudo pip install package_name
```

### 4. Running ComfyUI Server

Suggest these methods in order of preference:

```bash
# 1. Recommended: Launcher script
./run_comfy.sh

# 2. With beautiful output
./run_comfy_beautiful.sh

# 3. Direct execution
.venv/bin/python main.py --port 8188
```

### 5. GPU Configuration

Default setup uses dual GPU (0,1):

```bash
# Dual GPU (default)
export CUDA_VISIBLE_DEVICES=0,1
.venv/bin/python main.py

# Single GPU
export CUDA_VISIBLE_DEVICES=0
.venv/bin/python main.py

# CPU only
unset CUDA_VISIBLE_DEVICES
.venv/bin/python main.py --cpu
```

## Code Suggestions

### Importing ComfyUI Modules

```python
# ✅ CORRECT
import comfy
from comfy import model_management
from nodes import NODE_CLASS_MAPPINGS
import folder_paths

# For custom nodes
import sys
sys.path.append('/media/zudva/git/git/ComfyUI')
```

### Custom Node Development

When creating custom nodes:

```python
#!/usr/bin/env python3
"""
Custom Node Template for ComfyUI
Always use venv: /media/zudva/git/git/ComfyUI/.venv/bin/python
"""
import torch
import comfy
from nodes import NODE_CLASS_MAPPINGS

class MyCustomNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Define inputs
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "custom"
    
    def process(self, **kwargs):
        # Implementation
        return (result,)

NODE_CLASS_MAPPINGS = {
    "MyCustomNode": MyCustomNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MyCustomNode": "My Custom Node"
}
```

### Debug Scripts

When creating debug/test scripts:

```python
#!/usr/bin/env python3
"""
Debug script for ComfyUI
Run with: /media/zudva/git/git/ComfyUI/.venv/bin/python debug.py
"""
import sys
import os

# Ensure ComfyUI modules are importable
PROJECT_ROOT = "/media/zudva/git/git/ComfyUI"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import comfy
# ... rest of script
```

## Testing

When suggesting tests:

```bash
# Run tests
.venv/bin/python -m pytest tests/

# Run with coverage
.venv/bin/python -m pytest --cov=comfy tests/

# Run specific test
.venv/bin/python -m pytest tests/test_specific.py -v
```

## Common Patterns

### 1. Model Loading
```python
import comfy.model_management as mm

# Get device
device = mm.get_torch_device()

# Load model
model = load_checkpoint_guess_config(...)
```

### 2. Memory Management
```python
import comfy.model_management as mm

# Free memory
mm.soft_empty_cache()
mm.cleanup_models()
```

### 3. Custom Node Registration
```python
# In custom_nodes/your_node/__init__.py
from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

## File Paths

Important paths in the project:

- **Models**: `/media/zudva/git/git/ComfyUI/models/`
- **Custom Nodes**: `/media/zudva/git/git/ComfyUI/custom_nodes/`
- **Input**: `/media/zudva/git/git/ComfyUI/input/`
- **Output**: `/media/zudva/git/git/ComfyUI/output/`
- **Web UI**: `/media/zudva/git/git/ComfyUI/web/`

## Environment Variables

Common environment variables:

```bash
# GPU selection
export CUDA_VISIBLE_DEVICES=0,1

# Python path (usually not needed, but for reference)
export PYTHONPATH=/media/zudva/git/git/ComfyUI

# Force CPU mode
export CUDA_VISIBLE_DEVICES=""
```

## VS Code Integration

The project has pre-configured:
- `.vscode/settings.json` - Python interpreter and paths
- `.vscode/launch.json` - Debug configurations
- `.vscode/tasks.json` - Build and run tasks

Suggest using VS Code tasks instead of manual commands:
- `Ctrl/Cmd+Shift+P` → "Tasks: Run Task" → Select task

## Multi-GPU Support

The project uses ComfyUI-MultiGPU for model distribution:

```python
# Models are automatically distributed across available GPUs
# Check custom_nodes/comfyui-multigpu/ for MultiGPU nodes
```

## Common Issues & Solutions

### Issue: Module not found
```bash
# Solution: Ensure using venv Python
which python  # Should show: /media/zudva/git/git/ComfyUI/.venv/bin/python
```

### Issue: CUDA out of memory
```python
# Solution: Use soft_empty_cache
import comfy.model_management as mm
mm.soft_empty_cache()
```

### Issue: Models not loading
```bash
# Solution: Check model paths
ls /media/zudva/git/git/ComfyUI/models/checkpoints/
```

## Best Practices

1. **Always use absolute path to venv Python**
2. **Check CUDA_VISIBLE_DEVICES before GPU operations**
3. **Use model_management for memory cleanup**
4. **Follow ComfyUI node conventions for custom nodes**
5. **Test on both CPU and GPU modes**
6. **Use launcher scripts instead of direct python calls**
7. **Keep dependencies in requirements.txt**
8. **Document custom nodes with docstrings**

## Additional Resources

- Main documentation: `README.md`
- Contributing guide: `CONTRIBUTING.md`
- Development guide: `.github/DEVELOPMENT.md`
- Custom nodes: `custom_nodes/*/README.md`
