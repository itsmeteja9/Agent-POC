# GitHub Integration Guide for RCA Agent

## Prerequisites

- GitHub repository with Actions enabled
- Python 3.10+ installed in your runners
- Git configured locally

## Step 1: Push Project to GitHub

### Option A: Create New Repository

```bash
# Navigate to your project directory
cd Agent-POC

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial RCA Agent commit"

# Create repository on GitHub UI
# Then add remote and push
git remote add origin https://github.com/YOUR_USERNAME/Agent-POC.git
git branch -M main
git push -u origin main
```

### Option B: Push to Existing Repository

```bash
cd Agent-POC
git add .
git commit -m "Add RCA Agent"
git push origin main
```

## Step 2: GitHub Actions Workflow Configuration

The workflow file is already configured at `.github/workflows/rca.yml`:

### Key Components:

**Trigger Events:**
```yaml
on:
  push:
    branches: [ "main" ]
```
- Runs RCA on every push to main branch
- Add other branches or events as needed

**Environment:**
```yaml
runs-on: ubuntu-latest
```
- Uses Ubuntu latest runner
- Can change to `windows-latest` or `macos-latest` if needed

**Python Setup:**
```yaml
- name: ✅ Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: "3.10"
```
- Ensures Python 3.10 is available

**Log Capture & RCA Execution:**
```yaml
- name: 🚀 Run RCA Agent
  if: failure()
  run: python rca/run_rca.py | tee rca_output.txt
```
- Only runs if previous steps fail
- Captures output to `rca_output.txt`

**Artifact Upload:**
```yaml
- name: 📦 Upload RCA Artifact
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: rca-report
    path: rca_output.txt
```
- Stores RCA report as artifact for 30 days

## Step 3: Customize for Your Workflows

### Use with Multiple Workflows

Create separate workflow files for different pipelines:

**`.github/workflows/build.yml`** - Your main build workflow
```yaml
name: Build & Test

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install -r requirements.txt
      - run: pytest
      
  # Call RCA workflow on failure
  rca-on-failure:
    needs: build
    if: failure()
    uses: ./.github/workflows/rca.yml
```

### Use a central reusable RCA workflow

If you have many repos, keep the RCA logic in one central repo and call it from each project.

**In your central `Agent-POC` repo:**
```yaml
# .github/workflows/rca-reusable.yml
name: RCA Reusable Workflow

on:
  workflow_call:
    inputs:
      log_file:
        description: "Path to the log file to analyze"
        required: false
        default: "logs.txt"
        type: string
      artifact_name:
        description: "Artifact name for RCA report"
        required: false
        default: "rca-report"
        type: string
      python_version:
        description: "Python version to use"
        required: false
        default: "3.10"
        type: string

jobs:
  rca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ inputs.python_version }}
      - name: Run RCA analysis
        run: |
          python rca/run_rca.py --log-file "${{ inputs.log_file }}" | tee rca_output.txt
      - name: Upload RCA report
        uses: actions/upload-artifact@v4
        with:
          name: ${{ inputs.artifact_name }}
          path: rca_output.txt
          retention-days: 30
```

**In each repo that uses the RCA agent:**
```yaml
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ > logs.txt 2>&1

  rca:
    needs: build
    if: failure()
    uses: your-github-username/Agent-POC/.github/workflows/rca-reusable.yml@main
    with:
      tool_repo: your-github-username/Agent-POC
      log_file: logs.txt
      artifact_name: rca-report
```

> The caller repo does not need a local `rca/` directory if using the central reusable RCA workflow. The reusable workflow checks out the RCA tool from the central repo specified by `tool_repo`.

### Capture Real Build Logs

Replace the simulated failure in `rca.yml` with actual logs:

```yaml
- name: 🚀 Run RCA Agent
  if: failure()
  run: |
    # Capture logs from previous failed step
    python rca/run_rca.py
  
- name: 📦 Upload RCA Artifact
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: rca-report
    path: rca_output.txt
```

## Step 4: View RCA Results

### In GitHub Actions UI:

1. Go to repository → **Actions** tab
2. Click on the workflow run
3. Expand **Run RCA Agent** step to see output
4. Download RCA report from **Artifacts** section

### Access Artifacts:

```bash
# List artifacts for a run
gh run list --workflow=rca.yml

# Download specific artifact
gh run download <RUN_ID> -n rca-report
```

## Step 5: Enable Notifications (Optional)

### Email Notifications

Settings → Notifications → GitHub Actions

### Slack Integration

Add to workflow:

```yaml
- name: 💬 Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "RCA Analysis Completed",
        "attachments": [
          {
            "text": "Check artifact for detailed report"
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Step 6: Security Best Practices

### Set GitHub Secrets (if using notifications):

1. Go to Repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `SLACK_WEBHOOK_URL` (if using Slack)
4. Add any other credentials needed

### Code Review Requirements:

1. Go to Settings → Branch protection rules
2. Require status checks to pass (including RCA)
3. Dismiss stale reviews when new commits pushed

## Step 7: Monitor and Maintain

### Check Workflow Runs:

```bash
# List recent workflow runs
gh run list

# View logs of specific run
gh run view <RUN_ID> --log

# Check workflow syntax
git ls-files '.github/workflows/*.yml' | xargs -I {} yamllint {}
```

### Update Python Version (if needed):

Edit `.github/workflows/rca.yml`:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: "3.11"  # Update to newer version
```

## Troubleshooting

### Issue: Workflow not triggering
- **Solution**: Check branch protection rules, ensure `.github/workflows/` is committed

### Issue: RCA Agent errors
- **Solution**: Check Python version compatibility, verify all files are committed

### Issue: Artifacts not uploading
- **Solution**: Verify `rca_output.txt` is created, check disk space limits

### Issue: Workflow permission errors
- **Solution**: Go to Settings → Actions → Workflow permissions → Enable "Read and write permissions"

## Next Steps

1. **Commit & Push**: Push all files to GitHub
2. **Test**: Trigger workflow manually or on next push
3. **Monitor**: Check Actions tab for results
4. **Iterate**: Refine RCA patterns based on real logs
5. **Expand**: Integrate RCA into other workflows

## Useful Commands

```bash
# Validate workflow syntax locally
act -l

# Run workflow locally (requires act)
act -j rca-job

# Check last 10 workflow runs
gh run list -L 10

# Cancel running workflow
gh run cancel <RUN_ID>

# Get detailed run info
gh run view <RUN_ID> --json status,conclusion,startedAt,updatedAt
```
