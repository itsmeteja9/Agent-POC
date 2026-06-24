# RCA Agent for GitHub

An automated Root Cause Analysis (RCA) agent that analyzes CI/CD pipeline failures and provides detailed diagnostics.

## Features

- **Automated Log Analysis**: Analyzes pipeline logs to identify root causes
- **Multi-Category Detection**: Identifies issues across infrastructure, CI/CD, database, network, security, and configuration categories
- **Confidence Scoring**: Provides confidence levels for identified issues
- **Actionable Recommendations**: Suggests fixes for identified problems
- **GitHub Actions Integration**: Runs automatically on pipeline failures

## Supported Issue Categories

- **Infrastructure**: Memory exhaustion, disk space issues
- **CI/CD**: Build and test failures
- **Network**: Connection and connectivity issues
- **Database**: Connection pool and query failures
- **Security**: Authentication, authorization, and permission issues
- **Dependencies**: Missing or incompatible packages
- **Configuration**: Config and environment variable issues
- **Performance**: Timeout and slow operation detection

## Usage

### Local Testing

1. Create a `logs.txt` file with pipeline logs:
   ```
   [Pipeline] Start build
   [Pipeline] Running tests
   ERROR: Test suite failed: 12 failed, 5 passed
   [Pipeline] Build failed
   ```

2. Run the RCA agent:
   ```bash
   python rca/run_rca.py
   ```

3. View the analysis results in JSON format

### GitHub Actions Integration

The RCA agent automatically runs on pipeline failures:

```yaml
- name: 🚀 Run RCA Agent
  if: failure()
  run: python rca/run_rca.py | tee rca_output.txt

- name: 📦 Upload RCA Artifact
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: rca-report
    path: rca_output.txt
```

## Project Structure

```
Agent-POC/
├── .github/
│   └── workflows/
│       └── rca.yml          # GitHub Actions workflow
├── rca/
│   ├── rca_engine.py        # Core RCA analysis engine
│   └── run_rca.py           # CLI entry point
├── README.md
└── logs.txt                 # Sample/generated log file
```

## Output Example

```json
{
  "root_cause": "CI/CD pipeline failure due to failing tests",
  "impact": "Build failed -> deployment blocked",
  "confidence": "high",
  "category": "ci/cd",
  "recommended_fix": "Fix failing test cases or rollback code"
}
```

## Future Enhancements

- [ ] Machine learning-based pattern detection
- [ ] Integration with monitoring systems (DataDog, New Relic, etc.)
- [ ] Slack/Email notifications with RCA results
- [ ] Historical trend analysis
- [ ] Custom rule definitions
- [ ] Multi-language log parsing
