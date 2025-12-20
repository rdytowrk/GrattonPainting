"""Generate reports from test runs."""

from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..harness.config import HarnessConfig
from ..harness.models import TestRun, EvaluationScore, ConversionResult
from ..utils.run_manager import RunManager
from ..utils.file_utils import ensure_dir


class ReportGenerator:
    """Generates reports in various formats."""
    
    def __init__(self, config: HarnessConfig):
        """Initialize report generator."""
        self.config = config
        self.run_manager = RunManager(config)
        self.reports_dir = config.results_dir / "reports"
        ensure_dir(self.reports_dir)
    
    def generate_markdown_report(
        self,
        run_id: str,
        include_details: bool = True,
        include_recommendations: bool = True
    ) -> str:
        """
        Generate a markdown report for a test run.
        
        Args:
            run_id: Run ID to report on
            include_details: Include detailed metrics
            include_recommendations: Include improvement recommendations
            
        Returns:
            Markdown formatted report
        """
        # Load run data
        test_run = self.run_manager.load_run(run_id)
        if not test_run:
            return f"# Error\n\nRun '{run_id}' not found."
        
        results = self.run_manager.load_results(run_id)
        evaluations = self.run_manager.load_evaluations(run_id)
        
        # Build report
        lines = []
        
        # Header
        lines.append(f"# Test Run Report: {run_id}")
        lines.append("")
        lines.append(f"**Prompt:** {test_run.prompt_name}")
        lines.append(f"**Started:** {test_run.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if test_run.completed_at:
            lines.append(f"**Completed:** {test_run.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"**Duration:** {test_run.duration:.2f}s")
        lines.append("")
        
        if test_run.description:
            lines.append(f"**Description:** {test_run.description}")
            lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Tests:** {test_run.total_tests}")
        lines.append(f"- **Successful Conversions:** {test_run.successful_conversions} ({test_run.successful_conversions/test_run.total_tests*100:.1f}%)")
        lines.append(f"- **Failed Conversions:** {test_run.failed_conversions}")
        lines.append(f"- **Passed Evaluations:** {test_run.passed_evaluations} ({test_run.passed_evaluations/test_run.total_tests*100:.1f}% if test_run.total_tests > 0 else 0)")
        lines.append(f"- **Failed Evaluations:** {test_run.failed_evaluations}")
        lines.append("")
        
        # Scores
        lines.append("## Overall Scores")
        lines.append("")
        lines.append(f"- **Average Weighted Score:** {test_run.average_weighted_score:.3f}")
        lines.append(f"- **Average Simple Score:** {test_run.average_simple_score:.3f}")
        lines.append("")
        
        # Performance
        lines.append("## Performance Metrics")
        lines.append("")
        lines.append(f"- **Total Tokens Used:** {test_run.total_tokens:,}")
        lines.append(f"- **Total Cost:** ${test_run.total_cost:.4f}")
        lines.append(f"- **Average Response Time:** {test_run.average_response_time:.2f}s")
        lines.append("")
        
        # Detailed Results
        if include_details and evaluations:
            lines.append("## Detailed Results")
            lines.append("")
            
            for eval_score in evaluations:
                lines.append(f"### Test Case: {eval_score.test_case_id}")
                lines.append("")
                lines.append(f"- **Overall Score:** {eval_score.weighted_score:.3f} ({'✅ PASSED' if eval_score.passed else '❌ FAILED'})")
                lines.append(f"- **Metrics Passed:** {eval_score.passed_metrics}/{eval_score.total_metrics}")
                lines.append("")
                
                # Metric breakdown
                lines.append("#### Metric Scores")
                lines.append("")
                lines.append("| Metric | Score | Status | Weight |")
                lines.append("|--------|-------|--------|--------|")
                
                for metric in eval_score.metrics:
                    status = "✅" if metric.passed else "❌"
                    lines.append(f"| {metric.name} | {metric.score:.3f} | {status} | {metric.weight} |")
                
                lines.append("")
                
                # Show issues if any
                failed_metrics = [m for m in eval_score.metrics if not m.passed]
                if failed_metrics:
                    lines.append("**Issues Found:**")
                    lines.append("")
                    for metric in failed_metrics:
                        lines.append(f"- **{metric.name}:** Score {metric.score:.3f}")
                        if metric.details:
                            issues = metric.details.get('issues', [])
                            for issue in issues:
                                lines.append(f"  - {issue}")
                    lines.append("")
        
        # Recommendations
        if include_recommendations:
            recommendations = self._generate_recommendations(test_run, evaluations)
            if recommendations:
                lines.append("## Recommendations")
                lines.append("")
                for i, rec in enumerate(recommendations, 1):
                    lines.append(f"{i}. {rec}")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_json_report(self, run_id: str) -> Dict[str, Any]:
        """Generate a JSON report for a test run."""
        test_run = self.run_manager.load_run(run_id)
        if not test_run:
            return {"error": f"Run '{run_id}' not found"}
        
        results = self.run_manager.load_results(run_id)
        evaluations = self.run_manager.load_evaluations(run_id)
        
        return {
            "run_id": run_id,
            "prompt_name": test_run.prompt_name,
            "summary": {
                "total_tests": test_run.total_tests,
                "successful_conversions": test_run.successful_conversions,
                "failed_conversions": test_run.failed_conversions,
                "passed_evaluations": test_run.passed_evaluations,
                "failed_evaluations": test_run.failed_evaluations,
                "average_weighted_score": test_run.average_weighted_score,
                "average_simple_score": test_run.average_simple_score,
            },
            "performance": {
                "total_tokens": test_run.total_tokens,
                "total_cost": test_run.total_cost,
                "average_response_time": test_run.average_response_time,
                "duration": test_run.duration,
            },
            "results": [r.model_dump() for r in results],
            "evaluations": [e.model_dump() for e in evaluations],
        }
    
    def save_report(self, run_id: str, format: str = "markdown") -> Path:
        """
        Generate and save a report.
        
        Args:
            run_id: Run ID to report on
            format: Report format ('markdown' or 'json')
            
        Returns:
            Path to saved report
        """
        if format == "markdown":
            content = self.generate_markdown_report(run_id)
            report_file = self.reports_dir / f"{run_id}.md"
            
            with open(report_file, 'w') as f:
                f.write(content)
        
        elif format == "json":
            content = self.generate_json_report(run_id)
            report_file = self.reports_dir / f"{run_id}.json"
            
            import json
            with open(report_file, 'w') as f:
                json.dump(content, f, indent=2)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return report_file
    
    def generate_comparison_report(self, run_ids: List[str]) -> str:
        """Generate a comparison report for multiple runs."""
        lines = []
        
        lines.append("# Test Runs Comparison")
        lines.append("")
        
        # Load all runs
        runs_data = []
        for run_id in run_ids:
            test_run = self.run_manager.load_run(run_id)
            if test_run:
                runs_data.append(test_run)
        
        if not runs_data:
            return "# Error\n\nNo valid runs found."
        
        # Comparison table
        lines.append("## Summary Comparison")
        lines.append("")
        lines.append("| Run ID | Prompt | Tests | Success Rate | Avg Score | Tokens | Cost |")
        lines.append("|--------|--------|-------|--------------|-----------|--------|------|")
        
        for run in runs_data:
            success_rate = (run.passed_evaluations / run.total_tests * 100) if run.total_tests > 0 else 0
            lines.append(
                f"| {run.run_id} | {run.prompt_name} | {run.total_tests} | "
                f"{success_rate:.1f}% | {run.average_weighted_score:.3f} | "
                f"{run.total_tokens:,} | ${run.total_cost:.4f} |"
            )
        
        lines.append("")
        
        # Best performing
        best_run = max(runs_data, key=lambda r: r.average_weighted_score)
        lines.append(f"**Best Performing:** {best_run.run_id} ({best_run.prompt_name}) with score {best_run.average_weighted_score:.3f}")
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_recommendations(
        self,
        test_run: TestRun,
        evaluations: List[EvaluationScore]
    ) -> List[str]:
        """Generate improvement recommendations based on results."""
        recommendations = []
        
        if not evaluations:
            return recommendations
        
        # Analyze common failures
        metric_failures: Dict[str, int] = {}
        
        for eval_score in evaluations:
            for metric in eval_score.metrics:
                if not metric.passed:
                    metric_failures[metric.name] = metric_failures.get(metric.name, 0) + 1
        
        # Recommend improvements for common failures
        for metric_name, count in sorted(metric_failures.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(evaluations)) * 100
            
            if metric_name == "html_validity":
                recommendations.append(
                    f"Improve HTML validation (failing in {percentage:.0f}% of tests). "
                    "Consider adding examples of valid HTML5 structure in the prompt."
                )
            
            elif metric_name == "tailwind_coverage":
                recommendations.append(
                    f"Increase Tailwind class usage (failing in {percentage:.0f}% of tests). "
                    "Emphasize using Tailwind utility classes exclusively in the prompt."
                )
            
            elif metric_name == "semantic_score":
                recommendations.append(
                    f"Improve semantic HTML usage (failing in {percentage:.0f}% of tests). "
                    "Add explicit instructions to use semantic elements like <article>, <section>, <nav>."
                )
            
            elif metric_name == "accessibility_score":
                recommendations.append(
                    f"Enhance accessibility (failing in {percentage:.0f}% of tests). "
                    "Remind the model to add alt text, labels, and ARIA attributes."
                )
            
            elif metric_name == "code_quality":
                recommendations.append(
                    f"Improve code quality (failing in {percentage:.0f}% of tests). "
                    "Specify requirements for clean, well-indented code with minimal nesting."
                )
        
        # Cost recommendations
        avg_cost_per_test = test_run.total_cost / test_run.total_tests if test_run.total_tests > 0 else 0
        if avg_cost_per_test > 0.01:
            recommendations.append(
                f"Consider optimizing for cost (${avg_cost_per_test:.4f} per test). "
                "Try reducing prompt length or adjusting max_tokens."
            )
        
        # Performance recommendations
        if test_run.average_response_time > 10:
            recommendations.append(
                f"Response time is high ({test_run.average_response_time:.1f}s average). "
                "Consider using a faster model or reducing input size."
            )
        
        return recommendations
