# All Soccer Predictions — Dev Bible

Single-file overview for the project; detailed references included below.

## Project Snapshot
- Status: Production-ready MVP (queue + worker + auto-refresh UI)
- Cloud queue: Upstash Redis (TLS, rediss://)
- Modes: Queue mode (app + worker) or dev-sync (app only with `DEV_ANALYZE_SYNC=1`)

## Quick Start
- App: `npm run dev`
- Worker: `npm run worker` (queue mode)
- Dev-sync (no Redis/worker): set `DEV_ANALYZE_SYNC=1`, run `npm run dev`
- Test Redis/BullMQ: `node test-upstash.js`

## Key Docs (in this folder)
- FIXES_LOG.md — full changelog and fixes
- UPSTASH_SETUP.md — cloud Redis setup and troubleshooting
- LESSONS_OVERVIEW.md — concise lessons and next steps
- README.md — project overview

## Lessons (highlights)
- Use TLS (`tls: {}`) for Upstash `rediss://` URLs.
- Graceful Redis handling: lazy connect, stop retry spam, null-guard queue ops.
- Dev-sync fallback keeps local dev unblocked when Redis/worker unavailable.
- Auto-refresh detail pages for better UX while jobs complete.
- Zod validation + TypeScript guards to avoid runtime errors.
- Cookie override applied → npm audit: 0 vulnerabilities.

## Runbook
- Production-style: start app + worker with `REDIS_URL=rediss://...`.
- Dev-only: `DEV_ANALYZE_SYNC=1` to skip queue/worker.
- Check queue stats: worker logs; API `/api/admin/queue-stats` (if enabled).
- Health: create prediction → expect Pending → Processing → Completed with feedback.

## Fix Log Summary
See FIXES_LOG.md for detailed entries. Recent highlights:
- Upstash Redis + TLS, worker queue operational
- Dev-sync fallback for queue failures
- Auto-refresh on prediction details
- TypeScript fixes for retry strategies and undefined guards
- Cookie override to clear audit issues

## Next Steps
- Real AI (OpenAI) in `ai-analyzer.ts`
- Live data providers for fixtures/odds
- Sports-themed UI polish (Penpot design system → tokens)
- Replace polling with WebSocket/SSE for status updates
- Deploy app + worker with Upstash env vars
