# Usage Examples

This document provides practical examples for common use cases of the harness.

## Table of Contents

- [Basic Workflow](#basic-workflow)
- [Test Case Management](#test-case-management)
- [Running Tests](#running-tests)
- [Prompt Iteration](#prompt-iteration)
- [Analysis and Reporting](#analysis-and-reporting)
- [Advanced Scenarios](#advanced-scenarios)

## Basic Workflow

### Complete First-Time Setup

```bash
# 1. Clone and setup
cd /path/to/project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Initialize harness
python scripts/init_harness.py

# 5. Verify setup
python scripts/list_test_cases.py --stats
```

### Your First Test Run

```bash
# 1. Add a test case
python scripts/add_test_case.py \
  --url https://getbootstrap.com/docs/5.0/components/cards/ \
  --name "Bootstrap Card" \
  --category medium \
  --tags "bootstrap,card" \
  --description "Bootstrap card component to convert"

# 2. Run the test
python scripts/run_tests.py --all --verbose

# 3. View results
python scripts/generate_report.py --run latest
```

## Test Case Management

### Adding Test Cases from Different Sources

#### From a URL
```bash
python scripts/add_test_case.py \
  --url https://tailwindui.com/components/marketing/sections/heroes \
  --name "TailwindUI Hero" \
  --category complex \
  --tags "hero,marketing"
```

#### From a Local File
```bash
python scripts/add_test_case.py \
  --file examples/navbar.html \
  --name "Navigation Bar" \
  --category simple \
  --tags "navigation,header"
```

#### From stdin
```bash
echo '<div style="padding: 20px;">Hello</div>' | \
python scripts/add_test_case.py \
  --stdin \
  --name "Simple Div" \
  --category simple
```

#### With Expected Output
```bash
python scripts/add_test_case.py \
  --file input.html \
  --name "With Expected" \
  --expected expected.html \
  --description "Test case with expected output for comparison"
```

### Listing and Filtering Test Cases

```bash
# Show all test cases
python scripts/list_test_cases.py

# Show statistics only
python scripts/list_test_cases.py --stats

# Filter by category
python scripts/list_test_cases.py --category simple

# Filter by tags
python scripts/list_test_cases.py --tags "card,bootstrap"

# Detailed view
python scripts/list_test_cases.py --verbose
```

## Running Tests

### Basic Test Runs

```bash
# Run all tests
python scripts/run_tests.py --all

# Run specific test
python scripts/run_tests.py --test test_abc123

# Run by category
python scripts/run_tests.py --category simple

# Run by tags
python scripts/run_tests.py --tags "card"
```

### Test Runs with Options

```bash
# With verbose output
python scripts/run_tests.py --all --verbose

# With specific prompt
python scripts/run_tests.py --all --prompt experiment_001

# With description
python scripts/run_tests.py \
  --category medium \
  --description "Testing improved semantic HTML focus" \
  --verbose
```

### Targeted Testing

```bash
# Test only card components
python scripts/run_tests.py --tags "card"

# Test only simple cases (for quick iteration)
python scripts/run_tests.py --category simple

# Test specific problematic cases
python scripts/run_tests.py --test test_abc123 --test test_def456
```

## Prompt Iteration

### Creating a Prompt Variation

1. **Copy base prompt**:
```bash
cp prompts/base/conversion_v1.md prompts/variations/semantic_focus_v1.md
```

2. **Edit the prompt** (example changes):
```markdown
# In prompts/variations/semantic_focus_v1.md

## Enhanced Semantic HTML Guidelines

### CRITICAL: Semantic Element Usage
Always prefer semantic HTML5 elements over generic divs:
- `<article>` for independent, self-contained content
- `<section>` for thematic grouping of content
- `<nav>` for navigation links
- `<header>` for introductory content
- `<footer>` for footer content
- `<aside>` for tangentially related content

### Example Transformations

**Bad:**
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
</div>
```

**Good:**
```html
<article class="bg-white rounded-lg shadow-md">
  <header class="p-4 border-b">Title</header>
  <section class="p-4">Content</section>
</article>
```
```

3. **Register in config**:
```yaml
# In config/prompts.yaml
prompts:
  semantic_focus_v1:
    file: prompts/variations/semantic_focus_v1.md
    parent: base_v1
    description: "Enhanced focus on semantic HTML5 elements"
    active: true
    parameters:
      temperature: 0.6
      max_tokens: 8000
    metadata:
      created: "2025-12-20"
      author: "agent"
      version: "1.0.0"
    tags:
      - experiment
      - semantic
```

4. **Test the new prompt**:
```bash
python scripts/run_tests.py \
  --all \
  --prompt semantic_focus_v1 \
  --description "Testing enhanced semantic HTML guidelines"
```

### A/B Testing Prompts

```bash
# Run baseline
python scripts/run_tests.py \
  --all \
  --prompt base_v1 \
  --description "Baseline run"

# Get the run ID
BASELINE_RUN=$(ls -t results/runs/ | head -1)

# Run experiment
python scripts/run_tests.py \
  --all \
  --prompt semantic_focus_v1 \
  --description "Semantic focus experiment"

# Get experiment run ID
EXPERIMENT_RUN=$(ls -t results/runs/ | head -1)

# Compare
python scripts/generate_report.py \
  --compare "$BASELINE_RUN,$EXPERIMENT_RUN"
```

### Parameter Tuning

```yaml
# In config/prompts.yaml

# Lower temperature for more consistent output
experiment_low_temp:
  file: prompts/variations/same_prompt.md
  parameters:
    temperature: 0.3
    max_tokens: 8000

# Higher temperature for more creative output
experiment_high_temp:
  file: prompts/variations/same_prompt.md
  parameters:
    temperature: 0.9
    max_tokens: 8000
```

## Analysis and Reporting

### Basic Reports

```bash
# Latest run
python scripts/generate_report.py --run latest

# Specific run
python scripts/generate_report.py --run run_20250120_143022_abc123

# JSON format
python scripts/generate_report.py --run latest --format json

# Save to custom location
python scripts/generate_report.py \
  --run latest \
  --output my_report.md
```

### Detailed Analysis

```bash
# Full report with all details
python scripts/generate_report.py \
  --run latest \
  --format markdown

# Summary only (no detailed metrics)
python scripts/generate_report.py \
  --run latest \
  --no-details

# Without recommendations
python scripts/generate_report.py \
  --run latest \
  --no-recommendations
```

### Comparing Runs

```bash
# Compare two runs
python scripts/generate_report.py \
  --compare "run_baseline,run_experiment"

# Compare multiple runs
python scripts/generate_report.py \
  --compare "run_001,run_002,run_003"

# Save comparison
python scripts/generate_report.py \
  --compare "run_001,run_002" \
  --output comparison.md
```

### Reading Reports

Example report structure:
```markdown
# Test Run Report: run_20250120_143022_abc123

**Prompt:** base_v1
**Started:** 2025-01-20 14:30:22
**Duration:** 45.23s

## Summary
- Total Tests: 5
- Successful Conversions: 5 (100.0%)
- Passed Evaluations: 3 (60.0%)
- Average Score: 0.752

## Overall Scores
- Average Weighted Score: 0.752
- Average Simple Score: 0.741

## Recommendations
1. Improve semantic HTML usage (failing in 40% of tests).
   Add explicit instructions to use semantic elements.
2. Enhance accessibility (failing in 20% of tests).
   Remind the model to add alt text, labels, and ARIA attributes.
```

## Advanced Scenarios

### Custom Evaluation Criteria

Edit `config/evaluation.yaml`:

```yaml
metrics:
  # Make Tailwind coverage more strict
  tailwind_coverage:
    enabled: true
    weight: 1.0  # Increase weight
    min_threshold: 0.9  # Increase from 0.7 to 0.9
  
  # Add custom thresholds
  semantic_score:
    enabled: true
    weight: 1.0
    min_threshold: 0.8
    preferred_elements:
      - header
      - nav
      - main
      - article
      - section
      - aside
      - footer
      - figure
      - figcaption
```

### Batch Processing

Process multiple HTML files at once:

```bash
#!/bin/bash
# add_multiple_tests.sh

for file in html_samples/*.html; do
  name=$(basename "$file" .html)
  python scripts/add_test_case.py \
    --file "$file" \
    --name "$name" \
    --category medium \
    --tags "batch,$(echo $name | cut -d'_' -f1)"
done

# Run all new tests
python scripts/run_tests.py --tags "batch"
```

### Automated Iteration Loop

```python
#!/usr/bin/env python3
# automated_iteration.py

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.harness.config import load_config
from src.utils.test_case_manager import TestCaseManager
from src.utils.run_manager import RunManager
from src.agents.gemini_agent import GeminiAgent
from src.evaluators.evaluator import Evaluator

config = load_config()
test_manager = TestCaseManager(config)
run_manager = RunManager(config)

# Define prompts to test
prompts_to_test = [
    "base_v1",
    "semantic_focus_v1",
    "accessibility_focus_v1"
]

results = {}

for prompt_name in prompts_to_test:
    print(f"\nTesting prompt: {prompt_name}")
    
    # Get test cases
    test_cases = test_manager.list_test_cases()
    
    # Create run
    test_run = run_manager.create_run(
        prompt_name=prompt_name,
        test_case_ids=[tc.id for tc in test_cases],
        description=f"Automated test of {prompt_name}"
    )
    
    # Run tests (simplified)
    agent = GeminiAgent(config)
    evaluator = Evaluator(config)
    
    for test_case in test_cases:
        input_html = test_manager.get_test_input(test_case)
        result = agent.convert_html(test_case.id, prompt_name, input_html)
        
        if result.success:
            evaluation = evaluator.evaluate(result, test_run.run_id)
            test_run.results.append(result)
            test_run.evaluations.append(evaluation)
    
    run_manager.save_run(test_run)
    
    # Store results
    results[prompt_name] = {
        "run_id": test_run.run_id,
        "score": test_run.average_weighted_score,
        "passed": test_run.passed_evaluations,
        "total": test_run.total_tests
    }

# Find best prompt
best_prompt = max(results.items(), key=lambda x: x[1]["score"])

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
for prompt, data in results.items():
    print(f"{prompt}:")
    print(f"  Score: {data['score']:.3f}")
    print(f"  Passed: {data['passed']}/{data['total']}")

print(f"\nBest prompt: {best_prompt[0]} (score: {best_prompt[1]['score']:.3f})")
```

### Integration with CI/CD

```yaml
# .github/workflows/test-prompts.yml
name: Test Prompts

on:
  push:
    branches: [ main ]
    paths:
      - 'prompts/**'
      - 'config/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      run: |
        python scripts/run_tests.py --all
    
    - name: Generate report
      run: |
        python scripts/generate_report.py --run latest --format markdown > report.md
    
    - name: Upload report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: report.md
```

### Cost Tracking

```python
# track_costs.py
from src.harness.config import load_config
from src.utils.run_manager import RunManager
import json

config = load_config()
run_manager = RunManager(config)

# Get all runs
runs = run_manager.list_runs()

total_cost = 0
total_tokens = 0

for run_id in runs:
    test_run = run_manager.load_run(run_id)
    if test_run:
        total_cost += test_run.total_cost
        total_tokens += test_run.total_tokens

print(f"Total Cost: ${total_cost:.4f}")
print(f"Total Tokens: {total_tokens:,}")
print(f"Average Cost per Run: ${total_cost/len(runs):.4f}")
```

### Custom Metric Analysis

```python
# analyze_metrics.py
from src.harness.config import load_config
from src.utils.run_manager import RunManager

config = load_config()
run_manager = RunManager(config)

run_id = "run_20250120_143022_abc123"
evaluations = run_manager.load_evaluations(run_id)

# Analyze specific metric across all tests
metric_name = "tailwind_coverage"
scores = []

for evaluation in evaluations:
    metric = evaluation.get_metric_score(metric_name)
    if metric:
        scores.append(metric.score)

if scores:
    avg_score = sum(scores) / len(scores)
    min_score = min(scores)
    max_score = max(scores)
    
    print(f"Metric: {metric_name}")
    print(f"Average: {avg_score:.3f}")
    print(f"Min: {min_score:.3f}")
    print(f"Max: {max_score:.3f}")
    print(f"Range: {max_score - min_score:.3f}")
```

## Troubleshooting Examples

### Debug API Issues

```python
# test_api.py
from src.harness.config import load_config
from src.agents.gemini_agent import GeminiAgent

config = load_config()

try:
    api_key = config.get_gemini_api_key()
    print(f"API Key found: {api_key[:10]}...")
except Exception as e:
    print(f"Error getting API key: {e}")
    exit(1)

agent = GeminiAgent(config)

if agent.test_connection():
    print("✅ API connection successful")
else:
    print("❌ API connection failed")
```

### Validate Test Case

```python
# validate_test.py
from src.harness.config import load_config
from src.utils.test_case_manager import TestCaseManager
from bs4 import BeautifulSoup

config = load_config()
manager = TestCaseManager(config)

test_id = "test_abc123"
test_case = manager.get_test_case(test_id)

if test_case:
    input_html = manager.get_test_input(test_case)
    
    # Validate HTML
    try:
        soup = BeautifulSoup(input_html, 'html.parser')
        print(f"✅ Valid HTML ({len(input_html)} bytes)")
        print(f"   Elements: {len(soup.find_all())}")
    except Exception as e:
        print(f"❌ Invalid HTML: {e}")
else:
    print(f"❌ Test case '{test_id}' not found")
```

## Tips and Best Practices

1. **Start Simple**: Begin with simple test cases to validate your setup
2. **Iterate Incrementally**: Make small changes to prompts and test frequently
3. **Use Tags**: Organize test cases with meaningful tags
4. **Monitor Costs**: Keep an eye on API costs, especially during experimentation
5. **Version Control**: Commit prompts and significant results
6. **Document Changes**: Use descriptive run descriptions
7. **Baseline First**: Always establish a baseline before experimenting
8. **Read Reports**: Don't just look at scores; read the detailed feedback
