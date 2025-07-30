"""
DSPy LM configuration using LiteLLM for multi-provider support.
"""
import dspy
from ..config.settings import config

def initialize_litellm_dspy(llm_config=None):
    """
    Initialize DSPy with a LiteLLM-compatible LM.
    Uses DSPy's built-in LM class which has LiteLLM integration.
    
    Args:
        llm_config: Optional LLMConfig instance for testing
        
    Returns:
        Configured DSPy LM instance
        
    Raises:
        RuntimeError: If LM initialization fails
    """
    cfg = llm_config or config.llm
    
    # Create a DSPy LM instance that uses LiteLLM under the hood
    lm = dspy.LM(
        model=cfg.model,
        api_key=cfg.api_key,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
        cache=cfg.cache
    )
    
    # Configure DSPy with the LM
    dspy.configure(lm=lm)
    
    # Test the connection
    try:
        # Simple test to verify the LM is working
        test_response = lm("test")
        print(f"✓ DSPy LM connection test successful with model: {cfg.model}")
    except Exception as e:
        print(f"✗ DSPy LM connection test failed: {e}")
        raise RuntimeError(f"Failed to initialize DSPy LM with model {cfg.model}: {e}")
    
    return lm 