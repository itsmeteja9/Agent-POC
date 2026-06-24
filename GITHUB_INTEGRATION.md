# GitHub Integration Summary

## 🚀 Quick Start (5 Minutes)

### 1. Push to GitHub
```powershell
cd c:\Users\parva\Agent-POC

# Configure git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Add all files
git add .

# Commit
git commit -m "Add RCA Agent with GitHub Actions"

# Create repo on GitHub: https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/Agent-POC.git
git branch -M main
git push -u origin main
```

### 2. Wait for Workflow to Run
- Go to: `https://github.com/YOUR_USERNAME/Agent-POC/Actions`
- Watch the **Auto RCA Pipeline** workflow execute
- Should complete in 1-2 minutes

### 3. View Results
- Click the workflow run
- Expand **Run RCA Agent** step to see analysis
- Click **Artifacts** tab to download `rca-report`

---

## 📋 What's Included

### Workflow Files

| File | Purpose |
|------|---------|
| `.github/workflows/rca.yml` | Simple RCA pipeline (demo/testing) |
| `.github/workflows/production-build-with-rca.yml` | Advanced workflow for real projects |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | RCA Agent overview & features |
| `QUICK_START.md` | Step-by-step GitHub setup guide |
| `INTEGRATION_GUIDE.md` | Detailed integration & customization |
| `GITHUB_INTEGRATION.md` | This file - quick reference |

### Python Code

| File | Purpose |
|------|---------|
| `rca/rca_engine.py` | Core RCA analysis logic |
| `rca/run_rca.py` | CLI entry point |

---

## 🔧 Integration Patterns

### Pattern 1: Minimal (Existing Workflow)

Add RCA to your existing workflow:

```yaml
# In your .github/workflows/build.yml

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest  # Your actual build/test
      
  rca-on-failure:
    needs: build
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: python rca/run_rca.py | tee rca_output.txt
      - uses: actions/upload-artifact@v3
        with:
          name: rca-report
          path: rca_output.txt
```

### Pattern 2: Integrated (Recommended)

Include RCA in the same workflow:

```yaml
name: Build with RCA

on: [push, pull_request]

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      
      # Your build steps
      - run: pytest tests/
      - run: python setup.py build
      
      # RCA on failure
      - if: failure()
        run: python rca/run_rca.py | tee rca_output.txt
        
      - if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: rca-report
          path: rca_output.txt
      
      # Notify on failure
      - if: failure()
        uses: slack-notify-action@v1
        with:
          text: "Build failed! Check RCA report"
```

### Pattern 3: Advanced (PR Comments)

Automatically comment RCA results on PRs:

```yaml
- name: Comment RCA on PR
  if: failure() && github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const rca = fs.readFileSync('rca_output.txt', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## RCA Analysis\n\n\`\`\`\n${rca}\n\`\`\``
      });
```

---

## 🛠️ Customization Guide

### Capture Logs from Your Build

**Option 1: Redirect to logs.txt**
```yaml
- name: Run Tests
  run: pytest tests/ > logs.txt 2>&1 || true
  
- name: Run RCA
  if: always()
  run: python rca/run_rca.py
```

**Option 2: Collect Multiple Log Files**
```yaml
- name: Collect Logs
  if: always()
  run: |
    cat test-results.log > logs.txt
    cat build-output.log >> logs.txt
    cat deployment.log >> logs.txt
```

**Option 3: Extract from Docker/Container**
```yaml
- name: Extract Container Logs
  if: always()
  run: |
    docker logs $CONTAINER_ID > logs.txt 2>&1 || true
```

### Update RCA Patterns

Edit `rca/rca_engine.py` to add custom detection:

```python
# Add new pattern detection
if "your_error" in text:
    category = "custom"
    confidence = "high"
    fix = "Your recommended fix"
```

### Trigger on More Events

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:  # Manual trigger
```

---

## ✅ Verification Checklist

After pushing to GitHub:

- [ ] Repository is visible on GitHub
- [ ] `.github/workflows/` folder exists
- [ ] `rca.yml` workflow file is present
- [ ] Actions tab is enabled in repository settings
- [ ] First workflow run completes (check Actions tab)
- [ ] RCA report appears in Artifacts
- [ ] Can download and view `rca-report` artifact

---

## 📊 Monitoring Workflow Runs

### Using GitHub UI
1. Click **Actions** tab
2. Select **Auto RCA Pipeline** workflow
3. Click on recent run
4. Expand **Run RCA Agent** step
5. Scroll to see full analysis output

### Using GitHub CLI
```powershell
# List recent runs
gh run list -L 10

# Get specific run details
gh run view <RUN_ID> --log

# Download artifact
gh run download <RUN_ID> -n rca-report

# Cancel running workflow
gh run cancel <RUN_ID>
```

### Using curl/API
```powershell
# Get workflow runs (requires GITHUB_TOKEN)
$headers = @{
    "Authorization" = "token $env:GITHUB_TOKEN"
    "Accept" = "application/vnd.github.v3+json"
}

curl -H $headers `
  https://api.github.com/repos/YOUR_USERNAME/Agent-POC/actions/runs
```

---

## 🔐 Security Setup

### 1. Restrict Branch Pushes
Settings → Branches → Add rule → Require status checks

### 2. Add Secrets (for Slack/Email notifications)
Settings → Secrets and variables → Actions → New repository secret

### 3. Set Workflow Permissions
Settings → Actions → Workflow permissions → "Read and write permissions"

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflow won't run | Ensure `.github/workflows/rca.yml` is in main branch |
| RCA not triggering | Check `if: failure()` condition; previous step must fail |
| Python errors | Update python-version in workflow to match rca code |
| Permission errors | Enable write permissions in Actions settings |
| Artifacts not saving | Verify `rca_output.txt` path is correct |

---

## 🎯 Next Steps

1. **Immediate**: Push to GitHub using Quick Start
2. **Short-term**: Test with real build logs
3. **Medium-term**: Add Slack/Email notifications
4. **Long-term**: Integrate with monitoring systems

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Reference](https://cli.github.com/manual/)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Default Environment Variables](https://docs.github.com/en/actions/learn-github-actions/environment-variables)

---

## ❓ Support

See detailed docs in:
- `QUICK_START.md` - Step-by-step setup
- `INTEGRATION_GUIDE.md` - Advanced customization
- `README.md` - RCA Agent features
