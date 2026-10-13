# Diagram conventions

Use these conventions unless the repository already has a stronger visual system.

## Primary architecture

Organize the end-to-end map into three visible boundaries:

1. **Clients:** browser, CLI, mobile application, operator, downstream consumer.
2. **Application host:** API, services, matcher/orchestrator, workers, schedulers, local inference.
3. **Data and external services:** databases, object storage, queues, third-party APIs, remote models.

Keep the main map to roughly 8–18 objects. If it needs more, move implementation detail into separate process maps.

## Shape semantics

| Meaning | Shape | Typical examples |
|---|---|---|
| Service or operation | Rectangle or rounded rectangle | API, matcher, evidence builder |
| Background/predefined process | Rectangle with double vertical edges | Listener, worker, scheduler |
| Decision or rule boundary | Diamond/rhombus | Eligible?, valid output?, source choice |
| Database or durable storage | Cylinder | MySQL, PostgreSQL, object storage |
| Client or externally owned UI | Screen/card inside client boundary | Browser, downstream product |
| External API | Process block inside external-services boundary | Search provider, payment API |

Do not use a cylinder for an in-memory collection or a diamond for a step with no branch.

## Edges

- Use arrow direction to show control or data movement.
- Visually distinguish reads/calls, model inference, and writes when that improves comprehension.
- Use dashed edges for optional, indirect, inferred, or ownership-boundary relationships, and label why.
- Label branches (`YES`, `NO`, `VALID`, `INVALID`) near the originating decision.
- Avoid line crossings. Route long return paths around the outside of the main process.
- If a downstream integration is not implemented in the repository, label the edge as an unverified contract.

## Text density

- Shape title: usually 1–4 words.
- Optional subtitle: one short line.
- Put ports, tables, thresholds, file paths, and caveats in the inspector or detailed documentation.
- Prefer a small formula or count (`12 rows`, `4 workers`, `3 waves`) over a paragraph.

## Required process distinctions

- Separate HTTP/manual entry from background polling when both exist.
- Show eligibility, parsing, decision validation, and confidence rewriting as different concepts when code treats them separately.
- Distinguish batch intake from concurrency. A batch of 12 with 4 workers is not necessarily one 12-item model request.
- Show human review as a process that reads a stored result and writes verdict/notes back to its durable record.
- Give offline evaluation, comparison dashboards, diagnostics, migrations, and backfills their own maps if they are not called by production runtime.

## HTML interaction

- Use semantic buttons for tabs with `role="tab"`, `aria-controls`, `aria-selected`, and arrow-key support.
- Give the SVG a `<title>` and `<desc>`.
- Make interactive SVG groups keyboard focusable and expose detail outside the SVG in an `aria-live` inspector.
- Keep important meaning available without color.
- Provide horizontal scrolling for wide diagrams and a print stylesheet.
