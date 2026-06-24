# Quick Start: Push RCA Agent to GitHub

## Prerequisites Checklist

- [ ] GitHub account created
- [ ] Git installed on your machine (`git --version`)
- [ ] GitHub repository created (or will create)
- [ ] GitHub CLI installed (optional but recommended) - `gh --version`

## Quick Setup Steps

### Step 1: Verify Project Structure
```powershell
cd c:\Users\parva\Agent-POC
dir

# You should see:
# - .github\ (workflows directory)
# - rca\
# - README.md
# - INTEGRATION_GUIDE.md
```

### Step 2: Initialize Git (if not already done)
```powershell
# Check git status
git status

# If "fatal: not a git repository", run:
git init
```

### Step 3: Configure Git User (First Time Only)
```powershell
# Set your GitHub credentials (global)
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"

# Or just for this project (local)
git config user.name "Your Name"
git config user.email "your.email@github.com"
```

### Step 4: Add and Commit Files
```powershell
# Add all files
git add .

# Commit
git commit -m "Initial RCA Agent with GitHub Actions integration"
```

### Step 5: Create GitHub Repository

**Option A: Using GitHub Web UI**
1. Go to https://github.com/new
2. Enter repository name: `Agent-POC`
3. Add description: "Root Cause Analysis Agent for CI/CD pipelines"
4. Choose Public/Private
5. Click "Create repository"

**Option B: Using GitHub CLI**
```powershell
# Create public repository
gh repo create Agent-POC --public --source=. --remote=origin --push

# Or create private repository
gh repo create Agent-POC --private --source=. --remote=origin --push
```

### Step 6: Add Remote and Push (if using Web UI)
```powershell
# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/Agent-POC.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 7: Verify Workflow on GitHub

1. Go to: `https://github.com/USERNAME/Agent-POC`
2. Click **Actions** tab
3. Select **Auto RCA Pipeline** workflow
4. You should see the workflow running
5. Wait for completion (should take 1-2 minutes)

## View RCA Results

### In GitHub UI
1. Go to Actions tab → Click workflow run
2. Expand **Run RCA Agent** step
3. Scroll down to see RCA analysis output
4. Click **Artifacts** → Download `rca-report`

### Using GitHub CLI
```powershell
# List recent runs
gh run list --workflow=rca.yml

# Get details of specific run (replace RUN_ID)
gh run view <RUN_ID> --log

# Download artifact
gh run download <RUN_ID> -n rca-report
```

## Enable GitHub Actions (if needed)

1. Go to repository **Settings**
2. Click **Actions** → **General**
3. Select "Allow all actions and reusable workflows"
4. Click **Save**

## Configure Branch Protection (Optional)

1. Go to **Settings** → **Branches**
2. Add rule for branch `main`
3. Check "Require status checks to pass"
4. Select "Auto RCA Pipeline" as required check
5. Save changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow not triggering | Check Actions tab enabled; verify `.github/workflows/rca.yml` committed |
| Python version error | Update Python version in `rca.yml` to match your requirements |
| Permission denied | Check repository settings → Actions → Workflow permissions |
| Artifact not found | Verify `rca_output.txt` is created; check disk space |
| Remote already exists | Run `git remote remove origin` then add again |

## Next: Customize for Real Workflows

Replace the simulated failure in `rca.yml` with your actual build commands:

```yaml
- name: Run Tests
  run: pytest tests/
  
- name: Run Build
  run: python setup.py build
  
- name: Run RCA on Failure
  if: failure()
  run: python rca/run_rca.py
```

## Support

- GitHub Docs: https://docs.github.com/en/actions
- GitHub CLI Reference: https://cli.github.com/manual/
- See `INTEGRATION_GUIDE.md` for detailed configuration options
