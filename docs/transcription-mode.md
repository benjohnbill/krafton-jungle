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

The sheet is written **before** the code. It is what the critic judges the
generated code against, so his questions close rows instead of floating.
One function = one sheet. A stage (a batch of functions done together) has
one INDEX: the rows that cross functions, and one status line per function.

Row IDs work like variable names. The prefix is the type:

| Prefix | Type | Who drafts |
|---|---|---|
| `S` | Spec sentence, judged T/F | Agent, with the source quote and URL. He audits it against the source |
| `D` | Design decision: what to decide, options, his choice and reason | From the dialogue (step 2). The choice and reason are always his |
| `I` | Invariant: what must hold across lines or functions | From the dialogue (step 2) |

Columns: `ID | row | source (spec text / test file / user / agent) | check (test name / debugger / none) | status (T/F + evidence file:line)`.
A row with check "none" is a candidate for an own verification test.

Edit rules:

- Never renumber an ID. Strike through a dropped row.
- Read only the current function's sheet and its stage INDEX. Open other
  sheets only when he points at them.
- He saves the file before he sends a question.
- Format: the agent writes the first draft. When he reshapes it, follow his
  last shape from the next row on. Keep it compact: one screen shows what
  he watches live.

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
   and in the sheet — the return address.
5. **Close.** List open rows, hunks with no row (each is a design decision or
   excess: a D-row candidate), and the open 보류 lines. Then offer one
   question: build a counter-example from one D row (when would the other
   option break?).

T/F status is written at two times:

- **Generated code or a blank set** (no code yet): every row starts F; a row
  turns T when a hunk closes it, with evidence.
- **Teammate PR review** (code already exists): after step 2, judge every row
  against the PR. That judgment is the review: an F row or a hunk with no
  row is a review comment. Teammate code counts as generated code.

## Breaks

Debugging is not a required step. When he asks to break something, make
the broken version; he follows its flow. Keep each break as one patch; the
sheet row it violates points at the patch. The format of break records
(snapshot test, fix log) is decided later.

## Vocabulary layers (trial)

| Layer | Lives in |
|---|---|
| Code style | The project's style guide. Generated code follows it, so typed code passes lint |
| Method words (S/D/I, 보류, hunk with no row) | Part 1 of this file |
| Domain words (for example frame, page table) | The project glossary (`domain-modeling` format) |

# Part 2 — Krafton Jungle binding

## Selection

A week file selects this mode with its `Mode:` line (spine § Mode selection). The
week file also says on which branches it applies, and where AI-generated
code may go (branches, push, PR).

## Locations

Week repository, local only (`.git/info/exclude`):

```
notes/sheets/<stage>/INDEX.md          the stage INDEX
notes/sheets/<stage>/<func>.md         one sheet; name = the C identifier
lab/breaks/<stage>/<func>-<n>.patch    one break; mirrors the sheet path
```

Uppercase names are role files; lowercase names are subjects. He keeps the
current sheet open in a Zed markdown preview panel during transcription.
The sheet format (markdown or HTML) is not fixed yet.

Code style = the team `CONVENTION.md` in a team week. Glossary = the week's
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
| tutor-mode.md § The 5-step procedure: 1 predict, 4 evidence, 5 stress-test | Step 3 predict; the status evidence; the check column and breaks |
| tutor-mode.md § After it passes: rung 1, rung 2 | I rows; D-row options, before the code. The close step keeps one counter-example question |
| tutor-mode.md § Feedback, § Spoilers, § Escape hatch | Stay |
