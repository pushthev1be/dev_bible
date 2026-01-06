# Lessons Learned & Best Practices

## What Worked
- Cloud Redis (Upstash) with TLS for BullMQ: zero local deps, reliable queue.
- Dual-mode flow: queue for production, dev-sync fallback for local.
- Auto-refresh on detail pages: user sees status flip without manual reload.
- Clear validation with Zod on API routes.
- Typed guards (undefined checks) to quiet TS and prevent runtime crashes.

## Key Fixes Recap
- Added worker script using `tsx`; guarded `job.id` and `marketData` to remove TS errors.
- Awaited Next.js 16+ `params` in dynamic routes to fix undefined `id`.
- Replaced `cd` with `Set-Location` in PowerShell scripts to satisfy analyzer.
- Added cookie override to reach 0 npm vulnerabilities.
- Graceful Redis handling: stop retry spam, null-guard queue ops, TLS for Upstash.

## Operational Modes
- **Production:** `npm run dev` (app) + `npm run worker` (queue) with `REDIS_URL=rediss://...` (Upstash).
- **Dev Sync:** Set `DEV_ANALYZE_SYNC=1`; run only `npm run dev`; analysis runs synchronously.

## Testing / Verification
- `node test-upstash.js` to validate Redis + BullMQ.
- Hit `/predictions` list and `/predictions/[id]` detail to see auto-refresh and feedback.
- Worker logs should show Processing → Feedback created → Completed.

## Implementation Tips
- Use TLS (`tls: {}`) when `REDIS_URL` is `rediss://`.
- Keep queue creation lazy; fail softly and fallback to dev-sync in development.
- Keep status badges and confidence bars color-coded for instant scan.
- Use 8px spacing grid and consistent radii (4/8/12/16) for UI coherence.

## Next Steps
- Integrate real AI (OpenAI) in `ai-analyzer.ts`.
- Replace sample fixtures/odds with live data providers.
- Finish sports-themed UI polish (Penpot design system → implement tokens).
- Add WebSocket/SSE for real-time status instead of polling.
- Deploy app + worker (Vercel/Railway) with Upstash Redis env vars.
