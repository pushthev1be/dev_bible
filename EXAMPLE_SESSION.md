# Example Session: Using Project Bible

A realistic day-in-the-life showing how the Bible fits into your workflow.

---

## Morning: Starting a New Feature

**Context:** You need to add a webhook endpoint that accepts external payment notifications.

### Step 1: Search for relevant knowledge

```bash
$ cd my-project
$ grep '"webhook"' dev_bible/bible.jsonl
# No results - first webhook in this project

$ grep '"api"' dev_bible/bible.jsonl | grep PATTERN
{"type":"PATTERN","id":"pat.pagination_standard.v1",...}
# Found pagination pattern, not relevant

$ grep '"security"' dev_bible/bible.jsonl | grep MISTAKE
{"type":"MISTAKE","id":"m.auth_bypass.2025-10-16",...}
{"type":"MISTAKE","id":"m.sql_injection.2025-10-15",...}
# Good! Reminds me to validate inputs carefully
```

### Step 2: Check if there's a runbook for adding endpoints

```bash
$ grep 'add.*endpoint' dev_bible/bible.jsonl
{"type":"RUNBOOK","id":"rb.add_endpoint.v1","title":"Add new API endpoint",...}

$ cat dev_bible/bible.jsonl | jq -r 'select(.id=="rb.add_endpoint.v1") | .steps[]'
define route in routes file
implement service method with business logic
add input validation
write unit tests
add to API documentation
update bible with any patterns
```

**Perfect!** I have a checklist to follow.

---

## Midday: Hit a Bug

**Context:** Webhook is receiving duplicate events from the payment provider.

### Step 1: Check if this is a known issue

```bash
$ grep '"duplicate"' dev_bible/bible.jsonl
# No results

$ grep '"webhook"' dev_bible/bible.jsonl
# Still nothing - this is new territory

$ grep '"idempotent"' dev_bible/bible.jsonl
# No results
```

### Step 2: Research and fix

After investigation, you discover:
- Payment provider can send duplicate webhooks
- Need idempotency key to dedupe
- Should return 200 even if duplicate (to prevent retries)

### Step 3: Document the lesson

```bash
$ echo '{"type":"PATTERN","id":"pat.webhook_idempotency.v1","name":"Webhook idempotency","when":"External webhooks that may duplicate","steps":["extract idempotency key from payload","check if already processed","return 200 if duplicate","process and store key if new"],"tags":["webhook","reliability","api"]}' >> dev_bible/bible.jsonl

$ make -C dev_bible validate
✓ All lines are valid JSON

$ make -C dev_bible stats
=== Project Bible Stats ===
Total lessons: 18
Patterns:      4  # <-- One more!
```

---

## Afternoon: Code Review

**Context:** Teammate asks why you used Redis for session storage.

### Step 1: Search for the decision

```bash
$ grep '"redis"' dev_bible/bible.jsonl
# No specific Redis entry

$ grep '"session"' dev_bible/bible.jsonl
# Nothing

$ grep '"cache"' dev_bible/bible.jsonl
# Nothing yet
```

### Step 2: Document the decision (should have done this earlier!)

```bash
$ make -C dev_bible add-decision
=== Add DECISION ===
ID (e.g., d.cache_redis.2025-10): d.session_redis.2025-10
Question: Where to store user sessions?
Decision: Redis with 7-day TTL
Reason: Fast lookups, automatic expiry, horizontal scaling support
Tags (comma-separated): sessions,redis,infrastructure

✓ DECISION added to bible.jsonl
```

Now you can reference it: "See decision `d.session_redis.2025-10` in dev_bible/bible.jsonl"

---

## Evening: Found a Security Issue

**Context:** Realized webhook signature wasn't being verified.

### Step 1: Fix it immediately

```bash
# Fix the code...
git add .
git commit -m "fix: verify webhook signatures"
```

### Step 2: Document as a MISTAKE

```bash
$ make -C dev_bible add-mistake
=== Add MISTAKE ===
ID (e.g., m.auth_bypass.2025-10-16): m.webhook_unsigned.2025-10-16
Symptom: Webhooks accepted without signature verification
Root cause: Assumed payment provider was trusted, forgot to check HMAC signature
Fix step 1: Add signature verification middleware
Fix step 2 (optional): Reject requests with invalid signatures
Tags (comma-separated, e.g., auth,security): webhook,security,validation

✓ MISTAKE added to bible.jsonl
```

---

## Before Leaving: Review Your Day

```bash
$ make -C dev_bible stats
=== Project Bible Stats ===
Total lessons: 20
Mistakes:      6  # +1 (webhook signature)
Patterns:      4  # +1 (webhook idempotency)
Principles:    3
Runbooks:      3
Decisions:     4  # +1 (Redis sessions)

# What did I learn today?
$ grep '2025-10-16' dev_bible/bible.jsonl
{"type":"PATTERN","id":"pat.webhook_idempotency.v1",...}
{"type":"MISTAKE","id":"m.webhook_unsigned.2025-10-16",...}
{"type":"DECISION","id":"d.session_redis.2025-10",...}
```

**3 lessons captured.** Next person who works on webhooks will benefit from your hard-won knowledge.

---

## Next Sprint: Onboarding New Developer

**Context:** New dev asks "How do webhooks work here?"

### Instead of explaining everything...

```bash
$ grep '"webhook"' dev_bible/bible.jsonl

# They find:
# - pat.webhook_idempotency.v1 (the pattern to follow)
# - m.webhook_unsigned.2025-10-16 (the mistake to avoid)

# And they implement their webhook correctly on the first try!
```

---

## Month Later: Sprint Planning

**Context:** Planning to add more external integrations.

### Step 1: Review what we've learned

```bash
$ grep '"integration\|webhook\|external"' dev_bible/bible.jsonl

# Team discovers:
# - Idempotency pattern
# - Signature verification requirement
# - Session storage decisions
# - Common mistakes to avoid
```

### Step 2: Estimate more accurately

Because you have documented:
- What went wrong before (MISTAKES)
- What patterns work (PATTERNS)
- Why you made certain choices (DECISIONS)

You can estimate confidently and avoid repeating painful mistakes.

---

## Real Value: 6 Months Later

```bash
$ make -C dev_bible stats
=== Project Bible Stats ===
Total lessons: 87
Mistakes:      28  # All the scars
Patterns:      19  # All the wins
Principles:    12  # Architectural truths
Runbooks:      15  # Step-by-step guides
Decisions:     13  # Context on choices
```

**Every lesson came from real work.** Every lesson saves someone time.

New developers onboard faster. Code reviews reference lesson IDs. Estimates are more accurate. Fewer bugs repeat.

**The Bible compounds.**

---

## Key Takeaways

1. **Search before coding** — 30 seconds of grep can save hours
2. **Capture lessons immediately** — Right after fixing, while it's fresh
3. **Tag liberally** — Make lessons findable
4. **Reference in PRs** — "See pattern pat.xyz.v1"
5. **Review weekly** — See what you learned
6. **Share with team** — Collective knowledge > individual memory

---

## The Habit Loop

**Before coding:**
```bash
grep '"relevant-tag"' dev_bible/bible.jsonl
```

**After learning:**
```bash
echo '{"type":"..."}' >> dev_bible/bible.jsonl
make validate
```

**That's it.** Two commands. Massive long-term value.

---

## Anti-Example: What NOT to Do

❌ Write a lesson but never search the Bible (defeats the purpose)  
❌ Wait until end of sprint to add lessons (you'll forget details)  
❌ Write vague lessons ("Fixed a bug") — be specific!  
❌ Skip tags — makes lessons unfindable  
❌ Edit old lessons instead of adding v2 — breaks append-only principle  
❌ Use as a TODO list — it's for lessons learned, not tasks  
❌ Never validate — catch errors early  

---

**The Bible works best when it becomes second nature:**

See bug → Fix bug → Document lesson → Move on

30 seconds of discipline = hours of value later.
