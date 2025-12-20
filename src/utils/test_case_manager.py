"""Manage test cases."""

import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..harness.config import HarnessConfig
from ..harness.models import TestCase, InputType, TestCaseCategory
from .file_utils import save_json, load_json, save_html, load_html


class TestCaseManager:
    """Manages test cases and their metadata."""
    
    def __init__(self, config: HarnessConfig):
        """Initialize test case manager."""
        self.config = config
        self.test_cases_dir = config.test_cases_dir
        self.metadata_file = self.test_cases_dir / "metadata.json"
        
        # Load metadata
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load test cases metadata."""
        if not self.metadata_file.exists():
            return {
                "test_cases": [],
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "total_cases": 0,
                "categories": {
                    "simple": [],
                    "medium": [],
                    "complex": []
                },
                "tags": {}
            }
        
        return load_json(self.metadata_file)
    
    def _save_metadata(self):
        """Save test cases metadata."""
        self.metadata["last_updated"] = datetime.now().isoformat()
        save_json(self.metadata, self.metadata_file)
    
    def add_test_case(
        self,
        name: str,
        input_html: str,
        input_type: InputType = InputType.HTML,
        category: TestCaseCategory = TestCaseCategory.MEDIUM,
        description: Optional[str] = None,
        input_url: Optional[str] = None,
        expected_output: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> TestCase:
        """
        Add a new test case.
        
        Args:
            name: Name of the test case
            input_html: HTML content
            input_type: Type of input (HTML, URL, screenshot)
            category: Difficulty category
            description: Optional description
            input_url: Original URL if applicable
            expected_output: Optional expected output HTML
            tags: Optional tags for categorization
            
        Returns:
            TestCase object
        """
        # Generate ID
        test_id = f"test_{uuid.uuid4().hex[:8]}"
        
        # Save input HTML
        input_dir = self.test_cases_dir / "html_inputs"
        input_dir.mkdir(exist_ok=True)
        input_path = input_dir / f"{test_id}.html"
        save_html(input_html, input_path)
        
        # Save expected output if provided
        expected_output_path = None
        if expected_output:
            output_dir = self.test_cases_dir / "expected_outputs"
            output_dir.mkdir(exist_ok=True)
            expected_output_path = output_dir / f"{test_id}.html"
            save_html(expected_output, expected_output_path)
        
        # Create test case
        test_case = TestCase(
            id=test_id,
            name=name,
            description=description,
            input_type=input_type,
            input_path=str(input_path.relative_to(self.config.project_root)),
            input_url=input_url,
            expected_output_path=str(expected_output_path.relative_to(self.config.project_root)) if expected_output_path else None,
            category=category,
            tags=tags or [],
            created_at=datetime.now()
        )
        
        # Update metadata
        self.metadata["test_cases"].append(test_case.model_dump())
        self.metadata["total_cases"] = len(self.metadata["test_cases"])
        self.metadata["categories"][category.value].append(test_id)
        
        # Update tags
        for tag in test_case.tags:
            if tag not in self.metadata["tags"]:
                self.metadata["tags"][tag] = []
            self.metadata["tags"][tag].append(test_id)
        
        self._save_metadata()
        
        return test_case
    
    def get_test_case(self, test_id: str) -> Optional[TestCase]:
        """Get a test case by ID."""
        for case_data in self.metadata["test_cases"]:
            if case_data["id"] == test_id:
                return TestCase(**case_data)
        return None
    
    def list_test_cases(
        self,
        category: Optional[TestCaseCategory] = None,
        tags: Optional[List[str]] = None
    ) -> List[TestCase]:
        """
        List test cases with optional filtering.
        
        Args:
            category: Filter by category
            tags: Filter by tags (must have all tags)
            
        Returns:
            List of TestCase objects
        """
        cases = []
        
        for case_data in self.metadata["test_cases"]:
            # Filter by category
            if category and case_data["category"] != category.value:
                continue
            
            # Filter by tags
            if tags:
                case_tags = set(case_data.get("tags", []))
                if not all(tag in case_tags for tag in tags):
                    continue
            
            cases.append(TestCase(**case_data))
        
        return cases
    
    def get_test_input(self, test_case: TestCase) -> str:
        """Get the input HTML for a test case."""
        input_path = self.config.project_root / test_case.input_path
        return load_html(input_path)
    
    def get_expected_output(self, test_case: TestCase) -> Optional[str]:
        """Get the expected output HTML for a test case."""
        if not test_case.expected_output_path:
            return None
        
        output_path = self.config.project_root / test_case.expected_output_path
        return load_html(output_path)
    
    def delete_test_case(self, test_id: str) -> bool:
        """Delete a test case."""
        test_case = self.get_test_case(test_id)
        if not test_case:
            return False
        
        # Remove from metadata
        self.metadata["test_cases"] = [
            case for case in self.metadata["test_cases"]
            if case["id"] != test_id
        ]
        
        # Update category
        category = test_case.category.value
        if test_id in self.metadata["categories"][category]:
            self.metadata["categories"][category].remove(test_id)
        
        # Update tags
        for tag in test_case.tags:
            if tag in self.metadata["tags"] and test_id in self.metadata["tags"][tag]:
                self.metadata["tags"][tag].remove(test_id)
        
        self.metadata["total_cases"] = len(self.metadata["test_cases"])
        self._save_metadata()
        
        # Delete files
        try:
            input_path = self.config.project_root / test_case.input_path
            if input_path.exists():
                input_path.unlink()
            
            if test_case.expected_output_path:
                output_path = self.config.project_root / test_case.expected_output_path
                if output_path.exists():
                    output_path.unlink()
        except Exception:
            pass
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get test case statistics."""
        return {
            "total": self.metadata["total_cases"],
            "by_category": {
                category: len(test_ids)
                for category, test_ids in self.metadata["categories"].items()
            },
            "by_tag": {
                tag: len(test_ids)
                for tag, test_ids in self.metadata["tags"].items()
            }
        }
