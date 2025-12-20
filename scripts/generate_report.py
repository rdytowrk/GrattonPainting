#!/usr/bin/env python3
"""Generate a report from a test run."""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.harness.config import load_config
from src.utils.run_manager import RunManager
from src.reporters.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description="Generate test run report")
    
    parser.add_argument(
        "--run",
        help="Run ID to generate report for (use 'latest' for most recent)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Report format (default: markdown)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: results/reports/{run_id}.{ext})"
    )
    parser.add_argument(
        "--compare",
        help="Compare multiple runs (comma-separated run IDs)"
    )
    parser.add_argument(
        "--no-details",
        action="store_true",
        help="Exclude detailed metrics"
    )
    parser.add_argument(
        "--no-recommendations",
        action="store_true",
        help="Exclude recommendations"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    run_manager = RunManager(config)
    reporter = ReportGenerator(config)
    
    # Handle comparison mode
    if args.compare:
        run_ids = [rid.strip() for rid in args.compare.split(",")]
        
        print(f"Generating comparison report for {len(run_ids)} runs...")
        report = reporter.generate_comparison_report(run_ids)
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = reporter.reports_dir / f"comparison_{run_ids[0][:15]}.md"
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {output_path}")
        print("\n" + report)
        return
    
    # Single run report
    run_id = args.run
    
    if not run_id or run_id == "latest":
        run_id = run_manager.get_latest_run()
        if not run_id:
            print("Error: No runs found", file=sys.stderr)
            sys.exit(1)
        print(f"Using latest run: {run_id}")
    
    # Check if run exists
    test_run = run_manager.load_run(run_id)
    if not test_run:
        print(f"Error: Run '{run_id}' not found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generating {args.format} report for run: {run_id}")
    
    # Generate report
    if args.format == "markdown":
        report = reporter.generate_markdown_report(
            run_id,
            include_details=not args.no_details,
            include_recommendations=not args.no_recommendations
        )
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = reporter.reports_dir / f"{run_id}.md"
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {output_path}")
        
        # Also print to stdout
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80)
    
    elif args.format == "json":
        import json
        
        report = reporter.generate_json_report(run_id)
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = reporter.reports_dir / f"{run_id}.json"
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved to: {output_path}")
        
        # Print summary to stdout
        print("\nSummary:")
        print(json.dumps(report.get("summary", {}), indent=2))


if __name__ == "__main__":
    main()
