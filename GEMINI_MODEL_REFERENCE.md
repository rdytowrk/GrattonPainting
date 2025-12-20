# Gemini Model Reference

## Current Configuration

**Model**: `gemini-1.5-flash-latest` (Gemini 1.5 Flash - Stable)

## Available Models (December 2024)

### Gemini 1.5 (Recommended - Stable & Available)
- ✅ `gemini-1.5-flash-latest` - **CURRENT** - Auto-updated to latest stable
- `gemini-1.5-flash` - Stable Flash model (specific version)
- `gemini-1.5-pro-latest` - Pro model (more capable, slower)
- `gemini-1.5-pro` - Pro model (specific version)

### Gemini 2.0 (Experimental)
- `gemini-2.0-flash-exp` - Experimental version (may not be available)

### Gemini 2.5 (Not Yet Available)
- ❌ `gemini-2.5-flash-exp` - **NOT FOUND** (returns 404)
- ❌ `gemini-2.5-flash` - Not available yet

## Model Selection

The model name can be configured in three places (priority order):

1. **Environment Variable**: `GEMINI_MODEL` in `.env` file
2. **Config File**: `config/agents.yaml` → `internal_agent.model`
3. **Default**: Falls back to `gemini-2.5-flash-exp` in code

## Troubleshooting

If you get API connection errors:

1. **Check the API key**: Ensure `GEMINI_API_KEY` is valid
2. **Try different model names**:
   ```bash
   # Try these in order (from most to least recommended):
   export GEMINI_MODEL=gemini-1.5-flash-latest  # ✅ CURRENT (works!)
   export GEMINI_MODEL=gemini-1.5-flash
   export GEMINI_MODEL=gemini-2.0-flash-exp
   export GEMINI_MODEL=gemini-1.5-pro-latest
   ```
3. **Check model availability**: Some experimental models may not be available in all regions
4. **Verify API access**: Go to [Google AI Studio](https://aistudio.google.com/) to check your API key and available models

## Free Tier Limits

- **Gemini 1.5 Flash** (Current): 15 RPM, 1M TPM, 1.5K RPD (free)
- **Gemini 1.5 Pro**: 2 RPM, 32K TPM, 50 RPD (free)

RPM = Requests per minute
TPM = Tokens per minute  
RPD = Requests per day

## More Information

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Model Documentation](https://ai.google.dev/models/gemini)
