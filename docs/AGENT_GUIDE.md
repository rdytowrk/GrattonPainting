# Agent Guide: Using the HTML-to-Tailwind Harness

This guide is specifically designed for external coding agents (like Cursor) to effectively use the testing harness for iterating on HTML-to-Tailwind conversion prompts.

## Overview

As an external agent, your role is to:
1. **Iterate on prompts** - Modify and improve conversion prompts
2. **Run tests** - Execute test suites to evaluate prompt performance
3. **Analyze results** - Review metrics and identify improvement areas
4. **Refine** - Make targeted improvements based on data

## Quick Start

### 1. Setup
```bash
# Initialize the harness
python scripts/init_harness.py

# Verify setup
python scripts/list_test_cases.py --stats
```

### 2. Add Test Cases
```bash
# From a URL
python scripts/add_test_case.py --url https://example.com --name "homepage"

# From a file
python scripts/add_test_case.py --file input.html --name "card_component" --category simple

# With tags for organization
python scripts/add_test_case.py --file complex.html --name "dashboard" --category complex --tags "layout,grid"
```

### 3. Run Tests
```bash
# Run all tests
python scripts/run_tests.py --all --verbose

# Run specific test
python scripts/run_tests.py --test test_abc123

# Run by category
python scripts/run_tests.py --category simple

# Run by tags
python scripts/run_tests.py --tags "card,simple"
```

### 4. Review Results
```bash
# Generate report for latest run
python scripts/generate_report.py --run latest

# Compare multiple runs
python scripts/generate_report.py --compare "run_20250101_120000,run_20250101_130000"
```

## Workflow: Test/Review/Iterate Loop

### Phase 1: Baseline Testing

1. **Run baseline tests** with the default prompt:
   ```bash
   python scripts/run_tests.py --all --description "Baseline test with default prompt"
   ```

2. **Review baseline results**:
   ```bash
   python scripts/generate_report.py --run latest
   ```

3. **Identify weak areas** - Look for:
   - Low-scoring metrics (HTML validity, Tailwind coverage, etc.)
   - Common failure patterns
   - Specific test cases that consistently fail

### Phase 2: Prompt Iteration

1. **Create a prompt variation** based on findings:
   ```bash
   # Copy base prompt
   cp prompts/base/conversion_v1.md prompts/variations/experiment_001.md
   
   # Edit the new prompt with your improvements
   # Then update config/prompts.yaml to register it
   ```

2. **Register in config**:
   ```yaml
   # In config/prompts.yaml
   experiment_001:
     file: prompts/variations/experiment_001.md
     parent: base_v1
     description: "Emphasize semantic HTML and accessibility"
     active: true
     parameters:
       temperature: 0.6
       max_tokens: 8000
     tags:
       - experiment
       - semantic
   ```

3. **Run tests with new prompt**:
   ```bash
   python scripts/run_tests.py --all --prompt experiment_001 --description "Test semantic focus changes"
   ```

### Phase 3: Analysis & Comparison

1. **Generate comparison report**:
   ```bash
   # Get the two run IDs (baseline and experiment)
   python scripts/generate_report.py --compare "run_baseline,run_experiment"
   ```

2. **Analyze differences**:
   - Overall score improvement/degradation
   - Metric-by-metric comparison
   - Cost and performance changes
   - Specific test case improvements

3. **Read recommendations**:
   ```bash
   python scripts/generate_report.py --run latest
   # Look at the "Recommendations" section
   ```

### Phase 4: Refinement

Based on analysis:

1. **If improvement**: 
   - Keep the changes
   - Consider making it the new baseline
   - Iterate further on what worked

2. **If no improvement**:
   - Analyze why it didn't work
   - Try a different approach
   - Revert to previous version

3. **If mixed results**:
   - Identify which aspects improved
   - Combine successful elements
   - Create a new hybrid prompt

## Key Metrics to Monitor

### HTML Validity (Weight: 1.0)
- **What it measures**: Valid HTML5 structure
- **Improve by**: Adding examples of correct structure, emphasizing validation
- **Failure indicates**: Model not understanding HTML syntax

### Tailwind Coverage (Weight: 0.8)
- **What it measures**: % of styles using Tailwind classes
- **Improve by**: Explicitly forbidding inline styles, listing Tailwind patterns
- **Failure indicates**: Model using custom CSS or inline styles

### Semantic Score (Weight: 0.9)
- **What it measures**: Use of semantic HTML5 elements
- **Improve by**: Listing preferred elements, giving examples
- **Failure indicates**: Overuse of divs, non-semantic structure

### Accessibility Score (Weight: 0.7)
- **What it measures**: Basic a11y compliance
- **Improve by**: Emphasizing alt text, labels, ARIA attributes
- **Failure indicates**: Missing accessibility features

### Code Quality (Weight: 0.6)
- **What it measures**: Clean, maintainable code
- **Improve by**: Specifying formatting rules, nesting limits
- **Failure indicates**: Poor code organization

## Prompt Engineering Tips

### Effective Techniques

1. **Use Examples**
   - Show before/after conversions
   - Include edge cases
   - Demonstrate desired patterns

2. **Be Specific**
   - "Use flexbox for layout" vs. "Use modern layout techniques"
   - List specific Tailwind classes to prefer
   - Define maximum nesting depth

3. **Set Constraints**
   - "No inline styles allowed"
   - "Use semantic HTML5 elements exclusively"
   - "Maximum 8 levels of nesting"

4. **Provide Context**
   - Explain why Tailwind is being used
   - Mention the builder editor use case
   - Emphasize maintainability

5. **Format Instructions**
   - Use clear sections (Guidelines, Requirements, Examples)
   - Bullet points for easy scanning
   - Bold key requirements

### Common Pitfalls

1. **Too Vague**: "Make it better" → Specify what "better" means
2. **Too Long**: Model may lose focus → Keep concise, use structure
3. **Conflicting Instructions**: Ensure guidelines don't contradict
4. **No Examples**: Abstract instructions are harder to follow
5. **Missing Edge Cases**: Address common failure patterns explicitly

## Advanced: Pattern Detection

As you iterate, look for patterns in failures:

### Pattern: Excessive Divs
**Symptom**: Low semantic score, high div ratio  
**Solution**: Add to prompt:
```
Avoid unnecessary divs. Prefer semantic elements:
- Use <article> for self-contained content
- Use <section> for themed grouping
- Use <nav> for navigation
- Use <header> and <footer> appropriately
```

### Pattern: Inline Styles Persisting
**Symptom**: Warnings about inline styles, low Tailwind coverage  
**Solution**: Strengthen constraint:
```
CRITICAL: Remove ALL inline styles. Every style must use Tailwind classes.
If a style cannot be expressed with Tailwind, note it in a comment.
```

### Pattern: Missing Alt Text
**Symptom**: Low accessibility score  
**Solution**: Add explicit instruction:
```
Accessibility Requirements:
1. Every <img> must have an alt attribute
2. Alt text should be descriptive (not "image" or "icon")
3. Decorative images should use alt=""
```

## Cost Optimization

Monitor costs in your reports:

```
Total Cost: $0.0234
Average Cost per Test: $0.0039
```

### Reducing Costs

1. **Optimize Prompt Length**
   - Remove unnecessary examples
   - Use more concise language
   - Keep only what improves performance

2. **Adjust max_tokens**
   ```yaml
   parameters:
     max_tokens: 6000  # Reduce from 8000 if outputs are smaller
   ```

3. **Use Temperature Wisely**
   - Higher temperature = more creative but potentially more tokens
   - Lower temperature = more deterministic, often shorter

4. **Filter Test Cases**
   - Focus on problematic categories
   - Use representative samples
   - Archive passing tests

## Automated Agent Workflow

If you're implementing fully automated iteration:

```bash
#!/bin/bash
# Example automated workflow

# 1. Run tests
RUN_ID=$(python scripts/run_tests.py --all | grep "Run ID:" | cut -d' ' -f3)

# 2. Generate report
python scripts/generate_report.py --run $RUN_ID --format json > report.json

# 3. Parse results
SCORE=$(jq '.summary.average_weighted_score' report.json)

# 4. Decision logic
if (( $(echo "$SCORE < 0.8" | bc -l) )); then
  echo "Score below threshold, analyzing failures..."
  # Your analysis and prompt modification code here
fi
```

## File Locations

Key files you'll work with:

```
prompts/
  base/conversion_v1.md          # Base prompt
  variations/                     # Your experimental prompts
  active/                         # Currently active prompts

config/
  prompts.yaml                    # Prompt registration
  evaluation.yaml                 # Metric weights and thresholds

results/
  runs/                           # Individual run data
  reports/                        # Generated reports
```

## Best Practices

1. **Version Control**: Commit prompts and results to track progress
2. **Document Changes**: Use descriptive run descriptions
3. **Systematic Testing**: Test one change at a time when possible
4. **Keep Baseline**: Always maintain a working baseline prompt
5. **Archive Success**: Move successful prompts to active/
6. **Tag Thoughtfully**: Use consistent tags for easy filtering
7. **Review Reports**: Don't just look at scores, read the details
8. **Cost Awareness**: Monitor API costs, especially during experimentation

## Troubleshooting

### Tests Fail to Run
```bash
# Check API connection
python scripts/init_harness.py

# Verify test cases exist
python scripts/list_test_cases.py --stats

# Check configuration
python -c "from src.harness.config import load_config; load_config()"
```

### Poor Results Across All Tests
- Prompt may be too different from training data
- Try simpler, clearer instructions
- Add more examples
- Check if model version changed

### Inconsistent Results
- Increase temperature for variety or decrease for consistency
- Run tests multiple times to check variance
- Consider using a different seed or model parameter

### High Costs
- Review max_tokens setting
- Optimize prompt length
- Consider using a different model
- Cache successful conversions

## Support

For issues or questions:
1. Check the main [README.md](../README.md)
2. Review [API.md](API.md) for programmatic access
3. See [EXAMPLES.md](EXAMPLES.md) for more usage examples
