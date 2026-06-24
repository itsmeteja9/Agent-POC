# How to Check Your RCA Agent on GitHub

## 🔍 Overview

Once you push your RCA Agent to GitHub, you can verify it's working in multiple ways:
- Watch workflow execution in real-time
- View detailed logs and analysis
- Download RCA reports
- Check for errors and issues

---

## ✅ Method 1: GitHub Web UI (Easiest)

### Step 1: Navigate to Actions Tab
1. Go to your repository: `https://github.com/YOUR_USERNAME/Agent-POC`
2. Click **Actions** tab at the top
3. You'll see **Auto RCA Pipeline** workflow listed

### Step 2: Monitor Workflow Execution
1. Click on the latest workflow run
2. Watch the yellow/blue progress indicator
3. Wait for it to complete (should take 1-2 minutes)

### Step 3: View RCA Analysis Results

Once the workflow completes:

1. **View in-line logs:**
   - Expand **Run RCA Agent** step
   - Scroll down to see the analysis output
   - You'll see JSON with root_cause, impact, confidence, category, recommended_fix

2. **Download RCA Report:**
   - Click **Artifacts** section
   - Download `rca-report` zip file
   - Extract and view `rca_output.txt`

3. **View Build Summary:**
   - Check the green ✅ or red ❌ indicator
   - See step-by-step status for each action

### Example Output to Look For
```json
{
  "root_cause": "CI/CD pipeline failure due to failing tests",
  "impact": "Build failed -> deployment blocked",
  "confidence": "high",
  "category": "ci/cd",
  "recommended_fix": "Fix failing test cases or rollback code"
}
```

---

## 🖥️ Method 2: GitHub CLI (Fastest for Automation)

### Install GitHub CLI (if needed)
```powershell
# Check if installed
gh --version

# If not, install from:
# https://cli.github.com/
```

### List Recent Workflow Runs
```powershell
# Show last 10 runs
gh run list -L 10

# Output looks like:
# STATUS  TITLE                                WORKFLOW              BRANCH  EVENT  CREATED
# ✓       Auto RCA Pipeline                    rca.yml               main    push   2024-06-24
# ✗       Auto RCA Pipeline                    rca.yml               main    push   2024-06-23
```

### View Specific Run Details
```powershell
# Replace RUN_ID with actual ID from list above
gh run view <RUN_ID>

# Example:
gh run view 9876543210

# This shows:
# - Run status
# - Conclusion (success/failure)
# - Jobs and their statuses
# - Artifacts created
```

### View Detailed Logs
```powershell
# View all logs for a run
gh run view <RUN_ID> --log

# This streams the complete log output to your terminal
# Useful for debugging issues
```

### View Specific Job Logs
```powershell
# View logs from specific job
gh run view <RUN_ID> --log --job=rca-job

# Or view the "Run RCA Agent" step specifically:
gh run view <RUN_ID> --log | grep -A 50 "Run RCA Agent"
```

### Download RCA Report
```powershell
# Download all artifacts
gh run download <RUN_ID>

# Download specific artifact
gh run download <RUN_ID> -n rca-report

# List available artifacts
gh run download <RUN_ID> --dir .

# Extract and view
cd <RUN_ID>
cat rca-report/rca_output.txt
```

---

## 📊 Method 3: API Inspection (Advanced)

### Get All Workflow Runs (JSON)
```powershell
# Using curl
$headers = @{
    "Authorization" = "token $env:GITHUB_TOKEN"
    "Accept" = "application/vnd.github.v3+json"
}

$response = Invoke-WebRequest `
  -Uri "https://api.github.com/repos/YOUR_USERNAME/Agent-POC/actions/runs" `
  -Headers $headers

$response.Content | ConvertFrom-Json | Select-Object -ExpandProperty workflow_runs
```

### Get Specific Run Details
```powershell
$runId = "9876543210"
$response = Invoke-WebRequest `
  -Uri "https://api.github.com/repos/YOUR_USERNAME/Agent-POC/actions/runs/$runId" `
  -Headers $headers

$response.Content | ConvertFrom-Json | Format-List
```

---

## 🔗 Method 4: Direct Links to Check

### Quick Links Template
```
📋 Workflow Runs:
https://github.com/YOUR_USERNAME/Agent-POC/actions

🔍 Latest Run Details:
https://github.com/YOUR_USERNAME/Agent-POC/actions/runs/[RUN_ID]

📦 Artifacts:
https://github.com/YOUR_USERNAME/Agent-POC/actions/runs/[RUN_ID]#artifacts

📝 Workflow File:
https://github.com/YOUR_USERNAME/Agent-POC/blob/main/.github/workflows/rca.yml
```

---

## ✔️ Verification Checklist

Use this checklist to verify your RCA Agent is working correctly:

### Basic Setup
- [ ] Repository is public or accessible to you
- [ ] `.github/workflows/rca.yml` file exists in main branch
- [ ] GitHub Actions is enabled in repository settings
- [ ] Python 3.10 is specified in workflow

### Workflow Execution
- [ ] Workflow triggers on push (check Actions tab)
- [ ] Workflow runs appear in Actions history
- [ ] Workflow completes within 2-3 minutes
- [ ] All steps show ✅ green checkmarks

### RCA Analysis
- [ ] "Run RCA Agent" step completes successfully
- [ ] RCA analysis output is visible in logs
- [ ] JSON output includes all required fields:
  - [ ] `root_cause`
  - [ ] `impact`
  - [ ] `confidence`
  - [ ] `category`
  - [ ] `recommended_fix`

### Artifacts
- [ ] "Upload RCA Artifact" step succeeds
- [ ] `rca-report` artifact appears in Artifacts section
- [ ] `rca_output.txt` can be downloaded
- [ ] Downloaded file contains valid JSON

### Code Quality
- [ ] No Python syntax errors
- [ ] No missing dependencies
- [ ] All imports resolve correctly
- [ ] Log file is being created and read properly

---

## 🐛 Troubleshooting Guide

### Issue: Workflow Doesn't Run
**Symptom:** No workflow appears in Actions tab

**Solutions:**
```powershell
# 1. Check if actions are enabled
# Go to: Settings → Actions → General
# Select "Allow all actions and reusable workflows"

# 2. Verify file is committed
git log --oneline -- .github/workflows/rca.yml

# 3. Check branch name
git branch

# 4. Force push if needed
git push -f origin main
```

### Issue: Workflow Errors
**Symptom:** Red ❌ in Actions, workflow fails

**Solutions:**
```powershell
# View detailed error logs
gh run view <RUN_ID> --log

# Check for Python errors specifically
gh run view <RUN_ID> --log | grep -i "error\|traceback"

# Verify Python version
gh run view <RUN_ID> --log | grep "python"
```

### Issue: RCA Step Fails
**Symptom:** "Run RCA Agent" step shows error

**Solutions:**
```powershell
# Check if logs.txt is being created
gh run view <RUN_ID> --log | grep "logs.txt"

# Verify rca_engine.py exists and has no syntax errors
gh run view <RUN_ID> --log | grep -A 5 "rca_engine"

# Test locally first
cd c:\Users\parva\Agent-POC
python rca/run_rca.py
```

### Issue: Artifacts Not Saved
**Symptom:** Artifacts section is empty

**Solutions:**
```powershell
# Check if upload step ran
gh run view <RUN_ID> --log | grep "Upload RCA"

# Verify rca_output.txt was created
gh run view <RUN_ID> --log | grep "rca_output.txt"

# Check file paths in workflow
cat .github/workflows/rca.yml | grep -A 5 "Upload"
```

### Issue: Wrong Python Version
**Symptom:** Python 3.10 expected but different version used

**Solutions:**
```powershell
# Update workflow file
# In .github/workflows/rca.yml:
# python-version: "3.11"

# Then commit and push
git add .github/workflows/rca.yml
git commit -m "Update Python version"
git push origin main
```

---

## 📈 Advanced Monitoring

### Watch Workflow Status
```powershell
# Create a PowerShell script to monitor runs
while ($true) {
    Clear-Host
    Write-Host "Recent Workflow Runs:" -ForegroundColor Green
    gh run list -L 5
    Write-Host "`nRefreshing in 30 seconds..."
    Start-Sleep -Seconds 30
}
```

### Get Slack Notifications
```powershell
# When workflow completes, get status
$latestRun = gh run list -L 1 --json status,conclusion,createdAt
$latestRun | ConvertFrom-Json
```

### Export Run History
```powershell
# Export recent runs to CSV for analysis
gh run list -L 100 --json status,conclusion,name,createdAt > runs.json

# Convert to CSV
$runs = Get-Content runs.json | ConvertFrom-Json
$runs | Export-Csv -Path runs.csv -NoTypeInformation
```

---

## 🎯 Step-by-Step Verification Process

### Complete Verification Flow

**1. After First Push (1 min)**
```powershell
# Check if workflow triggered
gh run list -L 1
```

**2. Wait for Execution (2 min)**
```powershell
# Monitor workflow status
gh run view <RUN_ID>
```

**3. Verify Results (2 min)**
```powershell
# View full output
gh run view <RUN_ID> --log | tail -50

# Download artifact
gh run download <RUN_ID> -n rca-report
cat rca-report/rca_output.txt
```

**4. Validate Output (1 min)**
```powershell
# Check if JSON is valid
$json = Get-Content rca-report/rca_output.txt | ConvertFrom-Json
$json | Format-Table -AutoSize
```

**5. Check for Errors (1 min)**
```powershell
# Look for any errors or warnings
gh run view <RUN_ID> --log | Select-String -Pattern "error|warning|failed|traceback"
```

---

## 🔄 Continuous Verification

### Set Up Regular Checks
```powershell
# Create a monitoring script
@"
# Monitor RCA Agent Health

while (`$true) {
    `$status = gh run list -L 1 --json status,conclusion | ConvertFrom-Json
    
    if (`$status[0].conclusion -eq 'failure') {
        Write-Host 'ALERT: Last run failed!' -ForegroundColor Red
    } elseif (`$status[0].conclusion -eq 'success') {
        Write-Host 'OK: Last run successful' -ForegroundColor Green
    }
    
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
"@ | Out-File monitor-rca.ps1

# Run it
.\monitor-rca.ps1
```

---

## 📝 Example: Full Verification Session

```powershell
# 1. List recent runs
gh run list -L 5

# 2. Get latest run ID (e.g., 9876543210)
$runId = 9876543210

# 3. View status
gh run view $runId

# 4. Check logs for RCA section
gh run view $runId --log | Select-String -A 30 "RCA ANALYSIS"

# 5. Download report
gh run download $runId -n rca-report

# 6. View results
$json = Get-Content rca-report/rca_output.txt | ConvertFrom-Json
Write-Host "Root Cause: $($json.root_cause)"
Write-Host "Category: $($json.category)"
Write-Host "Fix: $($json.recommended_fix)"
```

---

## 🎓 What to Expect

### Successful Run
```
✅ Checkout code → ✅ Setup Python → ❌ Simulate Failure → ✅ Run RCA Agent → ✅ Upload Artifact
```

### Expected Log Output
```
[Pipeline] Start build
[Pipeline] Running tests
ERROR: Test suite failed: 12 failed, 5 passed
[Pipeline] Build failed
[Pipeline] Deployment aborted

==================================================
   RCA ANALYSIS RESULTS
==================================================

{
  "root_cause": "CI/CD pipeline failure due to failing tests",
  "impact": "Build failed -> deployment blocked",
  "confidence": "high",
  "category": "ci/cd",
  "recommended_fix": "Fix failing test cases or rollback code"
}

==================================================
```

### Artifact File
```
rca-report/
├── rca_output.txt          ← Contains the JSON analysis
```

---

## 💡 Tips & Best Practices

1. **Always check logs first** - Most issues are visible in the step logs
2. **Use GitHub CLI for automation** - Faster than web UI for repeated checks
3. **Save artifacts** - Download reports for record-keeping
4. **Test locally first** - Run `python rca/run_rca.py` locally before pushing
5. **Check branch** - Ensure you're pushing to the correct branch (main)
6. **Monitor regularly** - Set up alerts for failed runs

---

## 📚 Related Documentation

- `README.md` - RCA Agent features
- `QUICK_START.md` - Initial setup guide
- `INTEGRATION_GUIDE.md` - Detailed integration options
- `.github/workflows/rca.yml` - Workflow definition
