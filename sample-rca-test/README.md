# Sample RCA Test Repository

This repository is a minimal example for testing the RCA reusable workflow from `itsmeteja9/Agent-POC`.

## What it does

- Contains a small Node.js project
- Runs `npm test`
- Fails intentionally to trigger the RCA agent
- Uses the reusable workflow from `itsmeteja9/Agent-POC`

## Setup

1. Create a new GitHub repository, for example `sample-rca-test`
2. Push this folder contents to that repo
3. Make sure `itsmeteja9/Agent-POC` has the reusable workflow available
4. Run the GitHub Actions workflow

## Expected behavior

- `npm install` succeeds
- `npm test` fails
- `logs.txt` is generated
- RCA reusable workflow runs and uploads `rca-report`
