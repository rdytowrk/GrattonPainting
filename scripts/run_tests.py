#!/usr/bin/env python3
"""Run tests using the harness."""

import sys
import argparse
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.harness.config import load_config
from src.harness.models import TestCaseCategory
from src.utils.test_case_manager import TestCaseManager
from src.utils.run_manager import RunManager
from src.agents.gemini_agent import GeminiAgent
from src.evaluators.evaluator import Evaluator


def main():
    parser = argparse.ArgumentParser(description="Run tests with the harness")
    
    parser.add_argument(
        "--prompt",
        help="Prompt name to use (default: from config)"
    )
    parser.add_argument(
        "--test",
        help="Specific test case ID to run"
    )
    parser.add_argument(
        "--category",
        choices=["simple", "medium", "complex"],
        help="Run tests from specific category"
    )
    parser.add_argument(
        "--tags",
        help="Run tests with specific tags (comma-separated)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all test cases"
    )
    parser.add_argument(
        "--description",
        help="Description for this test run"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Get prompt name
    if args.prompt:
        prompt_name = args.prompt
    else:
        prompt_name = config.get_default_prompt()
    
    print(f"Using prompt: {prompt_name}")
    
    # Initialize managers
    test_manager = TestCaseManager(config)
    run_manager = RunManager(config)
    agent = GeminiAgent(config)
    evaluator = Evaluator(config)
    
    # Test API connection
    print("Testing API connection...")
    if not agent.test_connection():
        print("❌ Failed to connect to Gemini API. Check your API key.", file=sys.stderr)
        sys.exit(1)
    print("✅ API connection successful")
    
    # Get test cases to run
    test_cases: List = []
    
    if args.test:
        # Run specific test
        test_case = test_manager.get_test_case(args.test)
        if not test_case:
            print(f"Error: Test case '{args.test}' not found", file=sys.stderr)
            sys.exit(1)
        test_cases = [test_case]
    
    elif args.category:
        # Run tests from category
        category = TestCaseCategory(args.category)
        test_cases = test_manager.list_test_cases(category=category)
    
    elif args.tags:
        # Run tests with tags
        tags = [tag.strip() for tag in args.tags.split(",")]
        test_cases = test_manager.list_test_cases(tags=tags)
    
    elif args.all:
        # Run all tests
        test_cases = test_manager.list_test_cases()
    
    else:
        print("Error: No tests specified. Use --test, --category, --tags, or --all", file=sys.stderr)
        sys.exit(1)
    
    if not test_cases:
        print("No test cases found matching criteria", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nRunning {len(test_cases)} test(s)...")
    print("-" * 60)
    
    # Create test run
    test_case_ids = [tc.id for tc in test_cases]
    test_run = run_manager.create_run(
        prompt_name=prompt_name,
        test_case_ids=test_case_ids,
        description=args.description
    )
    
    print(f"Run ID: {test_run.run_id}\n")
    
    # Run each test
    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing: {test_case.name} ({test_case.id})")
        
        if args.verbose:
            print(f"  Category: {test_case.category}")
            if test_case.tags:
                print(f"  Tags: {', '.join(test_case.tags)}")
        
        try:
            # Get input HTML
            input_html = test_manager.get_test_input(test_case)
            
            if args.verbose:
                print(f"  Input size: {len(input_html)} bytes")
            
            # Convert HTML
            print("  Converting...", end=" ", flush=True)
            result = agent.convert_html(
                test_case_id=test_case.id,
                prompt_name=prompt_name,
                input_html=input_html
            )
            
            if result.success:
                print(f"✅ ({result.response_time:.2f}s)")
                
                if args.verbose:
                    print(f"  Output size: {result.output_size} bytes")
                    print(f"  Tokens: {result.tokens_used}")
                    print(f"  Cost: ${result.cost:.4f}")
                
                # Save result
                run_manager.save_result(test_run.run_id, result)
                
                # Evaluate
                print("  Evaluating...", end=" ", flush=True)
                evaluation = evaluator.evaluate(result, test_run.run_id)
                
                if evaluation.passed:
                    print(f"✅ Score: {evaluation.weighted_score:.3f}")
                else:
                    print(f"❌ Score: {evaluation.weighted_score:.3f}")
                
                if args.verbose:
                    print(f"  Passed metrics: {evaluation.passed_metrics}/{evaluation.total_metrics}")
                
                # Save evaluation
                run_manager.save_evaluation(test_run.run_id, evaluation)
                
                # Add to test run
                test_run.results.append(result)
                test_run.evaluations.append(evaluation)
            
            else:
                print(f"❌ Failed: {result.error_message}")
                
                # Save failed result
                run_manager.save_result(test_run.run_id, result)
                test_run.results.append(result)
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            if args.verbose:
                import traceback
                traceback.print_exc()
        
        print()
    
    # Save test run
    run_manager.save_run(test_run)
    
    # Print summary
    print("-" * 60)
    print("Test Run Summary")
    print("-" * 60)
    print(f"Run ID: {test_run.run_id}")
    print(f"Prompt: {test_run.prompt_name}")
    print(f"Total tests: {test_run.total_tests}")
    print(f"Successful conversions: {test_run.successful_conversions}/{test_run.total_tests}")
    print(f"Passed evaluations: {test_run.passed_evaluations}/{test_run.total_tests}")
    print(f"Average score: {test_run.average_weighted_score:.3f}")
    print(f"Total tokens: {test_run.total_tokens:,}")
    print(f"Total cost: ${test_run.total_cost:.4f}")
    print(f"Duration: {test_run.duration:.2f}s")
    print()
    
    # Generate report
    print("To generate a detailed report, run:")
    print(f"  python scripts/generate_report.py --run {test_run.run_id}")
    
    # Exit with appropriate code
    if test_run.failed_conversions > 0 or test_run.failed_evaluations > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
