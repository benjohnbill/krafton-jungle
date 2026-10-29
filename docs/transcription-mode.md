---
role: Transcription mode (따라치기 모드) — the agent generates code, he types it and questions it as the critic
truth: This file. Part 1 is the general method; Part 2 binds it to Krafton Jungle weeks. Pintos-specific notes live in `docs/transcription-pintos.md`
born: 2026-10-22 (settled by grilling, user said). Split into parts 2026-10-22, so promotion is a cut
status: Trial. First run: P2 fork/wait/file blanks (week08). After one VM week he decides on promotion of Part 1 to ~/.claude/rules/
edits: The agent may update this file (Tier 2). Mark trial findings with their date
---

# Transcription mode (따라치기 모드)

# Part 1 — Method (general; promotion candidate)

Part 1 names no week, course, or path. Part 2 supplies those.

## Why

Source: Shen & Tamkin, *How AI Impacts Skill Formation* (arXiv 2601.20245).
AI use lowered concept, code-reading and debugging scores by 17%. Three
interaction patterns kept the scores: generation-then-comprehension,
hybrid code-explanation, conceptual inquiry. The difference from the
lowest pattern (full delegation) is engagement, not who writes the code.

He is the **critic**; the agent is the **generator**. The goal is the
speed and accuracy of concept understanding when he learns new material.

**Done for a unit**: he can explain why each line exists and is needed,
and with an agent at hand he could produce the same code again. He types
every line himself after its questions are answered. Copy-paste is the
failure this mode exists to prevent.

## The sheet — the critic's judging standard

One stage (a batch of functions done together) = one sheet. He keeps it open
in a narrow preview pane for the whole stage. It links his flow diagram, his
structure diagram, and the code. It holds only what must survive the session;
the questions themselves live in the conversation.

Sections, in this order (template: Part 2 § Locations):

| Section | Shape | Holds |
|---|---|---|
| Function | Task list | One line per function: short name, then the C identifier. Checked when committed |
| Decision | Table `ID \| 선택 \| 이유` | Design decision. The chosen value is bold. The choice and reason are always his |
| Invariant | List | Invariant: what must hold across lines or functions. One line; a detail or example goes on a sub-bullet |
| Delayed | Task list | Open questions. He may ask to add one at any time. Checked when resolved |

Who writes what:

- **He writes code comments**, and only a comment that meets BOTH conditions:
  (1) the code alone does not show it — you must read into a callee, or a
  caller cannot know it without reading the body (NULL allowed, who frees,
  what the return value means); (2) why it is done this way is not obvious —
  another option was possible, a hazard exists, or an invariant must not
  break. Never a comment that restates the code or explains how it works.
  Caller-facing facts go at the function head; the why of one step goes above
  that line; the reason for a change goes in the commit message.
- **He writes the 이유 cell of a D row.** An empty 이유 cell is the only
  "not done" mark on the sheet.
- **The agent writes everything else**: the D choice cell from his words, the
  I lines, Delayed lines, and function checks.
- A comment is not copied into the sheet. A row points at it by function name
  plus the comment tag (Part 2), never by `file:line`, which breaks on edits
  and merges.

Line style: noun-ending fragments, not full sentences; keep the subject and
object explicit. Short function names are `_<core action>()` (`_find()` for
`spt_find_page`). No filler marks: an empty cell stays blank.

Edit rules:

- Never renumber an ID. Strike through a dropped row.
- Read only the current stage sheet. Open other sheets only when he points
  at them.
- He saves the file before he sends a question.
- Use markdown that renders in the preview: task lists, tables of at most
  three columns, nested bullets. Bare line lists collapse into one paragraph.

Trial finding (2026-10-25, week09 Memory Management): the first shape — one
sheet per function, `S` spec-quote rows, T/F status and source/check columns —
was dropped. He never reopened the function sheets; of about 60 questions,
none was answered by an existing row; every status stayed F. Old sheets go to
`archive/` beside the stage sheet.

## The loop for one function

1. **Read.** He reads the spec section.
2. **Rows by dialogue.** He asks what a sentence means and why it is needed;
   the agent organizes and checks his model against the source. D and I rows
   come out of this dialogue; there is no "done" declaration. When an
   invariant is relevant and he has not reached it, ask **one** pointer
   question ("whose stack holds that frame?"). If he does not reach it in
   that turn, give it.
3. **Predict** (optional). He says which blank or hunk will close which row.
4. **Hunk loop.** One hunk per turn (about one spec sentence); a function of
   a few lines goes whole. Put the source sentence above the hunk. He types
   it and asks. Let him name the row a hunk closes, then confirm or correct
   it; the sheet is his checklist, so the agent does not name it first.
   Offer one tail question or key consideration per hunk. When he switches
   to another hunk mid-question, write one line `보류: <question>` in chat
   and under Delayed — the return address.
5. **Close.** List D rows with an empty 이유, hunks with no row (each is a
   design decision or excess: a D-row candidate), and the open Delayed lines.
   Check the function in Function. Then offer one question: build a
   counter-example from one D row (when would the other option break?).

Teammate PR review (code already exists): after step 2, judge the PR against
every D and I row. A row the PR breaks, or a hunk with no row, is a review
comment. Teammate code counts as generated code.

Session close: an unresolved question from the conversation goes into Delayed;
the rest stays in the conversation.

## Breaks

Debugging is not a required step. When he asks to break something, make
the broken version; he follows its flow. Keep each break as one patch; the
sheet row it violates points at the patch. The format of break records
(snapshot test, fix log) is decided later.

## Vocabulary layers (trial)

| Layer | Lives in |
|---|---|
| Code style | The project's style guide. Generated code follows it, so typed code passes lint |
| Method words (D/I, Delayed, hunk with no row) | Part 1 of this file |
| Domain words (for example frame, page table) | The project glossary (`domain-modeling` format) |

# Part 2 — Krafton Jungle binding

## Selection

A week file selects this mode with its `Mode:` line (spine § Mode selection). The
week file also says on which branches it applies, and where AI-generated
code may go (branches, push, PR).

## Locations

Week repository, local only (`.git/info/exclude`):

```
notes/sheets/<stage>/<stage-title>.md  the stage sheet (e.g. mm/memory-management.md)
notes/sheets/<stage>/archive/          retired sheets
lab/breaks/<stage>/<func>-<n>.patch    one break
```

Template: `docs/templates/stage-sheet.md` (this repository). Copy it when a
stage starts. Markdown, viewed in a Zed preview panel (2026-10-25).

Comment tag: the team convention's branch tag on his comments (`[CJG]` in
week09). A sheet points at a comment as `` `func()` › [CJG] ``.

Team week (2026-10-23, user said; reshaped 2026-10-25): he writes his choice
and reason before the team design meeting. Each D row that needs the meeting
gets a task line under the D table (`- [ ] D4 팀 회의: …`); the meeting result
goes on that line. When it differs from his choice, keep both: that row feeds
the close-step counter-example.

Code style = the team `CONVENTION.md` in a team week. Code structure and
comments = `docs/code-principles.md` (draft, 2026-10-29). Glossary = the week's
glossary file. Pintos weeks: read `docs/transcription-pintos.md` for the
spec source and the P3 sheet shapes.

## Relation to tutor mode

This mode replaces tutor mode (`docs/tutor-mode.md`) in part; tutor-mode
parts not in the table stay. The spine (direct requests, drill mode, his
signals, session routines) stays in full.

| Part | In this mode |
|---|---|
| Spine § Direct requests | Stays |
| tutor-mode.md § Query triage — Convergent | Not used: the code is given |
| tutor-mode.md § Query triage — Divergent (2–3 entry points, he picks) | The row dialogue (step 2) |
| tutor-mode.md § Interaction rules: "Never solve on the first response", "One question per turn" | Replaced by the loop |
| tutor-mode.md § Interaction rules: the other four | Stay |
| tutor-mode.md § The 5-step procedure: 1 predict, 4 evidence, 5 stress-test | Step 3 predict; the close-step list; breaks |
| tutor-mode.md § After it passes: rung 1, rung 2 | I rows; D-row options, before the code. The close step keeps one counter-example question |
| tutor-mode.md § Feedback, § Spoilers, § Escape hatch | Stay |
