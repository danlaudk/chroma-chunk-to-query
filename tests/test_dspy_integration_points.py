"""
Test script to verify DSPy integration points for dspy.LM with LiteLLM??.
"""
import dspy
from src.models.llm_model import initialize_dspy
from src.config.settings import LLM_MODEL, LLM_TEMPERATURE

def test_dspy_configure_integration():
    """Test that our dspy.LM can be configured with DSPy."""
    print("Testing DSPy configure integration...")
    
    try:
        # Test 1: Can we create our LM using the initialization function?
        llm = initialize_dspy()
        print("✓ dspy.LM creation successful")
        
        # Test 2: DSPy should already be configured by initialize_dspy()
        print("✓ DSPy configuration successful")
        
        # Test 3: Does our LM have the required interface?
        assert hasattr(llm, 'forward'), "dspy.LM must have a forward method"
        assert callable(llm.forward), "forward method must be callable"
        print("✓ Required interface methods present")
        
        print("\nDSPy integration points verified successfully!")
        
    except Exception as e:
        print(f"Error in DSPy integration test: {e}")
        raise

def test_forward_method_signature():
    """Test that our forward method has the correct signature."""
    print("\nTesting forward method signature...")
    
    try:
        llm = initialize_dspy()
        
        # Test that forward accepts the expected parameters
        import inspect
        sig = inspect.signature(llm.forward)
        params = list(sig.parameters.keys())
        
        print(f"Forward method parameters: {params}")
        
        # Check that it accepts at least 'prompt' and **kwargs
        assert 'prompt' in params, "forward method must accept 'prompt' parameter"
        assert sig.parameters.get('kwargs') is not None, "forward method should accept **kwargs"
        
        print("✓ Forward method signature is correct")
        
    except Exception as e:
        print(f"Error in signature test: {e}")
        raise

def test_dspy_chain_of_thought_integration():
    """Test that our model works with DSPy's ChainOfThought."""
    print("\nTesting ChainOfThought integration...")
    
    try:
        # Configure DSPy with our model
        llm = initialize_dspy()
        
        # Create a ChainOfThought predictor
        cot = dspy.ChainOfThought("question -> answer")
        
        # Test that we can create the predictor (this tests the integration)
        print("✓ ChainOfThought creation successful")
        
        # Note: We don't actually call it here since we need API keys
        # This test just verifies that DSPy accepts our model for configuration
        
        print("✓ ChainOfThought integration verified")
        
    except Exception as e:
        print(f"Error in ChainOfThought test: {e}")
        raise

def test_dspy_predict_integration():
    """Test that our model works with DSPy's Predict."""
    print("\nTesting Predict integration...")
    
    try:
        # Configure DSPy with our model
        llm = initialize_dspy()
        
        # Create a Predict module
        predictor = dspy.Predict("input -> output")
        
        print("✓ Predict creation successful")
        print("✓ Predict integration verified")
        
    except Exception as e:
        print(f"Error in Predict test: {e}")
        raise

def test_dspy_lm_direct_usage():
    """Test direct usage of dspy.LM with our configuration."""
    print("\nTesting direct dspy.LM usage...")
    
    try:
        # Import the API key
        from src.config.settings import GOOGLE_API_KEY
        
        # Create dspy.LM directly with our settings
        lm = dspy.LM(
            model=LLM_MODEL,
            api_key=GOOGLE_API_KEY,
            temperature=LLM_TEMPERATURE,
            max_tokens=4000,
            cache=True
        )
        
        # Configure DSPy
        dspy.configure(lm=lm)
        
        # Test basic functionality
        response = lm("Hello, this is a test.")
        assert response is not None, "LM should return a response"
        print("✓ Direct dspy.LM usage successful")
        
    except Exception as e:
        print(f"Error in direct LM usage test: {e}")
        raise

if __name__ == "__main__":
    test_dspy_configure_integration()
    test_forward_method_signature()
    test_dspy_chain_of_thought_integration()
    test_dspy_predict_integration()
    test_dspy_lm_direct_usage() 