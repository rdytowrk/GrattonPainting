# Gemini Model Reference

## Current Configuration

**Model**: `gemini-2.5-flash` (Gemini 2.5 Flash - Newest)

## Available Models (December 2024)

### Gemini 2.5 (Newest)
- ✅ `gemini-2.5-flash` - **CURRENT** - Newest Flash model (free)
- ❌ `gemini-2.5-flash-exp` - Not available (returns 404)
- ❌ `gemini-2.5-flash-latest` - Not available (returns 404)

### Gemini 2.0
- `gemini-2.0-flash-exp` - Experimental version

### Gemini 1.5 (Stable)
- `gemini-1.5-flash-latest` - Auto-updated to latest stable
- `gemini-1.5-flash` - Stable Flash model
- `gemini-1.5-pro-latest` - Pro model (more capable, slower)
- `gemini-1.5-pro` - Pro model

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
   export GEMINI_MODEL=gemini-2.5-flash         # ✅ CURRENT (newest!)
   export GEMINI_MODEL=gemini-1.5-flash-latest  # Stable fallback
   export GEMINI_MODEL=gemini-1.5-flash
   export GEMINI_MODEL=gemini-2.0-flash-exp
   ```
3. **Check model availability**: Some experimental models may not be available in all regions
4. **Verify API access**: Go to [Google AI Studio](https://aistudio.google.com/) to check your API key and available models

## Free Tier Limits

- **Gemini 2.5 Flash** (Current): High rate limits for developers (free)
- **Gemini 1.5 Flash**: 15 RPM, 1M TPM, 1.5K RPD (free)
- **Gemini 1.5 Pro**: 2 RPM, 32K TPM, 50 RPD (free)

RPM = Requests per minute
TPM = Tokens per minute  
RPD = Requests per day

## More Information

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Model Documentation](https://ai.google.dev/models/gemini)
