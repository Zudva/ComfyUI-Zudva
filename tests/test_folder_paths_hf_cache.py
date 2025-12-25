import importlib
import os
import sys
from pathlib import Path

import comfy.cli_args as cli_args


def reload_folder_paths_with_base(base_dir, hf_cache_dir=None):
    # Modify args.base_directory then reload folder_paths
    cli_args.args.base_directory = str(base_dir)
    if hf_cache_dir is not None:
        os.environ["HF_CACHE_DIR"] = str(hf_cache_dir)
    # Ensure module is reloaded fresh
    if 'folder_paths' in sys.modules:
        importlib.reload(sys.modules['folder_paths'])
    import folder_paths as folder_paths
    importlib.reload(folder_paths)
    return folder_paths


def test_hf_cache_fallback(tmp_path, monkeypatch):
    # Setup project structure without local model
    base = tmp_path / "comfy_root"
    models_unet = base / "models" / "unet"
    models_unet.mkdir(parents=True)

    # Setup HF cache with a model file
    hf_cache = tmp_path / "hf_cache" / "hub" / "some_repo"
    hf_cache.mkdir(parents=True)
    model_name = "Wan2.2-I2V-A14B-LowNoise-Q5_K_M.gguf"
    model_file = hf_cache / model_name
    model_file.write_text("dummy")

    # Reload folder_paths with base dir and HF cache env
    folder_paths = reload_folder_paths_with_base(base, hf_cache_dir=hf_cache.parent)

    # Ensure get_full_path returns HF cache path when local missing
    found = folder_paths.get_full_path('diffusion_models', model_name)
    assert found is not None
    assert str(hf_cache) in found


def test_local_precedence_over_hf_cache(tmp_path, monkeypatch):
    base = tmp_path / "comfy_root"
    local_unet = base / "models" / "unet"
    local_unet.mkdir(parents=True)

    model_name = "example_local_model.gguf"
    local_file = local_unet / model_name
    local_file.write_text("local")

    # Setup HF cache with the same file name
    hf_cache = tmp_path / "hf_cache" / "hub" / "other_repo"
    hf_cache.mkdir(parents=True)
    hf_file = hf_cache / model_name
    hf_file.write_text("hf")

    folder_paths = reload_folder_paths_with_base(base, hf_cache_dir=hf_cache.parent)

    found = folder_paths.get_full_path('diffusion_models', model_name)
    assert found is not None
    # Should point to local file, not HF cache
    assert str(local_unet) in found
    assert str(hf_cache) not in found
