@echo off
REM Quick GitHub Integration Setup Script for Windows

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  RCA Agent - GitHub Integration Setup
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist ".github\workflows\rca.yml" (
    echo Error: This script must be run from the Agent-POC root directory
    pause
    exit /b 1
)

echo.
echo Step 1: Checking git status...
git status

echo.
echo Step 2: Configure git (if needed)
set /p git_user="Enter your GitHub username (or press Enter to skip): "
if not "!git_user!"=="" (
    git config user.name "!git_user!"
    git config user.email "!git_user!@users.noreply.github.com"
    echo Git user configured: !git_user!
)

echo.
echo Step 3: Add all files
git add .
echo Files staged for commit

echo.
echo Step 4: Create initial commit
git commit -m "Initial RCA Agent commit with GitHub Actions integration"

echo.
echo Step 5: Set up remote (if needed)
git remote -v
set /p use_remote="Do you need to add remote? (y/n): "
if /i "!use_remote!"=="y" (
    set /p repo_url="Enter GitHub repository URL (https://github.com/username/repo.git): "
    git remote add origin !repo_url!
    echo Remote added
)

echo.
echo Step 6: Push to GitHub
git branch -M main
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to: https://github.com/YOUR_USERNAME/Agent-POC/actions
echo 2. Click on the "Auto RCA Pipeline" workflow
echo 3. Monitor the run progress
echo 4. Download the RCA report from Artifacts section
echo.
echo Useful GitHub CLI commands:
echo   gh run list                    - List recent workflow runs
echo   gh run view ^<RUN_ID^>         - View specific run details
echo   gh run download ^<RUN_ID^> -n rca-report - Download RCA report
echo.
pause
