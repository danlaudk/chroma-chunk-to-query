"""
DSPy LM configuration with multi-provider support. 
"""
import dspy
from ..config.settings import (
    GOOGLE_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE
)

def initialize_dspy():
    """
    Uses DSPy's built-in LM class which has LiteLLM integration.
    """
    lm = dspy.LM(
        model=LLM_MODEL,
        api_key=GOOGLE_API_KEY,
        temperature=LLM_TEMPERATURE,
        max_tokens=4000,
        cache=True
    )
    
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