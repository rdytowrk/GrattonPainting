# Gemini Model Reference

## Current Configuration

**Model**: `gemini-2.5-flash-exp` (Gemini 2.5 Flash Experimental)

## Available Models (December 2024)

### Gemini 2.5 (Latest)
- `gemini-2.5-flash-exp` - Experimental, newest, free (1M tokens/day)
- `gemini-2.5-flash` - Stable version (if available)

### Gemini 2.0
- `gemini-2.0-flash-exp` - Experimental version

### Gemini 1.5
- `gemini-1.5-flash` - Stable Flash model
- `gemini-1.5-flash-latest` - Auto-updated to latest stable
- `gemini-1.5-pro` - Pro model (more capable, slower)
- `gemini-1.5-pro-latest` - Auto-updated Pro

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
   # Try these in order:
   export GEMINI_MODEL=gemini-2.5-flash-exp
   export GEMINI_MODEL=gemini-2.5-flash
   export GEMINI_MODEL=gemini-2.0-flash-exp
   export GEMINI_MODEL=gemini-1.5-flash-latest
   ```
3. **Check model availability**: Some experimental models may not be available in all regions
4. **Verify API access**: Go to [Google AI Studio](https://aistudio.google.com/) to check your API key and available models

## Free Tier Limits

- **Gemini 2.5 Flash**: 1 million tokens per day (free)
- **Gemini 1.5 Flash**: 15 requests per minute, 1 million tokens per minute
- **Gemini 1.5 Pro**: 2 requests per minute

## More Information

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Model Documentation](https://ai.google.dev/models/gemini)
