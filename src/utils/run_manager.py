"""Manage test runs and results."""

import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..harness.config import HarnessConfig
from ..harness.models import TestRun, ConversionResult, EvaluationScore
from .file_utils import save_json, load_json, save_html, ensure_dir


class RunManager:
    """Manages test runs and their results."""
    
    def __init__(self, config: HarnessConfig):
        """Initialize run manager."""
        self.config = config
        self.runs_dir = config.results_dir / "runs"
        ensure_dir(self.runs_dir)
    
    def create_run(
        self,
        prompt_name: str,
        test_case_ids: List[str],
        description: Optional[str] = None
    ) -> TestRun:
        """
        Create a new test run.
        
        Args:
            prompt_name: Name of the prompt being tested
            test_case_ids: List of test case IDs to run
            description: Optional description
            
        Returns:
            TestRun object
        """
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # Create run directory
        run_dir = self.runs_dir / run_id
        ensure_dir(run_dir)
        
        # Snapshot current configuration
        config_snapshot = {
            "prompt_config": self.config.get_prompt_config(prompt_name),
            "evaluation_config": self.config.get_evaluation_metrics(),
            "scoring_config": self.config.get_scoring_config(),
        }
        
        test_run = TestRun(
            run_id=run_id,
            prompt_name=prompt_name,
            description=description,
            test_case_ids=test_case_ids,
            config_snapshot=config_snapshot
        )
        
        return test_run
    
    def save_result(self, run_id: str, result: ConversionResult):
        """Save a conversion result."""
        run_dir = self.runs_dir / run_id
        results_dir = run_dir / "results"
        ensure_dir(results_dir)
        
        # Save result as JSON
        result_file = results_dir / f"{result.test_case_id}_result.json"
        save_json(result.model_dump(), result_file)
        
        # Save output HTML
        if result.success and result.output_html:
            html_file = results_dir / f"{result.test_case_id}_output.html"
            save_html(result.output_html, html_file)
        
        # Save raw response if available
        if result.raw_response:
            raw_file = results_dir / f"{result.test_case_id}_raw.txt"
            with open(raw_file, 'w') as f:
                f.write(result.raw_response)
    
    def save_evaluation(self, run_id: str, evaluation: EvaluationScore):
        """Save an evaluation score."""
        run_dir = self.runs_dir / run_id
        evals_dir = run_dir / "evaluations"
        ensure_dir(evals_dir)
        
        eval_file = evals_dir / f"{evaluation.test_case_id}_eval.json"
        save_json(evaluation.model_dump(), eval_file)
    
    def save_run(self, test_run: TestRun):
        """Save complete test run."""
        run_dir = self.runs_dir / test_run.run_id
        
        # Mark as completed
        if not test_run.completed_at:
            test_run.completed_at = datetime.now()
        
        # Calculate summary
        test_run.calculate_summary()
        
        # Save run metadata
        run_file = run_dir / "run.json"
        save_json(test_run.model_dump(), run_file)
    
    def load_run(self, run_id: str) -> Optional[TestRun]:
        """Load a test run."""
        run_file = self.runs_dir / run_id / "run.json"
        
        if not run_file.exists():
            return None
        
        run_data = load_json(run_file)
        return TestRun(**run_data)
    
    def load_results(self, run_id: str) -> List[ConversionResult]:
        """Load all results for a run."""
        results_dir = self.runs_dir / run_id / "results"
        
        if not results_dir.exists():
            return []
        
        results = []
        for result_file in results_dir.glob("*_result.json"):
            result_data = load_json(result_file)
            results.append(ConversionResult(**result_data))
        
        return results
    
    def load_evaluations(self, run_id: str) -> List[EvaluationScore]:
        """Load all evaluations for a run."""
        evals_dir = self.runs_dir / run_id / "evaluations"
        
        if not evals_dir.exists():
            return []
        
        evaluations = []
        for eval_file in evals_dir.glob("*_eval.json"):
            eval_data = load_json(eval_file)
            evaluations.append(EvaluationScore(**eval_data))
        
        return evaluations
    
    def list_runs(self, prompt_name: Optional[str] = None) -> List[str]:
        """
        List all run IDs, optionally filtered by prompt name.
        
        Args:
            prompt_name: Filter by prompt name
            
        Returns:
            List of run IDs
        """
        runs = []
        
        for run_dir in self.runs_dir.iterdir():
            if not run_dir.is_dir():
                continue
            
            run_file = run_dir / "run.json"
            if not run_file.exists():
                continue
            
            if prompt_name:
                run_data = load_json(run_file)
                if run_data.get("prompt_name") != prompt_name:
                    continue
            
            runs.append(run_dir.name)
        
        # Sort by date (newest first)
        runs.sort(reverse=True)
        return runs
    
    def get_latest_run(self, prompt_name: Optional[str] = None) -> Optional[str]:
        """Get the most recent run ID."""
        runs = self.list_runs(prompt_name)
        return runs[0] if runs else None
    
    def delete_run(self, run_id: str) -> bool:
        """Delete a test run and all its data."""
        run_dir = self.runs_dir / run_id
        
        if not run_dir.exists():
            return False
        
        # Delete all files in the run directory
        import shutil
        shutil.rmtree(run_dir)
        
        return True
