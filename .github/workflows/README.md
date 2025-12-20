# GitHub Actions Workflows

This directory contains CI/CD workflows for the HTML-to-Tailwind Conversion Harness.

## Workflows

### 1. Test Prompt Changes (`test-prompts.yml`)

**Triggers:**
- Push to `main` or `cursor/**` branches when prompt files change
- Pull requests modifying prompt files
- Manual dispatch with custom parameters

**What it does:**
- Detects which prompts were modified
- Runs tests with the changed prompts
- Generates detailed reports
- Uploads results as artifacts
- Tests across multiple Python versions (3.9-3.12)
- For PRs: Compares results with baseline and comments on the PR

**Usage:**
```bash
# Automatically runs when you commit prompt changes
git add prompts/variations/my_new_prompt.md
git commit -m "feat: Add new semantic-focused prompt"
git push

# Or trigger manually via GitHub UI:
# Actions → Test Prompt Changes → Run workflow
```

### 2. Manual Test Execution (`manual-test.yml`)

**Triggers:**
- Manual dispatch only (via GitHub UI or API)

**What it does:**
- Allows you to manually trigger tests with specific parameters
- Choose which prompt to test
- Select test categories or specific test case IDs
- Generate comparison reports with previous runs
- Full control over test execution

**Usage:**
```bash
# Via GitHub CLI
gh workflow run manual-test.yml \
  -f prompt_name=experiment_001 \
  -f test_cases=simple \
  -f verbose=true

# Or use GitHub UI:
# Actions → Manual Test Execution → Run workflow
```

**Parameters:**
- `prompt_name`: Prompt to test (default: base_v1)
- `test_cases`: all/simple/medium/complex
- `test_ids`: Specific test IDs (optional)
- `verbose`: Enable verbose output
- `generate_comparison`: Compare with previous run

### 3. Scheduled Baseline Tests (`scheduled-baseline.yml`)

**Triggers:**
- Daily at 2 AM UTC (scheduled)
- Manual dispatch

**What it does:**
- Runs baseline tests with `base_v1` prompt daily
- Compares results with previous baseline
- Detects regressions (>5% score drop)
- Creates GitHub issues for regressions
- Maintains historical baseline data

**Usage:**
```bash
# Automatic - runs every day at 2 AM UTC

# Or trigger manually:
gh workflow run scheduled-baseline.yml -f notify=true
```

**Regression Detection:**
- Compares daily scores
- Alerts if quality drops >5%
- Creates GitHub issue with details
- Uploads comparison artifacts

### 4. Add Test Case via PR (`add-test-case.yml`)

**Triggers:**
- Pull requests modifying test case files
- Manual dispatch to add new test cases

**What it does:**
- Validates test case metadata structure
- Checks that all referenced files exist
- For manual dispatch: Adds test case from URL
- Commits changes back to the branch

**Usage:**
```bash
# Via GitHub CLI
gh workflow run add-test-case.yml \
  -f test_url=https://example.com \
  -f test_name="Example Homepage" \
  -f category=medium \
  -f tags="homepage,example"

# Or via GitHub UI:
# Actions → Add Test Case via PR → Run workflow
```

## Setup Requirements

### GitHub Secrets

You must add the following secret to your repository:

1. Go to: Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Your Google Gemini API key

### Permissions

Ensure GitHub Actions has the following permissions:

1. Go to: Repository → Settings → Actions → General
2. Under "Workflow permissions":
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

## Workflow Files

| File | Purpose | Trigger |
|------|---------|---------|
| `test-prompts.yml` | Test prompt changes | Push, PR, Manual |
| `manual-test.yml` | Manual test execution | Manual only |
| `scheduled-baseline.yml` | Daily baseline tests | Schedule, Manual |
| `add-test-case.yml` | Add/validate test cases | PR, Manual |

## Artifacts

Each workflow uploads artifacts that you can download:

- **test-results-python-X.X**: Complete test run data and reports
- **test-reports-python-X.X**: Generated markdown and JSON reports  
- **manual-test-results**: Results from manual test runs
- **baseline-results-N**: Daily baseline test results (kept for 90 days)

## Common Scenarios

### Scenario 1: Iterate on a New Prompt

```bash
# 1. Create a new prompt file
cp prompts/base/conversion_v1.md prompts/variations/experiment_001.md
# Edit the file...

# 2. Register in config
echo "experiment_001:
  file: prompts/variations/experiment_001.md
  description: 'My experimental prompt'
  active: true" >> config/prompts.yaml

# 3. Commit and push
git add prompts/variations/experiment_001.md config/prompts.yaml
git commit -m "feat: Add experiment_001 prompt"
git push

# GitHub Actions will automatically:
# - Detect the prompt change
# - Run tests with experiment_001
# - Generate reports
# - Upload results as artifacts
```

### Scenario 2: Compare Two Prompts

```bash
# Use manual workflow to test first prompt
gh workflow run manual-test.yml -f prompt_name=base_v1

# Wait for completion, then test second prompt with comparison
gh workflow run manual-test.yml \
  -f prompt_name=experiment_001 \
  -f generate_comparison=true

# Download and review the comparison report
```

### Scenario 3: Add Test Cases in Bulk

```bash
# Create a PR with new test case files
git checkout -b add-test-cases

# Add test cases manually or via workflow
gh workflow run add-test-case.yml \
  -f test_url=https://example.com/page1 \
  -f test_name="Page 1" \
  -f category=simple

gh workflow run add-test-case.yml \
  -f test_url=https://example.com/page2 \
  -f test_name="Page 2" \
  -f category=medium

# Create PR
git push origin add-test-cases
gh pr create --title "Add new test cases"

# GitHub Actions will validate the test cases
```

### Scenario 4: Monitor Quality Over Time

```bash
# Baseline tests run automatically every day

# View historical results:
gh run list --workflow=scheduled-baseline.yml --limit 10

# Download specific baseline:
gh run download <run-id>

# View trends in reports/
```

## Viewing Results

### In GitHub UI

1. Go to: Repository → Actions
2. Click on a workflow run
3. View the summary (includes pass/fail, scores)
4. Download artifacts for detailed reports

### Via GitHub CLI

```bash
# List recent runs
gh run list --workflow=test-prompts.yml

# View specific run
gh run view <run-id>

# Download artifacts
gh run download <run-id>

# View logs
gh run view <run-id> --log
```

### In Reports

Each workflow generates:
- **Markdown reports**: Human-readable summaries
- **JSON reports**: Machine-parseable data
- **Comparison reports**: Side-by-side analysis

## Troubleshooting

### Tests Fail with "GEMINI_API_KEY not found"

**Solution:** Add the secret to your repository (see Setup Requirements above)

### Workflow doesn't trigger on prompt changes

**Check:**
1. File paths match the workflow `paths:` filter
2. Branch is included in the workflow triggers
3. GitHub Actions is enabled for your repository

### Baseline tests create too many issues

**Solution:** Adjust regression threshold in `scheduled-baseline.yml`:
```yaml
REGRESSION=$(echo "$LATEST_SCORE < $PREVIOUS_SCORE * 0.95" | bc -l)
# Change 0.95 to 0.90 for 10% threshold
```

### Want to test locally before pushing

```bash
# Install act (GitHub Actions local runner)
brew install act  # or: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run a workflow locally
act -W .github/workflows/test-prompts.yml -s GEMINI_API_KEY="your_key"
```

## Best Practices

1. **Always test manually first** before pushing to main
2. **Use descriptive commit messages** for prompt changes
3. **Review workflow summaries** after each run
4. **Download artifacts** for detailed analysis
5. **Monitor baseline tests** for quality regressions
6. **Keep test cases organized** with proper tags and categories
7. **Document prompt changes** in commit messages or PR descriptions

## Cost Management

Each test run uses the Gemini API and incurs costs:

- Typical cost: $0.001-$0.005 per test case
- Daily baseline: ~$0.01-$0.05 depending on test count
- Monitor costs in the generated reports

**Tips:**
- Use `simple` category for quick iterations
- Limit scheduled tests if costs are a concern
- Review cost reports in artifacts

## Future Enhancements

Potential improvements to the CI/CD pipeline:

- [ ] Slack/Discord notifications
- [ ] Automatic prompt optimization suggestions
- [ ] Visual diff generation for HTML outputs
- [ ] Performance benchmarking over time
- [ ] Cost alerts and budgets
- [ ] A/B testing automation
- [ ] Integration with external monitoring
