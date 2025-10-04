# 🔄 Auto-Updating Architecture Documentation

## How It Works

The architecture documentation at `docs/architecture-overview.md` is **automatically generated** by scanning the workspace.

## When to Update

Run the updater after:
- Adding new agents to `agents/` directory
- Creating new scripts in `scripts/` directory
- Adding knowledge base entries
- Creating new documentation
- Adding test files

## How to Update

### Option 1: Quick Update (Recommended)
```bash
bash scripts/update_architecture.sh
```

### Option 2: Direct Python
```bash
python scripts/architecture_scanner.py
```

### Option 3: Preview Changes
```bash
python scripts/architecture_scanner.py --print
```

## What Gets Scanned

The scanner automatically detects:

1. **Agents** (`agents/*.yml`)
   - Categorizes by type (orchestrator, acquisition, analysis, etc.)
   - Counts lines of code
   - Detects tools used

2. **Scripts** (`scripts/*.py`)
   - Extracts docstrings
   - Counts lines of code

3. **Knowledge Base**
   - Topics and entry counts
   - Speaker profiles
   - Relationships
   - Raw transcripts

4. **Documentation** (`docs/*.md`)
   - Lists all documentation files

5. **Tests** (`test_*.py`, `*_test.py`)
   - Identifies test coverage

## Architecture Stats

The scanner provides real-time statistics:
- Total agents and their hierarchy
- Knowledge base growth
- Documentation coverage
- Test file count

## Making Changes Stick

After adding new components:

1. **Add Agent**: Place `.yml` file in `agents/`
2. **Add Script**: Place `.py` file in `scripts/`
3. **Run Update**: `bash scripts/update_architecture.sh`
4. **Commit Both**: The new files AND updated `architecture-overview.md`

## Integration with Git

Consider adding to your workflow:
```bash
# After making architecture changes
bash scripts/update_architecture.sh
git add .
git commit -m "feat: Add new agent and update architecture"
```

## Customization

Edit `scripts/architecture_scanner.py` to:
- Change categorization rules
- Add new sections
- Modify the output format
- Include additional directories

---

**Pro Tip**: The architecture document is version-controlled, so you can track how your system grows over time by viewing its git history!