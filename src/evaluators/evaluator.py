"""Main evaluator orchestrator."""

from typing import Dict, Any, List
from ..harness.config import HarnessConfig
from ..harness.models import ConversionResult, EvaluationScore, MetricScore

from .html_validator import HTMLValidator
from .tailwind_analyzer import TailwindAnalyzer
from .semantic_analyzer import SemanticAnalyzer
from .accessibility_checker import AccessibilityChecker
from .code_quality import CodeQualityChecker


class Evaluator:
    """Orchestrates all evaluation metrics."""
    
    def __init__(self, config: HarnessConfig):
        """Initialize evaluator with configuration."""
        self.config = config
        self.metrics_config = config.get_enabled_metrics()
        self.scoring_config = config.get_scoring_config()
        
        # Initialize metric analyzers
        self.validators = {
            'html_validity': HTMLValidator(),
            'tailwind_coverage': TailwindAnalyzer(),
            'semantic_score': SemanticAnalyzer(),
            'accessibility_score': AccessibilityChecker(),
            'code_quality': CodeQualityChecker(),
        }
    
    def evaluate(self, result: ConversionResult, run_id: str) -> EvaluationScore:
        """
        Evaluate a conversion result.
        
        Args:
            result: ConversionResult to evaluate
            run_id: ID of the test run
            
        Returns:
            EvaluationScore with all metrics
        """
        if not result.success:
            # Can't evaluate failed conversion
            return EvaluationScore(
                test_case_id=result.test_case_id,
                prompt_name=result.prompt_name,
                run_id=run_id,
                metrics=[],
                weighted_score=0.0,
                simple_average=0.0,
                passed=False,
                passed_metrics=0,
                failed_metrics=0,
                total_metrics=0
            )
        
        metric_scores: List[MetricScore] = []
        
        # Run each enabled metric
        for metric_name, metric_config in self.metrics_config.items():
            if not metric_config.get('enabled', False):
                continue
            
            try:
                # Get the appropriate validator
                validator = self.validators.get(metric_name)
                if not validator:
                    continue
                
                # Run analysis
                analysis_result = validator.analyze(result.output_html)
                
                # Get weight and threshold
                weight = metric_config.get('weight', 1.0)
                min_threshold = metric_config.get('min_threshold', 0.0)
                
                # Create metric score
                score = analysis_result.get('score', 0.0)
                passed = score >= min_threshold
                
                metric_score = MetricScore(
                    name=metric_name,
                    score=score,
                    weight=weight,
                    passed=passed,
                    details=analysis_result.get('details', {})
                )
                
                metric_scores.append(metric_score)
                
            except Exception as e:
                # If a metric fails, record it but continue
                metric_score = MetricScore(
                    name=metric_name,
                    score=0.0,
                    weight=metric_config.get('weight', 1.0),
                    passed=False,
                    error=str(e)
                )
                metric_scores.append(metric_score)
        
        # Calculate overall scores
        weighted_score = self._calculate_weighted_score(metric_scores)
        simple_average = self._calculate_simple_average(metric_scores)
        
        # Determine if passed based on scoring method
        scoring_method = self.scoring_config.get('method', 'weighted_average')
        pass_threshold = self.scoring_config.get('pass_threshold', 0.7)
        
        if scoring_method == 'weighted_average':
            overall_score = weighted_score
        elif scoring_method == 'simple_average':
            overall_score = simple_average
        elif scoring_method == 'minimum':
            overall_score = min((m.score for m in metric_scores), default=0.0)
        else:
            overall_score = weighted_score
        
        passed = overall_score >= pass_threshold
        
        # Count passed/failed metrics
        passed_metrics = sum(1 for m in metric_scores if m.passed)
        failed_metrics = len(metric_scores) - passed_metrics
        
        return EvaluationScore(
            test_case_id=result.test_case_id,
            prompt_name=result.prompt_name,
            run_id=run_id,
            metrics=metric_scores,
            weighted_score=weighted_score,
            simple_average=simple_average,
            passed=passed,
            passed_metrics=passed_metrics,
            failed_metrics=failed_metrics,
            total_metrics=len(metric_scores)
        )
    
    def _calculate_weighted_score(self, metrics: List[MetricScore]) -> float:
        """Calculate weighted average score."""
        if not metrics:
            return 0.0
        
        total_weight = sum(m.weight for m in metrics)
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(m.score * m.weight for m in metrics)
        return weighted_sum / total_weight
    
    def _calculate_simple_average(self, metrics: List[MetricScore]) -> float:
        """Calculate simple average score."""
        if not metrics:
            return 0.0
        
        return sum(m.score for m in metrics) / len(metrics)
