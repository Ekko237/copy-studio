# Copy Studio

A **Claude Code / Codex skill** that runs one marketing-copy job through five stages — **strategy → framework → draft → polish → de-AI** — and **stops for your approval after every stage**. Plus an optional sixth stage that localizes the approved copy into the channel's language.

It orchestrates five existing skills instead of replacing them:

| Stage | Skill | What it produces |
|---|---|---|
| 1. Strategy | `brainstorming` | goal · target user · pains · desires · result-oriented value proposition |
| 2. Framework | `writing-plans` | block-by-block structure, each block tied to a pain or desire |
| 3. Draft | `copywriting` | the real copy, in the shape of the channel's recipe |
| 4. Polish | `copy-editing` | the Seven Sweeps line edit |
| 5. De-AI | `humanizer` | AI tells removed, voice matched → final deliverable |
| 6. Localize *(optional)* | your localization skill | the approved master localized into the channel's language |

None of those five skills ship with this repo — see [Dependencies](#dependencies--five-skills-you-install-yourself).

The point is not speed. It's one entry point, one strategy carried all the way through, and a guaranteed review gate between stages.

## Why the gates matter

The failure this skill is built to prevent: an assistant hands you a strategy, a framework, *and* a finished draft in a single message — having quietly decided the angle for you. So the strategy gate is a hard stop. The turn that proposes the direction contains **no candidate copy**. Even a one-line comment reply gets two gates in two separate turns: direction first, finished copy second.

Its companion rule: right-size the *ceremony*, never drop a *stage*. "Lightweight" means fewer turns, not fewer stages — a raw Stage 3 draft is never the deliverable.

## Install

```bash
git clone https://github.com/Ekko237/copy-studio.git ~/.claude/skills/copy-studio
```

- **Claude Code** → `~/.claude/skills/copy-studio/`
- **Codex** → `~/.codex/skills/copy-studio/`
- On Windows, `~` is `C:\Users\<you>`.

For the `/copy-studio` slash command, also copy `commands/copy-studio.md` into `~/.claude/commands/`.

## Dependencies — five skills you install yourself

Copy Studio is an **orchestrator**. It does not contain the five skills it drives, and it does not
redistribute them — they are separate projects by other authors, each under its own license:

| Stage | Skill it calls |
|---|---|
| 1. Strategy | `brainstorming` |
| 2. Framework | `writing-plans` |
| 3. Draft | `copywriting` |
| 4. Polish | `copy-editing` |
| 5. De-AI | `humanizer` — https://github.com/blader/humanizer |

**Install them separately**, from wherever each one is distributed, into the same skills directory
(`~/.claude/skills/` or `~/.codex/skills/`). Copy Studio invokes them by name, so it works with
whatever version of each skill you have. Missing one? Then the stage that calls it can't run —
Copy Studio won't substitute its own.

Stage 6 (localization) is optional and needs a localization skill of your own.

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
> ✅ Approved, continue · ✏️ Change something · ⏪ Redo this stage · ⛔ Stop here

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

```
copy-studio/
├─ README.md                you are here
├─ SKILL.md                 the skill: stages, gates, recipe library, self-checks
├─ commands/copy-studio.md  optional /copy-studio slash command
├─ agents/openai.yaml       Codex agent interface metadata
└─ references/
   └─ channel-calibration-template.md   scaffold for your fact base + samples
```

## License

MIT — see [LICENSE](LICENSE).
