"""
DSPy LM configuration with model-name based setups via JSON config.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field
from pydantic import field_validator, model_validator
import dspy
# No longer import model/env specifics from settings; handled via JSON config

class ModelConfig(BaseModel):
    """Type-safe model configuration with Pydantic validation."""
    model_name: str = Field(..., min_length=1, description="Name of the model to use")
    provider: Optional[str] = Field(None, description="LLM provider (e.g., 'openai', 'anthropic')")
    api_base: Optional[str] = Field(None, description="Custom API base URL")
    api_key_env: str = Field("GOOGLE_API_KEY", description="Environment variable name for API key")
    temperature: float = Field(0.2, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(4000, gt=0, description="Maximum tokens to generate")
    cache: bool = Field(True, description="Whether to enable caching")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"  # Prevent unexpected fields
        json_schema_extra = {
            "example": {
                "model_name": "gpt-4",
                "provider": "openai",
                "api_base": "https://api.openai.com/v1",
                "api_key_env": "OPENAI_API_KEY",
                "temperature": 0.7,
                "max_tokens": 2000,
                "cache": True
            }
        }

    @field_validator('api_base')
    def validate_api_base(cls, v):
        """Validate API base URL format."""
        if v is not None and v.strip():
            # Basic URL validation
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('api_base must be a valid HTTP/HTTPS URL')
        return v

    @field_validator('api_key_env')
    def validate_api_key_env(cls, v):
        """Validate environment variable name format."""
        if not re.match(r'^[A-Z][A-Z0-9_]*$', v):
            raise ValueError('api_key_env must be a valid environment variable name (uppercase, underscores allowed)')
        return v

    @model_validator(mode='after')
    def validate_provider_consistency(self):
        """Validate consistency between provider and other fields."""
        provider = self.provider
        api_base = self.api_base
        model_name = self.model_name or ''

        if provider == 'openai' and api_base and 'openai.com' not in api_base:
            # Allow custom OpenAI-compatible endpoints
            pass
        elif provider == 'anthropic' and model_name and not model_name.startswith('claude'):
            raise ValueError('Anthropic provider should typically use Claude models')

        return self


class ConfigError(Exception):
    """Configuration-related errors."""
    pass


class ModelConfigLoader:
    """Handles loading and processing of model configurations with Pydantic validation."""
    
    ENV_VAR_PATTERN = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*)(:-([^}]*))?\}')
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or (
            Path(__file__).resolve().parent.parent / "config" / "model_configs.json"
        )
    
    def _expand_env_vars(self, value: Any) -> Any:
        """Expand environment variables with proper error handling."""
        if not isinstance(value, str):
            return value
        
        def replace_var(match):
            var_name = match.group(1)
            default_value = match.group(3) if match.group(3) is not None else None
            
            env_value = os.environ.get(var_name)
            if env_value is not None:
                return env_value
            elif default_value is not None:
                return default_value
            else:
                raise ConfigError(
                    f"Environment variable '{var_name}' not found and no default provided"
                )
        
        return self.ENV_VAR_PATTERN.sub(replace_var, value)
    
    def _process_config(self, raw_config: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw config, expanding env vars with smart type conversion."""
        processed = {}
        
        for key, value in raw_config.items():
            try:
                expanded = self._expand_env_vars(value)
                
                # Handle empty strings from environment variables
                if expanded == "":
                    # Skip empty values, let Pydantic use defaults
                    continue
                
                # Smart type conversion for string values from env vars
                if isinstance(expanded, str) and key in {"temperature", "max_tokens", "cache"}:
                    if key == "temperature":
                        processed[key] = float(expanded)
                    elif key == "max_tokens":
                        processed[key] = int(expanded)
                    elif key == "cache":
                        processed[key] = expanded.lower() in ("true", "1", "yes", "on")
                else:
                    processed[key] = expanded
                    
            except (ValueError, TypeError) as e:
                raise ConfigError(f"Invalid value for '{key}': {value} - {e}")
        
        return processed
    
    def load_config(self, model_name: Optional[str] = None) -> ModelConfig:
        """Load and validate model configuration using Pydantic."""
        if not self.config_path.exists():
            raise ConfigError(f"Config file not found: {self.config_path}")
        
        try:
            with self.config_path.open("r", encoding="utf-8") as f:
                all_configs = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config file: {e}")
        
        key = model_name or "default"
        if key not in all_configs:
            available = list(all_configs.keys())
            raise ConfigError(f"Model config '{key}' not found. Available: {available}")
        
        raw_config = all_configs[key]
        processed_config = self._process_config(raw_config)
        
        try:
            # Let Pydantic handle validation and type conversion
            return ModelConfig(**processed_config)
        except Exception as e:
            raise ConfigError(f"Invalid configuration for '{key}': {e}")


def initialize_dspy(model_name: Optional[str] = None, config_path: Optional[Path] = None) -> dspy.LM:
    """
    Initialize DSPy LM with robust Pydantic-validated configuration loading.
    
    Args:
        model_name: Name of the model configuration to use (defaults to "default")
        config_path: Path to configuration file (optional)
    
    Returns:
        Configured DSPy LM instance
        
    Raises:
        RuntimeError: If configuration loading or model initialization fails
    """
    
    loader = ModelConfigLoader(config_path)
    
    try:
        config = loader.load_config(model_name)
    except ConfigError as e:
        raise RuntimeError(f"Configuration error: {e}")
    
    # Get API key from environment
    api_key = os.environ.get(config.api_key_env)
    if not api_key:
        raise RuntimeError(
            f"API key not found in environment variable '{config.api_key_env}'. "
            f"Please set this environment variable."
        )
    
    # Build LM parameters
    lm_params = {
        "model": config.model_name,
        "api_key": api_key,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "cache": config.cache,
    }
    
    # Add optional parameters
    if config.api_base:
        lm_params["api_base"] = config.api_base
    
    # Set provider-specific environment if needed (contained approach)
    env_context = {}
    if config.provider:
        env_context["LITELLM_PROVIDER"] = config.provider
    if config.api_base:
        env_context["LITELLM_API_BASE"] = config.api_base
    
    # Temporarily set environment variables
    # When you create a dspy.LM instance,
    #  LiteLLM internally looks for env vars like LITELLM_PROVIDER and LITELLM_API_BASE
    old_env = {}
    for key, value in env_context.items():
        old_env[key] = os.environ.get(key)
        os.environ[key] = value
    
    try:
        # Test connection before full initialization
        print(f"Initializing DSPy LM with model: {config.model_name}")
        if config.provider:
            print(f"Provider: {config.provider}")
        if config.api_base:
            print(f"API base: {config.api_base}")
        print(f"Temperature: {config.temperature}, Max tokens: {config.max_tokens}")

        lm = dspy.LM(**lm_params)

        # Quick connection test
        try:
            test_response = lm("Hello")  # Minimal test
            print("✓ DSPy LM connection test successful")
        except Exception as e:
            raise RuntimeError(f"Connection test failed for model '{config.model_name}': {e}")
        
        dspy.configure(lm=lm)
        return lm

    finally:
        # Restore original environment
        for key, old_value in old_env.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value


def get_available_configs(config_path: Optional[Path] = None) -> list[str]:
    """Get list of available model configuration names."""
    loader = ModelConfigLoader(config_path)
    
    if not loader.config_path.exists():
        return []
    
    try:
        with loader.config_path.open("r", encoding="utf-8") as f:
            all_configs = json.load(f)
        return list(all_configs.keys())
    except (json.JSONDecodeError, OSError):
        return []


# Usage examples:
if __name__ == "__main__":
    # Show available configurations
    available = get_available_configs()
    print(f"Available configurations: {available}")
    
    # Use default config
    try:
        lm = initialize_dspy()
    except RuntimeError as e:
        print(f"Failed to initialize default model: {e}")
    
    # Use specific config with validation
    try:
        lm = initialize_dspy("summllama3")
    except RuntimeError as e:
        print(f"Failed to initialize summllama3 model: {e}")
    
    # Example of direct config validation
    try:
        config = ModelConfig(
            model_name="gpt-4",
            temperature=0.7,
            api_key_env="OPENAI_API_KEY"
        )
        print(f"Valid config created: {config.model_name}")
    except Exception as e:
        print(f"Config validation failed: {e}")