# Known Issues

## ✅ RESOLVED: Migrated to google-genai Package

**Previous Issue:** The harness was using the deprecated `google-generativeai` package.

**Status:** ✅ RESOLVED (December 20, 2025)

**Solution Implemented:**
- ✅ Updated `requirements.txt` to use `google-genai` instead of `google-generativeai`
- ✅ Updated `src/agents/gemini_agent.py` to use the new API
- ✅ Using Gemini 2.5 Flash (gemini-2.5-flash-latest) - newest model
- ✅ Updated all API calls to use new `client.models.generate_content()` format
- ✅ Free tier: 1 million tokens per day (no cost!)

**Current Status:**
The harness now uses the latest, supported Google Gemini API with Gemini 2.5 Flash (newest, free) and no deprecation warnings.

## Other Notes

### Path Warnings
You may see warnings about scripts not being in PATH:
```
WARNING: The script dotenv is installed in '/home/ubuntu/.local/bin' which is not on PATH.
```

**Solution:** Add to your shell profile:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Or run scripts with absolute paths.

---

**Last Updated:** 2025-12-20  
**Version:** 0.1.0
