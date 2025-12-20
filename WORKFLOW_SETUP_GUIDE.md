# Workflow Setup Guide - Fix "Artifact Not Found" Error

## ✅ Issue Fixed!

I've fixed the workflow to handle the case when no test cases exist yet. The error you saw was because the workflow tried to download artifacts that didn't exist.

## 🚀 How to Use the Workflows Properly

### Step 1: Add Test Cases First (Required!)

Before running the workflows, you need to add at least one test case. The workflows can't run without test cases.

#### Option A: Add Test Cases Locally

```bash
# Clone your repo (if not already)
git clone -b cursor/harness-testing-tool-setup-ce15 \
  https://github.com/rdytowrk/agent-harness-test-loop.git
cd agent-harness-test-loop

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_actual_key

# Add test cases from URLs
python scripts/add_test_case.py \
  --url "https://getbootstrap.com/docs/5.3/components/cards/" \
  --name "Bootstrap Cards" \
  --category medium \
  --tags "bootstrap,cards"

python scripts/add_test_case.py \
  --url "https://tailwindcss.com/docs/installation" \
  --name "Tailwind Docs" \
  --category simple \
  --tags "tailwind,docs"

# Or run init to create a sample test case
python scripts/init_harness.py

# Commit and push
git add test_cases/
git commit -m "test: Add initial test cases"
git push origin cursor/harness-testing-tool-setup-ce15
```

#### Option B: Add Test Cases via GitHub Workflow

```bash
# Use the add-test-case workflow
gh workflow run add-test-case.yml \
  -f test_url="https://getbootstrap.com/docs/5.3/components/cards/" \
  -f test_name="Bootstrap Cards" \
  -f category=medium \
  -f tags="bootstrap,cards"

# Wait for it to complete
gh run watch

# The workflow will automatically commit the test case
```

### Step 2: Now Run the Test Workflows

Once you have test cases, you can run the workflows:

```bash
# Manual test workflow
gh workflow run manual-test.yml \
  -f prompt_name=base_v1 \
  -f test_cases=all \
  -f verbose=true

# Or trigger by changing a prompt
echo "" >> prompts/base/conversion_v1.md
git add prompts/
git commit -m "test: Trigger workflow"
git push
```

---

## 🎯 Quick Start Commands

Run these commands in order:

```bash
# 1. Clone and setup
git clone -b cursor/harness-testing-tool-setup-ce15 \
  https://github.com/rdytowrk/agent-harness-test-loop.git
cd agent-harness-test-loop

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env: Add GEMINI_API_KEY=your_key

# 4. Create sample test case
python scripts/init_harness.py

# 5. Verify test case was created
python scripts/list_test_cases.py --stats

# 6. Commit test cases
git add test_cases/
git commit -m "test: Add sample test case"
git push origin cursor/harness-testing-tool-setup-ce15

# 7. Now trigger the workflow
gh workflow run manual-test.yml -f prompt_name=base_v1

# 8. Watch it run
gh run watch
```

---

## 🐛 What Was Wrong?

**Original Error:**
```
Error: Unable to download artifact(s): Artifact not found for name: test-results-python-3.9
```

**Cause:**
The `compare-with-baseline` job tried to download artifacts from the `test-prompts` job, but:
1. No test cases existed yet
2. The test job skipped execution
3. No artifacts were created
4. The download step failed

**Fix:**
- ✅ Added check for test case existence before running tests
- ✅ Made artifact download `continue-on-error`
- ✅ Added conditional execution based on test availability
- ✅ Created helpful summary when no tests are available
- ✅ Fixed compare job to handle missing artifacts gracefully

---

## 📊 Current Status

After pushing the fix:

✅ **Workflow fixed** - No more "artifact not found" errors  
⚠️ **Need test cases** - Add at least one test case before running workflows  
✅ **Instructions added** - This guide shows you how  

---

## 💡 Recommended Workflow

### For First Time Setup:

1. **Add test cases locally** (easier for multiple cases):
   ```bash
   python scripts/add_test_case.py --url <url1> --name "Test 1"
   python scripts/add_test_case.py --url <url2> --name "Test 2"
   python scripts/add_test_case.py --url <url3> --name "Test 3"
   git add test_cases/
   git commit -m "test: Add initial test suite"
   git push
   ```

2. **Run manual test** to verify everything works:
   ```bash
   gh workflow run manual-test.yml -f prompt_name=base_v1
   ```

3. **Check results** in the Actions tab

4. **Now you can iterate on prompts** and tests will run automatically!

### For Ongoing Use:

Once test cases are set up, just edit prompts and push:

```bash
vim prompts/variations/my_prompt.md
git add prompts/
git commit -m "feat: Improve prompt"
git push

# Workflows automatically run and report results!
```

---

## 🎨 Example: Complete First Setup

```bash
# Clone
git clone -b cursor/harness-testing-tool-setup-ce15 \
  https://github.com/rdytowrk/agent-harness-test-loop.git
cd agent-harness-test-loop

# Setup
pip install -r requirements.txt
cp .env.example .env
# Add GEMINI_API_KEY to .env

# Add 3 test cases
python scripts/add_test_case.py \
  --url "https://getbootstrap.com/docs/5.3/components/cards/" \
  --name "Bootstrap Cards" \
  --category medium \
  --tags "bootstrap,component"

python scripts/add_test_case.py \
  --url "https://tailwindui.com/components" \
  --name "TailwindUI" \
  --category medium \
  --tags "tailwind,ui"

python scripts/add_test_case.py \
  --url "https://flowbite.com/docs/components/buttons/" \
  --name "Flowbite Buttons" \
  --category simple \
  --tags "flowbite,buttons"

# Verify
python scripts/list_test_cases.py

# Commit
git add test_cases/
git commit -m "test: Add initial test suite with 3 cases"
git push origin cursor/harness-testing-tool-setup-ce15

# Test workflow
gh workflow run manual-test.yml -f prompt_name=base_v1

# Watch
gh run watch
```

---

## ✅ Checklist

- [x] Fix workflow artifact error
- [x] Push fix to repository
- [ ] **Add test cases** ← YOU ARE HERE
- [ ] Run workflow to verify
- [ ] Iterate on prompts
- [ ] Monitor results

---

## 🆘 Still Having Issues?

### Error: "No test cases available"

**Solution:** Add test cases using the commands above

### Error: "GEMINI_API_KEY not found"

**Solution:** 
1. Check GitHub Secrets: Settings → Secrets → Actions
2. Verify secret name is exactly: `GEMINI_API_KEY`
3. Make sure you added the actual API key value

### Error: Workflow doesn't trigger

**Solution:**
1. Make sure you pushed test cases to the repository
2. Trigger manually first: `gh workflow run manual-test.yml`
3. Check Actions tab for status

### Need Help?

Run this diagnostic:
```bash
cd agent-harness-test-loop
python scripts/list_test_cases.py --stats

# Should show:
# Total test cases: X (where X > 0)
```

If X = 0, you need to add test cases!

---

## 📍 Quick Links

- **Repository:** https://github.com/rdytowrk/agent-harness-test-loop
- **Actions Tab:** https://github.com/rdytowrk/agent-harness-test-loop/actions
- **Add Secret:** https://github.com/rdytowrk/agent-harness-test-loop/settings/secrets/actions

---

**Updated:** December 20, 2025  
**Status:** ✅ Workflow fixed, ready to add test cases
