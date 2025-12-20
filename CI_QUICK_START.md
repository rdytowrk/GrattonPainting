# CI/CD Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Add API Key Secret (2 minutes)
1. Go to: https://github.com/rdytowrk/agent-harness-test-loop/settings/secrets/actions
2. Click **"New repository secret"**
3. Add:
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key
4. Click **"Add secret"**

### Step 2: Enable Permissions (1 minute)
1. Go to: https://github.com/rdytowrk/agent-harness-test-loop/settings/actions
2. Under "Workflow permissions":
   - Select ✅ **"Read and write permissions"**
   - Check ✅ **"Allow GitHub Actions to create and approve pull requests"**
3. Click **"Save"**

### Step 3: Test It! (2 minutes)
```bash
# Trigger a manual test run
gh workflow run manual-test.yml -f prompt_name=base_v1

# Watch it run
gh run watch

# Or view in browser:
# https://github.com/rdytowrk/agent-harness-test-loop/actions
```

**Done!** 🎉 Your CI/CD pipeline is ready.

---

## 📋 What You Got

### 4 Automated Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **Test Prompt Changes** | Auto on push | Tests prompts when modified |
| **Manual Test** | On-demand | Full control testing |
| **Baseline Tests** | Daily 2AM UTC | Quality monitoring |
| **Add Test Case** | Manual/PR | Add & validate tests |

---

## 🎯 Common Commands

### Test a Prompt Change
```bash
# Edit prompt
vim prompts/variations/my_prompt.md

# Commit (triggers CI automatically)
git add prompts/
git commit -m "feat: Improve semantic focus"
git push

# CI runs automatically!
# View: Actions tab on GitHub
```

### Run Manual Test
```bash
# Basic test
gh workflow run manual-test.yml \
  -f prompt_name=base_v1 \
  -f test_cases=all

# With comparison
gh workflow run manual-test.yml \
  -f prompt_name=experiment_001 \
  -f generate_comparison=true

# Specific category
gh workflow run manual-test.yml \
  -f prompt_name=base_v1 \
  -f test_cases=simple
```

### Add Test Case
```bash
# Via workflow
gh workflow run add-test-case.yml \
  -f test_url="https://example.com" \
  -f test_name="Example Site" \
  -f category=medium \
  -f tags="example,test"

# Or manually
python scripts/add_test_case.py \
  --url https://example.com \
  --name "Example" \
  --category medium
```

### View Results
```bash
# List recent runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# Download results
gh run download <run-id>

# Watch live
gh run watch
```

---

## 📊 What Gets Tested

Every workflow run:
- ✅ Installs dependencies
- ✅ Runs harness tests
- ✅ Generates reports (Markdown + JSON)
- ✅ Uploads artifacts (30-90 day retention)
- ✅ Tests multiple Python versions (3.9-3.12)
- ✅ Tracks costs and performance

---

## 💰 Cost Tracking

Each test shows costs:
- **Per test case:** $0.001-$0.005
- **Full suite:** $0.05-$0.20
- **Daily baseline:** $0.01-$0.05
- **Monthly (w/ daily):** $1-$10

View in reports:
```bash
gh run download <run-id>
cat results/reports/*.json | jq '.performance.total_cost'
```

---

## 🔔 What Happens When

### When you commit prompt changes:
1. ✅ Workflow detects changes
2. ✅ Runs tests with modified prompt
3. ✅ Generates reports
4. ✅ Uploads artifacts
5. ✅ Shows results in Actions tab

### When you create a PR with prompts:
1. ✅ All of the above, PLUS:
2. ✅ Compares with baseline
3. ✅ Posts comment on PR with results
4. ✅ Blocks merge if tests fail (optional)

### Daily at 2 AM UTC:
1. ✅ Runs baseline tests
2. ✅ Compares with previous day
3. ✅ Creates issue if regression detected (>5% drop)
4. ✅ Uploads 90-day historical data

---

## 🎨 Example Workflow

### Scenario: Test a New Prompt

```bash
# 1. Create branch
git checkout -b prompt/semantic-focus

# 2. Copy and edit prompt
cp prompts/base/conversion_v1.md prompts/variations/semantic_v1.md
vim prompts/variations/semantic_v1.md
# ... make your improvements ...

# 3. Register in config
vim config/prompts.yaml
# Add your prompt config

# 4. Commit and push
git add prompts/ config/
git commit -m "feat: Add semantic HTML focused prompt"
git push origin prompt/semantic-focus

# 5. Create PR
gh pr create \
  --title "Add semantic-focused prompt" \
  --body "Testing emphasis on semantic HTML5 elements"

# 6. CI automatically:
#    ✅ Runs tests
#    ✅ Generates reports  
#    ✅ Comments on PR with results
#    ✅ Compares with baseline

# 7. Review results in PR
# 8. Iterate if needed
# 9. Merge when satisfied
```

---

## 📁 Where to Find Results

### GitHub UI
- **Actions tab:** Overall status
- **Workflow summary:** Pass/fail, scores, costs
- **Artifacts:** Download detailed reports
- **Job logs:** Debugging information

### Downloaded Artifacts
```
test-results-python-3.9/
├── results/
│   ├── runs/
│   │   └── run_20251220_143022_abc123/
│   │       ├── results/
│   │       ├── evaluations/
│   │       └── run.json
│   └── reports/
│       ├── run_20251220_143022_abc123.md
│       └── run_20251220_143022_abc123.json
```

### Key Files
- `*.md` - Human-readable reports
- `*.json` - Machine-parseable data
- `run.json` - Complete run metadata

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
**Fix:** Add secret in Settings → Secrets → Actions

### Workflow doesn't trigger
**Fix:** Check file paths match workflow triggers
```yaml
paths:
  - 'prompts/**'  # Must match your commit
```

### Tests fail but work locally
**Debug:** Check workflow logs
```bash
gh run view <run-id> --log
```

### Want to test locally first
```bash
# Install act (local GitHub Actions runner)
brew install act

# Run workflow locally
act -W .github/workflows/test-prompts.yml \
  -s GEMINI_API_KEY="your_key"
```

---

## 📚 Full Documentation

- **Setup Guide:** [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)
- **Workflow Docs:** [.github/workflows/README.md](.github/workflows/README.md)
- **Examples:** [docs/EXAMPLES.md](docs/EXAMPLES.md)
- **Agent Guide:** [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)

---

## 🎯 Next Steps

1. ✅ **Complete setup** (API key + permissions)
2. ✅ **Test it** with manual workflow
3. ✅ **Make a prompt change** and see it run
4. ✅ **Review results** in Actions tab
5. ✅ **Iterate** based on feedback

**Ready to go!** 🚀

---

## 💡 Pro Tips

1. **Test simple category first** for fast iteration
2. **Use manual workflow** to experiment
3. **Monitor daily baselines** for quality trends
4. **Download artifacts** for deep analysis
5. **Tag test cases** for better organization
6. **Check costs** in reports monthly
7. **Create PRs** for prompt changes to get comparisons

---

## 🆘 Need Help?

- **GitHub Actions Logs:** Check workflow runs for errors
- **Documentation:** See GITHUB_ACTIONS_SETUP.md
- **Examples:** See docs/EXAMPLES.md
- **Issues:** Create issue in repo
- **Discussions:** Use GitHub Discussions

Happy testing! 🧪✨
