# Project Bible Cheat Sheet

## The 3 Core Commands

```bash
# 1. Search before coding
grep '"your-tag"' dev_bible/bible.jsonl

# 2. Append after learning
echo '{"type":"...","id":"...","..."}' >> dev_bible/bible.jsonl

# 3. Validate
make validate
```

## The 5 Types (Copy & Paste)

### PRINCIPLE
```json
{"type":"PRINCIPLE","id":"p.your_principle","text":"Your principle text","tags":["tag1","tag2"]}
```

### PATTERN
```json
{"type":"PATTERN","id":"pat.pattern_name.v1","name":"Pattern Name","when":"When to use it","steps":["step1","step2"],"tags":["tag1"]}
```

### MISTAKE
```json
{"type":"MISTAKE","id":"m.bug_name.2025-10-16","symptom":"What went wrong","root_cause":"Why it happened","fix_steps":["how to fix"],"tags":["tag1"]}
```

### RUNBOOK
```json
{"type":"RUNBOOK","id":"rb.task_name.v1","title":"Task Title","steps":["step1","step2","step3"],"tags":["tag1"]}
```

### DECISION
```json
{"type":"DECISION","id":"d.choice_name.2025-10","question":"What did you choose?","decision":"Your choice","reason":"Why","tags":["tag1"]}
```

## Common Searches

```bash
# Find mistakes by tag
grep '"auth"' dev_bible/bible.jsonl | grep MISTAKE

# Find all patterns
grep '"PATTERN"' dev_bible/bible.jsonl

# Search multiple tags
grep '"auth"' dev_bible/bible.jsonl | grep '"security"'

# Recent lessons (this month)
grep '2025-10' dev_bible/bible.jsonl

# Count lessons
wc -l dev_bible/bible.jsonl
```

## Makefile Commands

```bash
make stats              # View counts
make search TAG=auth    # Search by tag
make validate          # Check JSON
make add-lesson        # Interactive add
make help              # Show all commands
```

## ID Naming Convention

```
p.feature_name           # Principle
pat.pattern_name.v1      # Pattern (versioned)
m.bug_name.2025-10-16   # Mistake (dated)
rb.task_name.v1         # Runbook (versioned)
d.choice_name.2025-10   # Decision (dated)
```

## Quick Add Alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias bible='cd $(git rev-parse --show-toplevel 2>/dev/null) && echo "Tag: "; read tag; make -C dev_bible search TAG=$tag'

alias bible-mistake='echo "ID: "; read id; echo "Symptom: "; read symptom; echo "Root: "; read root; echo "Fix: "; read fix; echo "Tags: "; read tags; echo "{\"type\":\"MISTAKE\",\"id\":\"$id\",\"symptom\":\"$symptom\",\"root_cause\":\"$root\",\"fix_steps\":[\"$fix\"],\"tags\":[\"${tags//,/\",\"}\"]}" >> dev_bible/bible.jsonl'
```

## jq Pretty Printing

```bash
# Show all mistakes nicely
cat dev_bible/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "[\(.id)] \(.symptom)"'

# Show patterns with steps
cat dev_bible/bible.jsonl | jq 'select(.type=="PATTERN") | {name, steps}'

# Export to markdown
cat dev_bible/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "## \(.id)\n\(.symptom)\n"'
```

## Daily Workflow

**Morning (Before coding):**
```bash
grep '"feature-area"' dev_bible/bible.jsonl
```

**Evening (After coding):**
```bash
# Add what you learned
echo '{"type":"MISTAKE",...}' >> dev_bible/bible.jsonl
make validate
```

**Weekly:**
```bash
make stats  # See growth
```

## One-Liners

```bash
# Count mistakes this month
grep '"2025-10"' dev_bible/bible.jsonl | grep MISTAKE | wc -l

# Most common tags
cat dev_bible/bible.jsonl | jq -r '.tags[]' | sort | uniq -c | sort -rn | head

# Lessons added today
grep "$(date +%Y-%m-%d)" dev_bible/bible.jsonl

# All lessons with specific ID prefix
grep '"id":"m\.' dev_bible/bible.jsonl  # All mistakes

# Validate and show errors
python3 dev_bible/validate.py dev_bible/bible.jsonl
```

## PR Template Snippet

```markdown
## Bible Update
```json
{"type":"MISTAKE","id":"m.FIXME.2025-10-16","symptom":"FIXME","root_cause":"FIXME","fix_steps":["FIXME"],"tags":["FIXME"]}
```
```

## Git Hook (pre-commit)

```bash
#!/bin/bash
if [ -f dev_bible/bible.jsonl ]; then
    python3 dev_bible/validate.py dev_bible/bible.jsonl || exit 1
fi
```

---

**Remember:** The Bible is append-only. Never edit old lessons—add new versions.

**Golden Rule:** Search before coding, append after learning.
