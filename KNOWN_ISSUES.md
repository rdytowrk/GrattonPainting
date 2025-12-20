# Known Issues

## Deprecation Warning: google.generativeai Package

**Issue:** When importing the Gemini agent, you may see this warning:

```
FutureWarning: All support for the `google.generativeai` package has ended. 
It will no longer be receiving updates or bug fixes. 
Please switch to the `google.genai` package as soon as possible.
```

**Status:** Known deprecation warning

**Impact:** 
- ⚠️ The current implementation uses `google-generativeai` package
- ✅ The harness still works correctly
- ⚠️ Future updates from Google will require migration

**Solution:**
The Google team has deprecated `google.generativeai` in favor of `google.genai`. 

**Workaround for now:**
The current implementation continues to work. The warning is informational and doesn't affect functionality.

**Future Fix (TODO):**
We should migrate to the new `google.genai` package. This will require:
1. Updating `requirements.txt` to use `google-genai` instead of `google-generativeai`
2. Updating `src/agents/gemini_agent.py` to use the new API
3. Testing compatibility

**Migration Timeline:**
- Current version (v0.1.0): Uses deprecated package but fully functional
- Future version (v0.2.0): Will migrate to `google.genai`

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
