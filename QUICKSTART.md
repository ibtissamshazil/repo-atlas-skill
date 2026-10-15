# Repo Atlas quickstart

Repo Atlas creates or updates a self-contained HTML architecture and handover guide for the repository open in your coding agent.

## Prerequisites

- Git
- Codex or Claude Code
- Python 3 to run the optional validation command

## Install for Codex

### Windows PowerShell

```powershell
git clone https://github.com/ibtissamshazil/repo-atlas-skill.git "$env:USERPROFILE\.codex\skills\repo-atlas"
```

### macOS or Linux

```bash
git clone https://github.com/ibtissamshazil/repo-atlas-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/repo-atlas"
```

Restart Codex after installation. Open the repository you want to document and enter this in the Codex chat, not in the shell:

```text
$repo-atlas Analyze this repository deeply and create a complete HTML architecture and handover guide.
```

To choose the output and scope explicitly:

```text
$repo-atlas Analyze this repository deeply and create docs/documentation.html. Include the production pipeline, clients, hosts, services, databases, decisions, workers and batching, model prompts, human review, persistence, and separate offline workflows. Verify every relationship from source code. Keep connectors clean and add accessible zoom controls to any diagram that cannot remain readable at its default size.
```

## Install for Claude Code

### Windows PowerShell

```powershell
git clone https://github.com/ibtissamshazil/repo-atlas-skill.git "$env:USERPROFILE\.claude\skills\repo-atlas"
```

### macOS or Linux

```bash
git clone https://github.com/ibtissamshazil/repo-atlas-skill.git "$HOME/.claude/skills/repo-atlas"
```

Restart Claude Code, open the target repository, and enter:

```text
/repo-atlas Analyze this repository deeply and create a complete HTML architecture and handover guide.
```

## Validate a generated document

From the target repository, run one of the following commands.

### Codex installation on Windows

```powershell
python "$env:USERPROFILE\.codex\skills\repo-atlas\scripts\validate_documentation.py" "docs\documentation.html"
```

### Codex installation on macOS or Linux

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/repo-atlas/scripts/validate_documentation.py" "docs/documentation.html"
```

Replace `docs/documentation.html` with the actual generated file when a repository uses a different static or public directory.

## Update the installed skill

### Codex on Windows

```powershell
git -C "$env:USERPROFILE\.codex\skills\repo-atlas" pull --ff-only
```

### Claude Code on Windows

```powershell
git -C "$env:USERPROFILE\.claude\skills\repo-atlas" pull --ff-only
```

For macOS or Linux, use the equivalent installed path shown above.
