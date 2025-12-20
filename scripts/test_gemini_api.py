#!/usr/bin/env python3
"""
Test Gemini API connection with detailed diagnostics.
Usage: python scripts/test_gemini_api.py
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_api_connection():
    """Test Gemini API with detailed error reporting."""
    print("=" * 60)
    print("Gemini API Connection Test")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in environment")
        print("\n💡 Set it with:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        return False
    
    print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Check model name
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-exp")
    print(f"✓ Using model: {model_name}")
    
    # Try to import the library
    try:
        from google import genai
        print("✓ google-genai library imported successfully")
    except ImportError as e:
        print(f"❌ ERROR: Failed to import google-genai: {e}")
        print("\n💡 Install it with:")
        print("   pip install google-genai")
        return False
    
    # Test API connection
    print("\nTesting API connection...")
    try:
        client = genai.Client(api_key=api_key)
        print("✓ Client created successfully")
        
        # Try to generate content
        print(f"\nSending test request to {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents="Respond with exactly: OK"
        )
        
        response_text = response.text
        print(f"✓ Response received: '{response_text}'")
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! API connection is working")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: API request failed")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        # Provide helpful suggestions
        print("\n💡 Troubleshooting:")
        print("1. Check if your API key is valid at https://aistudio.google.com/")
        print("2. Verify the model name is correct")
        print(f"   Current model: {model_name}")
        print("   Try these alternatives:")
        print("   - gemini-2.5-flash-exp")
        print("   - gemini-2.5-flash")
        print("   - gemini-2.0-flash-exp")
        print("   - gemini-1.5-flash-latest")
        print("\n3. Check if you have API quota remaining (free tier: 1M tokens/day)")
        print("4. Ensure you have enabled the Gemini API in your Google Cloud project")
        
        return False

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)
