# Pre-Launch Checklist ✓

Use this checklist before starting to use the harness.

## Setup Verification

### Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Add your `GEMINI_API_KEY` to `.env`
- [ ] Verify environment: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key:', os.getenv('GEMINI_API_KEY')[:10] + '...')"`

### Dependencies
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Verify installation: `python -c "import google.generativeai; print('✓ Dependencies installed')"`

### API Connection
- [ ] Run initialization: `python scripts/init_harness.py`
- [ ] Verify API connection test passes
- [ ] Verify sample test case is created

### Directory Structure
- [ ] Verify `prompts/` directories exist
- [ ] Verify `test_cases/` directories exist
- [ ] Verify `results/` directories exist
- [ ] Verify `config/` files exist
- [ ] Verify `scripts/` are executable

## Functional Tests

### Test Case Management
- [ ] Add a test case: `python scripts/add_test_case.py --stdin --name "Quick Test"` (paste HTML, Ctrl+D)
- [ ] List test cases: `python scripts/list_test_cases.py`
- [ ] Verify test case appears in list
- [ ] Check metadata file: `cat test_cases/metadata.json`

### Test Execution
- [ ] Run a test: `python scripts/run_tests.py --all`
- [ ] Verify test completes successfully
- [ ] Check results directory: `ls -la results/runs/`
- [ ] Verify result files are created

### Reporting
- [ ] Generate report: `python scripts/generate_report.py --run latest`
- [ ] Verify report displays correctly
- [ ] Check report file: `ls -la results/reports/`

### Configuration
- [ ] Review prompt config: `cat config/prompts.yaml`
- [ ] Review evaluation config: `cat config/evaluation.yaml`
- [ ] Review agent config: `cat config/agents.yaml`
- [ ] Check base prompt: `cat prompts/base/conversion_v1.md`

## Documentation Review

### Core Documentation
- [ ] Read [README.md](README.md) - Overview and quick start
- [ ] Read [PROJECT_PLAN.md](PROJECT_PLAN.md) - Architecture and design
- [ ] Read [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - Setup summary

### Agent Documentation
- [ ] Read [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md) - Workflow guide
- [ ] Read [docs/API.md](docs/API.md) - Python API reference
- [ ] Read [docs/EXAMPLES.md](docs/EXAMPLES.md) - Usage examples

## Optional: Advanced Verification

### Python API
```python
# Create a file test_api.py with this content:
from src.harness.config import load_config
from src.utils.test_case_manager import TestCaseManager

config = load_config()
manager = TestCaseManager(config)
stats = manager.get_statistics()
print(f"Test cases: {stats['total']}")
print("✓ API working")
```
- [ ] Run: `python test_api.py`
- [ ] Verify output shows test case count

### Cost Tracking
- [ ] Run a few tests
- [ ] Check cost tracking in reports
- [ ] Verify token counts are reasonable
- [ ] Compare costs to expectations

### Prompt Iteration (Optional)
- [ ] Copy base prompt to variations: `cp prompts/base/conversion_v1.md prompts/variations/test.md`
- [ ] Register in `config/prompts.yaml`
- [ ] Run test with new prompt
- [ ] Compare results

## Common Issues

### Issue: "GEMINI_API_KEY not found"
**Solution:** 
```bash
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here
```

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
# Or specifically: pip install google-generativeai python-dotenv pydantic pyyaml beautifulsoup4 click rich
```

### Issue: API connection fails
**Solution:**
1. Verify API key is correct
2. Check internet connection
3. Verify Gemini API is accessible in your region
4. Try: `python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('OK')"`

### Issue: Scripts not executable
**Solution:**
```bash
chmod +x scripts/*.py
```

### Issue: Empty test results
**Solution:**
1. Verify test cases exist: `python scripts/list_test_cases.py`
2. Check test case files exist: `ls test_cases/html_inputs/`
3. Verify metadata.json: `cat test_cases/metadata.json`

## Ready to Use!

Once all checkboxes are complete, you're ready to start using the harness. Your next steps:

1. **Add Real Test Cases**
   ```bash
   python scripts/add_test_case.py --url https://your-site.com --name "Real Test"
   ```

2. **Run Full Test Suite**
   ```bash
   python scripts/run_tests.py --all --verbose
   ```

3. **Analyze Results**
   ```bash
   python scripts/generate_report.py --run latest
   ```

4. **Iterate on Prompts**
   - Review recommendations in report
   - Modify prompts based on findings
   - Re-run tests to verify improvements

## Support

If you encounter issues not covered here:
1. Check [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md) troubleshooting section
2. Review [PROJECT_PLAN.md](PROJECT_PLAN.md) for architecture details
3. Check Python error messages carefully
4. Verify all files are in place: `ls -R`

---

**Last Updated:** 2025-12-20  
**Version:** 0.1.0
