# Migration Notes

## 2026-05: dev-skills aggregate target

Some free developer/meta skills should live directly in `lovstudio/dev-skills`
instead of requiring a dedicated repo. Use `--target dev-skills` for those:

```bash
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py tanstack-query --target dev-skills
```

The skill directory is:

```text
~/lovstudio/coding/lovstudio-dev-skills/skills/tanstack-query/
```

`skills.yaml` must include:

```yaml
repo: lovstudio/dev-skills
skill_path: skills/tanstack-query
```

## 2026-04: independent per-skill repos

The ecosystem was refactored from a monorepo (`lovstudio/skills` containing
`skills/lovstudio-<name>/`) + mirror (`lovstudio/pro-skills`) into independent
per-skill repos + central index. The old `lovstudio/pro-skills` was archived.

If working on a legacy skill still in the old structure, migrate it first:

```bash
# 1. Extract from monorepo subdirectory
cp -r ~/projects/lovstudio-skills/skills/lovstudio-<name> \
      ~/lovstudio/coding/skills/<name>-skill
cd ~/lovstudio/coding/skills/<name>-skill

# 2. Fresh git history
rm -rf .git
git init && git add -A && git commit -m "import: <name> from monorepo"

# 3. Create independent repo
gh repo create lovstudio/<name>-skill --public --source=. --push
```
