# Templates

## SKILL.md Template

```yaml
---
name: lovstudio-<name>
description: >
  <What it does — 1-2 sentences.>
  <When to trigger — specific scenarios, file types, user phrases.>
  Also trigger when the user mentions "<中文触发词>", "<english trigger>".
license: MIT
compatibility: >
  Portable Agent Skills format. Requires Python 3.8+ and <library>.
  User-specific paths, brand assets, and workspace settings must come from
  explicit CLI flags, environment variables, or the shared user profile.
# Optional: declare required skill-level dependencies by exact SKILL.md
# frontmatter name. Example:
# depends_on:
#   - lovstudio-<other-skill>
metadata:
  author: lovstudio
  version: "0.1.0"
  tags: <space-separated tags>
---

# <name> — <Short Title>

<1-2 sentence overview.>

## User Configuration

This skill must not assume Mark's local workspace, `~/lovstudio`,
`/Users/mark`, or a fixed Claude install path. If user-specific paths or brand
settings are needed, follow `references/user-config.md`.

## When to Use

- <Scenario 1>
- <Scenario 2>

## Workflow (MANDATORY)

### Step 0: Resolve skill root and user config

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills/lovstudio-<name>}"
```

If user-specific fields are missing, ask once and map the answer to CLI flags,
environment variables, or the shared profile described in
`references/user-config.md`.

### Step 1: <First action>

```bash
python3 "$SKILL_DIR/scripts/<script>.py" --flag value
```

### Step 2: Ask the user

**Use `AskUserQuestion` to collect options BEFORE running.**

### Step 3: Execute

```bash
python3 "$SKILL_DIR/scripts/<script>.py" --input <path> --output <path>
```

## CLI Reference

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | (required) | ... |
| `--output` | `output.ext` | ... |

## Dependencies

```bash
pip install <library> --break-system-packages
```
```

## README.md Template

```markdown
# lovstudio-<name>

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

<One-line description.>

Part of [lovstudio general skills](https://github.com/lovstudio/general-skills) — by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
git clone https://github.com/lovstudio/<name>-skill "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/lovstudio-<name>"
```

Requires: Python 3.8+ and `pip install <library>`

## Configuration

This skill is portable by default. User-specific paths and brand settings should
be provided through CLI flags, environment variables, or:

```bash
${AGENT_SKILL_PROFILE:-$HOME/.config/agent-skills/profile.json}
```

See `references/user-config.md`.

## Usage

```bash
SKILL_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/lovstudio-<name>"
python3 "$SKILL_DIR/scripts/<script>.py" --input file.ext --output result.ext
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | (required) | ... |
| `--output` | `output.ext` | ... |

## License

MIT
```

## Dev-Skills README Install Block

Use this block instead of the independent `git clone` install when the skill
lives directly in `lovstudio/dev-skills`:

~~~markdown
## Install

```bash
npx skills add lovstudio/dev-skills
```

Or through Claude Code plugin marketplace:

```text
/plugin marketplace add lovstudio/dev-skills
/plugin install dev-tools@lovstudio-dev
```
~~~

## Notes

- Version source of truth: `README.md` badge. `SKILL.md` frontmatter
  `metadata.version` is kept in sync by `skill-optimizer`.
- New skills use Agent Skills-compatible frontmatter names:
  `lovstudio-<name>`. Legacy `lovstudio:<name>` skills should be migrated
  opportunistically, not copied into new templates.
- User-specific paths, workspaces, brand profiles, and design guides must be
  initialized through `references/user-config.md`, environment variables, or
  CLI flags. Do not hard-code `/Users/mark`, `~/lovstudio`, or private
  LovStudio workspace paths in reusable workflow steps.
- Start at `0.1.0`, not `1.0.0` — per repo release conventions (stay in 0.x
  unless explicitly promoted).
- `paid` is **not** in SKILL.md frontmatter. It lives only in
  `~/lovstudio/coding/lovstudio-general-skills/skills.yaml`.
- `depends_on` may appear in SKILL.md frontmatter when a skill requires another
  skill. Use the dependency skill's exact SKILL.md `name`; when registering the
  same relationship in `skills.yaml`, use the catalog skill name.
- Dev-skills entries use `repo: lovstudio/dev-skills` and
  `skill_path: skills/<name>` in `~/lovstudio/coding/lovstudio-dev-skills/skills.yaml`.
