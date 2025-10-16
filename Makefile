.PHONY: add-lesson add-mistake add-pattern add-principle add-runbook add-decision stats search help

BIBLE_FILE := bible.jsonl

help:
	@echo "Project Bible Helper Commands"
	@echo "=============================="
	@echo ""
	@echo "  make add-lesson       Interactive: add any type of lesson"
	@echo "  make add-mistake      Quick: add a MISTAKE"
	@echo "  make add-pattern      Quick: add a PATTERN"
	@echo "  make add-principle    Quick: add a PRINCIPLE"
	@echo "  make add-runbook      Quick: add a RUNBOOK"
	@echo "  make add-decision     Quick: add a DECISION"
	@echo ""
	@echo "  make stats            Show bible statistics"
	@echo "  make search TAG=auth  Search by tag"
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
	@echo ""

search:
ifndef TAG
	@echo "Usage: make search TAG=yourTag"
	@echo "Example: make search TAG=auth"
else
	@echo "=== Lessons tagged with '$(TAG)' ==="
	@grep '"$(TAG)"' $(BIBLE_FILE) || echo "No lessons found with tag '$(TAG)'"
	@echo ""
endif

validate:
	@echo "Validating bible.jsonl..."
	@cat $(BIBLE_FILE) | while read line; do echo "$$line" | jq empty 2>&1 || exit 1; done && echo "✓ All lines are valid JSON" || echo "✗ Invalid JSON found"

add-lesson:
	@echo "=== Add a New Lesson ==="
	@echo ""
	@echo "Select type:"
	@echo "  1) MISTAKE"
	@echo "  2) PATTERN"
	@echo "  3) PRINCIPLE"
	@echo "  4) RUNBOOK"
	@echo "  5) DECISION"
	@echo ""
	@read -p "Choice [1-5]: " choice; \
	case $$choice in \
		1) $(MAKE) add-mistake ;; \
		2) $(MAKE) add-pattern ;; \
		3) $(MAKE) add-principle ;; \
		4) $(MAKE) add-runbook ;; \
		5) $(MAKE) add-decision ;; \
		*) echo "Invalid choice" ;; \
	esac

add-mistake:
	@echo "=== Add MISTAKE ==="
	@read -p "ID (e.g., m.auth_bypass.2025-10-16): " id; \
	read -p "Symptom: " symptom; \
	read -p "Root cause: " root_cause; \
	read -p "Fix step 1: " step1; \
	read -p "Fix step 2 (optional): " step2; \
	read -p "Tags (comma-separated, e.g., auth,security): " tags; \
	if [ -z "$$step2" ]; then \
		echo "{\"type\":\"MISTAKE\",\"id\":\"$$id\",\"symptom\":\"$$symptom\",\"root_cause\":\"$$root_cause\",\"fix_steps\":[\"$$step1\"],\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	else \
		echo "{\"type\":\"MISTAKE\",\"id\":\"$$id\",\"symptom\":\"$$symptom\",\"root_cause\":\"$$root_cause\",\"fix_steps\":[\"$$step1\",\"$$step2\"],\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	fi; \
	echo "✓ MISTAKE added to $(BIBLE_FILE)"

add-pattern:
	@echo "=== Add PATTERN ==="
	@read -p "ID (e.g., pat.retry_backoff.v1): " id; \
	read -p "Name: " name; \
	read -p "When to use: " when; \
	read -p "Step 1: " step1; \
	read -p "Step 2: " step2; \
	read -p "Step 3 (optional): " step3; \
	read -p "Tags (comma-separated): " tags; \
	if [ -z "$$step3" ]; then \
		echo "{\"type\":\"PATTERN\",\"id\":\"$$id\",\"name\":\"$$name\",\"when\":\"$$when\",\"steps\":[\"$$step1\",\"$$step2\"],\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	else \
		echo "{\"type\":\"PATTERN\",\"id\":\"$$id\",\"name\":\"$$name\",\"when\":\"$$when\",\"steps\":[\"$$step1\",\"$$step2\",\"$$step3\"],\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	fi; \
	echo "✓ PATTERN added to $(BIBLE_FILE)"

add-principle:
	@echo "=== Add PRINCIPLE ==="
	@read -p "ID (e.g., p.controllers_thin): " id; \
	read -p "Principle text: " text; \
	read -p "Tags (comma-separated): " tags; \
	echo "{\"type\":\"PRINCIPLE\",\"id\":\"$$id\",\"text\":\"$$text\",\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	echo "✓ PRINCIPLE added to $(BIBLE_FILE)"

add-runbook:
	@echo "=== Add RUNBOOK ==="
	@read -p "ID (e.g., rb.deploy_prod.v1): " id; \
	read -p "Title: " title; \
	read -p "Step 1: " step1; \
	read -p "Step 2: " step2; \
	read -p "Step 3 (optional): " step3; \
	read -p "Tags (comma-separated): " tags; \
	if [ -z "$$step3" ]; then \
		echo "{\"type\":\"RUNBOOK\",\"id\":\"$$id\",\"title\":\"$$title\",\"steps\":[\"$$step1\",\"$$step2\"],\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	else \
		echo "{\"type\":\"RUNBOOK\",\"id\":\"$$id\",\"title\":\"$$title\",\"steps\":[\"$$step1\",\"$$step2\",\"$$step3\"],\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	fi; \
	echo "✓ RUNBOOK added to $(BIBLE_FILE)"

add-decision:
	@echo "=== Add DECISION ==="
	@read -p "ID (e.g., d.database_choice.2025-10): " id; \
	read -p "Question: " question; \
	read -p "Decision: " decision; \
	read -p "Reason: " reason; \
	read -p "Tags (comma-separated): " tags; \
	echo "{\"type\":\"DECISION\",\"id\":\"$$id\",\"question\":\"$$question\",\"decision\":\"$$decision\",\"reason\":\"$$reason\",\"tags\":[\"$${tags//,/\",\"}\"]}" >> $(BIBLE_FILE); \
	echo "✓ DECISION added to $(BIBLE_FILE)"
