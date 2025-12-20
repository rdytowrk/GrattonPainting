"""Data models for the harness."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TestCaseCategory(str, Enum):
    """Test case difficulty categories."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class InputType(str, Enum):
    """Type of input for conversion."""
    HTML = "html"
    URL = "url"
    SCREENSHOT = "screenshot"


class TestCase(BaseModel):
    """Represents a single test case."""
    
    id: str
    name: str
    description: Optional[str] = None
    input_type: InputType
    input_path: str  # Path to HTML file or screenshot
    input_url: Optional[str] = None  # Original URL if applicable
    expected_output_path: Optional[str] = None
    category: TestCaseCategory = TestCaseCategory.MEDIUM
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True


class ConversionResult(BaseModel):
    """Result of a single HTML conversion."""
    
    test_case_id: str
    prompt_name: str
    output_html: str
    raw_response: Optional[str] = None  # Full API response
    success: bool = True
    error_message: Optional[str] = None
    
    # API metadata
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None  # seconds
    cost: Optional[float] = None  # estimated cost in USD
    
    # Output analysis
    output_size: Optional[int] = None  # bytes
    line_count: Optional[int] = None
    
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True


class MetricScore(BaseModel):
    """Score for a single metric."""
    
    name: str
    score: float  # 0.0 to 1.0
    weight: float
    passed: bool
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class EvaluationScore(BaseModel):
    """Complete evaluation score for a conversion result."""
    
    test_case_id: str
    prompt_name: str
    run_id: str
    
    # Individual metric scores
    metrics: List[MetricScore] = Field(default_factory=list)
    
    # Overall scores
    weighted_score: float  # Weighted average of all metrics
    simple_average: float  # Simple average
    passed: bool  # Based on threshold
    
    # Summary
    passed_metrics: int
    failed_metrics: int
    total_metrics: int
    
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def get_metric_score(self, metric_name: str) -> Optional[MetricScore]:
        """Get score for a specific metric."""
        for metric in self.metrics:
            if metric.name == metric_name:
                return metric
        return None


class TestRun(BaseModel):
    """Represents a complete test run."""
    
    run_id: str
    prompt_name: str
    description: Optional[str] = None
    
    # Test execution
    test_case_ids: List[str] = Field(default_factory=list)
    results: List[ConversionResult] = Field(default_factory=list)
    evaluations: List[EvaluationScore] = Field(default_factory=list)
    
    # Summary statistics
    total_tests: int = 0
    successful_conversions: int = 0
    failed_conversions: int = 0
    passed_evaluations: int = 0
    failed_evaluations: int = 0
    
    # Performance metrics
    total_tokens: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    
    # Overall scores
    average_weighted_score: float = 0.0
    average_simple_score: float = 0.0
    
    # Metadata
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None  # seconds
    
    # Configuration snapshot
    config_snapshot: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True
    
    def calculate_summary(self):
        """Calculate summary statistics from results and evaluations."""
        self.total_tests = len(self.test_case_ids)
        self.successful_conversions = sum(1 for r in self.results if r.success)
        self.failed_conversions = self.total_tests - self.successful_conversions
        
        self.passed_evaluations = sum(1 for e in self.evaluations if e.passed)
        self.failed_evaluations = len(self.evaluations) - self.passed_evaluations
        
        if self.results:
            self.total_tokens = sum(r.tokens_used or 0 for r in self.results)
            self.total_cost = sum(r.cost or 0.0 for r in self.results)
            
            response_times = [r.response_time for r in self.results if r.response_time]
            if response_times:
                self.average_response_time = sum(response_times) / len(response_times)
        
        if self.evaluations:
            self.average_weighted_score = sum(e.weighted_score for e in self.evaluations) / len(self.evaluations)
            self.average_simple_score = sum(e.simple_average for e in self.evaluations) / len(self.evaluations)
        
        if self.started_at and self.completed_at:
            self.duration = (self.completed_at - self.started_at).total_seconds()


class PromptConfig(BaseModel):
    """Configuration for a prompt."""
    
    name: str
    file: str
    description: str
    active: bool = True
    parent: Optional[str] = None
    
    parameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    
    # Performance tracking
    runs: int = 0
    average_score: Optional[float] = None
    best_score: Optional[float] = None
    worst_score: Optional[float] = None
