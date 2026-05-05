---
name: lovstudio-skill-creator
category: Meta Skills
tagline: "Scaffold lovstudio skills as independent repos or dev-skills entries."
description: >
  Create new skills for the lovstudio ecosystem. Skills can be scaffolded as
  independent GitHub repos at lovstudio/{name}-skill or as bundled entries in
  the lovstudio/dev-skills aggregate repo under skills/{name}/. The workflow
  also sets up local symlinks for immediate use and registers the skill in the
  appropriate index (skills.yaml + README.md).
  Lovstudio conventions: `lovstudio:{name}` frontmatter, mandatory README.md
  per skill, AskUserQuestion interactive flow, standalone Python CLI scripts
  with argparse, CJK text handling.
  Use when the user wants to create a new skill, add a skill to the lovstudio
  ecosystem, scaffold a skill, or mentions "新建skill", "创建skill", "封装成skill",
  "new skill", "add skill", "scaffold skill", "生成skill".
license: MIT
compatibility: >
  Scaffolds into ~/lovstudio/coding/skills/. Requires Python 3.8+, git, and gh CLI.
metadata:
  author: lovstudio
  version: "2.1.0"
  tags: skill-creator scaffold generator lovstudio
---

# lovstudio:skill-creator

Scaffold a new lovstudio skill either as an **independent GitHub repo** under
`lovstudio/{name}-skill` or as a bundled entry inside
`lovstudio/dev-skills`. The default is still the independent repo model; use
`dev-skills` for Lovstudio meta/dev tooling that should ship as part of the
developer skill bundle.

## Architecture

```
~/lovstudio/coding/
├── lovstudio-skills/     ← main skills index (lovstudio/skills repo)
│   ├── skills.yaml                ← machine-readable manifest (paid flag lives here)
│   └── README.md                  ← human-readable catalog
├── lovstudio-dev-skills/          ← aggregate repo for meta/dev skills
│   ├── skills.yaml
│   ├── .claude-plugin/marketplace.json
│   └── skills/{name}/
│       ├── SKILL.md
│       ├── README.md
│       ├── scripts/
│       └── references/
├── skills/                        ← independent per-skill source repos
│   └── {name}-skill/
│       ├── SKILL.md
│       ├── README.md
│       ├── CHANGELOG.md           ← managed by skill-optimizer
│       ├── scripts/               ← standalone Python CLI scripts
│       └── references/            ← optional progressive-disclosure docs
└── ...

~/.claude/skills/lovstudio-{name}  ← symlink → ~/.agents/skills/lovstudio-{name}
                                                 → ~/lovstudio/coding/skills/{name}-skill/
```

Key facts:
- Default GitHub repo name: `lovstudio/{name}-skill` (with `-skill` suffix)
- Default local source path: `~/lovstudio/coding/skills/{name}-skill/` (no `lovstudio-` prefix)
- Main index checkout path: `~/lovstudio/coding/lovstudio-skills/`
- Dev-skills source path: `~/lovstudio/coding/lovstudio-dev-skills/skills/{name}/`
- Dev-skills catalog entry uses `repo: lovstudio/dev-skills` and `skill_path: skills/{name}`
- Claude Code reads: `~/.claude/skills/lovstudio-{name}/` (with `lovstudio-` prefix, via symlink)
- Frontmatter `name`: `lovstudio:{name}` (with `:` separator)
- `paid: true/false` lives **only** in `lovstudio-skills/skills.yaml`, never in SKILL.md

## Skill Creation Process

### Step 1: Understand the Skill

Ask the user what the skill should do. Use `AskUserQuestion` — one question at
a time, in the order below. **Do not skip or reorder.** The distribution model
decides the architecture, so it has to come before any implementation question.

**Required question order:**

#### Q1. Commercial / protection model — ALWAYS ask first

Even for "obvious" simple skills, ask. Users may have future monetization plans
you can't infer from the initial request.

> 这个 skill 的分发定位?
>
> 1. **Free (public)** — 任何人 git clone 就能用。适合引流、通用工具、开源贡献。
> 2. **Paid, 普通 IP** — 核心逻辑是流程/模板/prompt 编排,用户 grep 出来不心疼。用加密分发 + license 鉴权。
> 3. **Paid, 敏感 IP** — 含算法参数/业务规则/调好的 prompt/API 密钥,用户反编译会心疼。用 cloud-split:核心逻辑放云端,本地只有瘦客户端。
>
> 提示:不确定 → 选 2。未来升级到 3 比降级容易。

这个答案决定后续流程分支:
- 选 1 → 走标准公开 repo 流程
- 选 2 → 走 encrypted skill 流程(README 里坦诚说明 "加密 = 鉴权闸门,不保证反提取")
- 选 3 → **停下来读 `references/cloud-split.md`**,然后走 cloud-split 流程

#### Q1.5. Repository target — ask after Q1

This is separate from the commercial/protection model. It answers "where does
the source live and how is it distributed?"

> 这个 skill 放在哪里分发?
>
> 1. **Independent repo (default)** — `~/lovstudio/coding/skills/{name}-skill/`
>    → `lovstudio/{name}-skill` → central `lovstudio/skills` index.
> 2. **dev-skills bundle** — `~/lovstudio/coding/lovstudio-dev-skills/skills/{name}/`
>    → `lovstudio/dev-skills` → bundled install via `npx skills add lovstudio/dev-skills`
>    or Claude Code plugin marketplace.
>
> 判断:面向技能作者/开发流程/内部工程规范的免费工具 → 选 2。通用用户工具、
> 付费 skill、cloud-split thin client → 选 1。

Consistency rules:
- If Q1 is **Paid** or **Cloud-split**, do **not** use dev-skills. Use an
  independent repo so licensing, encryption, and cloud-split thin-client
  packaging stay isolated.
- Use dev-skills for free Meta / Dev Tools skills such as `skill-creator`,
  `skill-optimizer`, `project-port`, or project refactor/init helpers.

#### Q2. Problem & shape
- 解决什么问题?输入 → 输出是什么?
- 2-3 个具体使用示例
- 触发短语(中文 + English)

#### Q2.5. Decompose into protected vs public layers  ⟵ MANDATORY, do not skip

Before any file is created, **decompose the skill** into two layers and **show
the user the decomposition** for confirmation. This step catches two common
failures: (a) cloud-split chosen with empty protected layer (over-engineering),
(b) encrypted chosen but real secrets exist (under-protection).

Present like this:

> 我先拆解一下这个 skill 的结构:
>
> **公开层(瘦客户端 SKILL.md 会暴露这些)**:
> - [具体列出:对话流、输入解析、输出渲染、错误处理]
>
> **保护层(需要藏起来的)**:
> - [具体列出:算法/阈值/规则/prompt 工程/密钥/数据]
> - 或明确写 "**无** — 这个 skill 没有需要保护的核心逻辑"
>
> 按这个拆解,你选的 [Q1 答案] [合理 / 不合理,建议改成 X]。确认继续?

**Consistency check** — if decomposition contradicts Q1, challenge it:

| Q1 选择 | 保护层内容 | 判断 |
|---|---|---|
| Free | 任何 | ✓ 无需保护问题 |
| Encrypted | 非空 | ⚠️ 警告:encrypted 不防 L2 grep,真敏感的请升级 cloud-split |
| Encrypted | 空 | ✓ 合理(典型场景:付费模板/工作流) |
| Cloud-split | 非空且有实质 | ✓ 合理 |
| **Cloud-split** | **空或琐碎** | ✗ **停下,反问用户是否过度设计,建议降级到 encrypted 或 free** |

对琐碎 demo(如"两数之和")尤其要质询 —— cloud-split 的服务端成本 + 部署复杂度
对"其实没东西可保护"的 skill 是净负收益。除非用户明确说"做模板/教学样本",
否则建议降级。

#### Q2.7. Naming — de-business the name  ⟵ MANDATORY for paid skills

Bad naming leaks the logic through the API surface. Even with cloud-split, if
the skill name + op name + input schema together describe the business logic,
`grep` on jsonl reveals intent.

**Rule**: name the **capability domain**, not the **specific logic**.

| ✗ 逻辑自述(坏) | ✓ 能力域(好) |
|---|---|
| `sum-gt-ten` | `threshold-check` |
| `extract-chinese-poem-style` | `text-style-analyzer` |
| `detect-viral-headline` | `text-scorer` |
| `calculate-compatibility` | `profile-matcher` |

Propose 2-3 de-businessed names and let the user pick via AskUserQuestion.
For the **op** names inside the handler, same rule — `op: "score"` beats
`op: "check_if_sum_exceeds_10"`.

Skip this step only if Q1 == Free and the user doesn't care about future
paid upgrades.

#### Q3. Implementation type
- 纯指令 SKILL.md,还是需要 Python CLI 脚本?
- (如果 Q1 选了 3:这一问跳过。cloud-split 的"实现"就是云端 handler,不是本地脚本。)

### Protection model — what each tier actually buys you

Be honest about what each tier protects against. Do not market encrypted skills
as "IP protection" — it's a gate, not a vault.

| Tier | Protects against | Does NOT protect against |
|---|---|---|
| Free | 无 | 无 |
| Paid / encrypted | 路人 `git clone` 就能用(L1) | 技术用户 grep `~/.claude/projects/*.jsonl` 取回明文(L2) |
| Paid / cloud-split | L1 + L2 + 反汇编客户端 | 反向推理 I/O 做劣质 clone |

核心逻辑真正不下发到用户机器的 **只有 cloud-split**。其他 tier 都不要对用户承诺"加密保护"。

### Step 2: Plan Contents

Analyze the examples and identify:

1. **Scripts** — deterministic operations → `scripts/`
2. **References** — domain knowledge Claude needs while working → `references/`
3. **Assets** — files used in output (templates, fonts, etc.) → `assets/`

Rules:
- Python scripts must be **standalone single-file CLIs** with `argparse`
- No package structure, no `setup.py`, no `__init__.py`
- CJK text handling is a core concern if the skill deals with documents

### Step 3: Initialize

Run the init script. Independent repo is the default:

```bash
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py <name>
```

For a dev-skills bundled skill:

```bash
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py <name> --target dev-skills
```

Independent repo creates `~/lovstudio/coding/skills/{name}-skill/` with:

```
{name}-skill/
├── SKILL.md          ← frontmatter + TODO workflow
├── README.md         ← human-readable docs with version badge
└── scripts/          ← empty, ready for implementation
```

Dev-skills creates `~/lovstudio/coding/lovstudio-dev-skills/skills/{name}/` with
the same skill-internal structure.

Pass `--paid` if this is a paid skill (adjusts README + metadata hints).
Do not combine `--paid` with `--target dev-skills`; use an independent repo for
paid distribution.

**If Q1 chose cloud-split (tier 3)**: after running init_skill.py, don't put
your real logic in `scripts/`. Instead:
1. Read `references/cloud-split.md` end-to-end before writing any code
   **(this is not optional — the rules for non-leaky payloads are there, not here)**
2. **Start from `threshold-check` as the reference pattern**, NOT `paid-add`.
   `paid-add` is an architecture demo with an intentionally leaky payload
   (for teaching). Copying its return shape into a real skill defeats the
   whole point of cloud-split.
3. Write the handler at `~/lovstudio/coding/web/supabase/functions/skill_call/handlers/<name>.ts`
   — return a minimal symbolic payload (`{verdict: "A" | "B"}` style), not
   descriptive strings or narrative `display` fields
4. Write the thin SKILL.md per the `threshold-check` template — rendering
   via a **symbol → text table**, never via a computed algorithm
5. **MANDATORY pre-flight audit** — before registering the handler in the
   dispatcher, before deploying, before telling the user "done":
   run the checklist in `references/cloud-split.md` → "MANDATORY pre-flight
   audit" section. Report each item's result to the user. If any item
   fails, rewrite before moving on.
6. Skip the normal Step 4 "write scripts" — there usually aren't any for
   cloud-split skills (unless you need client-side rendering of server output)

**Why the audit is mandatory**: a real incident during skill-creator
development produced a cloud-split skill whose handler returned
`{score, verdict: "below", display: "2+6=8 (below 10)"}`. Architecture was
correct; protection was zero. The audit catches this class of bug before
it ships.

### Step 4: Implement

1. **Write scripts** in `scripts/` — test by running directly
2. **Write SKILL.md** — instructions for AI assistants:
   - Frontmatter `description` is the trigger mechanism — cover what + when +
     concrete trigger phrases (中文 + English)
   - Body contains workflow steps, CLI reference, field mappings
   - Use `AskUserQuestion` for interactive prompts before running scripts
   - Keep SKILL.md under 500 lines; split to `references/` if longer
3. **Write README.md** — docs for humans on GitHub:
   - Version badge (source of truth for version)
   - Install command: `git clone https://github.com/lovstudio/{name}-skill ~/.claude/skills/lovstudio-{name}`
   - Dependencies
   - Usage examples, options table
   - ASCII diagrams if useful

See `references/templates.md` for SKILL.md / README.md templates.

### Step 5: Publish

Follow the branch matching Q1.5.

### Independent Repo Target

#### 5a. Initialize & push the skill's own repo

```bash
cd ~/lovstudio/coding/skills/<name>-skill
git init
git add -A
git commit -m "feat: initial release of <name> skill"

# Free skill (public):
gh repo create lovstudio/<name>-skill --public --source=. --push

# Paid skill (private):
gh repo create lovstudio/<name>-skill --private --source=. --push
```

#### 5b. Register in the central index

Edit `~/lovstudio/coding/lovstudio-skills/skills.yaml` — append under the right
category (category order in the yaml determines display order on the website):

```yaml
  - name: <name>
    repo: lovstudio/<name>-skill
    paid: false                         # or true for paid skills
    category: "<Category>"              # must match an existing category heading
    version: "0.1.0"
    description: "<One-line description matching SKILL.md tagline>"
```

Also add a row to `~/lovstudio/coding/lovstudio-skills/README.md` under the matching
category section. Then PR against `lovstudio/skills`:

```bash
cd ~/lovstudio/coding/lovstudio-skills
git checkout -b add/<name>
git add skills.yaml README.md
git commit -m "add: <name> skill"
git push -u origin HEAD
gh pr create --fill
```

#### 5c. Symlink for local availability

Make the skill immediately usable in Claude Code:

```bash
# Layer 1: source → .agents
ln -s ~/lovstudio/coding/skills/<name>-skill \
      ~/.agents/skills/lovstudio-<name>

# Layer 2: .agents → .claude/skills (where Claude Code reads)
ln -s ../../.agents/skills/lovstudio-<name> \
      ~/.claude/skills/lovstudio-<name>
```

Verify: `ls ~/.claude/skills/lovstudio-<name>/SKILL.md` resolves.

#### 5d. Trigger lovstudio.ai cache refresh (optional)

After the skill is indexed in `skills.yaml`, the lovstudio.ai `/agent` page caches
the index for 1 hour (Next.js ISR). Trigger on-demand revalidation so the new
skill appears immediately:

```bash
if [ -n "$LOVSTUDIO_REVALIDATE_SECRET" ]; then
  curl -sfX POST https://lovstudio.ai/api/revalidate \
    -H "x-revalidate-secret: $LOVSTUDIO_REVALIDATE_SECRET" \
    -H "content-type: application/json" \
    -d '{"tags":["skills-index"]}' \
    && echo "✓ cache refreshed" \
    || echo "⚠ revalidate failed (will appear within 1h)"
fi
```

Known tags (see `lovstudio/web:src/data/skills.ts`):
- `skills-index` — the yaml index (invalidates all list pages)
- `skill:<id>` — detail for a single skill
- `skill-cases:<id>` — cases.json for a skill

### Dev-Skills Target

Use this for free Meta / Dev Tools skills that belong in the
`lovstudio/dev-skills` bundle.

#### 5a. Commit inside dev-skills

```bash
cd ~/lovstudio/coding/lovstudio-dev-skills
git checkout -b add/<name>
git add skills/<name>
```

#### 5b. Register in dev-skills metadata

Edit `~/lovstudio/coding/lovstudio-dev-skills/skills.yaml`:

```yaml
- name: <name>
  repo: lovstudio/dev-skills
  skill_path: skills/<name>
  name_zh: <中文名>
  paid: false
  category: "Dev Tools"                 # or "Meta"
  version: "0.1.0"
  description: "<Agent-facing trigger description>"
  tagline_en: "<Human-facing English tagline>"
  tagline_zh: "<Human-facing Chinese tagline>"
```

Also update `.claude-plugin/marketplace.json` so the correct plugin includes
`"./skills/<name>"`:
- Meta skills → `plugins[].name == "meta"`
- Dev tooling → `plugins[].name == "dev-tools"`

Then render the READMEs:

```bash
python3 scripts/render-readme.py
```

#### 5c. Symlink for local availability

```bash
ln -s ~/lovstudio/coding/lovstudio-dev-skills/skills/<name> \
      ~/.agents/skills/lovstudio-<name>
ln -s ../../.agents/skills/lovstudio-<name> \
      ~/.claude/skills/lovstudio-<name>
```

#### 5d. Commit and push

```bash
git add skills.yaml README.md README.en.md .claude-plugin/marketplace.json
git commit -m "add: <name> skill"
git push -u origin HEAD
gh pr create --fill
```

Do not register dev-skills-only skills in the central `~/lovstudio/coding/lovstudio-skills/`
unless the user explicitly asks for the main Lovstudio skills index to list the
bundle entry.

### Step 6: Test & Iterate

1. In a new conversation, invoke `/lovstudio:<name>` — confirm it triggers
2. Notice struggles → edit SKILL.md / scripts in the source repo
3. Commit & push in the chosen target repo (independent repo or dev-skills)

## Design Patterns

### Interactive Pre-Execution (MANDATORY for generation/conversion skills)

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

- `INSTALLATION_GUIDE.md` — clutter; install instructions go in README.md
- Test files — scripts are tested by running, not with test frameworks
- `__pycache__/`, `*.pyc`, `.DS_Store` — add to `.gitignore`
- `paid` field in frontmatter — it lives only in `lovstudio-skills/skills.yaml`

## Migration Notes

### 2026-05: dev-skills aggregate target

Some free developer/meta skills should live directly in `lovstudio/dev-skills`
instead of requiring a dedicated repo. Use `--target dev-skills` for those:

```bash
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py tanstack-query --target dev-skills
```

The skill directory is `~/lovstudio/coding/lovstudio-dev-skills/skills/tanstack-query/`, and `skills.yaml`
must include `repo: lovstudio/dev-skills` plus `skill_path: skills/tanstack-query`.

### 2026-04: independent per-skill repos

The ecosystem was refactored from a monorepo (`lovstudio/skills` containing
`skills/lovstudio-<name>/`) + mirror (`lovstudio/pro-skills`) into independent
per-skill repos + central index. The old `lovstudio/pro-skills` was archived.
If working on a legacy skill still in the old structure, migrate it first:

```bash
# 1. Extract from monorepo subdirectory
cp -r ~/projects/lovstudio-skills/skills/lovstudio-<name> \
      ~/lovstudio/coding/skills/<name>-skill
cd ~/lovstudio/coding/skills/<name>-skill
# (remove the lovstudio- prefix from the directory by creating fresh)

# 2. Fresh git history
rm -rf .git
git init && git add -A && git commit -m "import: <name> from monorepo"

# 3. Create independent repo
gh repo create lovstudio/<name>-skill --public --source=. --push
```
