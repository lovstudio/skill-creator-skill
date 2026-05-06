# lovstudio-skill-creator

![Version](https://img.shields.io/badge/version-2.3.0-CC785C)

Scaffold new skills for the lovstudio ecosystem. Skills can be created as
**independent GitHub repos** at `lovstudio/{name}-skill` or as bundled entries
inside [`lovstudio/dev-skills`](https://github.com/lovstudio/dev-skills).
New scaffolds use Agent Skills-compatible `lovstudio-<name>` frontmatter and a
portable user configuration layer for workspace, output, and brand settings.

Part of [lovstudio general skills](https://github.com/lovstudio/general-skills) &mdash; by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
git clone https://github.com/lovstudio/skill-creator-skill ~/.claude/skills/lovstudio-skill-creator
```

## What It Does

```
┌────────────────────────────────────────────────────────────┐
│  You: "封装成 wcx skill"                                    │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│  init_skill.py wcx                                          │
│                                                             │
│  ~/lovstudio/coding/skills/wcx-skill/                       │
│  ├── SKILL.md      ← AI reads this                          │
│  ├── README.md     ← Humans read this on GitHub             │
│  ├── .gitignore                                             │
│  ├── references/user-config.md                               │
│  └── scripts/      ← Python CLI scripts                     │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│  Implement → gh repo create lovstudio/wcx-skill --push      │
│           → PR into lovstudio-general-skills/skills.yaml + lovstudio-general-skills/README.md     │
│           → symlink to ~/.claude/skills/lovstudio-wcx       │
└────────────────────────────────────────────────────────────┘

Dev-skills bundle target:

┌────────────────────────────────────────────────────────────┐
│  init_skill.py tanstack-query --target dev-skills           │
│                                                             │
│  ~/lovstudio/coding/lovstudio-dev-skills/skills/tanstack-query/│
│  ├── SKILL.md                                               │
│  ├── README.md                                              │
│  ├── .gitignore                                             │
│  └── scripts/                                               │
│                                                             │
│  Register in dev-skills/skills.yaml with:                   │
│    repo: lovstudio/dev-skills                               │
│    skill_path: skills/tanstack-query                        │
└────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Scaffold
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py wcx

# → ~/lovstudio/coding/skills/wcx-skill/
#     ├── SKILL.md       (TODO placeholders)
#     ├── README.md      (version badge + install stub)
#     ├── .gitignore
#     ├── references/user-config.md
#     └── scripts/
```

```bash
# Scaffold a free Meta / Dev Tools skill into lovstudio/dev-skills
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py tanstack-query --target dev-skills

# → ~/lovstudio/coding/lovstudio-dev-skills/skills/tanstack-query/
```

Then:

1. Implement `scripts/` and fill the TODOs in `SKILL.md` / `README.md`
2. For independent repos: `cd ~/lovstudio/coding/skills/wcx-skill && git init && git add -A && git commit -m "feat: initial release"`
3. For independent repos: `gh repo create lovstudio/wcx-skill --public --source=. --push`
4. For dev-skills: edit `~/lovstudio/coding/lovstudio-dev-skills/skills.yaml`, update `.claude-plugin/marketplace.json`, then run `python3 scripts/render-readme.py`
5. Symlink into `~/.claude/skills/lovstudio-<name>` for local use

## Architecture

The lovstudio skill ecosystem:

| Layer | Location | Purpose |
|-------|----------|---------|
| General skills index | `lovstudio/general-skills` repo & `~/lovstudio/coding/lovstudio-general-skills/` | `skills.yaml` + human README; consumed by agentskills.io & lovstudio.ai/agent |
| Per-skill repo | `lovstudio/{name}-skill` & `~/lovstudio/coding/skills/{name}-skill/` | All skill code + SKILL.md + README.md + CHANGELOG.md |
| Dev skills bundle | `lovstudio/dev-skills` & `~/lovstudio/coding/lovstudio-dev-skills/skills/{name}/` | Free Meta / Dev Tools skills installed together |
| Local Claude Code | `~/.claude/skills/lovstudio-{name}/` | Symlink chain into the per-skill repo |

`paid: true/false` lives **only** in `lovstudio-general-skills/skills.yaml` — never in SKILL.md.

User-specific paths, brand profiles, design guides, and output directories must
come from explicit CLI flags, environment variables, or
`${AGENT_SKILL_PROFILE:-$HOME/.config/agent-skills/profile.json}`.
Reusable skills must not hard-code `/Users/mark`, `~/lovstudio`, or private
LovStudio workspace paths.

## Differences from Official skill-creator

| | Official | Lovstudio |
|--|----------|-----------|
| **README.md** | Explicitly forbidden | **Required** — repos are on GitHub |
| **Frontmatter** | `name` + `description` | + `license`, `compatibility`, optional `depends_on`, `metadata.version`, `tags` |
| **Naming** | Name matches installed skill dir | `lovstudio-<name>` frontmatter / `{name}-skill` source repo / `lovstudio-<name>` installed dir |
| **Scripts** | Any format | Standalone Python CLI with `argparse` |
| **Distribution** | `.skill` package | Independent repo or `lovstudio/dev-skills` bundle |
| **Interactive** | Optional | `AskUserQuestion` mandatory for generation/conversion skills |
| **General catalog** | — | `skills.yaml` + `README.md` in `lovstudio/general-skills` |
| **User config** | Optional | Required when paths, brand, profile, or workspace conventions are user-specific |

## License

MIT
