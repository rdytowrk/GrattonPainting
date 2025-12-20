# API Connection Fix - December 20, 2024

## Problem

Workflow was running but tests weren't executing successfully. The error message was:

```
❌ Failed to connect to Gemini API. Check your API key.
```

## Root Causes Found

1. **Incorrect Model Name**: Using `gemini-2.5-flash-latest` which is not the correct format
2. **Missing Diagnostics**: Hard to debug API connection issues

## Solutions Implemented

### 1. Fixed Model Name
Updated from `gemini-2.5-flash-latest` → `gemini-2.5-flash-exp`

**Files changed:**
- `.env.example`
- `config/agents.yaml`
- `src/harness/config.py`

### 2. Added Diagnostic Script
Created `scripts/test_gemini_api.py` to test API connections with detailed error messages.

**Usage:**
```bash
export GEMINI_API_KEY="your-key-here"
python scripts/test_gemini_api.py
```

**Features:**
- ✓ Checks if API key is set
- ✓ Verifies google-genai library
- ✓ Tests actual API connection
- ✓ Provides troubleshooting suggestions

### 3. Added Pre-Test API Check in Workflow
Updated `.github/workflows/test-prompts.yml` to run API connection test before main tests.

This will help identify API issues early in the workflow.

### 4. Created Model Reference Guide
Added `GEMINI_MODEL_REFERENCE.md` with:
- List of available models
- Configuration instructions
- Troubleshooting guide
- Free tier limits

## Next Steps

### Option 1: Model Name Alternatives (If Still Failing)

If `gemini-2.5-flash-exp` doesn't work, try these in order:

```bash
# 1. Try without -exp suffix
gemini-2.5-flash

# 2. Try Gemini 2.0
gemini-2.0-flash-exp

# 3. Fall back to stable Gemini 1.5
gemini-1.5-flash-latest
gemini-1.5-flash
```

Update in: `config/agents.yaml` or set `GEMINI_MODEL` environment variable in GitHub Secrets.

### Option 2: Verify API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Check if your API key is valid
3. Verify you have remaining quota (free tier: 1M tokens/day)
4. Regenerate key if needed
5. Update GitHub Secret: `Settings → Secrets → GEMINI_API_KEY`

### Option 3: Check Model Availability

Some experimental models may not be available in all regions or accounts.

**To check available models:**
```bash
# Using the diagnostic script
export GEMINI_API_KEY="your-key-here"
python scripts/test_gemini_api.py
```

## Testing Locally

Run the diagnostic script to verify everything works:

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your real API key

# 2. Test API connection
python scripts/test_gemini_api.py

# 3. If successful, run actual tests
python scripts/run_tests.py --all --prompt conversion_v1 --verbose
```

## Workflow Will Now Show

When the workflow runs next, you'll see:
1. ✅ **API Connection Test** - Shows detailed diagnostics
2. ✅ **Run Tests** - Only runs if API test passes
3. ✅ **Upload Results** - Test artifacts for comparison

## Common Issues

### Issue: "Invalid API key"
- Check GitHub Secret is set correctly
- Verify key at https://aistudio.google.com/

### Issue: "Model not found"
- Try alternative model names (see Option 1 above)
- Check if experimental models are enabled for your account

### Issue: "Quota exceeded"
- Free tier limit: 1M tokens per day
- Wait 24 hours or upgrade to paid tier

### Issue: "Region not available"
- Some experimental models may not be available in all regions
- Try stable models: `gemini-1.5-flash-latest`

## Files Modified in This Fix

```
Modified:
  .env.example
  config/agents.yaml
  src/harness/config.py
  .github/workflows/test-prompts.yml

Added:
  scripts/test_gemini_api.py
  GEMINI_MODEL_REFERENCE.md
  API_CONNECTION_FIX.md (this file)
```

## Commits
- `fc6860e` - Upgrade to Gemini 2.5 Flash (newest, free model)
- `8ee5ed9` - Fix Gemini model name: use gemini-2.5-flash-exp + add model reference doc
- `6090527` - Add API diagnostics script and pre-test API check in workflow
- `fc19808` - Add API connection test step to workflow with GEMINI_API_KEY env
