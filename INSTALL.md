# Project Bible Installation Guide

Three ways to get started, pick what works for you.

## Option 1: Full Package (Recommended)

Copy the complete dev_bible folder into your project.

```bash
# From your project root
cp -r /path/to/dev_bible ./

# Verify it works
make -C dev_bible stats

# Commit it
git add dev_bible/
git commit -m "Add Project Bible"
```

**You get:** All examples, full docs, complete tooling.

---

## Option 2: Bootstrap with Init Script

Use the init script to create a minimal setup.

```bash
# From your project root
/path/to/dev_bible/init-bible.sh .

# Add your first lesson
make -C dev_bible add-lesson

# Commit it
git add dev_bible/
git commit -m "Initialize Project Bible"
```

**You get:** Clean slate with starter docs.

---

## Option 3: Manual Setup (Minimalist)

Create it yourself in 60 seconds.

```bash
# Create the structure
mkdir -p dev_bible
cd dev_bible

# Create the file
touch bible.jsonl

# Add your first lesson
echo '{"type":"PRINCIPLE","id":"p.start","text":"Always capture lessons learned","tags":["meta"]}' >> bible.jsonl

# Verify
cat bible.jsonl | python3 -m json.tool
```

**You get:** Just the essentials, customize as needed.

---

## Post-Installation

### 1. Clear examples (if you used Option 1)
```bash
echo '' > dev_bible/bible.jsonl
```

### 2. Add your first real lesson
```bash
# Think of a bug you fixed recently
make -C dev_bible add-mistake

# Or just append directly
echo '{"type":"MISTAKE","id":"m.first_bug.2025-10-16","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}' >> dev_bible/bible.jsonl
```

### 3. Verify it works
```bash
make -C dev_bible stats
make -C dev_bible validate
```

### 4. Add to .gitignore (if needed)
Most people commit the Bible, but if you want it local-only:
```bash
echo "dev_bible/bible.jsonl" >> .gitignore
```

---

## Integration Setup

### Git Hook (Optional but recommended)

Validate on commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash
if [ -f dev_bible/bible.jsonl ]; then
    python3 dev_bible/validate.py dev_bible/bible.jsonl || exit 1
fi

# Make it executable
chmod +x .git/hooks/pre-commit
```

### PR Template (Optional)

Add to `.github/pull_request_template.md`:

````markdown
## Changes
<!-- Your changes here -->

## Project Bible
Did you learn something? Add a lesson:

```json
{"type":"MISTAKE","id":"m.<name>.<date>","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}
```
````

### CI Pipeline (Optional)

GitHub Actions example (`.github/workflows/validate-bible.yml`):

```yaml
name: Validate Bible
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate Project Bible
        run: |
          if [ -f dev_bible/bible.jsonl ]; then
            python3 dev_bible/validate.py dev_bible/bible.jsonl
          fi
```

---

## Configuration

### Customize for your team

**Change the location:**
```bash
# Put it anywhere
mkdir -p docs/knowledge
mv dev_bible docs/knowledge/
```

**Change the filename:**
```bash
# Edit dev_bible/Makefile
BIBLE_FILE := lessons.jsonl
```

**Add custom tags:**
Just use them! Tags are free-form. Common ones:
- `security`, `performance`, `ux`, `api`, `database`
- Your feature names: `payments`, `auth`, `notifications`
- Your tech stack: `react`, `python`, `postgres`, `aws`

---

## Teach Your AI Assistant

Add this to your project docs or `.cursorrules`:

```
## Project Bible Usage

Before coding:
- Search: grep '"relevant-tag"' dev_bible/bible.jsonl
- Check for MISTAKES and PATTERNS in your area

After coding:
- Append lessons learned: echo '{"type":"..."}' >> dev_bible/bible.jsonl
- Validate: make -C dev_bible validate
- Keep lessons short, tag liberally
```

---

## Troubleshooting

**Makefile not working?**
- Install make: `sudo apt install make` (Linux) or use Homebrew (Mac)
- Or just use direct commands from CHEATSHEET.md

**Validation failing?**
- Check JSON syntax: `cat bible.jsonl | python3 -m json.tool`
- Look for duplicate IDs: `cat bible.jsonl | jq -r .id | sort | uniq -d`

**Can't find lessons?**
- Check your tags: `cat bible.jsonl | jq -r .tags[]`
- Use broader search: `grep '"keyword"' bible.jsonl`

**Too many files?**
Keep only: `bible.jsonl`, `README.md`, `Makefile`
Delete: `USAGE_GUIDE.md`, `CHEATSHEET.md`, `init-bible.sh`, `INSTALL.md`

---

## Next Steps

1. Read [README.md](README.md) for the philosophy and structure
2. Check [CHEATSHEET.md](CHEATSHEET.md) for daily commands
3. Browse [USAGE_GUIDE.md](USAGE_GUIDE.md) for real-world examples
4. Add your first lesson: `make -C dev_bible add-lesson`
5. Search before you code: `make -C dev_bible search TAG=yourTag`

---

**That's it!** You now have a knowledge base that grows with your project.

The more you use it, the more valuable it becomes. Start today with just one lesson.
