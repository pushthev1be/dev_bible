#!/bin/bash
#
#
#

set -e

TARGET_DIR="${1:-.}"
BIBLE_DIR="$TARGET_DIR/dev_bible"

echo "🔖 Initializing Project Bible..."

if [ -d "$BIBLE_DIR" ]; then
    echo "⚠️  Warning: $BIBLE_DIR already exists. Aborting to prevent overwriting."
    exit 1
fi

mkdir -p "$BIBLE_DIR"

cat > "$BIBLE_DIR/bible.jsonl" << 'EOF'
{"type":"PRINCIPLE","id":"p.fail_fast","text":"Validate inputs at API boundaries and fail fast with clear error messages.","tags":["architecture","api"]}
EOF

cat > "$BIBLE_DIR/README.md" << 'EOF'

A simple, append-only knowledge base that captures project lessons in one place.


```bash
grep '"auth"' dev_bible/bible.jsonl | grep MISTAKE

grep '"your-tag"' dev_bible/bible.jsonl | grep PATTERN
```

```bash
echo '{"type":"MISTAKE","id":"m.your_bug.2025-10-16","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}' >> dev_bible/bible.jsonl
```

```bash
make stats          # View statistics
make search TAG=x   # Search by tag
make add-lesson     # Interactive lesson creation
make validate       # Check JSON formatting
```


1. **PRINCIPLE** — Architectural truths
2. **PATTERN** — Reusable solutions
3. **MISTAKE** — Bugs fixed (your "scars")
4. **RUNBOOK** — Step-by-step guides
5. **DECISION** — Why you chose X over Y


1. One idea per line
2. Append only (never edit old lessons)
3. Tag everything

See full documentation: https://github.com/your-org/dev-bible
EOF

cat > "$BIBLE_DIR/Makefile" << 'EOF'
.PHONY: stats search validate help

BIBLE_FILE := bible.jsonl

help:
	@echo "Project Bible Commands:"
	@echo "  make stats            Show bible statistics"
	@echo "  make search TAG=x     Search by tag"
	@echo "  make validate         Check JSON formatting"
	@echo ""

stats:
	@echo "=== Project Bible Stats ==="
	@echo "Total lessons: $$(wc -l < $(BIBLE_FILE))"
	@echo "Mistakes:      $$(grep -c '"type":"MISTAKE"' $(BIBLE_FILE) || echo 0)"
	@echo "Patterns:      $$(grep -c '"type":"PATTERN"' $(BIBLE_FILE) || echo 0)"
	@echo "Principles:    $$(grep -c '"type":"PRINCIPLE"' $(BIBLE_FILE) || echo 0)"
	@echo "Runbooks:      $$(grep -c '"type":"RUNBOOK"' $(BIBLE_FILE) || echo 0)"
	@echo "Decisions:     $$(grep -c '"type":"DECISION"' $(BIBLE_FILE) || echo 0)"

search:
ifndef TAG
	@echo "Usage: make search TAG=yourTag"
else
	@grep '"$(TAG)"' $(BIBLE_FILE) || echo "No lessons found"
endif

validate:
	@cat $(BIBLE_FILE) | while read line; do echo "$$line" | python3 -m json.tool > /dev/null || exit 1; done && echo "✓ Valid JSON"
EOF

echo ""
echo "✅ Project Bible initialized at: $BIBLE_DIR"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Add your first lesson:"
echo "     echo '{\"type\":\"PRINCIPLE\",\"id\":\"p.your_first\",\"text\":\"Your first lesson\",\"tags\":[\"start\"]}' >> dev_bible/bible.jsonl"
echo "  3. Run: make -C dev_bible stats"
echo ""
echo "📖 Happy learning!"
