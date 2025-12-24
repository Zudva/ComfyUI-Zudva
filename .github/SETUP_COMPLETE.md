# ComfyUI Development Environment Setup

## ✅ Configuration Complete

This workspace is now fully configured for ComfyUI development with:

### 🐍 Python Virtual Environment
- **Path**: `/media/zudva/git/git/ComfyUI/.venv`
- **Python**: `/media/zudva/git/git/ComfyUI/.venv/bin/python`
- **Auto-activation**: VS Code terminals automatically use venv

### 🔧 VS Code Integration
- Python interpreter configured
- Debug configurations (F5)
- Build tasks (Ctrl+Shift+P)
- Import paths set for `comfy/` and `custom_nodes/`

### 📚 Documentation Created
- [.github/DEVELOPMENT.md](.github/DEVELOPMENT.md) - Full development guide
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - GitHub Copilot context
- [.vscode/README.md](.vscode/README.md) - VS Code setup guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Updated with venv requirements

## 🚀 Quick Start

```bash
# View configuration summary
.vscode/show-config.sh

# Run ComfyUI (standard)
./run_comfy.sh

# Run ComfyUI (beautiful output with Rich)
./run_comfy_beautiful.sh

# Install a package
.venv/bin/pip install package_name
```

## 📖 Next Steps

1. **Open in VS Code**: `code /media/zudva/git/git/ComfyUI`
2. **Install recommended extensions** when prompted
3. **Select Python interpreter**: `.venv/bin/python`
4. **Run tasks**: `Ctrl+Shift+P` → "Tasks: Run Task"
5. **Start debugging**: Press `F5`

## 💡 Key Features

- ✅ Automatic venv activation in all terminals
- ✅ GPU configuration (dual/single/CPU modes)
- ✅ Rich library launcher for formatted output
- ✅ Debug configurations for all scenarios
- ✅ Task runners for common operations
- ✅ GitHub Copilot integration

## 🔗 Documentation

| Document | Description |
|----------|-------------|
| [.github/DEVELOPMENT.md](.github/DEVELOPMENT.md) | Complete development guide |
| [.vscode/README.md](.vscode/README.md) | VS Code configuration |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | AI assistant context |

---

**Note**: All commands and scripts in this repository use the virtual environment located at `/media/zudva/git/git/ComfyUI/.venv`. Never use system Python for ComfyUI operations.
