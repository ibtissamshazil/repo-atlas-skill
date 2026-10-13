# Review checklist

## Evidence

- Every service, table, queue, API, and arrow is supported by source, configuration, or clearly labeled inference.
- Current behavior is separated from planned or standalone behavior.
- External ownership and unknown integration contracts are explicit.
- Configuration examples contain no passwords, tokens, connection credentials, private URLs, or raw `.env` values.

## Coverage

- Primary end-to-end runtime and both automatic/manual entry points.
- Clients, host/process boundaries, durable stores, object storage, and external services.
- Decision rules, validation, confidence changes, persistence, review, and failure states.
- Workers, batch size, scheduling/polling, concurrency limits, shutdown, and backpressure when present.
- Standalone dashboards, comparisons, evaluation samples, diagnostics, migrations, backfills, and operator commands.
- Tests, safe smoke checks, deployment/startup order, and known gaps.

## Visual quality

- Flow tab is understandable without reading paragraphs.
- Shapes have consistent semantics and branch labels.
- No obvious overlap, clipping, tiny text, or avoidable edge crossings.
- Mobile/narrow layout scrolls or reflows safely.
- Tabs and diagram nodes work with keyboard input.
- Printed/PDF output remains legible.

## Repository integration

- Output path follows repository conventions.
- Any new route returns the intended file and is hidden from API schema when appropriate.
- README links are accurate and concise.
- No unrelated files, generated caches, secrets, or local absolute paths entered the diff.
- Validation and focused tests pass, or failures are reported with their pre-existing/new status.
