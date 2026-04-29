---
name: lovstudio-skill-creator
category: Meta Skills
tagline: "Scaffold new lovstudio skills as independent repos under lovstudio/{name}-skill."
description: >
  Create new skills for the lovstudio ecosystem. Each skill is its own
  independent GitHub repo at lovstudio/{name}-skill, scaffolded locally at
  ~/lovstudio/coding/skills/{name}-skill/, symlinked to ~/.claude/skills/
  for immediate use, and registered in the central index at
  ~/lovstudio/coding/skills/index/ (skills.yaml + README.md).
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
  version: "2.0.0"
  tags: skill-creator scaffold generator lovstudio
---

# lovstudio:skill-creator

Scaffold a new lovstudio skill as an **independent GitHub repo** under
`lovstudio/{name}-skill`. The lovstudio ecosystem is no longer a monorepo —
each skill is its own repo, and a central index at
`~/lovstudio/coding/skills/index/` tracks them.

## Architecture

```
~/lovstudio/coding/skills/
├── index/                     ← central catalog (lovstudio/skills repo)
│   ├── skills.yaml            ← machine-readable manifest (paid flag lives here)
│   └── README.md              ← human-readable catalog
├── {name}-skill/              ← each skill is an independent repo
│   ├── SKILL.md
│   ├── README.md
│   ├── CHANGELOG.md           ← managed by skill-optimizer
│   ├── scripts/               ← standalone Python CLI scripts
│   └── references/            ← optional progressive-disclosure docs
└── ...

~/.claude/skills/lovstudio-{name}  ← symlink → ~/.agents/skills/lovstudio-{name}
                                                 → ~/lovstudio/coding/skills/{name}-skill/
```

Key facts:
- GitHub repo name: `lovstudio/{name}-skill` (with `-skill` suffix)
- Local source path: `~/lovstudio/coding/skills/{name}-skill/` (no `lovstudio-` prefix)
- Claude Code reads: `~/.claude/skills/lovstudio-{name}/` (with `lovstudio-` prefix, via symlink)
- Frontmatter `name`: `lovstudio:{name}` (with `:` separator)
- `paid: true/false` lives **only** in `index/skills.yaml`, never in SKILL.md

## Skill Creation Process

### Step 1: Understand the Skill

Ask the user what the skill should do. Use `AskUserQuestion` — one question at
a time, in the order below. **Do not skip or reorder.** The distribution model
decides the architecture, so it has to come before any implementation question.

**Required question order:**

#### Q1. Distribution model — ALWAYS ask first

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

Run the init script (it auto-detects the target directory):

```bash
python3 ~/.claude/skills/lovstudio-skill-creator/scripts/init_skill.py <name>
```

This creates `~/lovstudio/coding/skills/{name}-skill/` with:

```
{name}-skill/
├── SKILL.md          ← frontmatter + TODO workflow
├── README.md         ← human-readable docs with version badge
└── scripts/          ← empty, ready for implementation
```

Pass `--paid` if this is a paid skill (adjusts README + metadata hints).

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

Edit `~/lovstudio/coding/skills/index/skills.yaml` — append under the right
category (category order in the yaml determines display order on the website):

```yaml
  - name: <name>
    repo: lovstudio/<name>-skill
    paid: false                         # or true for paid skills
    category: "<Category>"              # must match an existing category heading
    version: "0.1.0"
    description: "<One-line description matching SKILL.md tagline>"
```

Also add a row to `~/lovstudio/coding/skills/index/README.md` under the matching
category section. Then PR against `lovstudio/skills`:

```bash
cd ~/lovstudio/coding/skills/index
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

### Step 6: Test & Iterate

1. In a new conversation, invoke `/lovstudio:<name>` — confirm it triggers
2. Notice struggles → edit SKILL.md / scripts in the source repo
3. Commit & push (the symlink chain means no local copy to sync)

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
- `paid` field in frontmatter — it lives only in `index/skills.yaml`

## Migration Note (2026-04)

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
