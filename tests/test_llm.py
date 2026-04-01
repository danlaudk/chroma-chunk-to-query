"""
Test script to verify DSPy and LLM integration.
"""
import dspy
from src.models.llm_model import initialize_dspy

def test_llm_setup():
    print("Testing LLM Integration...")
    
    try:
        # Initialize the LLM using default config (mapped via JSON)
        llm = initialize_dspy(model_name="z-ai")
        # llm = initialize_dspy(model_name="summllama3")

        print("✓ LLM initialization successful")
        
        # Test basic completion
        prompt = "What is the capital of GERMANY?"
        print(f"\nTesting completion with prompt: '{prompt}'")
        
        response = llm(prompt)
        print(f"Response received: {response}")
        
        print("\nLLM integration is working correctly!")
        
    except Exception as e:
        print(f"Error in LLM setup: {e}")
        raise

if __name__ == "__main__":
    test_llm_setup() 