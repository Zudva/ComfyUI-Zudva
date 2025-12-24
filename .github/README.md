# GitHub Configuration for ComfyUI

This directory contains GitHub-specific documentation and configurations.

## Files

- **DEVELOPMENT.md** - Comprehensive development guide
- **copilot-instructions.md** - Instructions for GitHub Copilot
- **workflows/** - GitHub Actions CI/CD workflows

## Important: Virtual Environment

All ComfyUI operations **must** use the project virtual environment:

```
/media/zudva/git/git/ComfyUI/.venv
```

### For Contributors

When working on ComfyUI:

1. **Always use venv Python:**
   ```bash
   /media/zudva/git/git/ComfyUI/.venv/bin/python
   ```

2. **Install dependencies in venv:**
   ```bash
   /media/zudva/git/git/ComfyUI/.venv/bin/pip install package_name
   ```

3. **Run ComfyUI:**
   ```bash
   ./run_comfy.sh              # Standard
   ./run_comfy_beautiful.sh    # With Rich UI
   ```

### For GitHub Copilot Users

See [copilot-instructions.md](copilot-instructions.md) for detailed context on:
- How to suggest code that uses correct Python paths
- ComfyUI-specific patterns and conventions
- GPU configuration
- Custom node development

## Quick Reference

### Running Commands

```bash
# ✅ CORRECT
.venv/bin/python script.py
.venv/bin/pip install package

# ❌ WRONG
python script.py
pip install package
```

### Environment Setup

```bash
cd /media/zudva/git/git/ComfyUI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### GPU Configuration

```bash
# Dual GPU (default)
export CUDA_VISIBLE_DEVICES=0,1

# Single GPU
export CUDA_VISIBLE_DEVICES=0

# CPU only
unset CUDA_VISIBLE_DEVICES
```

## Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Full development guide
  - Setup instructions
  - Running ComfyUI
  - Debugging
  - Testing
  - Common issues

- **[copilot-instructions.md](copilot-instructions.md)** - GitHub Copilot context
  - Code suggestion guidelines
  - Project patterns
  - Best practices

## Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

All contributions must:
- Use the project venv
- Follow existing code style
- Include tests for new features
- Update documentation as needed

## Resources

- Main README: [../README.md](../README.md)
- VS Code Setup: [../.vscode/README.md](../.vscode/README.md)
- Issue Templates: [ISSUE_TEMPLATE/](ISSUE_TEMPLATE/)
- PR Templates: [PULL_REQUEST_TEMPLATE/](PULL_REQUEST_TEMPLATE/)
