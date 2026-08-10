---
name: copy-studio
description: "Use to run the full end-to-end marketing-copy workflow as one staged pipeline — strategy → framework → draft → polish → de-AI — pausing for the user's approval between every stage. Trigger when the user wants to take a piece of copy (social-media post, comment reply, PPT/deck, landing page, ad, email) from scratch all the way to a finished, human-sounding draft, or says things like 'run my copy workflow', 'full copy pipeline', 'take this from brief to final', 'brainstorm then write then polish', or names several of these stages together. It orchestrates the brainstorming, writing-plans, copywriting, copy-editing, and humanizer skills in sequence with confirmation gates, and — when the finished copy must ship in a language other than the one it was written in — localizes it via a localization skill as an optional final step. For a single stage only (just write, just polish, just de-AI, just translate), use that individual skill directly instead."
compatibility: "Orchestrator only — it bundles none of the skills it calls. Install these five separately, from their own sources: brainstorming, writing-plans, copywriting, copy-editing, humanizer. Optional: a localization skill for Stage 6, and any domain skills you route to for specific artifacts."
version: "2.0.0"
---

# Copy Studio — staged marketing-copy pipeline (5 stages + recipe library + optional localization)

## Purpose

Run one marketing-copy job through five stages in order, **stopping after each stage for the user to approve or edit before the next begins**:

1. **Strategy** (via `brainstorming`) — goal, target user, fears/pains, desires/selling points, result-oriented value proposition
2. **Framework** (via `writing-plans`) — the section/slide/post structure, each block tied to a pain or desire
3. **Draft** (via `copywriting`) — write the actual copy on that framework
4. **Polish** (via `copy-editing`) — the Seven Sweeps line edit
5. **De-AI** (via `humanizer`) — remove AI tells, match a human/brand voice → final deliverable

**Plus an optional final step:** when the finished copy must ship in a language **other than the one it was written in** — a German FB group, a Japanese landing page, a Spanish Instagram thread — a sixth step **localizes** it via a localization skill. **Translation happens ONLY here — Stages 1–5 have no translation step, so their output stays in the source language; the target language first appears at Stage 6.** It is conditional (skip it when the deliverable is already in its target language) and localizes **only to the channel's language(s), locked at Stage 0 — never a default full-language fan-out** for a single-channel piece. See *Working vs deliverable language* and *Stage 6*.

It is for marketing copy of many kinds — community posts and comment replies, social captions, landing-page value modules and full pages, deck slides, ads, emails, and more (see *Output recipe*). The point of merging these skills here is one entry point, one carried-through strategy, and a guaranteed review gate between stages — not a faster auto-run.

**Three principles run through everything below — #1 is the soul of every piece of copy:**
1. **Result-oriented is the spine — EVERY piece of copy follows it, whatever the type or channel.** Work the chain every time: **target user → their fear / pain → their desire / selling point → land on the result: tell and SHOW them the concrete benefit and value they get**. Never a feature list. The copy type / recipe only decides the *shape*; this chain is what fills it.
2. **The copy is the deliverable.** The gates, the framework, and any image / visual direction all exist to serve the words. When in doubt, spend the effort on the copy.
3. **General process, brand-tuned output.** The five-stage *process* is general-purpose. The **house voice**, the **domain routing**, and the **calibration samples** are yours to supply — see *Bring your own brand reference* below. This skill ships with no brand baked in.

## Bring your own brand reference (read before first use)

This skill deliberately contains **no brand facts, no product stats, no prize/reward figures, and no verbatim sample copy** — those are specific to whoever runs it, and inventing them is the single worst failure mode in marketing copy. Before real work, create your own reference files under `references/` and point this skill at them:

- **A fact base** — the only citable source for your product's stats, capabilities, URLs, pricing, and any program/reward figures. Rule: quote it verbatim, never round, never re-derive from memory, and mark anything absent as `TBD` instead of guessing.
- **A channel calibration file** — 2–3 approved, real samples per channel you actually ship to (landing module, community post, comment reply, deck slide, caption, email). These teach shape and voice far better than any description.

`references/channel-calibration-template.md` in this repo is an empty scaffold for both. Everywhere below that says *"cite your fact base"* means that file — **not** the model's memory. If you have no fact base yet, every number in a draft must be marked `TBD` and surfaced at the gate.

## Working vs deliverable language — covers the whole pipeline, read this first

Two layers, treated separately. Set both at Stage 0; the defaults below suit a team whose working language differs from its market's language (adjust to your own setup).

- **Working layer (everything you say to the user / their reviewers).** One language throughout — Stage 0 intake, the Stage 1 brief, the Stage 2 outline, every gate menu, the reasoning behind an angle, self-check notes, narration. Default: the language the user is talking to you in.
- **Deliverable layer (the copy that actually ships).** The audience's language. If the channel's audience speaks the working language, both layers coincide and there's nothing special to do.
- **When the deliverable must ship in a third language → run Stages 1–5 in the source language, and only then localize at Stage 6.** Do the strategy, framework, draft, polish, and de-AI work in one source language, land an approved master, *then* hand it to a localization skill for **localization, not literal translation**: per-market search intent, consistent terminology, brand voice, per-language length and format. The result-oriented spine and the voice get built once, in the master.
  - **⚠️ Never skip the source-language master just because you know the final language.** Writing straight into the target language from Stage 1 loses the strategy work and produces translationese.
  - **⚠️ Target language = the channel's language, locked at Stage 0 — not a default full set.** A single-channel piece (one comment / post / ad / page) ships in **one** language: replying to a Spanish post produces Spanish only. Multi-language fan-out belongs to site-wide, multi-market content (blog, SEO metadata, UI strings) — applying it to one comment and emitting 17 versions is a bug. Multi-language requires that the job itself spans markets, or that the user asked.
- **Attach a working-language note to every deliverable.** When you present copy in a language a reviewer may not read, put a short note beside it: what this line is doing and why it's written that way. The note is **support** — it never replaces or edits the deliverable.

This section overrides any language convention implied elsewhere in this file.

## Scope — what this supports

Any marketing copy that ships to a named channel. The recipe library below covers: landing-page value module cards, full landing pages, community seeding posts, comment replies (invite · contest · creator recruitment · support), social captions per platform, deck slides (launch · single-product spotlight · partner/KOL), ads, emails, and image-heavy template emails. Anything not in the library gets its six fields filled live (see *Fallback*).

## When NOT to use

- The user wants **one stage only** ("just polish this", "just write a headline", "de-AI this") → invoke that single skill directly.
- It is a software/feature task → use `brainstorming` and `writing-plans` in their native code mode, not this pipeline.

## Core rule: staged, confirm between stages

Never run all five stages in one pass. After every stage, present the output and **STOP**. Do not start the next stage until the user responds. Stages 1 and 2 especially need the user's judgment — that is where strategy gets locked in, and silently guessing it wastes the whole pipeline.

**The strategy gate is a HARD stop — no exceptions, not even for a one-line comment.** You may NEVER present a later stage's output in the same message where you first propose the strategy. Concretely: the turn where you show the Stage 1 strategy (for a small unit, the compressed strategy+framework) contains **no draft, no candidate copy, no finished deliverable** — it ends at the gate and waits. Producing the framework/draft/polished copy before the user has approved the strategy direction is the #1 failure of this skill: it means you decided the angle for them and raced to a deliverable they never signed off on. If you catch yourself about to output both the strategy and the copy in one turn, stop and output only the strategy.

## Reframing brainstorming & writing-plans for copy (read this — it is load-bearing)

`brainstorming` and `writing-plans` are written for **software** work. Used as-is on copy they will talk about architecture, write test tasks, save specs to a docs path, and try to `git commit`. That is wrong here, and the commit will fail because this is not a code repo. When you invoke them, **override their defaults** with the frames below. You are borrowing their *thinking discipline* (one question at a time; a structured outline before writing), not their code machinery.

For both: **no architecture/components/data-flow/testing language, no code blocks, no test frameworks, no file paths as tasks, no git commits, and no auto-transition to the next skill.** Keep artifacts inline in the conversation; save to a file only if the user asks. STOP at the gate instead of chaining onward.

## Stage 0 — Intake (you do this directly, before Stage 1)

In one short exchange, lock the logistics so the rest runs clean:

- **Copy type (→ output recipe):** which artifact — landing-page value module card / full landing page / community post / comment reply (invite · contest · creator recruitment · support) / social caption / deck slide / ad / email / template email / other. For social, note the platform (X / LinkedIn / Instagram / Facebook / Reddit / a regional platform). This picks the **recipe** Stage 3 fills; if the type isn't in the library, fill the six-field template live and confirm at the Stage 3 gate.
- **The asset & goal in one line:** e.g. "acquisition post for feature X", "selling-points deck for sales", "traffic landing page hero + sections".
- **Scope:** a single small unit (one card / post / comment / caption / ad) or a whole page / deck / campaign? This sets **how heavy Stages 1–2 are** — lightweight/inline for a small unit, full multi-turn for a big one — but Stages 1–2 (the result-oriented core) **always run; never skip them**.
- **Working language + deliverable language** (see that section): lock the target language *by channel* at intake, since it decides whether Stage 6 runs at all and into which language. Single channel = single language.
- **Source material:** product brief, feature notes, screenshots, prior copy, reviews/voice-of-customer — or "infer conservatively from the product name/category".
- **Grounding rule (state it back):** every claim must trace to the source; mark gaps as `TBD` rather than inventing. These drafts may go to a stakeholder, so fabrication is not acceptable. Reusable product facts come from **your fact base** (see *Bring your own brand reference*) — cite that file, never recalled figures.

Then say which stage you're starting at (Stage 1 by default, or a later stage if the user already has a brief/draft — see *Entering mid-pipeline*), and begin.

## The stages (five core + optional Stage 6 localize)

### Stage 1 — Strategy  ·  invoke `brainstorming`
Frame it: *"This is marketing copy, not software. The 'design' you are producing is a **copy strategy brief**."* Drive brainstorming's one-question-at-a-time dialogue and its 2–3 alternative *angles* (positioning, not architecture) toward a brief that nails:

- **Goal** — acquisition / explain the value / drive traffic / convert / educate (pick the real one).
- **Target user** — a specific segment, not "everyone".
- **Fears = pain points** — what goes wrong, what they're stuck on, what they're afraid of.
- **Desires = selling points** — what they want to achieve, feel, sell, or prove.
- **Result-oriented value proposition** — the value/benefit *shown* to the user ("you get / you avoid / you can now…"), never a feature list.

**Gate:** present the brief, get approval or edits. Do not proceed to Stage 2 on your own.

### Stage 2 — Framework  ·  invoke `writing-plans`
Frame it: *"The 'implementation plan' here is the **copy framework / outline** for this channel — not code tasks."* Produce a block-by-block structure (sections for a landing page, slides for a deck, post beats for social) where **each block names its job, the one pain or desire it carries (drawn from the Stage 1 brief), the result-oriented message, and an approximate length/format** for the channel. Map the through-line (hook → value → proof → CTA, adapted to the channel). The Stage 1 brief is the spine — every block must trace back to the goal/user/pain/desire. For a landing page the framework is the ordered list of **modules** to spec; for a deck, the **slides**; for social, the **post angles**. Stage 3 then fills each block using its **output recipe**.

**Gate:** present the framework, get approval or edits.

### Stage 3 — Draft  ·  invoke `copywriting`  (or a domain skill — see routing)
Write the real copy on the approved framework, in the source language, **producing the type's output recipe** — for a landing page that means polished **copy** for every module (title options + one description sentence) first, plus supporting image direction. Apply copywriting's principles: benefits over features, specificity over vagueness, customer language, one idea per block. Keep the grounding rule: mark anything unsupported `TBD`; cite facts from your fact base.

**Domain routing.** If you maintain skills for specific artifacts, route to them instead of generic copywriting — e.g. a structured product-overview skill for catalog rows, or a full-page architecture skill when a brand-new page needs its whole structure (hero / how-it-works / FAQ / CTA) rather than module copy. List your own routes here. Anything unrouted → stay in `copywriting`.

**Stage 3 pre-show self-check** (run these binary checks silently before showing the draft; fix any FAIL in place — do not show the checklist):
1. **Voice** — plain, confident, concrete, benefit + the mechanism that earns it; zero hype words (revolutionary / seamless / effortless / unleash / game-changing).
2. **Grounding** *(hard stop)* — every number, claim, and capability traces to the fact base; unsupported claims marked `TBD`, not guessed.
3. **Shape** — matches the type's six-field recipe, not generic prose (required beats present, none bolted on).
4. **Length** — inside the type's size budget; not padded.
5. **No AI tells** — no em-dash overuse, forced rule-of-three, "not X but Y", AI-vocab (delve / leverage / robust / elevate / foster).
6. **Copy-first** — words lead; image/layout direction is secondary, or "none" for words-only types.
7. **Channel rules** *(hard stop)* — Reddit: zero links/hashtags, no rewards in the main comment; emoji only on social/community; clean output (mark emphasis with 【】, never raw HTML).
8. **Language** — the deliverable is in the channel's language; each deliverable carries its working-language note; all conversation with the user stays in the working language.

Never ship a draft that fails check 2 or 7. If a FAIL needs a missing fact, mark `TBD` and surface it at the gate.

**Gate:** present the draft, get approval or edits.

### Stage 4 — Polish  ·  invoke `copy-editing`
Run the Seven Sweeps over the draft (clarity, voice/tone, so-what, …). Enhance, don't rewrite; preserve the message and the on-strategy claims from the brief.

**Gate:** present the polished copy, get approval or edits.

### Stage 5 — De-AI  ·  invoke `humanizer`
Remove AI tells and make it sound like a real person/brand. **If the user has a voice sample** (prior posts, a brand guide, a past page that sounds right), feed it to humanizer for voice calibration — otherwise use its default natural-voice mode. If no localization is needed, this is the final deliverable: present the finished copy plus a one-line note of what changed from the polished version, and attach the working-language note alongside it so reviewers can read it. **If the deliverable must ship in another language, this is the source-language master that feeds Stage 6.**

### Stage 6 (optional / conditional) — Localize
**This is the ONLY step where translation happens. Stages 1–5 run in the source language; a third language appears only here.**

**Trigger test (all must be YES):**
1. Is the Stage 5 master's language ≠ the channel's language?
2. Is the channel's language outside the set where source = target?
3. If both YES → run Stage 6, localizing **only into that channel's language**.

**Skip it (Stage 5 is final) when** the deliverable already ships in its target language.

**The target language comes from the channel, not from a default set:**
- Single-channel deliverable (one comment / post / ad / page, one language market) → **produce that one language only**.
- **Never** fan out to a full language set just because the user didn't name one — that default belongs to site-wide, multi-market content (blog, SEO metadata, UI strings). Emitting 17 versions of one community reply is wrong.
- Multi-language requires that the job itself spans markets, or that the user named the set. Lock it at Stage 0.

Once the target language is confirmed: take the **final, approved copy from Stage 5** and hand it to your localization skill, which does **localization, not literal translation**: per-market search-intent keywords, consistent domain terminology, brand voice, per-language length/format adaptation, with its own QC. Frame it: *"Here is finished, on-strategy marketing copy — localize it into [the channel-locked language], preserving the result-oriented message and voice."* Pass the **channel-locked target language(s)** (from Stage 0) and the relevant slice of the **Stage 1 brief** (target market / audience) so market fit stays on-strategy.

- **Do NOT re-run humanizer on the localized text** — the localization step owns target-language voice and machine-translation-tell removal; running a source-language de-AI pass over it would only corrupt it.
- **Each localized deliverable still gets its own working-language note**, plus any terminology uncertainties the localization step flagged.
- Localization never publishes — the copy comes back for review.

**Gate:** present the localized copy per language (with its note), get approval or edits. This is the final deliverable when localization was needed.

## Context hand-off (what must travel between stages)

The Stage 1 brief (goal / user / fears / desires / value prop) is the spine of the whole run. **Restate the relevant slice of it when you invoke each later stage**, so the sub-skill stays on-strategy instead of drifting. The framework feeds Stage 3; the draft feeds Stage 4; the polished copy feeds Stage 5. **When localization is needed, the Stage 5 final copy feeds Stage 6, together with the target language (Stage 0) and the brief's target-market slice** — Stage 6 must localize the approved message, never drift off it or introduce a new claim. Never let a later stage quietly introduce a claim the brief didn't support.

## Confirmation-gate format

After each stage, end with this compact menu (in the working language) and then wait:

> **Stage N complete.** [the output above]
> ✅ Approved, continue to Stage N+1 · ✏️ Change something (tell me what) · ⏪ Redo this stage · ⛔ Stop here

Do not narrate the next stage or start it until the user picks.

(After Stage 5: if the deliverable needs another language, "continue" means Stage 6 localization; otherwise Stage 5 is final and the menu shouldn't mention Stage 6.)

## Entering mid-pipeline

The user often won't start at zero. Match the entry point to what they already have:

- Have a clear brief already → start at **Stage 2**.
- Have a draft, want it finished → start at **Stage 4** (polish → de-AI).
- "Just take the AI smell off this" → **Stage 5** only (and at that point prefer invoking `humanizer` directly).
- Have final, approved copy and just need it in other languages → jump to **Stage 6** (or, for a pure one-off translate with no pipeline context, invoke the localization skill directly).

**Scale to the job — right-size the *ceremony*, never drop a *stage*.** "Lightweight" means fewer turns and fewer gates, **NOT fewer stages.** Every piece — even a one-line comment — runs all five: Stage 1 strategy → 2 framework → 3 draft → **4 polish → 5 de-AI**. Stage 3 is **never** the finish line: a raw draft is not a deliverable until it has been polished (Stage 4) and de-AI'd (Stage 5). Declaring a small unit "done" at Stage 3 is a bug — polish + de-AI are what turn a draft into finished copy.

**How small units differ from big ones — only the gating. "Fewer gates" means fewer than five; it NEVER means one, and it NEVER means folding the strategy in with the deliverable.**
- **Big unit** (whole page / deck / campaign): full multi-turn Stage 1 and Stage 2 dialogue, then a **separate gate after every stage** (1→2→3→4→5, five gates).
- **Small unit** (card / post / comment / caption / ad): you may compress the *dialogue* (Stages 1–2 become a few lines of strategy + a one-line structure instead of a multi-turn Q&A), and you may fold the *production* stages (3→4→5, +6 if localizing) into a single presentation of the finished copy. What you may NOT do is skip the first gate. **A small unit still needs at least TWO gates, in two separate turns:**
  - **Gate 1 — direction (STOP here).** Present ONLY the compressed strategy (+ the one-line framework). **Write no draft, show no candidate copy, in this turn.** End at the gate menu and wait for the user to approve or redirect the angle. This gate is mandatory even for a single-line comment reply.
  - **Gate 2 — finished copy.** ONLY after Gate 1 is cleared: run draft → polish → de-AI (→ localize) and present the finished deliverable. If you folded 4–5(–6) into this pass, say so explicitly ("polished + de-AI'd" / "localized") — don't silently skip them and don't stop at the raw Stage 3 draft.
- **The bug to never repeat:** presenting the strategy and the finished copy in the *same* message (e.g. "here's the strategy, framework, and here's the reply"). That runs the whole pipeline before the user confirmed the strategy — exactly what a gate exists to prevent. Strategy and deliverable always live in different turns.

Shrink the number of turns, never the thinking, never the number of stages, and never the Gate-1 strategy stop. Confirm which stages you're running before you begin.

## Output recipe — what each copy type's deliverable actually looks like

The Stage 3 draft must match the **real shape** of the piece you're writing — not generic prose. Instead of a fixed list of channels, every copy type fills the **same six-field recipe**. Write the recipe once (below), then read each library row *as* that recipe. New types don't need a new section — you fill the six fields live and the result becomes a new row. **A recipe is only a *shape*** — what fills every recipe is the spine from Principle 1 (target user → pain → desire → shown value). The recipe gives the parts and length; the spine gives what to actually say.

**Across every type, the copy itself is the deliverable and the priority.** Image direction and slide layout are supporting guidance that serve the words — added only after the copy is locked, never the other way around. House voice throughout: plain, confident, concrete (benefit + mechanism), a real number when there is one, no hype. The one voice exception: **emoji are allowed on social/community only.** Calibration samples come from your own channel reference file.

### The recipe template (six fields — fill these for any type)

1. **Shape** — what the finished piece physically is: the ordered parts and roughly how many (e.g. "title option 1 / option 2 + ONE description sentence"; "hook → what-it-is → 3–4 ✅ bullets → link → question"). This is the skeleton Stage 2's framework fills.
2. **Must-include** — the 1–3 non-negotiable beats this type always carries (e.g. result-oriented value in the title; first-person "found this" register; the one core belief to land). Leave blank if none.
3. **Length & voice** — the size budget and any shift from house voice. Emoji allowed on social/community only.
4. **CTA / link** — what the reader does next and how the link is handled. Some types have no CTA (say so).
5. **Grounding** — *universal, so it's omitted from the library rows below:* every claim traces to source; mark gaps `TBD`; never invent numbers, proof, or capabilities (drafts may reach a stakeholder). **Citable product facts live in your fact base — quote them verbatim, don't re-derive from memory.**
6. **Visual support** *(optional, always secondary)* — only if the type ships with a visual: image direction / slide layout in text logic, added **after** the copy is locked. Words-only types (comment reply, caption) → write "none".

**Two rules that apply to every recipe:**
- **Tracked links/UTMs are user-supplied.** Any type with a link gets a single `[link]` slot — never mark it `TBD`, never invent a URL. *(Exception: Reddit — no link or hashtag in the body; see Reddit rules, which own this override.)*
- **Clean output only — no raw markup.** Never emit HTML tags (`<span style="color:red">`, etc.) or stray markdown inside a deliverable; it renders as clutter. Mark visual emphasis (a highlighted word) with **【】 around the word**, or a short `red: …` note — never inline HTML.

**A/B variants:** when the user wants variants (or there's a real strategic fork), label them `A`/`B`, change exactly ONE testable lever per variant (hook / angle / CTA / segment — not a cosmetic reword), name the lever in one line (e.g. "A = speed angle, B = craft angle"), and cap at 2–3. Ad / caption / email / video cover are the natural A/B candidates.

### Recipe library (one row per known type — read each row through the template above)

| Type | Shape (field 1) | Must-include (2) | Length & voice (3) | CTA / link (4) | Visual (6) |
|---|---|---|---|---|---|
| **Landing-page value module card** *(full spec below)* | title 3–5 words (a second option only on a real fork) + ONE description sentence | result-oriented title; benefit-first + mechanism in the one sentence | one sentence, house voice, no emoji | none (module copy) | image direction (text logic) |
| **Community seeding post** *(full spec below)* | emoji hook → what-it-is → 3–4 ✅ bullets → `[link]` → question | first-person "found this" register, not ad-voice | post-length, conversational, emoji ok | one `[link]` slot | none |
| **Comment reply — community invite** *(full spec below)* | 3–5 sentences, reactive: react to THEIR post → soft bridge → one concrete reason → soft invite | react first; warm host voice; one concrete detail, no slogan-stack | 40–70 words, warm, ≤1 emoji | soft invite + `[link]` | none |
| **Contest / event invite comment** | react to their work → invite to the contest → name the prize → join steps | name the specific contest + prize (from the fact base); **Reddit variant softens promo** | short comment | join steps + `[link]` | none |
| **Creator recruitment comment** | react to their work → invite them to publish → name the reward/program | **Reddit variant drops rewards**, peer-voice | short | publish invite + `[link]` | none |
| **Support / objection-handling reply** | thank → acknowledge concern → your stance → point to the in-product action | calm, respectful, non-defensive; don't over-promise | 3–6 sentences | point to in-product report/feedback | none |
| **Deck slide** *(full spec below — 3 kinds by audience × scope)* | launch: slogan headline + transformation subhead + demo + proof footer · single-product spotlight: product-name headline + subhead + demo + proof (real number or `TBD`) · partner/KOL deck: showcase cards (name + 1 benefit sentence) | one idea per slide; audience × scope matched | no paragraphs; proof uses a real number | usually none | product demo / card grid |
| **Video cover / thumbnail overlay** (on-video text; a different owner from the ad headline) | 2–3 big lines: transformation hook + one standalone value line | second-person "your"; curiosity / before→after gap; ≤4 words per line | very short, bold, legible at thumbnail size; no emoji | none (the video drives the click) | overlays the "after" frame; mark highlighted words with 【】 |
| **Full landing page** | whole page (hero → how-it-works → features → cards → FAQ → CTA) | — | — | — | **→ route to a full-page skill if you have one** |
| **Ad** (Meta/Google) | hook line (survives truncation) + benefit+mechanism + 1 CTA; headline ≤~5 words | hook in line 1; outcome-named headline | platform char limits | one `[link]`/button | optional |
| **Social promo caption** (per platform) | one hook line + brief context + light CTA/hashtags; **each platform gets its OWN caption — never ship one shared across two** | benefit before feature; one idea | sized to platform — some run short + hashtag-heavy, others longer; emoji ok | **platform-dependent: where in-feed URLs aren't clickable (e.g. Instagram), the CTA points to the bio and the `[link]` lives there; elsewhere an inline `[link]` is fine** | optional |
| **Email** | subject + preview (matched pair) → one-idea body → one CTA | one segment, one job (acquire/educate/reactivate); win-back: lead with what changed since they left + one frictionless CTA, don't guilt-trip | benefit-led, no feature dump | one CTA + `[link]` | none |
| **Template email** (image-heavy, fixed blocks) *(full spec below)* | **Full:** hook question → body 3–4 sentences → 3 product images + names → How It Works (transition + zero-barrier line + GIF + 3 steps + CTA) → link. **Compact:** ONE 3–4-sentence paragraph + image spec + link | hook = aspiration ("What if…"), not a feature; body names the product + one-line capability + a **bolded 2–3-scenario** parallel; vary the transition line every send | email house voice, no emoji; concise | `Create Now`-style CTA → `[link]`; all CTAs/names/images point to it. UTM user-supplied | ships WITH visuals — see the full spec |

> **Platform rule for social (load-bearing — a real mistake to avoid):** two social platforms are NOT one channel. Never paste the same caption to both. Where in-feed captions render URLs as plain, **un-clickable** text (Instagram being the common case), the CTA must point to the bio with the tracked link placed there, while platforms that accept inline clickable links get one. Give each channel its OWN tracked link. A **group** post additionally drops hashtags and uses the softer community-seeding register.

### Spelled out in full — the highest-value types

**1. Landing-page value module card (the most common small ask — run Stages 1–2 lightweight/inline, then write).**
The value-card module on a page whose architecture is already set. **The copy is the point.**
- **Copy — the focus, where the work goes.**
  - **Title** — 3–5 words naming the value or outcome (not a feature name). Give one option; give a second only on a real strategic fork framed as distinct *directions* (e.g. a speed angle vs a craft angle).
  - **Description** — ONE declarative sentence, and you only get one: benefit first + the mechanism that makes it true, plain and confident, a real number when supported, no emoji, no hype.
  - Run it through copy-editing + humanizer — this is the deliverable's core and it gets judged first.
- **Wireframe note — support.** A placeholder line for whoever builds the layout.
- **Image direction — support, added after the copy is locked.** Numbered text-logic guidance: ① the main visual's text/slogan ② display priority (what must be biggest/clearest vs auxiliary) ③ concrete example data to show (names, dates, materials, before→after pairs) ④ interaction hints (the buttons/affordances visible in the shot) ⑤ the one core belief the image must land ("you don't start from zero", "this really is achievable"). Keep example data generic unless the user supplies real values.

**2. Community seeding post (a real user sharing, not a brand announcing).**
- **Hook** — emoji + a relatable line, usually a question.
- **What it is** — one or two sentences in a "found this / they built…" register, not ad-voice.
- **✅ benefit bullets** — 3–4, concrete and grounded.
- **CTA + link** — one line; leave a single `[link]` slot for the user's tracked link (do **not** mark `TBD`).
- **Engagement question** — close by inviting a reply.
- Emoji yes, hype no. Match the named platform's length and voice.

**3. Comment reply — community invite (words-only).**
- **Shape** — 3–5 sentences, no headline: ① one specific, genuine reaction to THEIR post (name what they made/asked) → ② a light "you'd fit right in" bridge → ③ one concrete reason the community helps (shared settings, ready-made projects, other members) → ④ a soft invite + where to go.
- **Must-include** — open with ONE concrete physical detail about their work (warm, specific; using their name is fine); warm host voice ("we love seeing this", "we're rooting for you") — genuine, not salesy, not a stiff brand announcement; no stacked slogan-quotes.
- **Length & voice** — 40–70 words; warm, conversational; at most one emoji, only if the thread's tone fits.
- **CTA / link** — one soft invite plus the `[link]` (the user supplies the tracked link; don't mark `TBD`).
- **Visual** — none.

**4. Deck slide — three kinds by audience × scope:** a brand launch slide · a single-product spotlight (product-name headline + transformation subhead + demo + proof, using a real number or `TBD` for something brand-new) · a partner/KOL showcase grid. Shapes in the recipe row above.

**5. Template email (image-heavy, fixed blocks; two variants by placement).**
The deliverable is a **doc = copy + images + link**, handed to whoever lays it out in an email builder. Not free-form prose — it fills a fixed block template. Two variants by how much room the product gets:
- **Full standalone email (5 blocks)** — the whole email is this one product:
  1. **Hook** — one `What if…` question aimed at the aspiration, not the feature. Vary the sentence pattern per send.
  2. **Body (3–4 sentences)** — (1) the value / why it's worth it → (2) name the product + a one-line capability → (3) close with a **bolded 2–3-scenario** parallel ("whether you're …, …, or …").
  3. **3 product images + names** — three finished-result shots showing different styles/scenes, each with a short name.
  4. **How It Works** — the subhead + a **fresh transition line every send** (don't reuse the same "Looks impressive, right?") + a zero-experience reassurance (no prior experience needed; upload → auto-generate → done in minutes) + an operation GIF + 3 steps (adapt the last step to the product) + a CTA button.
  5. **Link** — all CTAs / product names / images point to the landing page with a UTM.
- **Compact shared-email slot (1 paragraph)** — when the product gets only a small slice inside a larger email: ONE 3–4-sentence paragraph (same body discipline: pain/value → product + capability → a scenario line → a zero-barrier close), plus the image spec + link. No separate Hook / How It Works blocks.
- **Handoff specs (both):** state the image dimensions, formats, and size cap your email builder needs, and give each image a short name. **UTM is user-supplied and differs by sending platform — never invent one.** Watch for assets exported from document tools that carry watermarks; get clean originals before handoff.

### Community comments & invites — cross-cutting rules

The comment-style types (community invite, contest invite, creator recruitment, engagement, support reply) are small-unit jobs — run Stages 1–2 lightweight/inline (don't skip the core: who's the reader, their pain/desire, the value to show), then write — and share three rules beyond their rows:

- **Reddit version vs general version.** Produce platform-tuned variants. The **general** version may name prizes, rewards, and programs explicitly (it's promo). The **Reddit** version strips overt promo and stays soft peer-voice ("you should share it", "it's a community where people post"), because Reddit communities reject ads. On Reddit, default to the soft variant — see *Reddit rules* for the hard constraints.
- **Language.** The reply's language = the language of the post being replied to. A post in a third language → build the source-language master through Stages 1–5, then Stage 6 localizes into that one language only. Never write straight into the foreign language, and never fan out to multiple languages.
- **Grounded rewards only.** Quote any prize / credit / program specifics from your fact base — never invent or change a number or prize; mark unknowns `TBD`.
- **One concrete detail, no slogan-stacking.** Open with ONE concrete, physical detail about their work ("the dragon head and rows of oars", "the wings and that pop of red") — warm and specific. **Using their name is fine.** The clutter to avoid is stacking abstract slogan-quotes from their caption or piling on multiple references. Then a warm line + the invite + link.

### Reddit rules (hard constraints — break them and the content gets removed + the account banned)

Reddit is the highest-risk channel: its filters read promotional signals aggressively, removals frequently arrive together with an account ban, and new accounts are treated with the least tolerance. For any Reddit post or comment:

- **No links, no hashtags in the body.** Link/hashtag content reads as marketing and gets filtered — zero of both. (This overrides the `[link]`-slot rule above: on Reddit there is no link in the body.)
- **Subreddit targeting.** Case/project sharing belongs in a brand's own official subreddit. Do **not** run strong solicitation or contest pushes in general category subs — strict mods, anti-promo norms, spam-flag risk. If the person you want to recruit is in a category sub, don't recruit there — reply with a pure compliment (no ask), or save the invite for your own sub or DMs.
- **Rewards stay out of the brand's main comment.** No gift-card/credit/prize mentions there. If a reward must surface, the original poster self-replies under their own post with a soft one-liner.
- **New accounts: extra caution** — low frequency, no promo signals, no links or tags.
- Keep your own evidence log (what got removed and why) in your channel reference file rather than here.

### Reply routing & batch replies

**Define the goal first:** most community comments aim at one specific action (follow the brand, share their work in your community, publish on your platform). Name it before writing, and include the user-supplied `[link]` that serves it.

**Keyword / signal → reply recipe** (route each community post before writing):
- contest / seasonal signal (a holiday, an event, a challenge tag) → **contest invite**
- "where do I get the file / free files / how did you make this" → **community invite**
- strong work by an active creator not yet on your platform → **creator recruitment**
- pain / friction / complaint / "it doesn't work" → **support / objection-handling**
- praise-worthy work but no ask fits → **engagement** — one warm line, no pitch, keep presence

**Batch comment replies — replying at scale:** given a list of posts, (1) route each by the map above; (2) write each reply individually — vary the opener and react to THAT specific post (never paste one template across many: copy-paste reads as spam and gets removed/banned); (3) obey each post's channel rules (Reddit = no link/hashtag; category sub = compliment-only); (4) match each reply's language to its post, and attach the working-language note to each. Output as a per-post list (post → finished reply + note). The core still applies per reply (the poster = the reader; their post = the context/pain; your reply shows the value) — just inline, not a multi-turn dialogue per post.

### Fallback — when the type isn't in the library yet

Do **not** stop, and do **not** shoehorn it into the nearest existing recipe. Fill the same six template fields live from Stage 0 intake and (if run) the Stage 1 brief: infer **Shape** from the asset, set **Must-include** from the goal/pain, apply house voice (emoji only if it's social/community), default any link to a `[link]` slot, keep the universal **Grounding** rule, add **Visual support** only if the piece ships with a visual (else "none"). State the inferred recipe back to the user at the Stage 3 gate for a quick confirm; once approved, capture it as a new one-line row here so the next job reuses it. Also name the channel's 2–3 **native constraints** (char-truncation point, SEO front-loading, QR-vs-URL for print, where a link can or can't live) — the six fields give shape, this gives fit. **Emoji tie-breaker:** social/community = emoji ok; everything else (email, print, deck, landing, video, description) = no emoji unless the user asks. **Extensible by default: the library documents what's known; the template handles everything else.**

## Self-check before declaring the run done

- **All five stages' work happened — Stage 3 was NOT the finish line.** Even a small unit got polish (4) + de-AI (5) applied before it was called final; if 4–5 were folded into the draft pass, that was stated, not silently skipped.
- **The strategy gate was honored:** the user approved the direction *before* any draft/candidate copy was shown. Strategy and finished copy were in **different turns** — never presented together in one message. (Big unit = a gate after every stage; small unit = ≥2 gates, Gate 1 = direction-only STOP, Gate 2 = finished copy.)
- `brainstorming` and `writing-plans` were reframed for copy — no code/spec/test/commit artifacts leaked in.
- The Stage 1 brief is visibly the spine of the framework, draft, and final copy.
- Each draft passed its **Stage 3 pre-show self-check** (voice · grounding · shape · length · no-AI-tells · copy-first · channel rules · language).
- Every number and claim traces to the fact base; nothing was recalled from memory or invented, and gaps are marked `TBD`.
- Artifacts that have their own domain skill were routed there instead of generic copywriting.
- **Stages 1–5 stayed in the source language — no translation crept in early.** The target language appeared **only at Stage 6**.
- **Stage 6 triggered correctly and with the right language scope:** only when source ≠ channel language; localized **only** into the channel-locked language (single channel = single language); no default full-set fan-out. If the deliverable was already in the channel's language, Stage 5 was final and Stage 6 did **not** run.
- If Stage 6 ran, it was localization (not literal translation), each language got its own gate + note, and humanizer was **not** re-run on the localized text.
