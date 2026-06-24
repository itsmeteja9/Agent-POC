# Universal Auto-Detect Workflow

**One workflow file for ALL projects.** No customization needed.

---

## How It Works

The workflow automatically detects your project type and runs the appropriate build:

| Project Type | Detection | Auto-Run |
|---|---|---|
| **Node.js** | `package.json` exists | `npm install` → `npm test` |
| **Python** | `requirements.txt` / `setup.py` / `pyproject.toml` | `pip install -r requirements.txt` → `pytest` |
| **Java/Maven** | `pom.xml` exists | `mvn clean test` |
| **Go** | `go.mod` exists | `go test ./...` |
| **Unknown** | None found | Creates generic log message |

---

## Setup (3 Steps)

1. **Copy workflow file to all repos:**
   ```
   .github/workflows/rca.yml
   ```
   Copy content from `WORKFLOW_AUTO_DETECT.yml`

2. **That's it!** No build section to edit.

3. **Push to GitHub** - workflow runs on push/PR

---

## Example: Add to Your Repos

### Repo 1: Node.js Project
- Copy `WORKFLOW_AUTO_DETECT.yml` to `.github/workflows/rca.yml`
- Push
- Workflow auto-detects `package.json` → runs `npm test`

### Repo 2: Python Project
- Copy `WORKFLOW_AUTO_DETECT.yml` to `.github/workflows/rca.yml`
- Push
- Workflow auto-detects `requirements.txt` → runs `pytest`

### Repo 3: Java Project
- Copy `WORKFLOW_AUTO_DETECT.yml` to `.github/workflows/rca.yml`
- Push
- Workflow auto-detects `pom.xml` → runs `mvn test`

**Same workflow file. Different projects. All working.**

---

## What Happens on Failure

1. Build fails (any project type)
2. Workflow captures logs to `logs.txt`
3. RCA Agent runs automatically
4. `rca-report` artifact created with analysis:
   - Root cause
   - Confidence level
   - Recommended fix

---

## Adding More Project Types

Edit `WORKFLOW_AUTO_DETECT.yml` to add Rust, Ruby, .NET, etc.:

```yaml
      - name: Detect Rust
        id: detect_rust
        run: |
          if [ -f "Cargo.toml" ]; then
            echo "detected=true" >> $GITHUB_OUTPUT
          fi

      - name: Run Rust tests
        if: steps.detect_rust.outputs.detected == 'true'
        run: cargo test > logs.txt 2>&1 || true
```

---

## One Workflow. All Repos. No Maintenance.

Copy once. Use everywhere.
