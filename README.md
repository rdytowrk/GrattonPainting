# HTML-to-Tailwind Conversion Harness

A powerful testing harness for iterating on AI prompts that convert HTML code and screenshots into clean, structured HTML with Tailwind CSS classes.

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Initialize the harness
python scripts/init_harness.py
```

### Basic Usage

```bash
# Add a test case from a URL
python scripts/add_test_case.py --url https://example.com --name "homepage"

# Add a test case from local HTML file
python scripts/add_test_case.py --file test.html --name "test_001"

# Run tests with the active prompt
python scripts/run_tests.py --prompt base_v1

# Generate a report
python scripts/generate_report.py --run latest --format markdown
```

## Key Features

- 🔄 **Rapid Iteration**: Test prompt variations in minutes
- 🤖 **Dual Agent Support**: External agents (Cursor) + Internal agents (Gemini)
- 📊 **Automated Evaluation**: Quality metrics and scoring
- 📈 **Progress Tracking**: Historical metrics and comparisons
- 🎯 **Agent-Optimized**: CLI and outputs designed for AI agents

## Architecture

The harness supports two types of agents:

1. **External Agent (Cursor/Coding Agent)**: Iterates on prompts, reviews outputs, runs tests
2. **Internal Agent (Gemini API)**: Performs the actual HTML-to-Tailwind conversion

## Project Structure

```
├── prompts/            # Prompt templates and variations
├── test_cases/         # Test inputs (HTML, screenshots)
├── results/            # Conversion results and reports
├── src/                # Core harness implementation
├── config/             # Configuration files
├── scripts/            # CLI tools
└── docs/               # Documentation
```

## Documentation

- [Project Plan](PROJECT_PLAN.md) - Detailed architecture and roadmap
- [Agent Guide](docs/AGENT_GUIDE.md) - Guide for external coding agents
- [API Documentation](docs/API.md) - Python API reference
- [Examples](docs/EXAMPLES.md) - Usage examples

## Workflow

1. **Add test cases** with various HTML inputs
2. **Create prompt variations** to experiment with
3. **Run tests** to generate outputs
4. **Review results** using automated metrics
5. **Iterate** on prompts based on findings

## Requirements

- Python 3.9+
- Google Gemini API key
- (Optional) Playwright for screenshot capture

## License

MIT
