# Master Bible - Your Personal Knowledge Base

This is your cross-project knowledge base. It captures YOUR patterns, YOUR flaws, and YOUR lessons that apply across all projects.

## Philosophy

While each project has its own Bible (`project/dev_bible/bible.jsonl`), this Master Bible captures the knowledge that transcends individual projects:

- **Your recurring mistakes** - "I always forget to validate wallet addresses"
- **Your preferred patterns** - "My standard auth flow"
- **Your tech decisions** - "Why I choose X over Y"
- **Your blind spots** - "I tend to skip error handling when prototyping"

## What Goes Here vs Project Bibles

**Master Bible (_master/bible.jsonl):**
- Personal patterns you use everywhere
- Mistakes you repeat across projects
- Your default tech choices
- Lessons about YOUR workflow

**Project Bibles (project/dev_bible/bible.jsonl):**
- Project-specific bugs and fixes
- Domain-specific patterns (e.g., crypto, AI)
- Project architectural decisions
- Team conventions

## Tag Convention

Add `"personal"` tag to lessons that are about YOU specifically:

```json
{"type":"MISTAKE","id":"m.personal.forgot_cors","symptom":"Deployed without CORS","root_cause":"I always forget CORS config","fix_steps":["Add to deployment checklist"],"tags":["personal","deployment","cors"]}
```

## Usage

**Add a personal lesson:**
```bash
echo '{"type":"MISTAKE","id":"m.personal.your_flaw","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["personal","..."]}' >> ~/dev_bibles/_master/bible.jsonl
```

**Search your personal flaws:**
```bash
grep '"personal"' ~/dev_bibles/_master/bible.jsonl
```

**Review before starting any project:**
```bash
cat ~/dev_bibles/_master/bible.jsonl | jq -r 'select(.type=="MISTAKE") | "[\(.id)] \(.symptom)"'
```

## Syncing with Projects

Use the `bible-sync` command (see main README) to:
1. Copy project-specific lessons FROM projects TO library
2. Review lessons across all projects
3. Promote project lessons to master when they apply everywhere

## Growth Path

**Week 1:** Add 3-5 mistakes you know you repeat
**Month 1:** Add your preferred patterns
**Month 3:** Add decisions about tech stack
**Year 1:** You have a comprehensive personal knowledge base

This becomes your competitive advantage - institutional knowledge that follows you project to project.
