"""
DSPy LM configuration with model-name based setups via JSON config.
"""
import json
import os
from pathlib import Path

import dspy
from ..config.settings import (
    GOOGLE_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE
)

def _load_model_config(model_name: str | None) -> dict:
    """Load model configuration from src/config/model_configs.json.

    Supports environment-variable expansion for values like ${LLM_MODEL}.
    """
    config_path = Path(__file__).resolve().parent.parent / "config" / "model_configs.json"
    with config_path.open("r", encoding="utf-8") as f:
        all_cfg = json.load(f)

    key = model_name or "default"
    if key not in all_cfg:
        raise KeyError(f"Model config '{key}' not found in {config_path}")

    cfg = all_cfg[key]

    # Expand env placeholders if present. LLM generated. unreviewed
    def expand(value):
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            # Simple ${VAR} or ${VAR:-default}
            inner = value[2:-1]
            if ":-" in inner:
                var, default = inner.split(":-", 1)
                return os.environ.get(var, default)
            return os.environ.get(inner, "")
        return value

    expanded = {k: expand(v) for k, v in cfg.items()}
    return expanded


def initialize_dspy(model_name: str | None = None):
    """
    Initialize DSPy LM using a named configuration from model_configs.json.

    Fallbacks use existing settings for compatibility with current tests.
    """
    cfg = _load_model_config(model_name)

    selected_model = cfg.get("model_name") or LLM_MODEL
    selected_temperature = float(cfg.get("temperature", LLM_TEMPERATURE))
    selected_max_tokens = int(cfg.get("max_tokens", 4000))
    selected_cache = bool(cfg.get("cache", True))

    # Determine API key from named env var in config, otherwise fallback
    api_key_env = cfg.get("api_key_env") or "GOOGLE_API_KEY"
    selected_api_key = os.environ.get(api_key_env, GOOGLE_API_KEY)

    # TODO: fix this mess
    # Optionally set provider-specific env vars if provided
    api_base = cfg.get("api_base") or ""
    if api_base:
        os.environ["LITELLM_API_BASE"] = str(api_base)
    provider = cfg.get("provider") or ""
    if provider:
        os.environ["LITELLM_PROVIDER"] = str(provider)

    lm = dspy.LM(
        model=selected_model,
        api_base=api_base,
        api_key=selected_api_key,
        temperature=selected_temperature,
        max_tokens=selected_max_tokens,
        cache=selected_cache,
    )
    
    dspy.configure(lm=lm)
    
    # Test the connection
    try:
        # Simple test to verify the LM is working
        print(f"Testing connection with base: {api_base}")
        test_response = lm("test")
        print(f"✓ DSPy LM connection test successful with model: {selected_model}")
    except Exception as e:
        print(f"✗ DSPy LM connection test failed: {e}")
        raise RuntimeError(f"Failed to initialize DSPy LM with model {selected_model}: {e}")
    
    return lm 