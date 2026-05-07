# Changelog

All notable changes to this skill are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: [SemVer](https://semver.org/)

## [2.6.1] - 2026-05-07

### Fixed

- publish LovStudio skill standard reference
- add references/skill-standard.md as the canonical standardization document

## [2.6.0] - 2026-05-07

### Added

- standardize config env vars on LOVSTUDIO_SKILLS namespace
- replace AGENT_SKILL_* in generated templates
- keep defaults under ~/.lovstudio/skills

## [2.5.0] - 2026-05-07

### Added

- move default skill profile under ~/.lovstudio
- keep AGENT_SKILL_PROFILE as the portable override
- default generated brand/design config paths to ~/.lovstudio/skills

## [2.4.0] - 2026-05-07

### Added

- switch public config contract to AGENT_SKILL profile
- replace LovStudio-prefixed profile paths in new-skill templates
- keep LovStudio paths as private authoring examples, not reusable runtime API

## [2.3.0] - 2026-05-06

### Added

- add portable user configuration scaffolding
- switch new templates to Agent Skills-compatible lovstudio-<name> frontmatter
- generate references/user-config.md for new skills
- move historical migration notes into references/migration.md for progressive disclosure

## [2.2.0] - 2026-05-06

### Added

- Document optional SKILL.md frontmatter `depends_on` for required skill-level dependencies.
- Scaffold templates now include commented `depends_on` guidance so new skills can declare reuse relationships explicitly.

## [2.1.0] - 2026-05-06

### Added

- Add `dev-skills` as a first-class repository target for free Meta / Dev Tools skills.
- `init_skill.py` now supports `--target dev-skills` and `--dev-skills`.
- Document `repo: lovstudio/dev-skills` + `skill_path: skills/<name>` registration and marketplace plugin updates.

## [2.0.0] - 2026-04-18

### Changed

- Rewrite for per-skill-repo architecture. Each skill is now an independent repo at `lovstudio/{name}-skill` instead of a subdirectory of a monorepo.
- Default scaffold path: `~/lovstudio/coding/skills/{name}-skill/` (was `skills/lovstudio-{name}/`).
- Install hint: `git clone` each skill repo (replaces `npx skills add lovstudio/skills`).
- `init_skill.py`: accepts `--paid`, auto-creates `.gitignore`, and prints `gh repo create` + symlink + index-registration next-steps instead of monorepo-dev-flow hints.

### Added

- Step 5b: PR to `lovstudio/skills` central index (`skills.yaml` + `README.md`).
- Step 5d: lovstudio.ai ISR cache revalidation via `skills-index` tag.
- Migration note for legacy skills still in the monorepo structure.

### Removed

- Step 0 (repo choice): `lovstudio/pro-skills` was archived 2026-04-16. `paid` now lives only in `lovstudio-general-skills/skills.yaml` as catalog metadata, not as a skill property.

## [1.2.0] - 2026-04-15

### Added

- Add Step 0: repo selection (lovstudio/skills vs lovstudio/pro-skills)
- Step 5c: create PR to chosen target repo instead of push to main

## [1.1.1] - 2026-04-14

### Fixed

- Add publish workflow: symlink chain + git push to Step 5

## [1.1.0] - 2026-04-14

### Added

- Fix init_skill.py repo detection — prefer lovstudio-skills over cwd
- README template now includes version badge
- Remove CHANGELOG from 'What NOT to Include' (managed by skill-optimizer)
