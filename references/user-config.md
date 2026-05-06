# User Configuration Reference

Use this reference when creating or refactoring skills that currently assume a
specific local machine, workspace, brand, or output path.

## Rule

Reusable skills must not depend on Mark's machine layout. Do not scatter these
values through `SKILL.md`, scripts, or README examples:

- `/Users/mark/...`
- `~/lovstudio/...`
- private LovStudio web, vault, brand, or design-guide paths
- `~/.claude/...` as a required runtime path

## Resolution Order

When a skill needs user-specific settings, resolve them in this order:

1. Explicit CLI flags.
2. Environment variables.
3. Shared user profile JSON.
4. Safe defaults such as the current working directory or `$HOME/Documents`.
5. Ask the user once and tell them which setting is missing.

## Shared Profile

Default profile path:

```bash
${AGENT_SKILL_PROFILE:-$HOME/.config/agent-skills/profile.json}
```

Recommended shape:

```json
{
  "user": {
    "name": "Your Name",
    "language": "zh-CN",
    "timezone": "Asia/Shanghai"
  },
  "workspace": {
    "root": "$HOME/projects",
    "output_dir": "$HOME/Documents/lovstudio-skill-output"
  },
  "brand": {
    "name": "Your Brand",
    "site": "https://example.com",
    "profile": "$HOME/.config/agent-skills/brand.json",
    "design_guide": "$HOME/.config/agent-skills/design-guide.md"
  }
}
```

Environment variable overrides:

| Variable | Meaning |
|----------|---------|
| `AGENT_SKILL_PROFILE` | Shared profile JSON path |
| `AGENT_SKILL_WORKSPACE_ROOT` | Workspace root |
| `AGENT_SKILL_OUTPUT_DIR` | Default output directory |
| `AGENT_SKILL_BRAND_PROFILE` | Brand profile JSON or Markdown |
| `AGENT_SKILL_DESIGN_GUIDE` | Design guide path |

## Refactor Pattern

Replace this:

```markdown
Read `/Users/mark/lovstudio/design/design-guide.md`.
Write output to `/Users/mark/lovstudio/output`.
```

With this:

```markdown
Resolve brand settings from `AGENT_SKILL_DESIGN_GUIDE` or the shared profile.
Resolve output from `--output`, `AGENT_SKILL_OUTPUT_DIR`, or the shared profile.
If neither exists, ask the user once and default to `$HOME/Documents`.
```

## Classification

- `portable`: no local or brand-specific assumptions.
- `config-needed`: reusable, but needs a profile/env layer before public use.
- `lovstudio-defaults`: generic core with optional LovStudio defaults.
- `author-only`: intentionally tied to Mark/LovStudio private workspace.
- `legacy-name`: still uses `lovstudio:<name>` or mismatched directory naming.
