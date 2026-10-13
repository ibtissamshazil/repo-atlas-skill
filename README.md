# Repo Atlas

A portable Agent Skill that inspects a software repository and creates a self-contained two-tab HTML architecture and handover guide. It uses the shared `SKILL.md` format supported by Codex and Claude Code.

The generated page emphasizes a low-text end-to-end diagram, conventional flowchart shapes, deployment boundaries, workers/batching, data stores, decision rules, review persistence, and separate maps for offline or standalone workflows.

## Install

Copy this entire directory into one of the following locations.

### Codex

- Project: `.codex/skills/repo-atlas/`
- Personal: `~/.codex/skills/repo-atlas/`

Invoke it as `$repo-atlas`, or ask Codex to create an HTML architecture/handover guide for the repository.

### Claude Code

- Project: `.claude/skills/repo-atlas/`
- Personal: `~/.claude/skills/repo-atlas/`

Invoke it as `/repo-atlas`, or describe a matching documentation request and let Claude load it automatically.

Restart the agent session after installing a project or personal skill if it is not discovered immediately.

## Package contents

```text
repo-atlas-skill/
|-- SKILL.md
|-- agents/openai.yaml
|-- assets/documentation-template.html
|-- references/diagram-conventions.md
|-- references/review-checklist.md
`-- scripts/
    |-- inventory_repo.py
    `-- validate_documentation.py
```

The helper scripts use only the Python standard library. `inventory_repo.py` is read-only and prints configuration names rather than values.

## Test the package

```bash
python scripts/inventory_repo.py --root /path/to/project
python scripts/validate_documentation.py /path/to/project/docs/documentation.html
```

Validate the skill manifest with the skill validator included in your Codex installation, or any validator implementing the Agent Skills standard.

Official references: [OpenAI Skills](https://developers.openai.com/plugins/concepts/skills), [Claude Code Skills](https://code.claude.com/docs/en/skills), and [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).
