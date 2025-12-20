# API Documentation

This document describes the Python API for programmatically using the harness. This is useful for:
- Building custom automation
- Integrating with other tools
- Creating custom workflows
- Building UIs on top of the harness

## Core Modules

### Configuration

```python
from src.harness.config import load_config

# Load configuration
config = load_config()

# Access configuration
api_key = config.get_gemini_api_key()
model = config.get_gemini_model()
prompts = config.get_active_prompts()
metrics = config.get_enabled_metrics()
```

### Test Case Management

```python
from src.utils.test_case_manager import TestCaseManager
from src.harness.models import InputType, TestCaseCategory

manager = TestCaseManager(config)

# Add a test case
test_case = manager.add_test_case(
    name="Example Test",
    input_html="<div>Hello</div>",
    input_type=InputType.HTML,
    category=TestCaseCategory.SIMPLE,
    tags=["example"]
)

# Get test case
test_case = manager.get_test_case("test_abc123")

# List test cases
all_cases = manager.list_test_cases()
simple_cases = manager.list_test_cases(category=TestCaseCategory.SIMPLE)
tagged_cases = manager.list_test_cases(tags=["card"])

# Get test input
input_html = manager.get_test_input(test_case)

# Get statistics
stats = manager.get_statistics()
```

### Gemini Agent

```python
from src.agents.gemini_agent import GeminiAgent

agent = GeminiAgent(config)

# Test connection
if agent.test_connection():
    print("Connected!")

# Convert HTML
result = agent.convert_html(
    test_case_id="test_abc123",
    prompt_name="base_v1",
    input_html="<div>Hello</div>"
)

# Check result
if result.success:
    print(f"Output: {result.output_html}")
    print(f"Tokens: {result.tokens_used}")
    print(f"Cost: ${result.cost}")
else:
    print(f"Error: {result.error_message}")
```

### Evaluation

```python
from src.evaluators.evaluator import Evaluator

evaluator = Evaluator(config)

# Evaluate a conversion result
evaluation = evaluator.evaluate(result, run_id="run_123")

# Check evaluation
if evaluation.passed:
    print(f"Score: {evaluation.weighted_score}")
else:
    print(f"Failed: {evaluation.weighted_score}")

# Get specific metric
metric = evaluation.get_metric_score("tailwind_coverage")
if metric:
    print(f"Tailwind coverage: {metric.score}")
```

### Run Management

```python
from src.utils.run_manager import RunManager

run_manager = RunManager(config)

# Create a test run
test_run = run_manager.create_run(
    prompt_name="base_v1",
    test_case_ids=["test_1", "test_2"],
    description="Testing new prompt"
)

# Save results
run_manager.save_result(test_run.run_id, result)
run_manager.save_evaluation(test_run.run_id, evaluation)

# Complete the run
test_run.results.append(result)
test_run.evaluations.append(evaluation)
run_manager.save_run(test_run)

# Load run data
test_run = run_manager.load_run("run_123")
results = run_manager.load_results("run_123")
evaluations = run_manager.load_evaluations("run_123")

# List runs
all_runs = run_manager.list_runs()
prompt_runs = run_manager.list_runs(prompt_name="base_v1")
latest = run_manager.get_latest_run()
```

### Reporting

```python
from src.reporters.report_generator import ReportGenerator

reporter = ReportGenerator(config)

# Generate markdown report
markdown = reporter.generate_markdown_report(
    run_id="run_123",
    include_details=True,
    include_recommendations=True
)

# Generate JSON report
json_data = reporter.generate_json_report("run_123")

# Save report
report_path = reporter.save_report("run_123", format="markdown")

# Generate comparison
comparison = reporter.generate_comparison_report([
    "run_123",
    "run_124"
])
```

## Data Models

### TestCase

```python
from src.harness.models import TestCase, InputType, TestCaseCategory

test_case = TestCase(
    id="test_abc123",
    name="Example Test",
    description="A test case",
    input_type=InputType.HTML,
    input_path="test_cases/html_inputs/test_abc123.html",
    input_url="https://example.com",
    expected_output_path=None,
    category=TestCaseCategory.MEDIUM,
    tags=["example", "card"],
    metadata={"author": "agent"},
    created_at=datetime.now()
)
```

### ConversionResult

```python
from src.harness.models import ConversionResult

result = ConversionResult(
    test_case_id="test_abc123",
    prompt_name="base_v1",
    output_html="<div class='p-4'>Hello</div>",
    raw_response="Full API response...",
    success=True,
    error_message=None,
    tokens_used=1234,
    response_time=2.5,
    cost=0.0012,
    output_size=45,
    line_count=1,
    timestamp=datetime.now()
)
```

### EvaluationScore

```python
from src.harness.models import EvaluationScore, MetricScore

metric = MetricScore(
    name="html_validity",
    score=0.95,
    weight=1.0,
    passed=True,
    details={"is_valid": True, "errors": []}
)

evaluation = EvaluationScore(
    test_case_id="test_abc123",
    prompt_name="base_v1",
    run_id="run_123",
    metrics=[metric],
    weighted_score=0.85,
    simple_average=0.82,
    passed=True,
    passed_metrics=4,
    failed_metrics=1,
    total_metrics=5,
    timestamp=datetime.now()
)
```

### TestRun

```python
from src.harness.models import TestRun

test_run = TestRun(
    run_id="run_123",
    prompt_name="base_v1",
    description="Testing changes",
    test_case_ids=["test_1", "test_2"],
    results=[],
    evaluations=[],
    total_tests=2,
    successful_conversions=2,
    failed_conversions=0,
    passed_evaluations=1,
    failed_evaluations=1,
    total_tokens=2468,
    total_cost=0.0024,
    average_response_time=2.3,
    average_weighted_score=0.75,
    average_simple_score=0.73,
    started_at=datetime.now(),
    completed_at=None,
    duration=None,
    config_snapshot={}
)

# Calculate summary statistics
test_run.calculate_summary()
```

## Complete Example

Here's a complete example of running tests programmatically:

```python
from src.harness.config import load_config
from src.utils.test_case_manager import TestCaseManager
from src.utils.run_manager import RunManager
from src.agents.gemini_agent import GeminiAgent
from src.evaluators.evaluator import Evaluator
from src.reporters.report_generator import ReportGenerator

# Initialize
config = load_config()
test_manager = TestCaseManager(config)
run_manager = RunManager(config)
agent = GeminiAgent(config)
evaluator = Evaluator(config)
reporter = ReportGenerator(config)

# Get test cases
test_cases = test_manager.list_test_cases(category=TestCaseCategory.SIMPLE)

# Create run
test_run = run_manager.create_run(
    prompt_name="base_v1",
    test_case_ids=[tc.id for tc in test_cases],
    description="API example run"
)

# Run tests
for test_case in test_cases:
    # Get input
    input_html = test_manager.get_test_input(test_case)
    
    # Convert
    result = agent.convert_html(
        test_case_id=test_case.id,
        prompt_name="base_v1",
        input_html=input_html
    )
    
    # Save result
    run_manager.save_result(test_run.run_id, result)
    test_run.results.append(result)
    
    if result.success:
        # Evaluate
        evaluation = evaluator.evaluate(result, test_run.run_id)
        
        # Save evaluation
        run_manager.save_evaluation(test_run.run_id, evaluation)
        test_run.evaluations.append(evaluation)

# Save run
run_manager.save_run(test_run)

# Generate report
report = reporter.generate_markdown_report(test_run.run_id)
print(report)

# Save report
report_path = reporter.save_report(test_run.run_id)
print(f"Report saved to: {report_path}")
```

## Custom Evaluators

You can create custom evaluators by implementing the same interface:

```python
from typing import Dict, Any

class CustomEvaluator:
    def __init__(self):
        pass
    
    def analyze(self, html: str) -> Dict[str, Any]:
        """
        Analyze HTML and return results.
        
        Returns:
            Dict with keys:
            - score: float (0.0 to 1.0)
            - passed: bool
            - details: dict with additional info
        """
        # Your analysis logic here
        score = 0.85
        passed = score >= 0.7
        
        return {
            "score": score,
            "passed": passed,
            "details": {
                "custom_metric": "value"
            }
        }

# Register in evaluator
from src.evaluators.evaluator import Evaluator

evaluator = Evaluator(config)
evaluator.validators['custom_metric'] = CustomEvaluator()
```

## Extending the Harness

### Adding a New Agent Provider

```python
from typing import Optional, Dict, Any
from src.harness.models import ConversionResult

class CustomAgent:
    def __init__(self, config):
        self.config = config
        # Initialize your agent
    
    def convert_html(
        self,
        test_case_id: str,
        prompt_name: str,
        input_html: str,
        generation_override: Optional[Dict[str, Any]] = None
    ) -> ConversionResult:
        # Your conversion logic
        
        return ConversionResult(
            test_case_id=test_case_id,
            prompt_name=prompt_name,
            output_html="<div>Result</div>",
            success=True,
            # ... other fields
        )
```

### Adding a New Report Format

```python
from src.reporters.report_generator import ReportGenerator

class CustomReportGenerator(ReportGenerator):
    def generate_html_report(self, run_id: str) -> str:
        """Generate HTML report."""
        test_run = self.run_manager.load_run(run_id)
        # Generate your HTML report
        return "<html>...</html>"
```

## Utility Functions

```python
from src.utils.file_utils import save_json, load_json, save_html, load_html, ensure_dir
from pathlib import Path

# JSON operations
save_json({"key": "value"}, Path("data.json"))
data = load_json(Path("data.json"))

# HTML operations
save_html("<div>Hello</div>", Path("output.html"))
html = load_html(Path("input.html"))

# Directory creation
path = ensure_dir(Path("new/directory"))
```

## Error Handling

```python
try:
    result = agent.convert_html(test_case_id, prompt_name, input_html)
    if not result.success:
        print(f"Conversion failed: {result.error_message}")
except Exception as e:
    print(f"Error: {e}")

try:
    test_case = manager.get_test_case("invalid_id")
    if test_case is None:
        print("Test case not found")
except Exception as e:
    print(f"Error: {e}")
```

## Configuration Access

```python
# Get prompt configuration
prompt_config = config.get_prompt_config("base_v1")
print(f"Temperature: {prompt_config['parameters']['temperature']}")

# Get evaluation configuration
metrics = config.get_enabled_metrics()
for name, metric_config in metrics.items():
    print(f"{name}: weight={metric_config['weight']}")

# Get agent configuration
internal_config = config.get_internal_agent_config()
model_name = internal_config['model']
```
