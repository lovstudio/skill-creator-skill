#!/usr/bin/env python3
"""
Initialize a new lovstudio skill scaffold.

Usage:
    python3 init_skill.py <name>
    python3 init_skill.py <name> --paid
    python3 init_skill.py <name> --target dev-skills
    python3 init_skill.py <name> --dev-skills
    python3 init_skill.py <name> --path /custom/path

Creates ~/lovstudio/coding/skills/<name>-skill/ by default.
With --target dev-skills, creates
~/lovstudio/coding/lovstudio-dev-skills/skills/<name>/.

Examples:
    python3 init_skill.py fill-form   → ~/lovstudio/coding/skills/fill-form-skill/
    python3 init_skill.py any2pptx    → ~/lovstudio/coding/skills/any2pptx-skill/
    python3 init_skill.py tanstack-query --target dev-skills
        → ~/lovstudio/coding/lovstudio-dev-skills/skills/tanstack-query/
"""

import sys, argparse, re
from pathlib import Path

SKILL_MD = '''---
name: lovstudio-{name}
description: >
  TODO: What this skill does (1-2 sentences).
  TODO: When to trigger — specific scenarios, file types, user phrases.
  Also trigger when the user mentions "TODO_CN", "TODO_EN".
license: MIT
compatibility: >
  Portable Agent Skills format. TODO: Requires Python 3.8+ and <library>.
  User-specific paths, brand assets, and workspace settings must come from
  explicit CLI flags, environment variables, or the shared user profile.
# Optional: declare required skill-level dependencies by exact SKILL.md
# frontmatter name. Example:
# depends_on:
#   - lovstudio-<other-skill>
metadata:
  author: lovstudio
  version: "0.1.0"
  tags: TODO
---

# {name} — TODO: Short Title

TODO: 1-2 sentence overview.

## User Configuration

This skill must not assume Mark's local workspace, `~/lovstudio`, `/Users/mark`,
or a fixed Claude install path. If user-specific paths or brand settings are
needed, follow `references/user-config.md`.

## When to Use

- TODO: Scenario 1
- TODO: Scenario 2

## Workflow (MANDATORY)

**You MUST follow these steps in order:**

### Step 0: Resolve skill root and user config

- Use `SKILL_DIR` if the environment provides it.
- Otherwise infer the installed skill directory from the current skill context.
- When running scripts manually, set:

```bash
SKILL_DIR="${{SKILL_DIR:-$HOME/.claude/skills/lovstudio-{name}}}"
```

If user-specific fields are missing, ask once and map the answer to CLI flags,
environment variables, or the shared profile described in
`references/user-config.md`.

### Step 1: TODO

```bash
python3 "$SKILL_DIR/scripts/TODO.py" --help
```

### Step 2: Ask the user when needed

**IMPORTANT: Use `AskUserQuestion` to collect options BEFORE running.**

### Step 3: Execute

```bash
python3 "$SKILL_DIR/scripts/TODO.py" --input <path> --output <path>
```

## CLI Reference

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | (required) | TODO |
| `--output` | `output.ext` | TODO |

## Dependencies

```bash
pip install TODO --break-system-packages
```
'''

README_MD = '''# lovstudio-{name}

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

TODO: One-line description.

Part of [lovstudio general skills](https://github.com/lovstudio/general-skills) — by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
git clone https://github.com/lovstudio/{name}-skill "${{CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}}/lovstudio-{name}"
```

Requires: Python 3.8+ and `pip install TODO`

## Configuration

This skill is portable by default. User-specific paths and brand settings should
be provided through CLI flags, environment variables, or:

```bash
${{AGENT_SKILL_PROFILE:-$HOME/.config/agent-skills/profile.json}}
```

See `references/user-config.md`.

## Usage

```bash
SKILL_DIR="${{CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}}/lovstudio-{name}"
python3 "$SKILL_DIR/scripts/TODO.py" --input file.ext --output result.ext
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | (required) | TODO |
| `--output` | `output.ext` | TODO |

## License

MIT
'''

DEV_SKILLS_README_MD = '''# lovstudio-{name}

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

TODO: One-line description.

Part of [lovstudio dev-skills](https://github.com/lovstudio/dev-skills) — by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
npx skills add lovstudio/dev-skills
```

Or through Claude Code plugin marketplace:

```text
/plugin marketplace add lovstudio/dev-skills
/plugin install dev-tools@lovstudio-dev
```

Requires: Python 3.8+ and `pip install TODO`

## Configuration

This skill is portable by default. User-specific paths and brand settings should
be provided through CLI flags, environment variables, or:

```bash
${{AGENT_SKILL_PROFILE:-$HOME/.config/agent-skills/profile.json}}
```

See `references/user-config.md`.

## Usage

```bash
SKILL_DIR="${{CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}}/lovstudio-{name}"
python3 "$SKILL_DIR/scripts/TODO.py" --input file.ext --output result.ext
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | (required) | TODO |
| `--output` | `output.ext` | TODO |

## License

MIT
'''

GITIGNORE = '''__pycache__/
*.pyc
*.pyo
.DS_Store
.venv/
venv/
node_modules/
.env
.env.local
'''

USER_CONFIG_MD = '''# User Configuration

This skill follows the portable agent skill profile contract. It must not
assume Mark's local workspace, `~/lovstudio`, `/Users/mark`, or private brand
assets.

## Resolution Order

1. Explicit CLI flags.
2. Environment variables.
3. Shared profile JSON.
4. Safe defaults such as the current working directory or `$HOME/Documents`.
5. Ask the user once for missing required fields.

## Shared Profile

Default profile path:

```bash
${{AGENT_SKILL_PROFILE:-$HOME/.config/agent-skills/profile.json}}
```

Example:

```json
{{
  "user": {{
    "name": "Your Name",
    "language": "zh-CN",
    "timezone": "Asia/Shanghai"
  }},
  "workspace": {{
    "root": "$HOME/projects",
    "output_dir": "$HOME/Documents/lovstudio-skill-output"
  }},
  "brand": {{
    "name": "Your Brand",
    "site": "https://example.com",
    "profile": "$HOME/.config/agent-skills/brand.json",
    "design_guide": "$HOME/.config/agent-skills/design-guide.md"
  }}
}}
```

Environment variable overrides:

| Variable | Meaning |
|----------|---------|
| `AGENT_SKILL_PROFILE` | Path to the shared profile JSON |
| `AGENT_SKILL_WORKSPACE_ROOT` | User workspace root |
| `AGENT_SKILL_OUTPUT_DIR` | Default generated output directory |
| `AGENT_SKILL_BRAND_PROFILE` | Brand profile JSON or Markdown |
| `AGENT_SKILL_DESIGN_GUIDE` | Design guide path |

## Implementation Notes

- Scripts should accept explicit paths via CLI flags.
- Missing profile fields should produce actionable errors.
- LovStudio/Mark defaults belong in an optional profile, not in the workflow.
'''


def main():
    ap = argparse.ArgumentParser(description="Initialize a new lovstudio skill")
    ap.add_argument("name", help="Skill short name (no prefix / no -skill suffix)")
    ap.add_argument(
        "--target",
        choices=("repo", "dev-skills"),
        default="repo",
        help="Scaffold target: independent per-skill repo (default) or lovstudio/dev-skills bundle",
    )
    ap.add_argument(
        "--dev-skills",
        action="store_true",
        help="Shortcut for --target dev-skills",
    )
    ap.add_argument(
        "--path",
        default="",
        help=(
            "Custom base directory. For --target repo, defaults to ~/lovstudio/coding/skills/. "
            "For --target dev-skills, defaults to ~/lovstudio/coding/lovstudio-dev-skills/skills/."
        ),
    )
    ap.add_argument("--paid", action="store_true", help="Mark as paid in hints (actual paid flag lives in lovstudio-general-skills/skills.yaml)")
    args = ap.parse_args()

    # Normalize: strip common prefixes / suffix users might paste
    name = args.name
    for pfx in ("lovstudio:", "lovstudio-"):
        if name.startswith(pfx):
            name = name[len(pfx):]
    if name.endswith("-skill"):
        name = name[: -len("-skill")]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        print(
            "ERROR: skill name must use lowercase letters, numbers, and single hyphens only",
            file=sys.stderr,
        )
        sys.exit(1)

    target = "dev-skills" if args.dev_skills else args.target
    if target == "dev-skills" and args.paid:
        print("ERROR: --target dev-skills is only for free Meta / Dev Tools skills. Use the default independent repo target for paid skills.", file=sys.stderr)
        sys.exit(1)

    if args.path:
        base = Path(args.path)
    elif target == "dev-skills":
        base = Path.home() / "lovstudio" / "coding" / "lovstudio-dev-skills" / "skills"
    else:
        base = Path.home() / "lovstudio" / "coding" / "skills"
    base.mkdir(parents=True, exist_ok=True)
    skill_dir = base / name if target == "dev-skills" else base / f"{name}-skill"

    if skill_dir.exists():
        print(f"ERROR: {skill_dir} already exists", file=sys.stderr)
        sys.exit(1)

    skill_dir.mkdir()
    (skill_dir / "scripts").mkdir()
    (skill_dir / "references").mkdir()

    (skill_dir / "SKILL.md").write_text(SKILL_MD.format(name=name))
    readme = DEV_SKILLS_README_MD if target == "dev-skills" else README_MD
    (skill_dir / "README.md").write_text(readme.format(name=name))
    (skill_dir / "references" / "user-config.md").write_text(USER_CONFIG_MD.format(name=name))
    (skill_dir / ".gitignore").write_text(GITIGNORE)

    print(f"✓ Created {skill_dir}/")
    print(f"  SKILL.md      — AI-facing frontmatter + workflow")
    print(f"  README.md     — human-facing GitHub docs")
    print(f"  references/   — user configuration contract")
    print(f"  scripts/      — add Python CLI scripts here")
    print(f"  .gitignore")
    print()
    print("Next steps:")
    if target == "dev-skills":
        dev_root = skill_dir.parents[1]
        print(f"  1. cd {dev_root}")
        print(f"  2. Implement skills/{name}/ and fill TODO placeholders in SKILL.md / README.md")
        print("  3. Add to skills.yaml:")
        print(f"       - name: {name}")
        print("         repo: lovstudio/dev-skills")
        print(f"         skill_path: skills/{name}")
        print("         paid: false")
        print('         category: "Dev Tools"  # or "Meta"')
        print("         version: \"0.1.0\"")
        print(f"  4. Add ./skills/{name} to .claude-plugin/marketplace.json under meta or dev-tools")
        print("  5. python3 scripts/render-readme.py")
        print("  6. Symlink:")
        print(f"       ln -s {skill_dir} ~/.agents/skills/lovstudio-{name}")
        print(f"       ln -s ../../.agents/skills/lovstudio-{name} ~/.claude/skills/lovstudio-{name}")
        print(f"  7. git add skills.yaml README.md README.en.md .claude-plugin/marketplace.json skills/{name}")
        print(f"     git commit -m 'add: {name} skill'")
    else:
        print(f"  1. cd {skill_dir}")
        print(f"  2. Implement scripts/ and fill TODO placeholders in SKILL.md / README.md")
        print(f"  3. git init && git add -A && git commit -m 'feat: initial release of {name} skill'")
        visibility = "--private" if args.paid else "--public"
        print(f"  4. gh repo create lovstudio/{name}-skill {visibility} --source=. --push")
        print(f"  5. Symlink:")
        print(f"       ln -s {skill_dir} ~/.agents/skills/lovstudio-{name}")
        print(f"       ln -s ../../.agents/skills/lovstudio-{name} ~/.claude/skills/lovstudio-{name}")
        paid_flag = "true" if args.paid else "false"
        print(f"  6. Register in ~/lovstudio/coding/lovstudio-general-skills/skills.yaml (paid: {paid_flag})")


if __name__ == "__main__":
    main()
