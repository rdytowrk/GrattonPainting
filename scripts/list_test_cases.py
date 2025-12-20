#!/usr/bin/env python3
"""List test cases in the harness."""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.harness.config import load_config
from src.harness.models import TestCaseCategory
from src.utils.test_case_manager import TestCaseManager


def main():
    parser = argparse.ArgumentParser(description="List test cases")
    
    parser.add_argument(
        "--category",
        choices=["simple", "medium", "complex"],
        help="Filter by category"
    )
    parser.add_argument(
        "--tags",
        help="Filter by tags (comma-separated)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed information"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics only"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    manager = TestCaseManager(config)
    
    # Show statistics
    if args.stats:
        stats = manager.get_statistics()
        
        print("Test Case Statistics")
        print("=" * 60)
        print(f"Total test cases: {stats['total']}")
        print()
        
        print("By Category:")
        for category, count in stats['by_category'].items():
            print(f"  {category}: {count}")
        print()
        
        if stats['by_tag']:
            print("By Tag:")
            for tag, count in sorted(stats['by_tag'].items()):
                print(f"  {tag}: {count}")
        
        return
    
    # Filter parameters
    category = TestCaseCategory(args.category) if args.category else None
    tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else None
    
    # Get test cases
    test_cases = manager.list_test_cases(category=category, tags=tags)
    
    if not test_cases:
        print("No test cases found.")
        return
    
    # Display test cases
    print(f"Found {len(test_cases)} test case(s)")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\n{test_case.name}")
        print(f"  ID: {test_case.id}")
        print(f"  Category: {test_case.category}")
        
        if args.verbose:
            if test_case.description:
                print(f"  Description: {test_case.description}")
            
            print(f"  Input type: {test_case.input_type}")
            
            if test_case.input_url:
                print(f"  URL: {test_case.input_url}")
            
            if test_case.tags:
                print(f"  Tags: {', '.join(test_case.tags)}")
            
            print(f"  Created: {test_case.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Get file size
            input_path = config.project_root / test_case.input_path
            if input_path.exists():
                size = input_path.stat().st_size
                print(f"  Input size: {size} bytes")


if __name__ == "__main__":
    main()
