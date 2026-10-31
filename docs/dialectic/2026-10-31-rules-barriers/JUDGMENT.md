---
role: Main session judgment over CASE.md, five critiques, and defense.md
truth: Judgment on 2026-10-31. Accepted items are settled by evidence; open items wait for the user's grilling
born: 2026-10-31
status: Closed 2026-10-31. Decisions below are user said
---

# Judgment

Inputs: `CASE.md`, `critique-c-{problem,practice,universal,goodhart,learner}.md`,
`defense.md` (37 claims: 23 concede, 13 narrow, 1 rebut).

## Facts re-checked by the main session

- `W9/scripts/convention.py` never reads `returncode` (`:60-66`, `:96-106`).
  A crashed `clang-format` or `clang-tidy` can print "no violations". True.
- `multi-oom` (a leak test, `tests/userprog/no-vm/multi-oom.c:17`) is in
  `userprog/Make.vars:6` through `tests/userprog/no-vm`, not in
  `vm/Make.vars:6`. True. The directory name `no-vm` says the exclusion is by
  design, so "the barrier disappeared" is true but not an accident.
- `CONVENTION.md:192` approves `palloc_get_page`. Rule 1 conflicts. True.
- `code-principles.md:7` lets the agent edit the file (Tier 2). This
  conflicts with P4. True.
- `W9` changed during this session: `e542179` at the first check, branch
  `CJG` at `3c39884` with `pintos/include/vm/file.h` modified at the second.
  Not a survey error. Another actor switched the branch. Record the branch
  with every HEAD.

## Accepted (evidence settles them)

1. **P3 is replaced.** Obligation strength and detection reach are separate.
   Each absolute rule names: the obligation, its detector (tool, test, or a
   fixed review moment), what the detector covers, and its blind spots. A
   tool detector is proven in four steps: baseline green, mutant red for the
   intended reason, restore green, a legitimate neighbor stays green.
2. **P1 is replaced by two axes.** Checker: exact tool, proxy tool, or human
   question. State: wired, unwired, or claimed but absent. "Claimed but
   absent" is the harmful cell (`code-principles.md:20-21`). The always-red
   lint is an unwired check with a broken baseline, not class D.
3. **Order of correction.** Fix false claims first, then cheap wiring that he
   owns, then nothing until a risk is shown.
4. **"Fix" covers tools.** `convention.py` false green is a tool defect. It is
   team-owned, so the fix goes to the team.
5. **Rules rewritten.** Rule 1 becomes a contract rule (a name and its
   contract tell the caller the observable effects). Rule 2 becomes
   "responsibility for every acquired resource until release or explicit
   transfer, on every path" and stays unconditional. Rule 3 becomes a review
   question ("What necessary fact does this comment add?").
6. **Scope wording.** A second language can falsify a universal intent, not
   prove it.

## Decisions (user said, 2026-10-31)

- O1. Core question replaced: for each code path (typed by him, written unseen
  by an agent, teammate PR, foreign code), which artifact holds the intended
  shape, which shows the actual shape, and what tells him the two differ.
- O2. Universal intents stay local (`docs/code-principles.md`, section
  "Candidate universal intents") until one falsification attempt on a non-C
  task. At promotion: `~/.claude/docs/code-principles.md`, with a one-line
  conditional pointer in `~/.claude/rules/agent-operating-model.md`.
- O3. `code-principles.md`: the agent proposes a change; he approves it.
- O4. Agents may not edit upstream tests (files under `pintos/tests/` in the
  root commit). New test files and `Make.tests` are allowed. Done: hook
  `K/.claude/hooks/protect-upstream-tests.py`, wired in
  `K/.claude/settings.json` and `W9/.claude/settings.local.json`.
- O5. No lint hook in `week09` (the repo ends soon). Future projects follow
  `~/.claude/docs/tool-guides/barrier-placement.md`: one `verify` command
  (lint on the diff + the fastest full test runner), every moment reruns it,
  CI with a required check is the authority. Trial at the next
  `jungle-week-init`.
- O6. Sheet against `pintos-index` card check added to `jungle-close` step 1b
  as a one-stage trial; the agent runs it and reports differences.
