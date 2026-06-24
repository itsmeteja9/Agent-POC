# Quick Reference: Checking RCA Agent on GitHub

## 🚀 Fastest Way (30 seconds)

```powershell
# 1. Go to Actions tab
# https://github.com/YOUR_USERNAME/Agent-POC/actions

# 2. Click latest "Auto RCA Pipeline" run

# 3. Expand "Run RCA Agent" step → See results

# Done! ✅
```

---

## 📋 Using GitHub CLI (Recommended)

### Install GitHub CLI
```powershell
# Check if installed
gh --version

# If not: https://cli.github.com/
```

### Most Useful Commands

| Command | What It Does |
|---------|------------|
| `gh run list -L 5` | Show last 5 workflow runs |
| `gh run view <RUN_ID>` | Show run summary |
| `gh run view <RUN_ID> --log` | Show all logs |
| `gh run download <RUN_ID> -n rca-report` | Download RCA report |
| `gh run cancel <RUN_ID>` | Cancel running workflow |

### Complete Verification (Copy & Paste)
```powershell
# Step 1: List recent runs
Write-Host "=== Recent Runs ===" -ForegroundColor Green
gh run list -L 5

# Step 2: Get latest run ID (copy from output)
$runId = Read-Host "Enter RUN_ID"

# Step 3: View status
Write-Host "`n=== Run Status ===" -ForegroundColor Green
gh run view $runId

# Step 4: View RCA analysis
Write-Host "`n=== RCA Analysis ===" -ForegroundColor Green
gh run view $runId --log | Select-String -A 20 "RCA ANALYSIS"

# Step 5: Download report
Write-Host "`n=== Downloading Report ===" -ForegroundColor Green
gh run download $runId -n rca-report

# Step 6: View report
Write-Host "`n=== Report Content ===" -ForegroundColor Green
Get-Content rca-report/rca_output.txt | ConvertFrom-Json | Format-List
```

---

## 🎯 What to Look For

### ✅ Success Indicators
- [ ] Workflow shows **green checkmark** ✅
- [ ] All steps completed successfully
- [ ] "Run RCA Agent" step shows analysis output
- [ ] JSON includes: root_cause, impact, confidence, category, recommended_fix
- [ ] Artifact "rca-report" is available

### ❌ Failure Indicators
- [ ] Workflow shows **red X** ❌
- [ ] Step says "FAILED"
- [ ] Error messages in logs
- [ ] Missing artifact
- [ ] No RCA analysis output

### Expected JSON Output
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

## 🔧 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Workflow doesn't run | Enable Actions in Settings |
| Python error | Check Python version in rca.yml |
| RCA fails | Test locally: `python rca/run_rca.py` |
| No artifacts | Check if rca_output.txt was created |
| Workflow times out | Increase timeout value in workflow |

---

## 📍 Direct Links

Replace `YOUR_USERNAME` with your actual GitHub username:

```
🔗 Actions Tab:
https://github.com/YOUR_USERNAME/Agent-POC/actions

🔗 Latest Run:
https://github.com/YOUR_USERNAME/Agent-POC/actions/runs/LATEST

🔗 Workflow File:
https://github.com/YOUR_USERNAME/Agent-POC/blob/main/.github/workflows/rca.yml

🔗 RCA Engine:
https://github.com/YOUR_USERNAME/Agent-POC/blob/main/rca/rca_engine.py
```

---

## 🖥️ Step-by-Step: GitHub UI Method

### Method 1: Check in Browser (Easiest)

1. Open: `https://github.com/YOUR_USERNAME/Agent-POC`
2. Click **Actions** tab
3. Click **Auto RCA Pipeline** workflow
4. Click latest run
5. Expand **Run RCA Agent** step
6. Scroll down → See JSON analysis
7. Click **Artifacts** → Download `rca-report`

### Method 2: GitHub CLI (Fastest)

1. Open terminal in your project
2. Run: `gh run list -L 1`
3. Copy the RUN_ID
4. Run: `gh run view <RUN_ID> --log`
5. Scroll through logs to find RCA analysis
6. Download: `gh run download <RUN_ID> -n rca-report`

### Method 3: Direct URL (Quickest)

1. Go to: `https://github.com/YOUR_USERNAME/Agent-POC/actions`
2. Click the run you want
3. Expand steps to view logs

---

## ⏱️ Typical Timeline

| Action | Time |
|--------|------|
| Push to GitHub | 10 sec |
| Workflow starts | 5-10 sec |
| Workflow runs | 1-2 min |
| Download artifact | 5 sec |
| **Total** | **~2 min** |

---

## 🔐 If Using Private Repository

### Generate GitHub Token
1. Go to: Settings → Developer settings → Personal access tokens
2. Generate new token
3. Select `repo` scope
4. Copy token

### Use Token
```powershell
$env:GITHUB_TOKEN = "ghp_xxx..."
gh run list -L 5
```

---

## 📊 Monitoring Commands

### Watch Workflow Run (Auto-refresh every 10 seconds)
```powershell
while ($true) {
    Clear-Host
    gh run list -L 3
    Start-Sleep -Seconds 10
}
```

### Download Latest Artifact
```powershell
$latest = gh run list -L 1 --json databaseId -q '.[0].databaseId'
gh run download $latest -n rca-report
cat rca-report/rca_output.txt
```

### Get Run Status in JSON
```powershell
gh run list -L 5 --json status,conclusion,name,createdAt | ConvertFrom-Json
```

---

## 💾 Save for Later Reference

### Export Run History
```powershell
gh run list -L 50 --json status,conclusion,createdAt,name > runs.json
```

### Parse and Display
```powershell
$runs = Get-Content runs.json | ConvertFrom-Json
$runs | ForEach-Object {
    Write-Host "$($_.createdAt) | $($_.name) | $($_.conclusion)"
}
```

---

## 📱 Mobile/Browser Only

If you're checking from phone/browser only:

1. Go to: `https://github.com/YOUR_USERNAME/Agent-POC/actions`
2. Tap **Auto RCA Pipeline**
3. Tap latest run
4. Scroll down to see steps
5. Tap **Run RCA Agent** to expand
6. Tap **Artifacts** to download
7. Open `rca_output.txt` in text editor

---

## 🎓 Learning More

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub CLI Reference**: https://cli.github.com/manual/
- **Workflow Syntax**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- **Artifacts Storage**: https://docs.github.com/en/actions/managing-workflow-runs/downloading-workflow-artifacts

---

## 🚨 Emergency Commands

### If Workflow is Stuck
```powershell
gh run list -L 1
gh run cancel <RUN_ID>  # Cancel the run
```

### If You Need to Fix Workflow
```powershell
# Edit locally
code .github/workflows/rca.yml

# Push fix
git add .github/workflows/rca.yml
git commit -m "Fix workflow"
git push origin main

# Workflow will re-run automatically
```

### If You Want to Clear Artifacts
```powershell
# Unfortunately, GitHub doesn't provide CLI for this
# Do it manually in UI:
# Actions → Click run → Click "Delete artifacts"
```

---

**Still need help?** See the full guide in `CHECK_ON_GITHUB.md`
