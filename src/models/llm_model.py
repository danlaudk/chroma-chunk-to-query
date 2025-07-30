"""
DSPy LM configuration using LiteLLM for multi-provider support.
"""
import dspy
from ..config.settings import (
    GOOGLE_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE
)

def initialize_litellm_dspy():
    """
    Initialize DSPy with a LiteLLM-compatible LM.
    Uses DSPy's built-in LM class which has LiteLLM integration.
    """
    # Create a DSPy LM instance that uses LiteLLM under the hood
    lm = dspy.LM(
        model=LLM_MODEL,
        api_key=GOOGLE_API_KEY,
        temperature=LLM_TEMPERATURE,
        max_tokens=4000,
        cache=True
    )
    
    # Configure DSPy with the LM
    dspy.configure(lm=lm)
    
    # Test the connection
    try:
        # Simple test to verify the LM is working
        test_response = lm("test")
        print(f"✓ DSPy LM connection test successful with model: {LLM_MODEL}")
    except Exception as e:
        print(f"✗ DSPy LM connection test failed: {e}")
        raise RuntimeError(f"Failed to initialize DSPy LM with model {LLM_MODEL}: {e}")
    
    return lm 