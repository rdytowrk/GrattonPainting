#!/usr/bin/env python3
"""
Validate test case metadata and files.
Usage: python scripts/validate_test_cases.py
"""
import json
import sys
from pathlib import Path

def validate_metadata():
    """Validate test case metadata structure."""
    print("Validating test case metadata...")
    
    try:
        with open('test_cases/metadata.json', 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print("❌ test_cases/metadata.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in metadata.json: {e}")
        return False
    
    print(f"Total test cases: {metadata.get('total_cases', 0)}")
    print(f"Categories: {dict(metadata.get('categories', {}))}")
    print(f"Tags: {list(metadata.get('tags', {}).keys())}")
    
    # Validate structure
    required_keys = ['test_cases', 'version', 'total_cases', 'categories', 'tags']
    for key in required_keys:
        if key not in metadata:
            print(f'❌ Missing required key: {key}')
            return False
    
    print('✅ Metadata validation passed')
    return True

def check_files_exist():
    """Check that all test case files exist."""
    print("\nChecking test case files...")
    
    with open('test_cases/metadata.json', 'r') as f:
        metadata = json.load(f)
    
    errors = []
    for test_case in metadata['test_cases']:
        input_path = Path(test_case['input_path'])
        if not input_path.exists():
            errors.append(f'Missing input file: {input_path}')
        
        if test_case.get('expected_output_path'):
            output_path = Path(test_case['expected_output_path'])
            if not output_path.exists():
                errors.append(f'Missing expected output file: {output_path}')
    
    if errors:
        print('❌ Validation errors:')
        for error in errors:
            print(f'  - {error}')
        return False
    else:
        print('✅ All test case files exist')
        return True

if __name__ == "__main__":
    success = True
    success = validate_metadata() and success
    success = check_files_exist() and success
    
    if success:
        print("\n✅ All validations passed!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed!")
        sys.exit(1)
