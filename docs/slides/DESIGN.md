---
version: alpha
name: Plex Swiss Grid
description: >-
  Swiss Modern slide system for Korean technical talks about code.
  White paper, 12-column hairline grid, IBM Plex Sans KR + IBM Plex Mono,
  one accent color. Code panels are the hero. Built on frontend-slides.
colors:
  primary: "#0a0a0a"          # ink: text, rules, panel borders
  neutral: "#ffffff"          # paper: slide background
  accent: "#ff3300"           # signal red (default accent)
  accent-cobalt: "#1638c7"    # week06 variant (bsize-cast v2)
  muted: "#6b6b6b"            # labels, slide numbers, captions (cobalt variant: #5e5e5e)
  grid: "#ebebeb"             # background column lines, drawn at 60% opacity
  panel: "#f7f7f5"            # code panel fill (cobalt variant: #f3f5fc)
  code-comment: "#9a9a9a"
  code-dim: "#b4b4b4"
  highlight: "rgba(255,51,0,.13)"        # current code line fill
  highlight-cobalt: "rgba(22,56,199,.13)"
  terminal: "#14171c"         # machine output panel (red variant only)
  terminal-text: "#d5d1c9"
  terminal-err: "#ff6a3d"
  terminal-warn: "#e0a458"
  terminal-ok: "#8fbf8f"
  terminal-dim: "#7e858f"
typography:
  # Reference sizes at a 1440 x 900 viewport. The runtime values are the
  # clamp() expressions in "Implementation contract" below; those win.
  display:
    fontFamily: IBM Plex Sans KR
    fontSize: 69px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.02em
  headline:
    fontFamily: IBM Plex Sans KR
    fontSize: 33px
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: -0.015em
  thesis:
    fontFamily: IBM Plex Sans KR
    fontSize: 23px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: -0.01em
  subtitle:
    fontFamily: IBM Plex Sans KR
    fontSize: 22px
    fontWeight: 400
    lineHeight: 1.6
  punch:
    fontFamily: IBM Plex Sans KR
    fontSize: 19px
    fontWeight: 500
    lineHeight: 1.5
  body:
    fontFamily: IBM Plex Sans KR
    fontSize: 17px
    fontWeight: 500
    lineHeight: 1.5
  code:
    fontFamily: IBM Plex Mono
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: IBM Plex Mono
    fontSize: 11.5px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: 0.02em
  eyebrow:
    fontFamily: IBM Plex Mono
    fontSize: 11.5px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: 0.2em
rounded:
  none: 0px
  full: 9999px                # only the title dot, nav dots, step dot
spacing:
  slide-padding: "clamp(1rem, 4vw, 4rem)"
  content-gap: "clamp(0.5rem, 2vw, 2rem)"
  element-gap: "clamp(0.25rem, 1vw, 1rem)"
  panel-gap: "clamp(.6rem, 1.6vw, 1.4rem)"
  grid-columns: 12
  border-strong: 2px
  border-hair: 1px
components:
  slide:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.none}"
  head-band:
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    borderColor: "{colors.primary}"
  code-panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.primary}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    borderColor: "{colors.primary}"
  code-panel-accent:
    borderColor: "{colors.accent}"
  machine-panel:
    backgroundColor: "{colors.terminal}"
    textColor: "{colors.terminal-text}"
    typography: "{typography.code}"
    borderColor: "{colors.primary}"
  eyebrow:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.neutral}"
    typography: "{typography.eyebrow}"
    padding: 0.35em
  punch-line:
    textColor: "{colors.primary}"
    typography: "{typography.punch}"
  takeaway-box:
    backgroundColor: "{colors.neutral}"
    borderColor: "{colors.primary}"
    padding: 1.2rem
  progress-bar:
    backgroundColor: "{colors.accent}"
    height: 4px
---

# Plex Swiss Grid

Source decks (all made with the `frontend-slides` skill, then hand-tuned):

| Deck | Accent | Runtime | Slides | Note |
|---|---|---|---|---|
| `SW-AI-C/study/week04-array-in-c.html` | red | scroll-snap | 7 | The origin. 起承轉結 story |
| `study/week05/oop-in-c.html` | red | scroll-snap | 7 | week04 reused. Light panel caption, SVG map, flow diagram |
| `bsize-cast-v2.html` (week06 malloc-lab) | cobalt | stage | 6 | Newest. Speaker notes, per-element steps |

When the decks disagree, this file names both as variants. Pick one per deck.
Do not mix them in one deck.

## Context

The fixed setting of every deck in this system. The user said: "발표 맥락이나
장소/청중은 다 똑같아." So these values are defaults, not questions. Change a
row only when the user says so. Source: the user's own words in past sessions
(2026-09-16 to 2026-10-07), checked against claude-mem. A row marked
`unknown` has no evidence yet; ask once, then fill it.

| Field | Value | Design consequence |
|---|---|---|
| Event | Weekly Thursday talk at Krafton Jungle: troubleshooting from this week's work, in a refined WIL-like form, lead-first (두괄식, from the official notice) | One deck per week. Slide 00 head label: `Krafton Jungle · Week NN`. State the conclusion early |
| Audience | Krafton Jungle people who study C together. Wide level spread; more than half already know the topic | Do not explain the exercise. Lead with the surprise; define a domain macro (e.g. `GET_SIZE`) on the slide when it is not general C |
| Language | Korean speech and prose; code, identifiers, tool output in original form | Plex Sans KR + Plex Mono; `keep-all` breaking |
| Time limit | 2 minutes, every week. No Q&A time | 6 ± 2 slides. The 2 minutes is background, not a gate: notes are a suggested script, light weight. Do not cut content only to fit a timer |
| Speaker | user, alone, from his own script; calm speaking pace | In-browser editing is required: he revises the slides himself after every build, and that live loop is the main work. Speaker notes (`N`) stay, as a light suggestion he rewrites |
| Display | Large monitor in a bright lecture room | White paper theme. Accent and code must hold in bright ambient light. Test at 1280 × 720 and 1920 × 1080 |
| Room | Same lecture room every week. Size and head count `unknown` | Code font ≥ `.95rem` at 1280 × 720 |
| Presenter screen | Mirrored or extended, and whose laptop runs the deck: `unknown` | Until known, the notes panel stays hidden by default and opens only on `N` |
| Network | `unknown` | Single HTML file. Google Fonts is the only external request; the deck must still read with fallback fonts |
| Story type | Experiment / debugging story (실험형 · 삽질 서사형). "2분이지만 발표는 스토리텔링" | Use the narrative template in Layout. Most peers present explanation-style; this deck does not |
| Reuse | The deck is also the source of his WIL and blog post | Each slide must read without the speaker. Keep notes in the file, not only in speech |
| Deadline | Deck ready by the afternoon before the talk | Leave the last session for rehearsal, not for design |
| Format | Single self-contained `.html`; published decks get a card on `benjohnbill.github.io/index.html` | No build step; relative paths only |
| Evidence | Tool-output panels come from real gcc/gdb runs (practice so far, not a rule he stated) | Caption side tag `실제 기록` |

## Overview

A technical talk in Korean for peers (Krafton Jungle cohort), 2–5 minutes,
on a large monitor in a bright lecture room. The subject is always real code and real tool output:
gdb, compiler warnings, `nm`, test traces. The audience must read code
from the back of the room.

Personality: calm, exact, editorial. Swiss Modern: white paper, black ink,
a visible column grid, one accent. No illustration, no gradient, no shadow
on slides. The look says "this is evidence", not "this is a pitch".

The code panel is the hero of every content slide. Text exists to tell the
viewer where to look in the code, and what it means.

## Colors

- **Ink (#0a0a0a):** all text, rules, and panel borders.
- **Paper (#ffffff):** the only slide background.
- **Accent:** one color per deck, used as a pointer: "look here".
  - **Signal red (#ff3300):** default. Strong on monitors.
  - **Cobalt (#1638c7):** week06 variant. Chosen to vary the color from
    week04, not for a technical reason. Lemon and yellow were rejected as a
    matter of taste.
- **Muted gray (#6b6b6b):** head/foot bands, slide numbers, side labels.
- **Grid (#ebebeb at 60%):** the 12-column hairlines behind every slide.
- **Panel (#f7f7f5, cobalt variant #f3f5fc):** code panel fill.
- **Terminal set (#14171c base):** only for compiler and tool output, red
  variant only. It marks "the machine said this", apart from source code.
  The cobalt variant drops it and shows tool output in the light panel too.

Contrast: red on white (and white on red) is 3.67:1, below WCAG AA 4.5:1
for small text. Use red only on bold or large text, and prefer the outline
(`.ghost` / `.kicker`) eyebrow over the filled one. Cobalt on white passes.

Accent budget: one or two accent marks per screen. A bold word in the
thesis, one hit in the code, one punch marker. More than that and nothing
stands out.

## Typography

Two families, both from Google Fonts, nothing else:

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

- **IBM Plex Sans KR:** every Korean or prose text. Headlines 700, body 400–500.
- **IBM Plex Mono:** code, head/foot bands, slide numbers, eyebrows, captions.
  Stack it as `'IBM Plex Mono', 'IBM Plex Sans KR', monospace` so Korean
  inside code falls back to Plex Sans KR, not to a system font.

Rules:

- All sizes are `clamp()`. Code sizes use `min(vw, vh)` in the middle term,
  so a short screen shrinks the code instead of cutting it.
- Korean breaks by word: `word-break: keep-all; text-wrap: pretty` on h1, h2,
  `.sub`, `.punch`, `.takeaway`, list items, band text. `text-wrap: balance`
  on h1 and h2.
- `em` inside h1/h2 is not italic: `font-style: normal; color: accent`.
- Never uppercase identifiers. `len()`, `copy1`, `study-cli`, `main.c` are
  names; uppercase makes them different names. Uppercase is allowed only for
  plain English eyebrow words (TROUBLESHOOTING, INPUT, EXPECTED).

## Layout

Every slide has three bands:

```
┌ head ────────────────────────────── label ········ num ┐  2px ink rule below
│                                                         │
│  slide-content (flex column, vertically centered)       │
│    h2.thesis        ← the one sentence of this slide    │
│    panels / work / two / flow …                         │
│    p.punch          ← the conclusion line               │
│                                                         │
└ foot ─────────────── source path ··········· meta ──────┘  1px ink rule above
```

- **Head band:** left = section label (`起 · 내 len() 을 만들다`,
  `gdb · coalescing-bal.rep`), right = slide number in mono gray. The number
  is a count, not decoration: small, once. Format `02` (scroll-snap decks)
  or `02 / 06` (stage deck).
- **Thesis at the top.** The key sentence of the slide is `h2.thesis` under
  the head band. Never put it in the foot band: the foot is the smallest,
  palest place and inverts the hierarchy.
- **Foot band:** the source file path or command that the slide shows
  (`porting/08_bubble_sort.c`, `break mem_sbrk · bt 3 · track`).
- **Background:** 12-column hairlines on `.slide::before`, z-index 0. Every
  content element sits at z-index 2 so the lines never cross text.
- **Two columns align at the top edge.** Swiss grid discipline: columns use
  `align-items: start` or `stretch`, never `center`.
- Grid children that hold code get `min-width: 0`, so a long code line
  cannot push the grid wider than the screen.

Layout patterns (pick per slide):

| Pattern | Grid | Use |
|---|---|---|
| Title | flex column, dot at right | Slide 00. Eyebrow, h1, rule, sub |
| Mirror | `1fr 1fr` | Quiz. Two symmetric code snippets, answer hidden until step 1 |
| Work | `1.72fr 1fr` (src / ref) | Main story. Left = the code being discussed, large. Right = reference (header, expected output), small and quiet, stays in place across slides |
| Two | `1fr 1fr` or `1fr 1.3fr` | Code next to its consequence (source ↔ compiler error) |
| Trio | `1fr 1fr`, left spans 2 rows | One tall gdb panel + two short panels stacked |
| Flow | 5 columns: box, arrow, box, arrow, box | Compile and link diagram. Arrows are mono text; the link arrow is a 2px accent line |
| Map | inline SVG, `max-height: 62vh` | Structure diagram shown for ~5 seconds. Strokes use `currentColor`; accent only on the one key node |
| Takeaway | single bordered box, `max-width: 58ch` | Last slide. A mono kicker + 2–3 lines |
| Closing (stage) | two h1 lines, second in accent | Last slide of the stage variant, plus "질문 받을게요 · 감사합니다" |

Narrative template (both 7-slide decks follow it):

| # | Role | Head label |
|---|---|---|
| 00 | Title | `Krafton Jungle · Week NN` |
| 01 | Hook: a quiz or a structure map | `들어가기 전에 · 퀴즈 하나` |
| 02 | 起: what I built | `起 · …` |
| 03 | 承: how it grew | `承 · …` |
| 04 | 轉: where it broke (multi-step) | `轉 · …` |
| 05 | 結: the cause, with tool evidence | `結 · …` |
| 06 | Takeaway | `가져가실 것` |

The stage variant uses 6 slides: symptom → evidence → cause → quiz →
mechanism → closing, with a timed speaker note per slide.

## Elevation & Depth

Flat. No shadow on any slide element. Hierarchy comes from:

1. Border weight: 2px ink for panels and the head rule, 1px for the foot rule.
2. Accent color on one or two marks.
3. Surface tone: panel fill against paper; terminal-dark against panel.
4. Size: source code large, reference code small.

The only shadow in the system is on the speaker-notes panel
(`0 -8px 24px rgba(0,0,0,.08)`), which is presenter UI, not slide content.

## Shapes

Architectural sharpness: every box is square-cornered (`rounded.none`).
Round shapes have one job each:

- The title dot: an accent circle at the right edge of slide 00. The only
  decoration in the deck.
- Nav dots and the breathing step dot (presenter signals).

Markers are squares, not bars: `.punch::before` and `.msgs li::before`
draw a filled accent square (0.6em / 0.5em). Do not use a left vertical
bar for emphasis. The one exception is `.chain` (a 3px accent left border),
used for a single comparison expression.

## Components

**Code panel** (`.panel` > `.cap` + `pre`): 2px ink border, panel fill.
The caption shows the file name left and a side tag right (`4 – 9`, `INPUT`,
`EXPECTED`, `실제 기록`). Two caption styles exist:

- *Black band* (week04): caption is ink background, paper text, side tag
  in accent.
- *Light band* (week05, bsize): caption is paper background, ink or gray
  text, 1.5px rule under it. Prefer this one; it is quieter.

`.panel.accent` swaps the border (and the band rule) to the accent. Use it
for the panel that holds the bug.

**Code marks inside `pre`:**

| Class | Look | Meaning |
|---|---|---|
| `.c-hit` | accent, 600 | Look here |
| `.c-com` | gray #9a9a9a | Comment |
| `.c-dim` | light gray | Elided or unimportant lines (`⋮ 같은 패턴 7,670번`) |
| `.c-key` | muted | Keyword (week04 only) |
| `.hl` | 13% accent fill, block | The line being discussed now |
| `.ul` / `.uline` | accent underline; `.uline` draws left→right over .9s | Compare these tokens |
| `.squiggle` | wavy accent underline | Editor-style "this is suspicious" |
| `.zero` | accent box around a token | A single value that matters |

In a reference column (`.col.ref`) the accent is not used: `.c-hit`
becomes ink 600. The reference must stay quiet.

**Machine panel** (`.machine`, red variant): terminal-dark fill, light gray
text, `.m-err` orange-red, `.m-warn` amber, `.m-ok` green, `.m-dim` gray.
Only for text a tool printed.

**Thesis** (`h2.thesis`): one sentence, bold, `b` in accent.

**Punch** (`p.punch`): the conclusion under the code, 500 weight,
`max-width: 62ch`, accent square before it, `b` in accent.

**Message list** (`ul.msgs`): 2–3 short lines under a code block, square
markers. `.ask` is the question to the audience: 700, ink marker.

**Said** (`.said`, stage variant): "what I thought then", in accent curly
quotes.

**Eyebrow / kicker**: mono, uppercase, letter-spacing .2em. Red variant:
accent fill, paper text. `.ghost` variant: paper fill, accent border and
text, no uppercase (for program names). Cobalt variant (`.kicker`): accent
outline only.

**Rule** (`.rule`): a thick ink bar, `clamp(70px, 9vw, 180px)` by
`clamp(6px, .55vw, 12px)`, under the h1.

**Comparison table** (`table.rows`): 2px ink cell borders, mono header in
muted gray, `tr.hit` in accent.

**Args row** (`.args .arg`): bordered mono boxes above a function header
that show "this argument → that parameter". Space is reserved from the
start; each box fades in on its step.

**Presenter UI:** 4px accent progress bar at the top (animate `scaleX`, not
`width`); nav dots on the right; a keyboard hint at bottom left that fades
out after 5s; the breathing `.step-dot` at bottom right while steps remain.

**Inline edit mode** (frontend-slides): `E` key or the top-left hot corner.
Dashed accent outline on editable text, autosave to `localStorage` keyed by
a content signature, `Ctrl+S` exports the file. In edit mode, show all step
content so hidden text is editable too.

## Do's and Don'ts

- Do put one thesis sentence at the top of each content slide.
- Do show real tool output (gdb, compiler, nm) copied from a real run.
  Mark it `실제 기록` in the caption side tag.
- Do keep the accent to one or two marks per screen.
- Do reserve the space of step content from the start, and change only
  `opacity`, `visibility` and `transform`. The layout must not jump.
- Do overlay before/after code states in the same grid cell
  (`.swap > .st-b / .st-a`). Shared lines stay in the DOM once, so they
  do not blink.
- Do exit fast and enter slow: old state .15s ease-in, new state .26s
  ease-out with a .1s delay.
- Do size code to the screen with `min(vw, vh)`. Short code blocks get a
  larger zoom class so the slide does not look empty.
- Do support `prefers-reduced-motion`.
- Don't use a dark slide background. Dark is reserved for machine output.
- Don't use shadows, gradients, rounded boxes, or illustrations on slides.
- Don't uppercase identifiers or program names.
- Don't put the key sentence in the foot band.
- Don't use the accent in the reference column.
- Don't fade the leaving slide in the stage runtime: two half-transparent
  slides make the shared head rule and grid lines flicker.
- Don't mix red and cobalt, or the two runtimes, in one deck.
- Don't paraphrase the code on the slide; point at it.

## Runtime variants

Two runtimes exist. Both include the full `viewport-base.css` contract
from frontend-slides (100vh/100dvh slides, `overflow: hidden`, height
breakpoints at 700/600/500px).

| | Scroll-snap (week04, week05) | Stage (bsize v2) |
|---|---|---|
| Slide model | `html { scroll-snap-type: y mandatory }`, IntersectionObserver adds `.visible` | `.slide { position: fixed; inset: 0 }`, one `.active`, the previous one `.leaving` (not faded) |
| Steps | `data-step` / `data-max-step` on the `<section>`; CSS selects `.slide[data-step="2"] .at.s2` | `data-step="N"` on each element; JS adds `.on` when `N <= current step`; max step = the largest `data-step` in the slide |
| Entry motion | `.reveal` stagger, 24px rise, .65s `cubic-bezier(.16,1,.3,1)`, .1s steps | Step elements, 14px rise, .5s same ease |
| URL | none | `#N` hash, `hashchange` aware |
| Speaker notes | none | `<aside class="notes" data-sec="30">` per slide; `N` toggles a bottom panel with slide, target seconds, step, total. Each `<p>` starts with `<span class="st">▸2</span>` to match a step |
| Keys | ←/→, ↑/↓, Space, PageUp/Down, Home/End, E, Ctrl+S | Same, plus N. Use `e.code` (`KeyE`, `KeyN`) so keys work with a Korean IME on |

Choose **stage** for the weekly talk (the default: notes are required).
Choose **scroll-snap** for a deck that people read on their own.

## Implementation contract

Copy this `:root` block. The tokens above are its values at 1440 × 900.

```css
:root {
    --paper:  #ffffff;
    --ink:    #0a0a0a;
    --acc:    #ff3300;              /* or #1638c7 for the cobalt variant */
    --hl:     rgba(255,51,0,.13);   /* or rgba(22,56,199,.13) */
    --grid:   #ebebeb;
    --mut:    #6b6b6b;              /* cobalt: #5e5e5e */
    --panel:  #f7f7f5;              /* cobalt: #f3f5fc */
    --panel-b:#0a0a0a;

    --font-body: 'IBM Plex Sans KR', sans-serif;
    --font-mono: 'IBM Plex Mono', 'IBM Plex Sans KR', monospace;

    --title-size: clamp(2.4rem, 4.8vw, 7.5rem);
    --h2-size:    clamp(1.4rem, 2.3vw, 3.2rem);
    --h3-size:    clamp(1.1rem, 1.6vw, 2.2rem);   /* h2.thesis */
    --body-size:  clamp(0.95rem, 1.15vw, 1.65rem);
    --small-size: clamp(0.72rem, 0.78vw, 1.15rem);
    --code-size:  clamp(0.85rem, min(1.4vw, 2.4vh), 2.1rem);

    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap:   clamp(0.5rem, 2vw, 2rem);
    --element-gap:   clamp(0.25rem, 1vw, 1rem);

    --ease: cubic-bezier(0.16, 1, 0.3, 1);
    --dur:  0.65s;                  /* stage runtime: 0.5s */
}

.slide::before {                    /* 12-column grid */
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background: repeating-linear-gradient(90deg, var(--grid) 0 1px, transparent 1px 8.3333%);
    opacity: .6; z-index: 0;
}
```

Variable name note: the red decks call the accent `--red`; the cobalt deck
calls it `--acc`. New decks use `--acc`.

## Using with frontend-slides

This file replaces Phase 2 (style discovery) of the `frontend-slides`
skill. Everything else in the skill still applies.

1. **Phase 1:** the Context section answers Purpose (teaching, peer talk)
   and Length (6–7 slides, 2 minutes). Inline editing: yes. Ask only for
   the content: the week, the bug, and the real tool output.
2. **Phase 2:** skip. Tell the skill: "Style: Plex Swiss Grid, see
   DESIGN.md". Ask only one thing: the accent (red, cobalt, or a new
   variation; he likes to vary the color week to week). The runtime is
   stage, because speaker notes are required.
3. **Phase 3:** read `html-template.md`, `viewport-base.css`,
   `animation-patterns.md` from the skill, then this file. Where they
   conflict, this file wins on look; the skill wins on viewport fitting.
   Use the narrative template and the layout patterns above.
4. **Content density** follows the skill (code slide: 8–10 lines), with one
   exception: a Work slide may hold one 10–11 line source panel plus a
   reference column, if the code font stays at or above `.95rem`.
5. **Check before delivery:** render at 1280 × 720 and 1920 × 1080. No
   slide scrolls, no code line is cut, the accent count per screen is ≤ 2,
   and every tool-output panel came from a real run.

Preset entry for `STYLE_PRESETS.md` (paste under "Light Themes"):

```markdown
### Plex Swiss Grid

**Vibe:** Exact, calm, evidence-first. Korean technical talks about code.

**Layout:** Head band (label · number) / content / foot band (source path).
12-column hairline grid behind every slide. Code panels are the hero.

**Typography:**
- Display/Body: `IBM Plex Sans KR` (400/500/700)
- Code/Labels: `IBM Plex Mono` (400/500/600)

**Colors:**
:root { --paper:#ffffff; --ink:#0a0a0a; --acc:#ff3300; --grid:#ebebeb; --mut:#6b6b6b; --panel:#f7f7f5; }
Cobalt variant: --acc:#1638c7; --panel:#f3f5fc; --mut:#5e5e5e;

**Signature Elements:**
- Thesis sentence at the top, punch line with an accent square under the code
- Square-cornered code panels with a file-name caption
- One accent circle on the title slide, nothing else decorative
- Step reveals that reserve their space, so nothing jumps
```
