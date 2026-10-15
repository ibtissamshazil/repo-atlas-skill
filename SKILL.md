---
name: repo-atlas
description: Inspect a software repository and create or update a self-contained HTML architecture and handover guide with low-text process diagrams, deployment boundaries, data stores, decisions, workers, integrations, and operating documentation. Use when a user asks to visualize, simplify, document, onboard, or hand over a codebase as HTML. Do not use for ordinary README edits or implementation work without a documentation deliverable.
---

# Repo Atlas

Create one evidence-grounded HTML file that lets a new maintainer understand the repository quickly, then use the detailed tab to preserve operational depth.

## Ground the document in the repository

1. Read repository instructions such as `AGENTS.md`, `CLAUDE.md`, contribution guides, and the README.
2. Map the tree, manifests, entry points, runtime configuration names, routes, data access, background processes, prompts/models, tests, deployment files, and operator scripts. Run `python <skill-directory>/scripts/inventory_repo.py --root <repo-root>` when Python is available; treat its output as leads, not proof.
3. Trace the primary runtime path through actual callers and callees. Separately trace dashboards, evaluation tools, migrations, diagnostics, backfills, comparisons, and other workflows not invoked by the primary path.
4. Verify every diagram relationship in source or configuration. Mark inferred or externally owned behavior as a boundary or known gap.

Never expose secret values. Read `.env` only when necessary and report only non-secret settings that materially affect architecture. Prefer `.env.example`, configuration classes, and deployment manifests.

## Choose the output location

- Honor a requested path or filename.
- Otherwise update an existing architecture/handover page.
- For a web application with an established static/public directory, use `<static-dir>/documentation.html`.
- For repositories without a web-static convention, use `docs/documentation.html`.
- Do not add a server route merely to serve the file unless the user requested browser routing or the repository already has a clear static-page pattern. If a route is added, add only the minimal route and a concise README link.

## Build the document

Read [references/diagram-conventions.md](references/diagram-conventions.md) before authoring. Use [assets/documentation-template.html](assets/documentation-template.html) as a starting point when the repository has no established visual style.

The default deliverable has two tabs:

1. **Flow diagram:** low-text, scan-friendly architecture and process maps.
2. **Detailed documentation:** repository map, runtime, configuration, data model, APIs, failure behavior, testing, deployment, handover checklist, and verified gaps.

The flow tab should include:

- One end-to-end architecture map with explicit client, application-host, and data/external-service boundaries.
- Conventional shapes: cylinders for databases/storage, diamonds for decisions, process shapes for services and background workers, and directional arrows for reads/writes/calls.
- The persistence and human-review loop when results can be reviewed and saved back.
- Worker/batch behavior when concurrency exists; distinguish queue intake, concurrent tasks, and true provider-side batching.
- Separate compact maps for workflows that are standalone or offline. Never draw an edge into the production path when code does not contain that edge.
- Short labels in shapes. Put implementation detail in click/focus inspectors or the documentation tab.
- Clean connector routing: use continuous arrow paths with visible arrowheads, route edges through dedicated lanes, and never run arrows through nodes, labels, or other arrowheads. Reposition nodes or split the map when crossings cannot be avoided.
- Accessible zoom for large diagrams: when a map cannot remain legible at its normal responsive size, provide zoom in, zoom out, and reset controls plus scroll or pan. Keep controls keyboard accessible and preserve readable labels and arrowheads at every zoom level.

Keep the HTML self-contained: inline CSS, inline SVG, and small inline JavaScript only. Avoid network-loaded fonts, icon libraries, Mermaid CDNs, and build steps. Make it responsive, keyboard accessible, and printable.

## Preserve scope and truth

- Modify only the document and the smallest necessary route/README references.
- Preserve user changes and the repository's design language.
- Describe current behavior before recommendations.
- Do not present planned, configured-but-unused, or standalone code as integrated runtime behavior.
- Distinguish application ownership from downstream clients and external services.
- Show safe configuration names and verified active non-secret values, with the observation date when values may drift.
- If important behavior cannot be established, state the unknown and name the file, owner, or system that must confirm it.

## Validate

Read [references/review-checklist.md](references/review-checklist.md), then:

1. Run `python <skill-directory>/scripts/validate_documentation.py <output-html>`.
2. Render the page in a browser when available. Check desktop, narrow viewport, both tabs, keyboard navigation, clickable nodes, and print layout.
3. Check all anchors, duplicate IDs, SVG labels, arrow continuity, arrowhead visibility, line crossings, node/label overlaps, clipping, contrast, and any zoom controls.
4. If a route or application code changed, run focused tests and any inexpensive project lint/type checks.
5. Review the diff for secrets, invented facts, stale settings, and unrelated edits.

Report the output path, the major flows documented, validation performed, and any unresolved boundaries.
