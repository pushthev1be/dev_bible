# Quick Start - 2 Minutes to Your Personal Knowledge Library

## What You Have

A two-layer knowledge system:
- **Master Bible** - Your personal flaws, patterns, decisions (cross-project)
- **Project Bibles** - Specific lessons from each project

## Install (30 seconds)

```bash
# 1. Add aliases to your shell
echo 'source ~/dev_bibles/aliases.sh' >> ~/.bashrc
source ~/.bashrc

# 2. Import your existing projects
bible-discover
bible-import

# 3. Done! Test it
bible-stats
```

## Daily Use (Two Commands)

### Before coding:
```bash
bible <your-topic>              # Search all projects
bible-personal                  # Check your recurring mistakes
```

### After learning:
```bash
# In project: add to project Bible
echo '{"type":"MISTAKE",...}' >> dev_bible/bible.jsonl

# Personal flaw? Add to master Bible
bible-add-mistake
```

## Essential Commands

```bash
bible <tag>                # Search everything
bible-personal             # Your flaws & patterns
bible-stats               # See all your knowledge
bible-import              # Sync projects to library
bible-help                # Full command list
```

## Your First Steps

**1. Review your personal patterns:**
```bash
bible-personal
```

**2. Add one personal mistake:**
```bash
bible-add-mistake
# Example: "I always forget to validate wallet addresses"
```

**3. Search before your next feature:**
```bash
bible <your-feature-topic>
# Example: bible auth, bible wallet, bible api
```

**4. After fixing a bug, capture it:**
```bash
# If project-specific:
cd ~/repos/your-project
echo '{"type":"MISTAKE","id":"m.bug_name.2025-10-16","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}' >> dev_bible/bible.jsonl
bible-import your-project

# If you ALWAYS make this mistake:
bible-add-mistake
```

## File Locations

- **Master Bible**: `~/dev_bibles/_master/bible.jsonl`
- **Project Bibles**: `~/dev_bibles/<project>/bible.jsonl`
- **Project Source**: `~/repos/<project>/dev_bible/bible.jsonl`

## Adding a Bible to New Project

```bash
cp -r /home/ubuntu/dev_bible ~/repos/your-new-project/
cd ~/repos/your-new-project
make -C dev_bible add-lesson
```

Then sync:
```bash
bible-import your-new-project
```

## Understanding the Flow

```
┌─────────────────────────────────────────────────┐
│  Master Bible (~/_master/bible.jsonl)           │
│  • Your personal patterns                       │
│  • Mistakes you repeat                          │
│  • Cross-project wisdom                         │
└─────────────────────────────────────────────────┘
                        ▲
                        │
                    Promote when
                   applies everywhere
                        │
┌─────────────────────────────────────────────────┐
│  Project Bibles (~/repos/*/dev_bible/)          │
│  • Project-specific bugs                        │
│  • Domain knowledge                             │
│  • Team decisions                               │
└─────────────────────────────────────────────────┘
                        │
                  bible-import
                        ▼
┌─────────────────────────────────────────────────┐
│  Library (~/dev_bibles/*/bible.jsonl)          │
│  • Searchable copies                            │
│  • Cross-project queries                        │
│  • Historical record                            │
└─────────────────────────────────────────────────┘
```

## Common Workflows

### Scenario 1: Starting a feature
```bash
bible <feature-domain>    # Search for relevant lessons
bible-personal            # Check your blind spots
# Code with knowledge!
```

### Scenario 2: Fixed a bug
```bash
# Add to project
cd ~/repos/project
echo '{"type":"MISTAKE",...}' >> dev_bible/bible.jsonl

# Sync to library
bible-import project

# Is this a YOU problem? Add to master
bible-add-mistake
```

### Scenario 3: New project
```bash
# Copy template
cp -r /home/ubuntu/dev_bible ~/repos/new-project/

# Review your patterns first
bible-personal

# Apply your lessons from day 1!
```

### Scenario 4: Code review
```bash
# Reviewer: "Why did you choose X?"
bible-master personal    # Find your decision

# Reference it in PR comment:
# "See decision d.personal.tech_stack in master Bible"
```

### Scenario 5: Onboarding
```bash
# New dev: "How do we handle auth?"
bible auth project-name

# Shows all auth lessons in that project
```

## Tips for Success

1. **Be honest** - Document your ACTUAL mistakes, not ideal behavior
2. **Tag liberally** - `personal`, `security`, `auth`, `api`, etc.
3. **Search first** - Before every feature, search for lessons
4. **Capture immediately** - Right after fixing, while fresh
5. **Review weekly** - `bible-stats` to see growth
6. **Promote wisely** - Move project lessons to master when universal

## Example Master Bible Entries

```json
{"type":"MISTAKE","id":"m.personal.forgot_cors","symptom":"Deployed frontend can't reach backend","root_cause":"I always forget CORS configuration","fix_steps":["Add to deployment checklist","Test from public URL before launch"],"tags":["personal","deployment","cors"]}

{"type":"PATTERN","id":"pat.personal.api_error_handling","name":"My API error pattern","when":"Any API endpoint","steps":["try/catch at route level","log with context","return {error, message}","don't leak stack traces"],"tags":["personal","api","errors"]}

{"type":"PRINCIPLE","id":"p.personal.test_edge_cases","text":"I tend to only test happy path - force myself to write edge case tests first","tags":["personal","testing"]}

{"type":"DECISION","id":"d.personal.postgres_over_mongo","question":"SQL vs NoSQL default choice","decision":"PostgreSQL","reason":"ACID guarantees, JSON support when needed, mature ecosystem","tags":["personal","database"]}
```

## Getting Value Fast

- **Day 1**: Add 3 personal mistakes you know you make
- **Week 1**: Search before every feature
- **Week 2**: Add project lessons after each bug fix
- **Month 1**: 20+ lessons, measurable time savings
- **Month 3**: Cross-project patterns emerge
- **Year 1**: 100+ lessons, competitive advantage

## Need Help?

```bash
bible-help              # Show all commands
bible --help            # Detailed search help
bible-sync --help       # Sync options
```

Read the docs:
- `~/dev_bibles/README.md` - Full system documentation
- `~/dev_bibles/_master/README.md` - Master Bible guide
- `/home/ubuntu/dev_bible/README.md` - Single-project Bible

---

**The Bible compounds. Every lesson written saves time forever.**

Start now: `bible-personal`
