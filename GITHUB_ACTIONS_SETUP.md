# GitHub Actions Setup Guide

Complete guide to setting up and using the CI/CD pipeline for the HTML-to-Tailwind Conversion Harness.

## Quick Setup (5 minutes)

### Step 1: Add Your Gemini API Key

1. Go to your repository on GitHub
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add the secret:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Your Google Gemini API key (get it from https://makersuite.google.com/app/apikey)
5. Click **"Add secret"**

### Step 2: Enable GitHub Actions Permissions

1. Go to: **Settings** → **Actions** → **General**
2. Under **"Workflow permissions"**:
   - ✅ Select **"Read and write permissions"**
   - ✅ Check **"Allow GitHub Actions to create and approve pull requests"**
3. Click **"Save"**

### Step 3: Verify Workflows Are Active

1. Go to the **"Actions"** tab in your repository
2. You should see 4 workflows:
   - ✅ Test Prompt Changes
   - ✅ Manual Test Execution
   - ✅ Scheduled Baseline Tests
   - ✅ Add Test Case via PR

That's it! Your CI/CD pipeline is ready. 🎉

---

## Available Workflows

### 1. 🧪 Test Prompt Changes (Automatic)

**Purpose:** Automatically test prompts when they're modified

**Triggers:**
- ✅ When you commit changes to `prompts/**`
- ✅ When you update `config/prompts.yaml`
- ✅ When you create a PR with prompt changes
- ✅ Manual trigger via GitHub UI

**What it does:**
1. Detects which prompts were changed
2. Runs tests with the modified prompt
3. Generates detailed reports
4. Tests across Python 3.9, 3.10, 3.11, and 3.12
5. For PRs: Compares with baseline and comments results

**Example Usage:**
```bash
# Edit a prompt
vim prompts/variations/my_prompt.md

# Commit and push
git add prompts/variations/my_prompt.md
git commit -m "feat: Improve semantic HTML focus"
git push

# GitHub Actions automatically runs tests!
# View results: Repository → Actions → Latest run
```

### 2. 🎮 Manual Test Execution

**Purpose:** Run tests on-demand with full control

**Triggers:**
- Manual only (GitHub UI or CLI)

**Parameters:**
- `prompt_name`: Which prompt to test (default: base_v1)
- `test_cases`: all/simple/medium/complex
- `test_ids`: Specific test IDs (comma-separated)
- `verbose`: Enable detailed output
- `generate_comparison`: Compare with previous run

**Example Usage via GitHub UI:**
1. Go to **Actions** → **Manual Test Execution**
2. Click **"Run workflow"**
3. Fill in parameters:
   - Prompt name: `experiment_001`
   - Test cases: `simple`
   - Verbose: `true`
4. Click **"Run workflow"**
5. Wait for results and download artifacts

**Example Usage via GitHub CLI:**
```bash
# Test a specific prompt
gh workflow run manual-test.yml \
  -f prompt_name=experiment_001 \
  -f test_cases=all \
  -f verbose=true

# Test with comparison
gh workflow run manual-test.yml \
  -f prompt_name=new_prompt \
  -f test_cases=medium \
  -f generate_comparison=true

# Test specific test cases
gh workflow run manual-test.yml \
  -f prompt_name=base_v1 \
  -f test_ids="test_abc123,test_def456"
```

### 3. 📅 Scheduled Baseline Tests

**Purpose:** Daily quality monitoring and regression detection

**Triggers:**
- ⏰ Daily at 2 AM UTC (automatic)
- 🖱️ Manual trigger

**What it does:**
1. Runs baseline tests with `base_v1` prompt
2. Compares with previous day's results
3. Detects regressions (>5% score drop)
4. Creates GitHub issues for regressions
5. Maintains 90-day history

**Regression Detection:**
- Compares average quality scores
- Issues alert if score drops >5%
- Includes detailed comparison in issue
- Links to workflow run and artifacts

**Disable if needed:**
```yaml
# In .github/workflows/scheduled-baseline.yml
# Comment out the schedule trigger:
# schedule:
#   - cron: '0 2 * * *'
```

### 4. ➕ Add Test Case via PR

**Purpose:** Add and validate test cases programmatically

**Triggers:**
- PRs modifying `test_cases/**`
- Manual trigger to add test cases

**What it does:**
- Validates test case metadata structure
- Checks that all files exist
- For manual dispatch: Fetches HTML from URL and adds test case
- Commits changes to your branch

**Example Usage:**
```bash
# Add a test case from a URL
gh workflow run add-test-case.yml \
  -f test_url="https://getbootstrap.com/docs/5.3/components/cards/" \
  -f test_name="Bootstrap Cards" \
  -f category=medium \
  -f tags="bootstrap,cards,components"

# Wait for workflow to complete
gh run watch

# The workflow will:
# 1. Fetch HTML from the URL
# 2. Create test case files
# 3. Update metadata.json
# 4. Commit and push changes
```

---

## Workflow Architecture

```
┌─────────────────────────────────────────────────────┐
│  Developer commits prompt changes to repository      │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  GitHub Actions detects changes to prompts/**       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Test Prompt Changes Workflow                        │
│  ├─ Install dependencies                             │
│  ├─ Run tests with changed prompt                    │
│  ├─ Generate reports (markdown + JSON)              │
│  ├─ Upload artifacts                                 │
│  └─ For PRs: Comment comparison on PR                │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Results available:                                  │
│  ├─ Workflow summary (pass/fail, scores)            │
│  ├─ Downloadable artifacts (detailed reports)        │
│  ├─ PR comments (for pull requests)                  │
│  └─ Job logs (for debugging)                         │
└─────────────────────────────────────────────────────┘
```

---

## Common Workflows

### Workflow 1: Iterate on a Prompt

```bash
# 1. Create a new prompt variation
cp prompts/base/conversion_v1.md prompts/variations/semantic_v1.md
vim prompts/variations/semantic_v1.md  # Make your changes

# 2. Register it in the config
vim config/prompts.yaml
# Add:
#   semantic_v1:
#     file: prompts/variations/semantic_v1.md
#     description: "Focus on semantic HTML5"
#     active: true

# 3. Commit and push
git checkout -b prompt/semantic-v1
git add prompts/variations/semantic_v1.md config/prompts.yaml
git commit -m "feat: Add semantic HTML focused prompt"
git push origin prompt/semantic-v1

# 4. Create PR
gh pr create --title "Add semantic HTML prompt variation" \
  --body "Testing a prompt that emphasizes semantic HTML5 elements"

# GitHub Actions will:
# ✅ Run tests with your new prompt
# ✅ Compare with baseline
# ✅ Comment on PR with results
# ✅ Upload detailed reports
```

### Workflow 2: A/B Test Two Prompts

```bash
# Test prompt A
gh workflow run manual-test.yml \
  -f prompt_name=prompt_a \
  -f test_cases=all \
  -f verbose=true

# Wait for completion
sleep 300

# Test prompt B with comparison
gh workflow run manual-test.yml \
  -f prompt_name=prompt_b \
  -f test_cases=all \
  -f generate_comparison=true

# Download and review comparison
gh run list --workflow=manual-test.yml --limit 2
gh run download <latest-run-id>
```

### Workflow 3: Add Test Cases in Bulk

```bash
# Method 1: Via workflow (one at a time)
urls=(
  "https://example.com/page1"
  "https://example.com/page2"
  "https://example.com/page3"
)

for url in "${urls[@]}"; do
  gh workflow run add-test-case.yml \
    -f test_url="$url" \
    -f test_name="Test $(basename $url)" \
    -f category=medium
  sleep 10
done

# Method 2: Manual then commit
python scripts/add_test_case.py --url https://example.com --name "Test 1"
python scripts/add_test_case.py --url https://another.com --name "Test 2"
git add test_cases/
git commit -m "test: Add new test cases"
git push

# Validation workflow runs automatically on PR
```

### Workflow 4: Monitor Quality Over Time

```bash
# Baseline tests run automatically daily

# View recent baseline results
gh run list --workflow=scheduled-baseline.yml --limit 10

# Download specific baseline data
gh run download <run-id> --name baseline-results-*

# Analyze trends
cd baseline-results-*/results/reports/
jq '.summary.average_weighted_score' *.json | \
  awk '{sum+=$1; n++} END {print "Average:", sum/n}'
```

---

## Viewing Results

### Method 1: GitHub UI

1. Go to **Actions** tab
2. Click on a workflow run
3. View the **Summary** (includes):
   - ✅ Pass/fail status
   - 📊 Test scores
   - 💰 Cost information
   - ⏱️ Execution time
4. Click **"Artifacts"** to download detailed reports
5. View **job logs** for debugging

### Method 2: GitHub CLI

```bash
# List recent runs
gh run list --workflow=test-prompts.yml --limit 10

# View specific run details
gh run view <run-id>

# Download artifacts
gh run download <run-id>

# View logs
gh run view <run-id> --log

# Watch a run in real-time
gh run watch <run-id>
```

### Method 3: API Access

```bash
# Get run data via API
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/rdytowrk/agent-harness-test-loop/actions/runs

# Download artifacts
curl -L -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/rdytowrk/agent-harness-test-loop/actions/artifacts/<artifact-id>/zip \
  -o results.zip
```

---

## Artifacts

Each workflow uploads artifacts that persist for 30-90 days:

### Artifact Types

1. **test-results-python-X.X** (30 days)
   - Complete test run data
   - Individual test results
   - Evaluation scores
   - JSON format

2. **test-reports-python-X.X** (30 days)
   - Markdown reports (human-readable)
   - JSON reports (machine-parseable)
   - Summary statistics

3. **manual-test-results** (90 days)
   - Results from manual runs
   - Comparison reports
   - Historical data

4. **baseline-results-N** (90 days)
   - Daily baseline data
   - Regression analysis
   - Trend data

### Downloading Artifacts

```bash
# List artifacts for a run
gh run view <run-id> --json artifacts

# Download all artifacts
gh run download <run-id>

# Download specific artifact
gh run download <run-id> --name test-reports-python-3.9

# Extract and view
unzip test-reports-python-3.9.zip
cat results/reports/*.md
```

---

## Cost Management

### Monitoring Costs

Each test run shows costs in reports:
```json
{
  "performance": {
    "total_cost": 0.0234,
    "total_tokens": 12453,
    "average_response_time": 2.3
  }
}
```

### Typical Costs

- **Per test case:** $0.001 - $0.005
- **Daily baseline:** $0.01 - $0.05
- **Full test suite:** $0.05 - $0.20
- **Monthly (with daily baselines):** $1 - $10

### Cost Optimization Tips

1. **Use simple tests for iteration:**
   ```bash
   gh workflow run manual-test.yml -f test_cases=simple
   ```

2. **Limit scheduled runs:**
   ```yaml
   # Run weekly instead of daily
   schedule:
     - cron: '0 2 * * 0'  # Sunday at 2 AM
   ```

3. **Use specific test cases:**
   ```bash
   gh workflow run manual-test.yml -f test_ids="test_abc,test_def"
   ```

4. **Set up cost alerts** in your Google Cloud Console

---

## Troubleshooting

### Issue: Workflow doesn't trigger

**Check:**
- ✅ GitHub Actions is enabled (Settings → Actions)
- ✅ File paths match workflow triggers
- ✅ Branch is included in workflow `on:` configuration
- ✅ Push was to the correct branch

**Solution:**
```bash
# Trigger manually to test
gh workflow run test-prompts.yml
```

### Issue: "GEMINI_API_KEY not found"

**Solution:**
1. Go to Settings → Secrets → Actions
2. Ensure `GEMINI_API_KEY` is added
3. Value should be your actual API key (starts with `AI...`)
4. Re-run the workflow

### Issue: Tests fail but work locally

**Check:**
- Environment differences (Python version, dependencies)
- Paths are relative to project root
- All required files are committed

**Debug:**
```bash
# Check workflow logs
gh run view <run-id> --log

# Download artifacts and inspect
gh run download <run-id>
```

### Issue: Workflows run too often / too expensive

**Solutions:**

1. **Disable scheduled runs:**
   ```yaml
   # .github/workflows/scheduled-baseline.yml
   # Comment out schedule:
   ```

2. **Limit to specific branches:**
   ```yaml
   on:
     push:
       branches:
         - main  # Only main branch
   ```

3. **Use path filters:**
   ```yaml
   on:
     push:
       paths:
         - 'prompts/active/**'  # Only active prompts
   ```

### Issue: PR comments not appearing

**Solution:**
1. Check workflow permissions (Settings → Actions → General)
2. Ensure "Allow GitHub Actions to create PRs" is checked
3. Verify GitHub token has correct permissions

---

## Advanced Configuration

### Custom Notification

Add Slack notifications:

```yaml
# In any workflow, add this step:
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Test run failed: ${{ github.repository }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Matrix Testing

Test multiple prompts at once:

```yaml
strategy:
  matrix:
    prompt: [base_v1, experiment_001, semantic_v1]
    python-version: ['3.9', '3.12']
```

### Conditional Execution

Run only on specific conditions:

```yaml
- name: Run expensive tests
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  run: python scripts/run_tests.py --all
```

---

## Best Practices

### 1. Test Before Merging
Always create PRs for prompt changes and review CI results before merging.

### 2. Use Descriptive Commit Messages
```bash
✅ Good: "feat: Add semantic HTML emphasis to base prompt"
❌ Bad: "update prompt"
```

### 3. Monitor Baseline Tests
Check daily baseline results weekly to catch quality drift.

### 4. Keep Test Cases Current
Regularly review and update test cases to reflect real use cases.

### 5. Download Important Artifacts
Download and archive significant test results for future reference.

### 6. Use Tags for Organization
```bash
python scripts/add_test_case.py ... --tags "priority,regression,edge-case"
```

### 7. Review Cost Reports
Check monthly costs in reports and optimize if needed.

---

## Next Steps

✅ **Setup Complete!** Here's what to do next:

1. **Test the setup:**
   ```bash
   gh workflow run manual-test.yml -f prompt_name=base_v1
   ```

2. **Make a prompt change:**
   ```bash
   vim prompts/base/conversion_v1.md
   git commit -m "feat: Improve prompt"
   git push
   ```

3. **Watch it run:**
   ```bash
   gh run watch
   ```

4. **Review results:**
   - Check Actions tab
   - Download artifacts
   - Review reports

5. **Iterate:**
   - Based on results, refine prompts
   - Run tests again
   - Compare results
   - Repeat!

---

## Support

- **Documentation:** See [.github/workflows/README.md](.github/workflows/README.md)
- **Examples:** See [docs/EXAMPLES.md](docs/EXAMPLES.md)
- **Issues:** Create an issue in the repository
- **Discussions:** Use GitHub Discussions for questions

Happy testing! 🚀
