# Project Bible Usage Guide

Real-world examples of using the Project Bible in your daily workflow.

## Installation

### Option 1: Copy into existing project
```bash
cp -r /path/to/dev_bible /path/to/your-project/
cd your-project
make -C dev_bible stats
```

### Option 2: Use init script
```bash
cd your-project
/path/to/dev_bible/init-bible.sh .
```

### Option 3: Start fresh
```bash
mkdir -p dev_bible
touch dev_bible/bible.jsonl
# Copy Makefile, README, and validate.py as needed
```

## Real-World Workflows

### Scenario 1: Starting a new feature

You're about to add a new payment processing endpoint.

```bash
# BEFORE coding: Check for relevant lessons
grep '"payment"' dev_bible/bible.jsonl
grep '"api"' dev_bible/bible.jsonl | grep RUNBOOK
grep '"security"' dev_bible/bible.jsonl | grep MISTAKE

# Found a MISTAKE about validating external API responses
# Found a PATTERN about retry logic
# Use them in your implementation!
```

### Scenario 2: Just fixed a bug

You spent 2 hours debugging a race condition in the wallet system.

```bash
# AFTER fixing: Capture what you learned
echo '{"type":"MISTAKE","id":"m.wallet_race.2025-10-16","symptom":"Users could withdraw more than balance","root_cause":"No transaction isolation on balance check","fix_steps":["wrap in DB transaction","use SELECT FOR UPDATE","add concurrency tests"],"tags":["wallet","database","concurrency"]}' >> dev_bible/bible.jsonl

# Verify it's valid
make -C dev_bible validate

# Check your stats
make -C dev_bible stats
```

### Scenario 3: Code review

Reviewer asks: "Why did you choose Redis over Memcached?"

```bash
# Search for the decision
grep '"cache"' dev_bible/bible.jsonl | grep DECISION

# Found it! Reference the decision ID in your PR comment
# "See decision d.cache_redis.2025-09 in dev_bible/bible.jsonl"
```

### Scenario 4: Onboarding new developer

New dev asks: "How do we deploy to production?"

```bash
# Show them the runbook
grep '"deploy"' dev_bible/bible.jsonl | grep RUNBOOK

# Or search for the specific runbook
grep 'rb.deploy_prod' dev_bible/bible.jsonl
```

### Scenario 5: Sprint planning

Team is planning to add file uploads. Check what you've learned:

```bash
# Search for file-related lessons
grep '"files"' dev_bible/bible.jsonl

# Found a MISTAKE about MIME type validation
# Found a DECISION about cloud storage
# Use these to inform your implementation plan!
```

## Advanced Usage

### Using jq for prettier output

```bash
# Show all mistakes with their fix steps
cat dev_bible/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "[\(.id)]\n  Symptom: \(.symptom)\n  Fix: \(.fix_steps | join(", "))\n"'

# List all patterns by name
cat dev_bible/bible.jsonl | jq -r 'select(.type=="PATTERN") | "• \(.name) (\(.id))"'

# Find lessons added this month
cat dev_bible/bible.jsonl | jq -r 'select(.id | contains("2025-10")) | "\(.type): \(.id)"'
```

### Integration with git hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate bible before commit
if [ -f dev_bible/bible.jsonl ]; then
    python3 dev_bible/validate.py dev_bible/bible.jsonl || exit 1
fi
```

### CI/CD integration

Add to your CI pipeline (GitHub Actions example):

```yaml
- name: Validate Project Bible
  run: |
    if [ -f dev_bible/bible.jsonl ]; then
      python3 dev_bible/validate.py dev_bible/bible.jsonl
    fi
```

### PR template

Add to `.github/pull_request_template.md`:

````markdown
## Changes
<!-- Describe your changes -->

## Project Bible Update
If this PR fixes a bug or adds a pattern, add a lesson:

```json
{"type":"MISTAKE","id":"m.<slug>.<date>","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}
```
````

## Teaching Your AI Assistant

Add this to your project's README or `.cursorrules`:

```
## Project Bible Usage

Before implementing features:
1. Search dev_bible/bible.jsonl for relevant MISTAKES and PATTERNS
2. Use: grep '"tag"' dev_bible/bible.jsonl

After implementing features:
1. Append lessons learned to dev_bible/bible.jsonl
2. Format: {"type":"...", "id":"...", ...}
3. Validate: make -C dev_bible validate
```

## Common Patterns

### Adding a lesson quickly
```bash
# Set up an alias
alias bible-add='echo "ID: "; read id; echo "Text: "; read text; echo "Tags (comma-sep): "; read tags; echo "{\"type\":\"PRINCIPLE\",\"id\":\"$id\",\"text\":\"$text\",\"tags\":[\"${tags//,/\",\"}\"]}" >> dev_bible/bible.jsonl'

# Then just run
bible-add
```

### Searching multiple tags
```bash
# Find lessons with BOTH auth AND security
grep '"auth"' dev_bible/bible.jsonl | grep '"security"'

# Find lessons with auth OR security
grep -E '"(auth|security)"' dev_bible/bible.jsonl
```

### Exporting for documentation
```bash
# Generate markdown doc of all mistakes
cat dev_bible/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "### \(.id)\n**Symptom:** \(.symptom)\n**Root Cause:** \(.root_cause)\n**Fix Steps:**\n\(.fix_steps | map("- " + .) | join("\n"))\n"' > MISTAKES.md
```

## Anti-Patterns (Don't Do This)

❌ **Don't edit old lessons** — Append a new version instead
❌ **Don't write essays** — Keep lessons short and scannable
❌ **Don't skip tags** — Tags make lessons findable
❌ **Don't commit without validating** — Run `make validate` first
❌ **Don't use it as a TODO list** — It's for lessons learned, not tasks

## Maintenance

### Monthly review
```bash
# See what you learned this month
cat dev_bible/bible.jsonl | jq -r 'select(.id | contains("2025-10")) | "\(.type): \(.id)"'

# Count lessons by type
make -C dev_bible stats
```

### Yearly cleanup
```bash
# Check for duplicate IDs (validator catches this)
make -C dev_bible validate

# Look for lessons that might need v2 updates
grep '\.v1"' dev_bible/bible.jsonl
```

## Tips

1. **Start small** — One lesson is better than none
2. **Be consistent** — Add lessons right after fixing bugs
3. **Tag liberally** — More tags = easier searches
4. **Share lessons** — Reference Bible IDs in PR comments
5. **Review regularly** — Skim the Bible before sprint planning

## Getting Value Immediately

Week 1: Add 1-2 mistakes you've already fixed
Week 2: Add the patterns you're using right now  
Week 3: Document key architectural decisions
Week 4: Search the Bible before starting new features

By month 2, you'll wonder how you lived without it.
