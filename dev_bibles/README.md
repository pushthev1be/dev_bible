# Dev Bibles - Your Personal Knowledge Library

A simple, powerful system for capturing and organizing lessons learned across all your projects.

## Philosophy

Every developer has patterns they use, mistakes they repeat, and lessons they learn. This library system captures that knowledge in two layers:

**Layer 1: Master Bible** (`_master/bible.jsonl`)
- YOUR personal patterns across ALL projects
- YOUR recurring mistakes and how to avoid them
- YOUR preferred tech choices and why
- Cross-project wisdom that follows you everywhere

**Layer 2: Project Bibles** (`<project>/bible.jsonl`)
- Project-specific bugs and fixes
- Domain knowledge (crypto, AI, etc.)
- Team conventions
- Project architecture decisions

## Quick Start

### 1. Import your existing projects

```bash
# Discover projects with Bibles
~/dev_bibles/bible-sync --discover

# Import them all
~/dev_bibles/bible-sync --import

# Check status
~/dev_bibles/bible-sync --status
```

### 2. Set up shell aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'source ~/dev_bibles/aliases.sh' >> ~/.bashrc
source ~/.bashrc
```

### 3. Start searching

```bash
# Search all projects
bible auth

# Search specific project
bible wallet pushfundz

# Find all your security mistakes
bible-mistakes security

# Review your personal flaws
bible-personal

# Show stats
bible-stats
```

### 4. Add to your master Bible

```bash
# Interactive add
bible-add-mistake
bible-add-pattern
bible-add-principle

# Or append directly
echo '{"type":"MISTAKE","id":"m.personal.forgot_x","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["personal","..."]}' >> ~/dev_bibles/_master/bible.jsonl
```

## Directory Structure

```
~/dev_bibles/
├── _master/
│   ├── bible.jsonl          # Your personal cross-project lessons
│   └── README.md            # Master Bible docs
├── pushfundz/
│   └── bible.jsonl          # Crypto lending lessons
├── study-ai/
│   └── bible.jsonl          # AI tutoring lessons
├── cortexcoach-ai/
│   └── bible.jsonl          # RAG system lessons
├── bible-search             # Search tool (executable)
├── bible-sync               # Sync tool (executable)
├── aliases.sh               # Shell aliases
└── README.md                # This file
```

## Core Commands

### Searching

```bash
bible <tag>                    # Search all Bibles
bible <tag> <project>          # Search specific project
bible-mistakes <tag>           # Find mistakes only
bible-patterns <tag>           # Find patterns only
bible-personal                 # Show your personal flaws
bible-master <tag>             # Search master Bible only
bible-stats                    # Show stats for all Bibles
bibles                         # List all projects
```

### Syncing

```bash
bible-discover                 # Find projects with Bibles
bible-import                   # Import all project Bibles
bible-import <project>         # Import specific project
bible-status                   # Show sync status
```

### Adding to Master Bible

```bash
bible-add-mistake              # Interactive mistake entry
bible-add-pattern              # Interactive pattern entry
bible-add-principle            # Interactive principle entry
```

## Daily Workflow

### Starting a new feature

```bash
# Before coding: Search for relevant lessons
bible auth
bible-mistakes api
bible wallet pushfundz

# Found a mistake about JWT validation? Great, avoid it!
```

### Fixed a bug in a project

```bash
# Add to project Bible
cd ~/repos/pushfundz
echo '{"type":"MISTAKE","id":"m.wallet_race.2025-10-16",...}' >> dev_bible/bible.jsonl

# Is this a mistake you ALWAYS make? Add to master too
echo '{"type":"MISTAKE","id":"m.personal.race_conditions",...}' >> ~/dev_bibles/_master/bible.jsonl

# Sync to library
bible-import pushfundz
```

### Starting a new project

```bash
# Review your personal mistakes first
bible-personal

# Copy the single-project Bible template
cp -r /home/ubuntu/dev_bible ~/repos/new-project/

# Add your first lesson
cd ~/repos/new-project
make -C dev_bible add-lesson
```

### Weekly review

```bash
# See what you've learned
bible-stats

# Review personal patterns
bible-master personal

# Check which projects need syncing
bible-status
```

## What Goes Where?

### Master Bible (`_master/bible.jsonl`)

✅ Add here:
- "I always forget to validate wallet addresses"
- "My standard auth flow pattern"
- "Why I prefer FastAPI over Flask"
- "I tend to skip error handling in prototypes"

❌ Don't add here:
- "Fixed race condition in pushfundz wallet"
- "Study-AI uses spaced repetition algorithm"
- "Cortexcoach has 3 RAG strategies"

### Project Bibles (`<project>/bible.jsonl`)

✅ Add here:
- "Fixed wallet race condition with SELECT FOR UPDATE"
- "Spaced repetition algorithm implementation"
- "RAG strategy comparison and choice"
- "Team decided on React over Vue"

❌ Don't add here:
- Your personal recurring mistakes
- Generic patterns you use everywhere
- Your general tech preferences

### Rule of thumb:

- **Master**: If you'd want to know this when starting ANY project → Master
- **Project**: If it's specific to this domain/codebase → Project

## Integration with Project Bibles

Each project should have its own `dev_bible/` folder:

```bash
your-project/
├── src/
├── tests/
└── dev_bible/
    ├── bible.jsonl      # Project lessons
    ├── Makefile         # Helper commands
    └── README.md        # Project-specific docs
```

Then sync to your library:

```bash
bible-import your-project
```

Now you can search both:

```bash
# Search just this project
bible auth your-project

# Search across all projects
bible auth

# Search your personal master
bible-master auth
```

## Advanced Usage

### Search with jq

```bash
# Pretty print all personal mistakes
cat ~/dev_bibles/_master/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "[\(.id)] \(.symptom)"'

# Find patterns by tag
cat ~/dev_bibles/pushfundz/bible.jsonl | jq -r 'select(.type=="PATTERN" and (.tags | contains(["crypto"]))) | .name'
```

### Grep across all projects

```bash
# Find every mention of "wallet"
grep -r '"wallet"' ~/dev_bibles/

# Find all auth mistakes
grep -r '"auth"' ~/dev_bibles/ | grep MISTAKE
```

### Export for documentation

```bash
# Generate markdown of all personal mistakes
cat ~/dev_bibles/_master/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "## \(.id)\n\(.symptom)\n"' > MY_MISTAKES.md
```

### Promote project lesson to master

```bash
# Found a lesson in project that applies everywhere?
# Just copy it to master (with a new personal ID)

grep 'm.wallet_validation' ~/dev_bibles/pushfundz/bible.jsonl

# Edit and add to master
echo '{"type":"MISTAKE","id":"m.personal.wallet_validation",...}' >> ~/dev_bibles/_master/bible.jsonl
```

## Setup Checklist

- [ ] Import existing projects: `bible-discover && bible-import`
- [ ] Add aliases to shell: `echo 'source ~/dev_bibles/aliases.sh' >> ~/.bashrc`
- [ ] Add 3-5 personal mistakes to master: `bible-add-mistake`
- [ ] Add 2-3 personal patterns to master: `bible-add-pattern`
- [ ] Test search: `bible-personal`
- [ ] Review before next feature: `bible <your-domain>`

## The Value Proposition

**Week 1:** Import projects, add 5 personal lessons
**Week 2:** Search before coding, save 30 minutes
**Month 1:** 20+ personal lessons, faster onboarding
**Month 3:** Search across projects, discover patterns
**Year 1:** 100+ lessons, irreplaceable personal knowledge base

Your competitive advantage grows with every lesson.

## Tips

1. **Tag with "personal"** for master Bible lessons
2. **Sync weekly** - Don't let projects get out of sync
3. **Search before coding** - 30 seconds can save hours
4. **Review monthly** - See what patterns emerge
5. **Promote wisely** - Move project lessons to master when they're universal
6. **Be honest** - Document your actual flaws, not ideal behavior

## Troubleshooting

**"bible: command not found"**
- Run: `source ~/dev_bibles/aliases.sh`
- Or add to `~/.bashrc`

**"No projects found"**
- Run: `bible-discover` to see what's available
- Add Bible to project: `cp -r /home/ubuntu/dev_bible /path/to/project/`

**"jq not installed"**
- Install: `sudo apt install jq` (Linux) or `brew install jq` (Mac)
- Or use grep directly: `grep '"tag"' bible.jsonl`

**Want to reset?**
- Master: `echo '' > ~/dev_bibles/_master/bible.jsonl`
- Projects: `bible-import` will re-sync from repos

## Learn More

- **Master Bible**: See `_master/README.md`
- **Single-Project Template**: See `/home/ubuntu/dev_bible/`
- **Commands**: Run `bible-help` or `bible --help`

## Quick-Recall Aliases

For quick access to major Bible sections, use the aliases defined in `ALIASES.md` and `index.json`:

```bash
source dev_bibles/aliases.sh
# then run e.g.
bible master
bible ai-platforms
```

---

**Your knowledge compounds. Every lesson written saves time forever.**

Start today. Search before you code. Append after you learn.
