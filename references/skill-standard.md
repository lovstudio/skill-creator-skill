# LovStudio Skill Standard

This standard applies to public, paid, bundled, and internal LovStudio skills.
Its goal is portability first: a skill may carry LovStudio branding, but it
must not silently depend on Mark's local machine, workspace layout, or private
brand assets unless the skill is explicitly marked author-only.

## Naming

- Use Agent Skills-compatible names: lowercase letters, numbers, and hyphens.
- Prefer `lovstudio-<name>` in `SKILL.md` frontmatter.
- Avoid `lovstudio:<name>` for new skills. Treat colon names as legacy aliases.
- Source repos may still be named `<name>-skill`, but installed/distributed
  skill directories should resolve to `lovstudio-<name>/` so the directory and
  frontmatter name can match in user environments.

## Runtime Portability

Skills must not assume these paths in execution instructions or scripts:

- `/Users/mark/...`
- `~/lovstudio/...`
- `~/.claude/...` except in human-facing install examples
- `~/.agents/...` except in maintainer docs

Use this precedence whenever a skill needs user-specific paths, identity,
brand assets, or workspace settings:

1. Explicit CLI flags.
2. Environment variables.
3. User profile file.
4. Safe defaults such as the current working directory or an output directory
   under `$HOME/Documents`.
5. Ask the user once and explain what setting is missing.

## User Profile Contract

Portable skills may read a shared JSON profile at:

```bash
${LOVSTUDIO_SKILLS_PROFILE:-$HOME/.lovstudio/skills/profile.json}
```

Recommended fields:

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
    "profile": "$HOME/.lovstudio/skills/brand.json",
    "design_guide": "$HOME/.lovstudio/skills/design-guide.md"
  }
}
```

Environment variables override profile fields:

| Variable | Meaning |
|----------|---------|
| `LOVSTUDIO_SKILLS_PROFILE` | Path to the shared profile JSON |
| `LOVSTUDIO_SKILLS_HOME` | Shared LovStudio skills config/data directory |
| `LOVSTUDIO_SKILLS_INSTALL_DIR` | User's local agent skills installation directory |
| `LOVSTUDIO_SKILLS_WORKSPACE_ROOT` | User workspace root |
| `LOVSTUDIO_SKILLS_OUTPUT_DIR` | Default generated output directory |
| `LOVSTUDIO_SKILLS_BRAND_PROFILE` | Brand profile JSON or Markdown |
| `LOVSTUDIO_SKILLS_DESIGN_GUIDE` | Design guide path |

Skill-specific variables should use `LOVSTUDIO_<SKILL_NAME>_*`, for example
`LOVSTUDIO_MAINTAIN_PARTNERS_SITE_ROOT`. Avoid broad names such as
`PARTNERS_SITE_ROOT` and avoid pseudo-generic namespaces such as
`AGENT_SKILL_*` unless LovStudio is intentionally publishing a separate,
vendor-neutral standard.

Default files live under `~/.lovstudio/skills/` because these skills are
distributed by LovStudio. That directory is a storage namespace, not the public
API. Users can override it with `LOVSTUDIO_SKILLS_PROFILE`.

## Brand Coupling

Brand-aware skills should split their behavior into:

- Generic workflow: reusable by any user or brand.
- LovStudio defaults: optional profile/reference loaded only when configured.
- User initialization: a documented path for replacing LovStudio/Mark values
  with the user's own brand, workspace, design guide, and output directory.

If a skill is truly LovStudio-internal, say so in `compatibility` and README.
Internal skills may use LovStudio paths, but they should still keep them in one
configuration section rather than scattering absolute paths across workflows.

## Scripts

- Scripts should accept explicit paths via CLI flags.
- Scripts should not import from private absolute paths.
- Scripts may use the shared profile contract, but missing profile values must
  produce actionable errors.
- Prefer `argparse` for Python CLIs.

## Migration Labels

Use these labels when auditing existing skills:

- `portable`: no local or brand-specific assumptions.
- `config-needed`: useful to public users, but needs a profile/env layer.
- `lovstudio-defaults`: generic core with optional LovStudio defaults.
- `author-only`: intentionally tied to Mark/LovStudio private workspace.
- `legacy-name`: still uses `lovstudio:<name>` or mismatched directory naming.
