"""
Test script to verify DSPy LLM routing behavior and configuration.
"""
import dspy
from src.models.llm_model import initialize_dspy

def test_dspy_llm_routing():
    """Test how DSPy routes LLM calls in different contexts."""
    print("Testing DSPy LLM Routing...")
    
    try:
        # Initialize our custom LLM model
        llm = initialize_dspy()
        print("✓ Custom LLM model initialized")
        
        # Test 1: Direct call to our model
        print("\nTest 1: Direct call to our LLM")
        response1 = llm("What is 2+2?")
        print(f"Direct response: {response1}")
        
        # Test 2: DSPy ChainOfThought using our model
        print("\nTest 2: DSPy ChainOfThought")
        cot = dspy.ChainOfThought("question -> answer")
        response2 = cot(question="What is 2+2?")
        print(f"ChainOfThought response: {response2}")
        
        # Test 3: DSPy Predict using our model
        print("\nTest 3: DSPy Predict")
        predictor = dspy.Predict("input -> output")
        response3 = predictor(input="What is 2+2?")
        print(f"Predict response: {response3}")
        
        print("✓ DSPy LLM routing test completed!")
        
    except Exception as e:
        print(f"Error in DSPy LLM routing test: {e}")
        raise

def test_dspy_configuration_verification():
    """Test to verify DSPy's configuration is properly applied."""
    print("\nTesting DSPy Configuration Verification...")
    
    try:
        # Initialize our custom LLM model
        llm = initialize_dspy()
        print("✓ Custom LLM model initialized")
        
        # Check DSPy's current configuration
        print("\nDSPy Configuration Check:")
        print(f"Current LM: {dspy.settings.lm}")
        print(f"LM type: {type(dspy.settings.lm)}")
        
        # Test if DSPy is using our model
        if hasattr(dspy.settings.lm, 'model'):
            print(f"Configured model: {dspy.settings.lm.model}")
        else:
            print("Configured LM doesn't have 'model' attribute")
        
        # Test 4: Create a simple DSPy program and see what happens
        print("\nTest 4: Simple DSPy Program")
        simple_prog = dspy.ChainOfThought("x -> y")
        
        # This should use our configured LM
        result = simple_prog(x="What is the capital of France?")
        print(f"Simple program result: {result}")
        
        print("✓ DSPy configuration verification completed!")
        
    except Exception as e:
        print(f"Error in DSPy configuration verification: {e}")
        raise

def test_model_name_routing():
    """Test if different model names are routed differently."""
    print("\nTesting Model Name Routing...")
    
    try:
        # Test with our current model name
        print("Current model name test:")
        llm = initialize_dspy()
        
        # Try to create a ChainOfThought with explicit model specification
        print("\nTrying ChainOfThought with explicit model...")
        cot = dspy.ChainOfThought("question -> answer")
        
        # This should help us see if the issue is with model name routing
        result = cot(question="What is 2+2?")
        print(f"Explicit model result: {result}")
        
        print("✓ Model name routing test completed!")
        
    except Exception as e:
        print(f"Error in model name routing test: {e}")
        raise

if __name__ == "__main__":
    test_dspy_llm_routing()
    test_dspy_configuration_verification()
    test_model_name_routing() 