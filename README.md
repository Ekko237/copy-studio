# Copy Studio

A **Claude Code / Codex skill** that runs one marketing-copy job through five stages — **strategy → framework → draft → polish → de-AI** — and **stops for your approval after every stage**. Plus an optional sixth stage that localizes the approved copy into the channel's language.

[中文说明](README.zh-CN.md)

It orchestrates five existing skills instead of replacing them:

| Stage | Skill | What it produces |
|---|---|---|
| 1. Strategy | `brainstorming` | goal · target user · pains · desires · result-oriented value proposition |
| 2. Framework | `writing-plans` | block-by-block structure, each block tied to a pain or desire |
| 3. Draft | `copywriting` | the real copy, in the shape of the channel's recipe |
| 4. Polish | `copy-editing` | the Seven Sweeps line edit |
| 5. De-AI | `humanizer` | AI tells removed, voice matched → final deliverable |
| 6. Localize *(optional)* | your localization skill | the approved master localized into the channel's language |

None of those five skills ship with this repo — see [Dependencies](#dependencies--five-skills-each-under-its-own-license).

The point is not speed. It's one entry point, one strategy carried all the way through, and a guaranteed review gate between stages.

## Why the gates matter

The failure this skill is built to prevent: an assistant hands you a strategy, a framework, *and* a finished draft in a single message — having quietly decided the angle for you. So the strategy gate is a hard stop. The turn that proposes the direction contains **no candidate copy**. Even a one-line comment reply gets two gates in two separate turns: direction first, finished copy second.

Its companion rule: right-size the *ceremony*, never drop a *stage*. "Lightweight" means fewer turns, not fewer stages — a raw Stage 3 draft is never the deliverable.

## What a run looks like

A small job stops once before any copy exists, then once more on the finished piece. The transcript below is that shape. **Northwind Kettle is a placeholder, not a real brand.** The fact base has no price, no customer count, and no awards, so the draft has none either.

```text
You
  /copy-studio an Instagram caption for the spring kettle.
  Someone outfitting a one-person kitchen. The plastic lid on their
  current kettle slips when they pour. They want a kettle they can
  leave on the table.
  Fact base (placeholder only):
    Product: Northwind Kettle — an enamel kettle with a wooden handle
    URL: https://example.invalid/kettle
    Price, ratings, awards, customer counts: none recorded

Copy Studio
  Stage 0 · Intake
    Copy type: social promo caption (Instagram)
    Asset and goal: one caption for the spring kettle
    Size: small job — two gates, in two turns
    Channel language: English, so Stage 6 does not run
    Grounding: claims trace to the fact base above; gaps stay TBD

  Stage 1 · Strategy · brainstorming
    Goal: acquisition
    Target user: someone outfitting a one-person kitchen
    Pain: the plastic lid on their current kettle slips when they pour
    Desire: a kettle they can leave on the table
    Value proposition: an enamel kettle with a wooden handle
    The pain and the desire are the ones you supplied at intake.

  Stage 2 · Framework · writing-plans
    Hook (slipping lid) → the product as stated (enamel, wooden handle) → bio-link CTA
    No caption in this turn.

  Stage 1 complete.
  ✅ Approved — deliver the finished copy (polished + de-AI'd) · ✏️ Change something (say what) · ⏪ Redo this stage · ⛔ Stop here

You
  Approved

Copy Studio
  Stage 3 · Draft · copywriting
    The lid on my old kettle slips when I pour.
    This one is enamel, with a wooden handle.
    Spring kettle. Link in the bio.

  Stage 4 · Polish · copy-editing
    Seven Sweeps. A line that called the handle "effortless" came out:
    that word is not in the fact base. No new claim went in.

  Stage 5 · De-AI · humanizer
    A padded three-item list came out. The wording left is the draft above.
    Polished + de-AI'd. Price and any sales figure are TBD, so they are not in the caption.

  Stage 5 complete. Channel language matches the draft, so this is the deliverable.
  ✅ Approved · ✏️ Change something (say what) · ⏪ Redo this stage · ⛔ Stop here
```

On a big job the same menu is printed after every stage, and the first choice reads `✅ Approved, continue to Stage N+1`. The turn that proposes the direction still contains no candidate copy.

## Install

One command installs Copy Studio, the five dependency skills, and the `/copy-studio` slash command into both `~/.claude` and `~/.codex`:

```bash
curl -fsSL https://raw.githubusercontent.com/Ekko237/copy-studio/main/install.sh | bash
```

From a checkout of this repo, `bash install.sh` does the same thing. `bash scripts/install-deps.sh` installs only the five dependencies.

The script writes:

- `~/.claude/skills/copy-studio/` and `~/.codex/skills/copy-studio/`
- `brainstorming`, `writing-plans`, `copywriting`, `copy-editing`, and `humanizer`, in both skill folders, under those names
- `~/.claude/commands/copy-studio.md`, which is the `/copy-studio` slash command

Each dependency is cloned from its upstream repository and keeps that project's own license. The installed folder contains the upstream `LICENSE` (copied unchanged, including from the repository root when the skill directory itself has none) and an `UPSTREAM` file with the repository URL, path, and commit. Copy Studio does not relicense them. A folder that is already at one of those paths, and that this installer did not put there, is renamed to `*.bak-<timestamp>` first. Running the script again refreshes the copies it manages.

On Windows, run it from Git Bash or WSL. `~` is `C:\Users\<you>`. Skill folders elsewhere: set `COPY_STUDIO_CLAUDE_HOME` and `COPY_STUDIO_CODEX_HOME`.

Copy Studio alone, without the dependencies:

```bash
git clone https://github.com/Ekko237/copy-studio.git ~/.claude/skills/copy-studio
git clone https://github.com/Ekko237/copy-studio.git ~/.codex/skills/copy-studio
cp ~/.claude/skills/copy-studio/commands/copy-studio.md ~/.claude/commands/copy-studio.md
```

A stage whose skill is missing does not run. Copy Studio does not fill in with a copy of its own.

## Dependencies — five skills, each under its own license

Copy Studio is an **orchestrator**. It does not contain the five skills it drives. `install.sh` clones them for you; they stay separate projects by other authors, each under its own license:

| Stage | Skill it calls | Where to get it |
|---|---|---|
| 1. Strategy | `brainstorming` | [obra/superpowers](https://github.com/obra/superpowers) → `skills/brainstorming/` |
| 2. Framework | `writing-plans` | [obra/superpowers](https://github.com/obra/superpowers) → `skills/writing-plans/` |
| 3. Draft | `copywriting` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) → `skills/copywriting/` |
| 4. Polish | `copy-editing` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) → `skills/copy-editing/` |
| 5. De-AI | `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) |

All three upstream projects are MIT-licensed. Go to each repository for its current terms. Copy Studio invokes these skills by name, so a newer upstream copy still fits. Missing one? Then the stage that calls it can't run.

Stage 6 (localization) is optional and needs a localization skill of your own. The installer does not add one.

## Before your first real run: bring your own brand reference

This repo ships with **no brand facts, no product stats, no prize figures, and no sample copy** — deliberately. Inventing a number is the worst thing a copy pipeline can do, and someone else's samples teach the wrong voice. Two files are yours to create:

1. **A fact base** — the only citable source for your product's stats, capabilities, URLs, pricing, and program/reward figures. Quote it verbatim; anything not in it is `TBD`, never a guess.
2. **A channel calibration file** — 2–3 approved real samples per channel you ship to. These teach shape and voice better than any description.

[`references/channel-calibration-template.md`](references/channel-calibration-template.md) is the scaffold for both. Note that once it holds real material it's usually internal — the included `.gitignore` keeps filled-in copies out of git by default.

## Usage

```
/copy-studio an Instagram post for the new template library
```

Or just describe the job and let the skill trigger. It starts at **Stage 0 (intake)**: copy type + channel, the asset and goal in one line, scope, output language, and what source material exists. Then one stage per turn, stopping at each gate:

> **Stage N complete.** […output…]
> ✅ Approved, continue to Stage N+1 · ✏️ Change something · ⏪ Redo this stage · ⛔ Stop here

A big job (whole page, deck, campaign) gets a gate after every stage. A small job (one comment, post, caption, card) gets two: direction first, then the finished copy with polish and de-AI already applied.

Already have a brief? Start at Stage 2. Have a draft you want finished? Start at Stage 4. Just need the AI smell taken off? Invoke `humanizer` directly.

## What's in it beyond the pipeline

- **A six-field recipe per copy type** — shape · must-include · length & voice · CTA/link · grounding · visual support. New channels don't need new code: fill the six fields live and it becomes a library row.
- **A recipe library** covering landing-page value cards, community posts, four kinds of comment reply, deck slides, ads, per-platform social captions, email, and image-heavy template email.
- **Channel constraints that are easy to get wrong** — e.g. platforms whose in-feed links aren't clickable need a bio-link CTA instead, so two platforms never share one caption; Reddit takes zero links and zero hashtags in the body, keeps rewards out of the brand's main comment, and treats new accounts least generously.
- **A pre-show self-check** the draft must pass before you ever see it: voice, grounding, shape, length, AI tells, copy-first, channel rules, language.
- **Localize-last discipline** — translation happens only at Stage 6, into the channel's language only. One channel means one language; multi-language fan-out is for site-wide content, not a single comment.

## Working language vs deliverable language

The skill separates the language you *talk* in from the language the copy *ships* in — useful when a team works in one language and markets in another. Deliverables come with a short note in the working language explaining what each line is doing, so a reviewer who doesn't read the target language can still give feedback. Defaults are configurable at Stage 0.

## Layout

- `README.md` — you are here · [中文说明](README.zh-CN.md)
- `install.sh` — one-command install of this skill, the five dependencies, and the slash command
- `scripts/install-deps.sh` — the five dependencies only
- `SKILL.md` — the skill: stages, gates, recipe library, self-checks
- `commands/copy-studio.md` — `/copy-studio` slash command (`install.sh` copies it into `~/.claude/commands/`)
- `agents/openai.yaml` — Codex agent interface metadata
- `references/channel-calibration-template.md` — scaffold for your fact base and samples
- `scripts/check_skill.py` — structural check for `SKILL.md` (section references, table integrity, self-check count); run it after editing the skill

## License

MIT — see [LICENSE](LICENSE).
