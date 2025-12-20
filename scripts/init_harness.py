#!/usr/bin/env python3
"""Initialize the harness with a sample test case."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.harness.config import load_config
from src.harness.models import InputType, TestCaseCategory
from src.utils.test_case_manager import TestCaseManager


SAMPLE_HTML = """
<div style="display: flex; justify-content: center; padding: 20px; background-color: #f3f4f6;">
  <div style="max-width: 600px; background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h2 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #1f2937;">Welcome to the Harness</h2>
    <p style="color: #6b7280; margin-bottom: 12px;">This is a sample test case to verify the harness is working correctly.</p>
    <p style="color: #6b7280;">The goal is to convert this HTML with inline styles into clean HTML with Tailwind CSS classes.</p>
    <div style="margin-top: 24px;">
      <button style="background-color: #3b82f6; color: white; padding: 12px 24px; border-radius: 6px; border: none; cursor: pointer;">
        Get Started
      </button>
    </div>
  </div>
</div>
""".strip()


def main():
    print("Initializing HTML-to-Tailwind Conversion Harness")
    print("=" * 60)
    
    # Load configuration
    print("\n1. Loading configuration...")
    try:
        config = load_config()
        print("   ✅ Configuration loaded")
    except Exception as e:
        print(f"   ❌ Failed to load configuration: {e}")
        sys.exit(1)
    
    # Check environment
    print("\n2. Checking environment...")
    try:
        api_key = config.get_gemini_api_key()
        if api_key:
            print("   ✅ Gemini API key found")
        else:
            print("   ❌ Gemini API key not found")
            print("   Please set GEMINI_API_KEY in your .env file")
            sys.exit(1)
    except Exception as e:
        print(f"   ❌ {e}")
        print("   Please create a .env file with your GEMINI_API_KEY")
        sys.exit(1)
    
    # Test API connection
    print("\n3. Testing API connection...")
    try:
        from src.agents.gemini_agent import GeminiAgent
        agent = GeminiAgent(config)
        
        if agent.test_connection():
            print("   ✅ API connection successful")
        else:
            print("   ❌ API connection failed")
            print("   Please check your API key and internet connection")
            sys.exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # Add sample test case
    print("\n4. Adding sample test case...")
    try:
        manager = TestCaseManager(config)
        
        # Check if sample already exists
        existing_cases = manager.list_test_cases()
        if existing_cases:
            print(f"   ℹ️  Found {len(existing_cases)} existing test case(s)")
            print("   Skipping sample test case creation")
        else:
            test_case = manager.add_test_case(
                name="Sample: Card Component",
                input_html=SAMPLE_HTML,
                input_type=InputType.HTML,
                category=TestCaseCategory.SIMPLE,
                description="A simple card component with inline styles to be converted to Tailwind",
                tags=["sample", "card", "simple"]
            )
            print(f"   ✅ Sample test case created: {test_case.id}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # Print next steps
    print("\n" + "=" * 60)
    print("✅ Harness initialized successfully!")
    print("\nNext steps:")
    print("\n1. Add more test cases:")
    print("   python scripts/add_test_case.py --url https://example.com --name 'My Test'")
    print("   python scripts/add_test_case.py --file test.html --name 'My Test'")
    print("\n2. List test cases:")
    print("   python scripts/list_test_cases.py")
    print("\n3. Run tests:")
    print("   python scripts/run_tests.py --all")
    print("   python scripts/run_tests.py --test <test_id>")
    print("\n4. Generate reports:")
    print("   python scripts/generate_report.py --run latest")
    print("\nFor more information, see README.md and docs/")


if __name__ == "__main__":
    main()
