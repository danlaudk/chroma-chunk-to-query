"""
Test script to verify DSPy and LiteLLM integration.
"""
import dspy
from ..models.llm_model import initialize_litellm_dspy

def test_llm_setup():
    print("Testing LLM Integration...")
    
    try:
        # Initialize the LLM
        llm = initialize_litellm_dspy()
        print("✓ LiteLLM initialization successful")
        
        # Test basic completion
        prompt = "What is the capital of France?"
        print(f"\nTesting completion with prompt: '{prompt}'")
        
        response = llm(prompt)
        print(f"Response received: {response}")
        
        print("\nLLM integration is working correctly!")
        
    except Exception as e:
        print(f"Error in LLM setup: {e}")
        raise

if __name__ == "__main__":
    test_llm_setup() 