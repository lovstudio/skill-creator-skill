---
name: lovstudio:skill-creator
category: Meta Skills
tagline: "Scaffold new lovstudio skills with proper structure, SKILL.md + README.md."
description: >
  Create new skills for the lovstudio/skills repo. Fork of the official
  skill-creator with lovstudio conventions: lovstudio: name prefix,
  skills/lovstudio-<name>/ directory structure, mandatory README.md per skill,
  SKILL.md with AskUserQuestion interactive flow, standalone Python CLI scripts,
  CJK text handling, and auto-update of root README + CLAUDE.md.
  Use when the user wants to create a new skill, add a skill to this repo,
  scaffold a skill, or mentions "新建skill", "创建skill", "new skill",
  "add skill", "生成skill".
license: MIT
compatibility: >
  Works within the lovstudio/skills repo. Requires Python 3.8+.
metadata:
  author: lovstudio
  version: "1.2.0"
  tags: skill-creator scaffold generator lovstudio
---

# lovstudio:skill-creator

Create new skills for the lovstudio/skills repo. Based on the official
skill-creator methodology with lovstudio-specific conventions layered on top.

## Lovstudio Conventions (Override Official)

These OVERRIDE the official skill-creator defaults:

| Official | Lovstudio Override |
|----------|-------------------|
| `name` only in frontmatter | `name`, `description`, `license`, `compatibility`, `metadata` |
| No README.md | **README.md is REQUIRED** — this repo is on GitHub, humans read it |
| Any directory structure | `skills/lovstudio-<name>/` under repo root |
| Any naming | Name: `lovstudio:<name>`, Dir: `lovstudio-<name>` |
| Packaging with .skill | Publishing via `npx skills add lovstudio/skills` |

## Skill Creation Process

### Step 0: Choose Target Repo

**IMPORTANT: Use `AskUserQuestion` to ask BEFORE doing anything else.**

Ask which repo the skill should live in:

- **lovstudio/skills** (public) — open source skills, MIT licensed
- **lovstudio/pro-skills** (private) — proprietary/internal skills

This determines:
- Working directory: `~/projects/lovstudio-skills/` vs `~/projects/lovstudio-skills-pro/`
- Install command in README: `npx skills add lovstudio/skills` vs `npx skills add lovstudio/pro-skills`
- PR target repo in Step 5c

Store the choice — it affects Steps 3, 5a, 5b, and 5c.

### Step 1: Understand the Skill

Ask the user what the skill should do. Key questions:

- What problem does it solve? What's the input → output?
- Can you give 2-3 concrete usage examples?
- What would a user say that should trigger this skill?
- Does it need a Python script, or is it pure instructions?

Use `AskUserQuestion` — don't dump all questions at once, start with the most important.

### Step 2: Plan Contents

Analyze each example and identify:

1. **Scripts** — deterministic operations that get rewritten every time → `scripts/`
2. **References** — domain knowledge Claude needs while working → `references/`
3. **Assets** — files used in output (templates, fonts, etc.) → `assets/`

Rules for this repo:
- Python scripts must be **standalone single-file CLIs** with `argparse`
- No package structure, no setup.py, no __init__.py
- CJK text handling is a core concern if the skill deals with documents

### Step 3: Initialize

Run the init script:

```bash
python skills/lovstudio-skill-creator/scripts/init_skill.py <name>
```

This creates:

```
skills/lovstudio-<name>/
├── SKILL.md          # Frontmatter + TODO placeholders
├── README.md         # Human-readable docs for GitHub
└── scripts/          # Empty, ready for implementation
```

The script auto-generates:
- SKILL.md with lovstudio frontmatter template
- README.md with install command, usage, options table stubs
- scripts/ directory

### Step 4: Implement

1. **Write scripts** in `scripts/` — test them by running directly
2. **Write SKILL.md** — instructions for AI assistants:
   - Frontmatter `description` is the trigger mechanism — be comprehensive
   - Body contains workflow steps, CLI reference, field mappings
   - Use `AskUserQuestion` for interactive prompts before running scripts
   - Keep SKILL.md under 500 lines; split to `references/` if longer
3. **Write README.md** — docs for humans on GitHub:
   - Install command: `npx skills add lovstudio/skills --skill lovstudio:<name>`
   - Dependencies
   - Usage examples with code blocks
   - Options/arguments table
   - ASCII diagrams for visual explanation (if applicable)

See `references/templates.md` for SKILL.md and README.md templates.

### Step 5: Register & Publish

After the skill is complete, do ALL of the following:

#### 5a. Update repo indexes

1. **`CLAUDE.md`** — add row to Skills table:
   ```
   | `<name>` | `skills/lovstudio-<name>/scripts/<script>.py` (<lib>) | `pip install <lib>` |
   ```
   For pure-instruction skills (no script): `(pure instructions, no script)`

2. **Root `README.md`** — add row to Available Skills table:
   ```
   | [<name>](skills/lovstudio-<name>/) | One-line description. |
   ```

#### 5b. Symlink for local availability

Create the symlink chain so the skill is immediately usable in Claude Code:

```bash
# 1. Link from skills repo into .agents
ln -s /Users/mark/projects/lovstudio-skills/skills/lovstudio-<name> \
      /Users/mark/.agents/skills/lovstudio-<name>

# 2. Link from .agents into .claude/skills (where Claude Code reads)
ln -s ../../.agents/skills/lovstudio-<name> \
      /Users/mark/.claude/skills/lovstudio-<name>
```

Verify: `ls ~/.claude/skills/lovstudio-<name>/SKILL.md` should resolve.

#### 5c. Commit & create PR

Based on the repo chosen in Step 0:

```bash
# For lovstudio/skills (public):
cd /Users/mark/projects/lovstudio-skills

# For lovstudio/pro-skills (private):
cd /Users/mark/projects/lovstudio-skills-pro
```

Then:

```bash
git checkout -b feat/add-<name>
git add skills/lovstudio-<name>/ CLAUDE.md README.md
git commit -m "feat: add <name> skill — <one-line description>"
git push -u origin HEAD
gh pr create \
  --title "feat: add lovstudio:<name> skill" \
  --body "## Summary
- <what the skill does>
- <key implementation detail>

## Test plan
- [ ] Symlinked and tested in conversation
- [ ] Script runs without errors"
```

If the user declines PR creation, just commit and push to main directly.

### Step 6: Test & Iterate

1. Verify local availability: try invoking `/lovstudio:<name>` in a new conversation
2. Notice struggles → fix SKILL.md or scripts
3. Repeat

## Design Patterns

### Interactive Pre-Execution (MANDATORY for conversion/generation skills)

```markdown
**IMPORTANT: Use `AskUserQuestion` to collect options BEFORE running.**

Use `AskUserQuestion` with the following template:
[options list]

### Mapping User Choices to CLI Args
[table mapping choices to --flags]
```

### Progressive Disclosure

Keep SKILL.md lean. Split to references when:
- Multiple themes/variants → `references/themes.md`
- Complex API docs → `references/api.md`
- Large examples → `references/examples.md`

Reference from SKILL.md: "For theme details, see `references/themes.md`"

### Context-Aware Pre-Fill

For skills that fill or generate content:
1. Check user memory and conversation context first
2. Pre-fill what you can
3. Only ask for fields you truly don't know

## What NOT to Include

- INSTALLATION_GUIDE.md — unnecessary clutter (CHANGELOG.md is auto-managed by skill-optimizer)
- Test files — scripts are tested by running, not with test frameworks
- __pycache__, .pyc, .DS_Store — add to .gitignore
