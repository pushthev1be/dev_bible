# Dev Bibles Aliases Index

This file maps short recall aliases to the major Bible locations and includes 2-3 example lesson IDs for quick reference.

Aliases:

- alias: `bible:master`
  - path: `dev_bibles/_master/bible.jsonl`
  - examples: `p.search_before_code`, `p.document_immediately`, `m.personal.wallet_validation`
  - description: Cross-project personal rules, recurring mistakes, and master patterns.

- alias: `bible:template`
  - path: `./bible.jsonl` (project template)
  - examples: `p.controllers_thin`, `m.auth_bypass.2025-10-16`, `rb.add_endpoint.v1`
  - description: Single-project template and starter lessons.

- alias: `bible:study-ai`
  - path: `dev_bibles/STUDY-AI/bible.jsonl`
  - examples: `pat.spaced_repetition.v1`, `pat.pagination_standard.v1`, `m.sql_injection.2025-10-15`
  - description: Lessons and patterns specific to the STUDY-AI project (tutoring/flashcards).

- alias: `bible:ai-platforms`
  - path: `AI_LEARNING_PLATFORMS.md`
  - examples: `pat.subject_detection`, `pat.parallel_api_generation`, `m.memory_leak.chunking`
  - description: High-level, production-tested AI learning platform patterns and anti-patterns.

- alias: `bible:tooling`
  - path: `tooling/`
  - examples: `tooling/extractors/git2kb.py`, `tooling/validators/validate_kb.py`
  - description: Automation scripts and validators.

- alias: `bible:docs`
  - path: `README.md`, `USAGE_GUIDE.md`, `CHEATSHEET.md`, `INSTALL.md`
  - examples: `CHEATSHEET.md` snippets for quick use
  - description: User-facing documentation and onboarding content.

- alias: `bible:utils`
  - path: `validate.py`, `init-bible.sh`, `Makefile`
  - examples: `validate.py`, `init-bible.sh`
  - description: Operational utilities: validator and bootstrap script.

How to use

- Read the alias index: `cat dev_bibles/ALIASES.md`
- Use the shell helper `aliases.sh` (see next file) for quick commands.
