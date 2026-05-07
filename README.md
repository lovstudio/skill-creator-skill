# lovstudio-skill-creator

![Version](https://img.shields.io/badge/version-2.7.0-CC785C)

Scaffold new skills for the lovstudio ecosystem. Skills can be created as
**independent GitHub repos** at `lovstudio/{name}-skill` or as bundled entries
inside [`lovstudio/dev-skills`](https://github.com/lovstudio/dev-skills).
New scaffolds use Agent Skills-compatible `lovstudio-<name>` frontmatter and a
portable user configuration layer for workspace, output, and brand settings.

Part of [lovstudio general skills](https://github.com/lovstudio/general-skills) &mdash; by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
git clone https://github.com/lovstudio/skill-creator-skill "${LOVSTUDIO_SKILLS_INSTALL_DIR:?Set LOVSTUDIO_SKILLS_INSTALL_DIR}/lovstudio-skill-creator"
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
│  <configured repos root>/wcx-skill/                         │
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
│           → install or symlink as lovstudio-wcx             │
└────────────────────────────────────────────────────────────┘

Dev-skills bundle target:

┌────────────────────────────────────────────────────────────┐
│  init_skill.py tanstack-query --target dev-skills           │
│                                                             │
│  <configured dev-skills root>/tanstack-query/               │
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
python3 "$SKILL_DIR/scripts/init_skill.py" wcx

# → <configured repos root>/wcx-skill/
#     ├── SKILL.md       (TODO placeholders)
#     ├── README.md      (version badge + install stub)
#     ├── .gitignore
#     ├── references/user-config.md
#     └── scripts/
```

```bash
# Scaffold a free Meta / Dev Tools skill into lovstudio/dev-skills
python3 "$SKILL_DIR/scripts/init_skill.py" tanstack-query --target dev-skills

# → <configured dev-skills root>/tanstack-query/
```

Then:

1. Implement `scripts/` and fill the TODOs in `SKILL.md` / `README.md`
2. For independent repos: `cd <configured repos root>/wcx-skill && git init && git add -A && git commit -m "feat: initial release"`
3. For independent repos: `gh repo create lovstudio/wcx-skill --public --source=. --push`
4. For dev-skills: edit the configured `lovstudio-dev-skills/skills.yaml`, update `.claude-plugin/marketplace.json`, then run `python3 scripts/render-readme.py`
5. Install or symlink into your agent skills directory as `lovstudio-<name>`

## Architecture

The lovstudio skill ecosystem:

| Layer | Location | Purpose |
|-------|----------|---------|
| General skills index | `lovstudio/general-skills` repo & configured checkout | `skills.yaml` + human README; consumed by agentskills.io & lovstudio.ai/agent |
| Per-skill repo | `lovstudio/{name}-skill` & configured repos root | All skill code + SKILL.md + README.md + CHANGELOG.md |
| Dev skills bundle | `lovstudio/dev-skills` & configured dev-skills root | Free Meta / Dev Tools skills installed together |
| Local agent runtime | agent-specific skills directory | Installed or symlinked `lovstudio-{name}` directory |

`paid: true/false` lives **only** in `lovstudio-general-skills/skills.yaml` — never in SKILL.md.

User-specific paths, brand profiles, design guides, and output directories must
come from explicit CLI flags, environment variables, or
`${LOVSTUDIO_SKILLS_PROFILE:-$HOME/.lovstudio/skills/profile.json}`.
Reusable skills must not hard-code personal workspace paths or private
LovStudio workspace assumptions.

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
