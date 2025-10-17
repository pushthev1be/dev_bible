# Project Bible - Complete Knowledge Management System

A simple, powerful system for capturing and organizing lessons learned across all your projects.

## 📦 What's Included

This repository contains two complete systems:

### 1. Single-Project Bible (`/` root files)
The template you copy into individual projects:
- `bible.jsonl` - Example lessons (17 included)
- `Makefile` - Helper commands (stats, search, add, validate)
- `validate.py` - CI-ready JSON validator
- Complete documentation (README, CHEATSHEET, USAGE_GUIDE, etc.)

**Use this:** Copy these files into any project's `dev_bible/` folder

### 2. Multi-Project Library (`/dev_bibles/`)
Your personal cross-project knowledge system:
- `_master/` - Your personal patterns, flaws, decisions
- `<project>/` - Imported lessons from each project
- `bible-search` - Search across all projects
- `bible-sync` - Import and manage projects
- `aliases.sh` - Shell commands for daily use

**Use this:** Install once in `~/dev_bibles/` to search all projects

## 🚀 Quick Start

### For a Single Project

```bash
# Copy template into your project
cp -r /path/to/this/repo/* /path/to/your-project/dev_bible/

# Add a lesson
cd your-project
make -C dev_bible add-lesson

# View stats
make -C dev_bible stats
```

### For Multi-Project Library

```bash
# Install the library
cp -r /path/to/this/repo/dev_bibles ~/

# Set up aliases
echo 'source ~/dev_bibles/aliases.sh' >> ~/.bashrc
source ~/.bashrc

# Import your projects
bible-discover
bible-import

# Start searching
bible-stats
bible-personal
bible <your-topic>
```

## 📚 Documentation

**Start Here:**
- `dev_bibles/COMPLETE_SYSTEM.txt` - Full system overview
- `dev_bibles/QUICKSTART.md` - 2-minute setup guide
- **`AI_LEARNING_PLATFORMS.md`** - 185 lessons from real AI projects ⭐ NEW

**Single-Project Bible:**
- `README.md` - Project Bible documentation
- `CHEATSHEET.md` - Quick reference
- `USAGE_GUIDE.md` - Real-world workflows
- `EXAMPLE_SESSION.md` - Day-in-the-life example

**Multi-Project Library:**
- `dev_bibles/README.md` - Library system guide
- `dev_bibles/_master/README.md` - Master Bible philosophy

**Automation Tools:**
- `tooling/extractors/git2kb.py` - Extract knowledge from Git history
- `tooling/extractors/pr2kb.py` - Extract knowledge from GitHub PRs
- `tooling/validators/validate_kb.py` - Validate knowledge base
- `tooling/validators/validate_cards.py` - Validate PR cards (CI-ready)

## 🎯 The Two Layers

**Layer 1: Project Bibles** (in each project's `dev_bible/`)
- Project-specific bugs and fixes
- Domain knowledge (crypto, AI, etc.)
- Team conventions
- Project decisions

**Layer 2: Master Bible** (in `~/dev_bibles/_master/`)
- YOUR personal patterns across ALL projects
- Mistakes you repeat
- Your tech preferences
- Cross-project wisdom

## 💡 Daily Workflow

**Before coding:**
```bash
bible <topic>              # Search all projects
bible-personal             # Check your recurring mistakes
```

**After learning:**
```bash
# Project lesson
cd ~/repos/project
echo '{"type":"MISTAKE",...}' >> dev_bible/bible.jsonl
bible-import project

# Personal lesson
bible-add-mistake
```

## 🔧 Core Commands

```bash
# Search
bible <tag>                # All projects
bible <tag> <project>      # Specific project
bible-mistakes <tag>       # Mistakes only
bible-personal             # Your flaws

# Manage
bible-stats                # Show stats
bible-import               # Sync projects
bible-discover             # Find projects
bible-help                 # All commands
```

## 📖 The 5 Lesson Types

Every lesson is one JSON line in `bible.jsonl`:

1. **PRINCIPLE** - Architectural truths
2. **PATTERN** - Reusable solutions
3. **MISTAKE** - Bugs fixed (your "scars")
4. **RUNBOOK** - Step-by-step guides
5. **DECISION** - Why you chose X over Y

## 🎓 Learn More

1. Read `dev_bibles/COMPLETE_SYSTEM.txt` for the full overview
2. Check `CHEATSHEET.md` for copy-paste templates
3. Browse `EXAMPLE_SESSION.md` for realistic workflows
4. Review `USAGE_GUIDE.md` for integration tips

## 📊 What's Included

**Root Files (Single-Project Template):**
- 11 documentation files
- 17 example lessons
- Complete tooling (Makefile, validator)
- ~45 KB total

**dev_bibles/ (Multi-Project Library):**
- Master Bible with 4 example personal lessons
- 2 example projects (pushfundz, STUDY-AI)
- Search and sync tools
- Complete documentation
- ~31 KB compressed

## 🌟 Key Features

- ✅ Append-only JSONL (never lose knowledge)
- ✅ Grep-friendly (instant search)
- ✅ Zero dependencies (bash, grep, make)
- ✅ CI/CD ready (validator included)
- ✅ Language agnostic (works for any project)
- ✅ Git-friendly (text files, good diffs)

## 💎 The Value

**Week 1:** Add 5 personal lessons  
**Week 2:** Search before coding, save 30 minutes  
**Month 1:** 20+ lessons, faster debugging  
**Month 3:** Patterns emerge, better decisions  
**Year 1:** 100+ lessons, competitive advantage  

Your knowledge compounds. Every lesson written saves time forever.

## 📝 License

Free to use, modify, and distribute. No attribution needed. Make it yours.

## 🎉 Get Started

1. Clone this repo
2. Copy `dev_bibles/` to `~/dev_bibles/`
3. Copy root files to any project's `dev_bible/` folder
4. Add aliases: `echo 'source ~/dev_bibles/aliases.sh' >> ~/.bashrc`
5. Start: `bible-personal`

---

**Your second brain for software development.**

Search first. Capture always. Knowledge compounds.
