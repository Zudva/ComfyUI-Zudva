# Contributing to ComfyUI

Welcome, and thank you for your interest in contributing to ComfyUI!

There are several ways in which you can contribute, beyond writing code. The goal of this document is to provide a high-level overview of how you can get involved.

## Local environment (venv is mandatory)

Use the project-local virtual environment for any development (CLI, VS Code, GitHub Codespaces/Actions runners you start locally):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Important**: All terminal commands, scripts, and IDE configurations must use the virtual environment located at:
```
/media/zudva/git/git/ComfyUI/.venv
```

In VS Code, select interpreter `.venv/bin/python` (Ctrl/Cmd+Shift+P → "Python: Select Interpreter"). This keeps tooling, linting, and scripts aligned with the same Python that GitHub automation expects.

### Running ComfyUI

Always use the venv Python interpreter:

```bash
# Recommended: Use launcher scripts
./run_comfy.sh                    # Standard launcher
./run_comfy_beautiful.sh          # With Rich UI formatting

# Direct execution
.venv/bin/python main.py --port 8188

# With specific GPU configuration
CUDA_VISIBLE_DEVICES=0 .venv/bin/python main.py
```

For more details, see [Development Guide](.github/DEVELOPMENT.md).

## Asking Questions

Have a question? Instead of opening an issue, please ask on [Discord](https://comfy.org/discord) or [Matrix](https://app.element.io/#/room/%23comfyui_space%3Amatrix.org) channels. Our team and the community will help you.

## Providing Feedback

Your comments and feedback are welcome, and the development team is available via a handful of different channels.

See the `#bug-report`, `#feature-request` and `#feedback` channels on Discord.

## Reporting Issues

Have you identified a reproducible problem in ComfyUI? Do you have a feature request? We want to hear about it! Here's how you can report your issue as effectively as possible.


### Look For an Existing Issue

Before you create a new issue, please do a search in [open issues](https://github.com/comfyanonymous/ComfyUI/issues) to see if the issue or feature request has already been filed.

If you find your issue already exists, make relevant comments and add your [reaction](https://github.com/blog/2119-add-reactions-to-pull-requests-issues-and-comments). Use a reaction in place of a "+1" comment:

* 👍 - upvote
* 👎 - downvote

If you cannot find an existing issue that describes your bug or feature, create a new issue. We have an issue template in place to organize new issues.


### Creating Pull Requests

* Please refer to the article on [creating pull requests](https://github.com/comfyanonymous/ComfyUI/wiki/How-to-Contribute-Code) and contributing to this project.


## Thank You

Your contributions to open source, large or small, make great projects like this possible. Thank you for taking the time to contribute.
