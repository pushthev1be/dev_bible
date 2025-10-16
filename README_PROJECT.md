# Project Bible

A simple, append-only knowledge base that captures project lessons in one place. Think of it as your project's "scar tissue" and "wisdom library" rolled into one JSONL file.

## Philosophy

Every project accumulates knowledge the hard way: through bugs fixed, patterns discovered, and decisions made. The Project Bible captures that knowledge in a format that's easy to search, easy to grow, and impossible to forget.

## Structure

```
your-project/
└─ dev_bible/
   ├─ bible.jsonl        # one-line lessons, append-only
   ├─ README.md          # this file
   └─ Makefile           # helper commands (optional)
```

## The 5 Lesson Types

Every lesson is a single JSON line in `bible.jsonl`. There are only 5 types:

### 1. PRINCIPLE
Architectural truths that guide your project.

```json
{"type":"PRINCIPLE","id":"p.controllers_thin","text":"Controllers are thin; orchestration lives in services.","tags":["architecture"]}
```

### 2. PATTERN
Reusable solutions to recurring problems.

```json
{"type":"PATTERN","id":"pat.two_phase_delete.v1","name":"Two-phase delete","when":"External asset + local DB","steps":["delete external","verify","delete DB","invalidate cache"],"tags":["consistency"]}
```

### 3. MISTAKE
Bugs you've fixed. Your "scar tissue."

```json
{"type":"MISTAKE","id":"m.auth_bypass.2025-10-16","symptom":"Login bypass via demo path","root_cause":"Fallback token","fix_steps":["require JWT","remove demo fallback"],"tags":["auth","security"]}
```

### 4. RUNBOOK
Step-by-step guides for common tasks.

```json
{"type":"RUNBOOK","id":"rb.add_endpoint.v1","title":"Add endpoint","steps":["add route","service method","tests","update bible"],"tags":["api"]}
```

### 5. DECISION
Why you chose X over Y.

```json
{"type":"DECISION","id":"d.storage_choice.2025-10","question":"Where to store uploads?","decision":"Cloud vendor X","reason":"CDN + lifecycle","tags":["infra"]}
```

## Daily Workflow

### Before you code
Search for relevant lessons to avoid repeating mistakes:

```bash
# Find auth-related mistakes
grep '"auth"' dev_bible/bible.jsonl | grep MISTAKE

# Find patterns for file handling
grep '"files"' dev_bible/bible.jsonl | grep PATTERN

# Find decisions about databases
grep '"database"' dev_bible/bible.jsonl | grep DECISION
```

### After you code
Add what you learned (append one line):

```bash
# Quick add
echo '{"type":"MISTAKE","id":"m.upload_mime.2025-10-16","symptom":"Wrong MIME","root_cause":"Trusted headers","fix_steps":["detect bytes","reject mismatch"],"tags":["files","security"]}' >> dev_bible/bible.jsonl

# Or use the helper (if you have a Makefile)
make add-lesson
```

## The Only 3 Rules

1. **One idea per line** — Keep lessons atomic and searchable
2. **Append only** — Never edit old lessons; add new versions (e.g., `.v2`)
3. **Tag everything** — Liberal tagging makes grep land on target

## ID Conventions

Use prefixes to keep IDs organized:

- `p.*` — Principles (e.g., `p.separation_of_concerns`)
- `pat.*` — Patterns (e.g., `pat.retry_with_backoff.v1`)
- `m.*` — Mistakes (e.g., `m.sql_injection.2025-10-16`)
- `rb.*` — Runbooks (e.g., `rb.deploy_prod.v2`)
- `d.*` — Decisions (e.g., `d.framework_choice.2025-10`)

Add dates (YYYY-MM-DD) or versions (v1, v2) to keep IDs unique.

## Advanced Queries (with jq)

For prettier output:

```bash
# List all mistakes with auth tag
cat dev_bible/bible.jsonl | jq -r 'select(.type=="MISTAKE" and (.tags | contains(["auth"]))) | "\(.id): \(.symptom)"'

# Show all patterns
cat dev_bible/bible.jsonl | jq -r 'select(.type=="PATTERN") | "[\(.id)] \(.name)"'

# Find lessons from October 2025
cat dev_bible/bible.jsonl | jq -r 'select(.id | contains("2025-10")) | "\(.type): \(.id)"'
```

## PR Workflow

Add this to your PR template:

````markdown
## Project Bible Update

If this PR fixes a bug or introduces a pattern:

```json
{"type":"MISTAKE","id":"m.<slug>.<date>","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}
```

Or:

```json
{"type":"PATTERN","id":"pat.<name>.v1","name":"...","when":"...","steps":["..."],"tags":["..."]}
```
````

This creates a habit of capturing knowledge at merge time.

## Optional Enhancements

### 1. Validator
Add CI to enforce that PR lessons are well-formed (check required fields, valid JSON).

### 2. Auto-extraction
Build a tool that scans merged PRs and generates lesson entries automatically.

### 3. Stats Dashboard
Track how your Bible grows over time:

```bash
echo "Total lessons: $(wc -l < dev_bible/bible.jsonl)"
echo "Mistakes: $(grep -c '"MISTAKE"' dev_bible/bible.jsonl)"
echo "Patterns: $(grep -c '"PATTERN"' dev_bible/bible.jsonl)"
```

## Getting Started

1. **Copy this folder** into your project root
2. **Add one lesson** to `bible.jsonl` right now (a mistake you fixed recently)
3. **Search before coding** using grep/jq
4. **Append after solving** anything non-trivial

That's it. The Bible grows with your project.

## Why This Works

- **Low friction** — Appending one line is faster than writing documentation
- **High signal** — Every lesson came from real pain, so every lesson matters
- **Immediate value** — Grep finds answers in milliseconds
- **Cumulative** — Knowledge compounds with every fix, every pattern, every decision
- **Portable** — One JSONL file. Copy it, share it, version it.

## Examples

See the example lessons in `bible.jsonl` to get started. They cover common scenarios across all 5 types.

---

**Remember:** The best knowledge base is the one that actually gets used. Keep it simple, keep it searchable, keep it growing.
