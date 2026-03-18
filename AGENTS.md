# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>         # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>        # Complete work
bd sync              # Sync with git
```

## Development Setup

### Python (Backend)
```bash
cd backend
uv venv                  # Create virtual environment
uv pip install -r requirements.txt  # Install dependencies
uv pip install ruff pre-commit  # Install dev tools
pre-commit install        # Install git hooks
```

### JavaScript (Frontend)
```bash
cd frontend
npm install
```

### Running the App
```bash
# Backend (in one terminal)
cd backend && source .venv/bin/activate && python app.py

# Frontend (in another terminal)
cd frontend && npm start
```

## Code Quality

### Pre-commit Hooks
The project uses pre-commit with ruff for linting and formatting:
```bash
# Run manually
pre-commit run --all-files

# Skip hooks (when needed)
git commit --no-verify -m "message"
```

### Ruff Commands
```bash
# Lint
ruff check backend/

# Format
ruff format backend/
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed):
   ```bash
   ruff check backend/     # Python linting
   ruff format backend/   # Python formatting
   cd frontend && npm run build  # Frontend build
   ```
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

## Issue Workflow

1. Create issue: `bd create "Title" --type task --priority P0`
2. Claim: `bd update <id> --status in_progress`
3. Work on it
4. Commit with descriptive message
5. Close: `bd close <id>`
6. Sync: `bd sync`
7. Push
