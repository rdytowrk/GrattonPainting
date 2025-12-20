# HTML-to-Tailwind Conversion Harness Testing Tool

## Project Overview

A comprehensive testing harness designed to iterate, test, and optimize prompts for converting HTML code (from URLs or screenshots) into structured, clean HTML with Tailwind CSS classes.

## Core Objectives

1. **Rapid Prompt Iteration**: Enable quick testing of different prompt variations
2. **Automated Testing Loop**: Automated test/review/iterate cycle with minimal human intervention
3. **Dual Agent Architecture**: Support both external coding agents (Cursor) and internal conversion agents (Gemini API)
4. **Quality Metrics**: Objective and subjective quality measurements for outputs
5. **Historical Tracking**: Track performance improvements over time

## Architecture

### Agent Roles

#### 1. External Agent (Cursor/Coding Agent)
**Role**: Prompt Engineer & Quality Reviewer
- Iterates on prompt designs
- Reviews conversion outputs
- Identifies patterns in failures
- Suggests improvements to harness
- Runs test suites and analyzes results

#### 2. Internal Agent (Gemini API)
**Role**: HTML Converter
- Executes conversion tasks
- Takes prompt + input (HTML/screenshot)
- Returns structured HTML with Tailwind classes
- Provides reasoning/explanation when requested

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Testing Harness Core                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Prompt     │  │  Test Case   │  │  Evaluation  │      │
│  │  Management  │  │  Management  │  │    Engine    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Gemini     │  │   Results    │  │   Metrics    │      │
│  │  Integration │  │   Storage    │  │   Tracking   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    External Agent       Test Inputs          Reports/Logs
   (Cursor/Human)     (HTML/Screenshots)    (JSON/Markdown)
```

## Project Structure

```
/workspace/
├── prompts/                    # Prompt templates and variations
│   ├── base/                   # Base prompt templates
│   ├── variations/             # Experimental prompt variations
│   ├── active/                 # Currently active prompts
│   └── archive/                # Historical prompts
│
├── test_cases/                 # Test inputs and expected outputs
│   ├── html_inputs/            # Raw HTML test cases
│   ├── screenshots/            # Screenshot test cases
│   ├── expected_outputs/       # Expected/ideal outputs
│   └── metadata.json           # Test case metadata
│
├── results/                    # Conversion results and analysis
│   ├── runs/                   # Individual test run results
│   ├── comparisons/            # Side-by-side comparisons
│   └── reports/                # Generated reports
│
├── src/                        # Core harness implementation
│   ├── harness/                # Main harness logic
│   ├── agents/                 # Agent integrations (Gemini, etc.)
│   ├── evaluators/             # Quality evaluation logic
│   ├── reporters/              # Reporting and visualization
│   └── utils/                  # Shared utilities
│
├── config/                     # Configuration files
│   ├── prompts.yaml            # Prompt configurations
│   ├── evaluation.yaml         # Evaluation criteria
│   └── agents.yaml             # Agent configurations
│
├── scripts/                    # Utility scripts
│   ├── run_tests.py            # Run test suite
│   ├── compare_runs.py         # Compare multiple runs
│   ├── generate_report.py     # Generate detailed reports
│   └── agent_review.py         # Agent-assisted review
│
├── docs/                       # Documentation
│   ├── AGENT_GUIDE.md          # Guide for external agents
│   ├── API.md                  # API documentation
│   └── EXAMPLES.md             # Usage examples
│
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation
└── pyproject.toml              # Python project configuration
```

## Workflow: Test/Review/Iterate Loop

### 1. Setup Phase
```bash
# Add new test case
python scripts/add_test_case.py --input html_file.html --name "test_001"

# Configure prompt variation
python scripts/create_prompt_variation.py --base base_v1 --name experiment_001
```

### 2. Execution Phase
```bash
# Run tests with specific prompt
python scripts/run_tests.py --prompt experiment_001 --test-suite basic

# Or run all active prompts against all test cases
python scripts/run_tests.py --all
```

### 3. Evaluation Phase (Automated)
- **Structural Analysis**: Valid HTML, Tailwind class usage, semantic structure
- **Visual Similarity**: If screenshots available, compare rendered outputs
- **Code Quality**: Clean structure, proper nesting, accessibility
- **Performance Metrics**: Token usage, response time, success rate

### 4. Review Phase (Agent-Assisted)
```bash
# Generate comparison report for agent review
python scripts/generate_report.py --run latest --format markdown

# External agent reviews and provides feedback
python scripts/agent_review.py --run latest --feedback "feedback.md"
```

### 5. Iteration Phase
```bash
# Create new prompt based on findings
python scripts/create_prompt_variation.py --base experiment_001 --improvements feedback.md

# Archive old prompts
python scripts/archive_prompt.py --name experiment_001
```

## Key Features

### 1. Prompt Management
- Version-controlled prompt templates
- Easy A/B testing of variations
- Templating system for dynamic content
- Metadata tracking (author, date, purpose, results)

### 2. Test Case Management
- Import HTML from URLs or files
- Screenshot capture and storage
- Expected output definition (optional)
- Test case tagging and categorization
- Difficulty levels (simple, medium, complex)

### 3. Automated Evaluation
- **Syntax Validation**: HTML structure, Tailwind classes
- **Semantic Analysis**: Proper element usage, accessibility
- **Visual Comparison**: Screenshot diff (if baseline exists)
- **Code Metrics**: Lines of code, complexity, token count
- **Consistency Checks**: Class naming patterns, structure patterns

### 4. Agent Integration

#### External Agent (Cursor)
- Clear CLI commands for all operations
- Structured output formats (JSON, Markdown)
- Detailed error messages and suggestions
- Git-friendly file formats for diffs
- Agent-readable reports with actionable insights

#### Internal Agent (Gemini)
- Configurable API parameters (temperature, max_tokens)
- Prompt chaining for complex conversions
- Error handling and retry logic
- Response caching for cost optimization
- Multiple model support (gemini-pro, gemini-pro-vision)

### 5. Reporting & Metrics
- **Run Reports**: Individual test run details
- **Comparison Reports**: Side-by-side prompt comparisons
- **Trend Analysis**: Performance over time
- **Cost Tracking**: API usage and costs
- **Quality Scores**: Aggregated quality metrics

## Quality Metrics

### Automated Metrics
1. **HTML Validity Score**: Valid HTML5 structure
2. **Tailwind Coverage**: % of styles using Tailwind classes
3. **Semantic Score**: Proper HTML5 semantic elements
4. **Accessibility Score**: Basic a11y compliance
5. **Code Cleanliness**: Indentation, organization, comments
6. **Token Efficiency**: Output tokens / input tokens ratio

### Agent-Reviewable Metrics
1. **Visual Fidelity**: How well it matches the input
2. **Maintainability**: Code readability and structure
3. **Flexibility**: Ease of modification for builder editor
4. **Best Practices**: Following HTML/Tailwind conventions

## Configuration System

### Prompt Configuration (`prompts.yaml`)
```yaml
prompts:
  base_v1:
    file: prompts/base/conversion_v1.md
    description: "Initial base prompt"
    parameters:
      temperature: 0.7
      max_tokens: 4000
    
  experiment_001:
    file: prompts/variations/exp_001.md
    parent: base_v1
    description: "Focus on semantic HTML"
    parameters:
      temperature: 0.6
      max_tokens: 4000
```

### Evaluation Configuration (`evaluation.yaml`)
```yaml
evaluation:
  html_validity:
    enabled: true
    weight: 1.0
    
  tailwind_coverage:
    enabled: true
    weight: 0.8
    min_threshold: 0.7
    
  semantic_score:
    enabled: true
    weight: 0.9
    
  accessibility:
    enabled: true
    weight: 0.7
    checks:
      - alt_text
      - aria_labels
      - semantic_structure
```

## Getting Started

### Initial Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment: `cp .env.example .env` (add Gemini API key)
4. Initialize harness: `python scripts/init_harness.py`

### First Test Run
1. Add a test case: `python scripts/add_test_case.py --url https://example.com`
2. Run conversion: `python scripts/run_tests.py --prompt base_v1 --test test_001`
3. Review results: `python scripts/generate_report.py --run latest`
4. Iterate on prompt based on results

## Development Roadmap

### Phase 1: Core Harness (Current Focus)
- [x] Project structure setup
- [ ] Basic Gemini API integration
- [ ] Test case management
- [ ] Simple evaluation metrics
- [ ] CLI interface

### Phase 2: Advanced Features
- [ ] Screenshot comparison
- [ ] Multiple model support
- [ ] Batch processing
- [ ] Cost optimization
- [ ] Advanced metrics

### Phase 3: Agent Optimization
- [ ] Agent-assisted prompt improvement
- [ ] Automated pattern detection
- [ ] Self-improving evaluation criteria
- [ ] Integration with builder editor

## Best Practices for Agents

### For External Agents (Cursor)
1. Always run tests before and after prompt changes
2. Review comparison reports to understand impact
3. Use test case tagging to focus on specific scenarios
4. Document reasoning in prompt metadata
5. Archive successful prompts for future reference

### For Internal Agents (Gemini)
1. Use consistent output format for easier parsing
2. Include reasoning/explanation when available
3. Handle edge cases gracefully
4. Maintain consistent Tailwind class patterns
5. Follow semantic HTML5 guidelines

## Success Metrics

The harness is successful when:
1. **Iteration Speed**: New prompt variations can be tested in < 5 minutes
2. **Quality Improvement**: Measurable improvement in metrics over time
3. **Agent Autonomy**: External agent can complete full iteration cycle without human intervention
4. **Cost Efficiency**: Optimization of API usage while maintaining quality
5. **Reliability**: Consistent results across multiple runs

## Future Considerations

- Integration with builder editor for end-to-end testing
- Support for multiple LLM providers (Claude, GPT-4, etc.)
- Web UI for non-agent users
- Collaborative prompt engineering features
- Real-time monitoring dashboard
