#!/usr/bin/env python3
"""Add a new test case to the harness."""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.harness.config import load_config
from src.harness.models import InputType, TestCaseCategory
from src.utils.test_case_manager import TestCaseManager


def fetch_html_from_url(url: str) -> str:
    """Fetch HTML content from a URL."""
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Add a new test case to the harness")
    
    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--url", help="Fetch HTML from URL")
    input_group.add_argument("--file", help="Load HTML from local file")
    input_group.add_argument("--stdin", action="store_true", help="Read HTML from stdin")
    
    # Test case metadata
    parser.add_argument("--name", required=True, help="Name for the test case")
    parser.add_argument("--description", help="Description of the test case")
    parser.add_argument(
        "--category",
        choices=["simple", "medium", "complex"],
        default="medium",
        help="Difficulty category (default: medium)"
    )
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--expected", help="Path to expected output HTML file")
    
    args = parser.parse_args()
    
    # Load HTML content
    if args.url:
        print(f"Fetching HTML from {args.url}...")
        html_content = fetch_html_from_url(args.url)
        input_type = InputType.URL
        input_url = args.url
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        input_type = InputType.HTML
        input_url = None
    else:  # stdin
        print("Reading HTML from stdin...")
        html_content = sys.stdin.read()
        input_type = InputType.HTML
        input_url = None
    
    if not html_content.strip():
        print("Error: Empty HTML content", file=sys.stderr)
        sys.exit(1)
    
    # Load expected output if provided
    expected_output = None
    if args.expected:
        expected_path = Path(args.expected)
        if not expected_path.exists():
            print(f"Warning: Expected output file not found: {args.expected}", file=sys.stderr)
        else:
            with open(expected_path, 'r', encoding='utf-8') as f:
                expected_output = f.read()
    
    # Parse tags
    tags = []
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(",")]
    
    # Parse category
    category = TestCaseCategory(args.category)
    
    # Initialize manager
    config = load_config()
    manager = TestCaseManager(config)
    
    # Add test case
    print(f"Adding test case '{args.name}'...")
    test_case = manager.add_test_case(
        name=args.name,
        input_html=html_content,
        input_type=input_type,
        category=category,
        description=args.description,
        input_url=input_url,
        expected_output=expected_output,
        tags=tags
    )
    
    print(f"✅ Test case added successfully!")
    print(f"   ID: {test_case.id}")
    print(f"   Name: {test_case.name}")
    print(f"   Category: {test_case.category}")
    print(f"   Input size: {len(html_content)} bytes")
    if tags:
        print(f"   Tags: {', '.join(tags)}")


if __name__ == "__main__":
    main()
