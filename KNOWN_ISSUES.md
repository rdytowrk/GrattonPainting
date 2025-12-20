# Known Issues

## ✅ RESOLVED: Migrated to google-genai Package

**Previous Issue:** The harness was using the deprecated `google-generativeai` package.

**Status:** ✅ RESOLVED (December 20, 2025)

**Solution Implemented:**
- ✅ Updated `requirements.txt` to use `google-genai` instead of `google-generativeai`
- ✅ Updated `src/agents/gemini_agent.py` to use the new API
- ✅ Using Gemini 2.0 Flash (gemini-2.0-flash-exp)
- ✅ Updated all API calls to use new `client.models.generate_content()` format

**Current Status:**
The harness now uses the latest, supported Google Gemini API with no deprecation warnings.

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
