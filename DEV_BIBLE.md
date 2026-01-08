# All Soccer Predictions — Dev Bible

Single-file overview for the project; detailed references included below.

## Project Snapshot
- Status: Production-ready MVP (queue + worker + auto-refresh UI)
- Cloud queue: Upstash Redis (TLS, rediss://)
- Modes: Queue mode (app + worker) or dev-sync (app only with `DEV_ANALYZE_SYNC=1`)

## Quick Start
## Tooling & Scripts
- Web: `npm run dev`
- Worker: `npm run worker`
- Combined: `npm run dev:all` (runs web + worker together)
- Dev-sync (no worker required): `npm run dev:sync`
- Seed mixed statuses: `npm run db:seed-dev`
- Seed + start: `npm run dev:reset`
- Queue metrics: `npm run queue:stats`
- Docker helpers: `npm run dev:up`, `npm run dev:down`, `npm run dev:redis`, `npm run dev:db`

## VS Code Tasks
- Dev: Web — runs the Next dev server
- Dev: Worker — runs the BullMQ worker
- Dev: All — runs both via `dev:all`
- Dev: Start (Docker+All) — brings up Docker then starts Dev: All
- Queue: Stats — prints BullMQ queue metrics
- Docker: Up / Down — manage local services

## Design Tokens (Free, Local)
- Source: `tokens/tokens.json` (soccer/status colors, spacing, radius, typography)
- Importer: `scripts/tokens/import-tokens.ts`
- Generated:
	- CSS vars: `src/styles/tokens.css`
	- TS utils: `src/lib/tokens.ts` (`statusColors`, `soccerColors`)
- Build: `npm run tokens:build`
- Usage: import tokens.css in `src/app/globals.css`; components read vars and utilities.

## Auth Configuration
- Dev login: `CredentialsProvider` (id: `test`) allows quick sign-in by email.
- EmailProvider: conditionally enabled only when `EMAIL_*` env vars are present to avoid 500s in dev.
- Handler: `src/app/api/auth/[...nextauth]/route.ts` uses `authOptions` from `src/lib/auth.ts`.

## Queue & Worker
- Queue: `src/lib/queue.ts` — lazy Redis connect; Upstash TLS via `rediss://` with `tls: {}`.
- Worker: `src/workers/feedback.worker.ts` — sets `processing` → stores feedback → `completed` or `failed`.
- Dev-stall hint: `GET /api/predictions` includes `system.workerHint` when `waiting > 0 && active === 0`.
- Dev-sync mode: `POST /api/predictions` respects `DEV_ANALYZE_SYNC=1` to run `analyzePrediction()` synchronously.

## Data Seeding (Dev)
- Script: `scripts/seed-dev-data.ts` populates a mix of statuses (completed, processing, pending, failed) for realistic UI.
- Commands:
	- `npm run db:seed-dev`
	- `npm run dev:reset` (seed then start dev)

## Troubleshooting
- Next dev lock/port conflict:
	- Stop Node: `Get-Process | Where-Object { $_.ProcessName -like "node" } | Stop-Process -Force`
	- Remove lock: `Remove-Item -Force .next\dev\lock`
	- If needed: `Remove-Item -Recurse -Force .next`
- Upstash Redis:
	- Use `REDIS_URL=rediss://...` and ensure `tls: {}` is set in connection options.
	- Run `npm run worker` and check logs for connection/ready.
- Queue visibility: `npm run queue:stats` (prints waiting/active/completed/failed/delayed).
- NextAuth dev 500s: Ensure email env vars are set or rely on dev Credentials provider; EmailProvider is guarded.

- App: `npm run dev`
- Worker: `npm run worker` (queue mode)
- Dev-sync (no Redis/worker): set `DEV_ANALYZE_SYNC=1`, run `npm run dev`
- Test Redis/BullMQ: `node test-upstash.js`

## Key Docs (in this folder)
- FIXES_LOG.md — full changelog and fixes
- UPSTASH_SETUP.md — cloud Redis setup and troubleshooting
## Command Cheat Sheet
```powershell
# Start dev (web only)
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
