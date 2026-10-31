---
role: Case file for a critique panel. Five critics attack it, one defender answers them, the main session judges
truth: Snapshot of the main session's positions on 2026-10-31. Not a decision. The user decides in a later grilling
born: 2026-10-31
status: Closed 2026-10-31. Superseded by JUDGMENT.md
---

# Case: are the rule documents real barriers, or rules that only sound good?

## The user and the goal

The user is a Krafton Jungle trainee (week 9, Pintos VM in C). He builds while
he learns. Agents write much of the code, and he types and reviews it. His
goal for this panel, in his words: "I want to learn and accept how the real
agentic engineer or the best expert who work with AI" works. He wants **real
corrections, not corrections that only sound good.** He also said: "the
core/original questions of this session could be changed by those
criticisms." So you may attack the question itself, not only the answers.

## Trigger: an article

Baek Myung-seok, "개발자는 코딩을 해야 하나?" (brunch.co.kr/@cleancode/109,
2026-10-27). Claims that matter here:

- Let go of syntax (lines inside function bodies), not design. Keep the
  "shape of the code": function list, names, sizes, call relations,
  constructor arguments, module placement.
- "The barrier must be a tool, not a prompt." Rules in `CLAUDE.md` are
  guidance. Agents break them, and context compression drops them. Barriers:
  unit tests with high coverage (the agent cannot move on until they pass),
  Gherkin acceptance tests (a human owns the spec; the agent cannot change it
  without permission), mutation tests (find assertion gaps coverage misses),
  CRAP + dependency checker + lint (function size, dependency direction,
  basic quality).
- CRAP and DRY keep the shape; tidying and systemic refactoring make it.

## Scope (added 2026-10-31, user said)

C and Pintos are the evidence, not the scope. The user wants general options
for any future codebase. Method: settle the specific rules here, write each
surviving rule's intent with no language words, then check the intent against
a second language family. A universal principle keeps its intent across
languages; only its barrier changes (example: release on every path is prose
plus sanitizers in C, but `defer`, `with`, or `Drop` in Go, Python, or Rust).

## The user's questions

1. Which documents in his directories must he manage and read himself?
2. What must he correct?
3. Did the documents that Claude wrote with him follow these structural
   principles, or were they "a bundle of sounding code rules"?
4. Purpose: manage future codebases that he will analyze.

## Documents under review

Repo root `K` = `/home/benjohnbill/dev/krafton-jungle`. `W9` = `K/week09`
(team repo, its own git repo).

- `K/docs/code-principles.md` (Draft, 2026-10-29, agent co-authored after a
  grilling): 3 absolute rules, 5 judgment questions, refactoring bins.
- `K/docs/transcription-mode.md`, `K/docs/tutor-spine.md`, `K/AGENTS.md`,
  `K/CLAUDE.md`, `K/skills/jungle-close/SKILL.md`,
  `K/skills/jungle-team-merge/SKILL.md`.
- `W9/CONVENTION.md` (written by the user and team), `W9/README.md` (team),
  `W9/CLAUDE.md`, `W9/.clang-format`, `W9/.clang-tidy`, `W9/Makefile`,
  `W9/scripts/convention.py`, `W9/.github/pull_request_template.md`.
- Evidence of the user's interest: `K/docs/handoffs/2026-10-30-clean-code-interest-evidence.md`.
- Global agent rules (for the universal-principles question only):
  `~/.claude/CLAUDE.md`, `~/.claude/rules/agent-operating-model.md`.

## Verified facts (survey on 2026-10-31, main session re-checked the starred ones)

- ★ `W9` HEAD `e542179`: `make lint` exits non-zero (21 layout lines, 7
  naming or brace errors). Nothing blocks a failing commit.
- ★ `W9/.git/hooks` has only `*.sample` files. `core.hooksPath` is unset. No
  CI workflow, no pre-commit config in any week repo.
- ★ `W9/.clang-tidy` enables only `readability-identifier-naming` and
  `readability-braces-around-statements`. `bugprone-*` is off on purpose
  (kernel false positives).
- The only barrier that runs automatically and blocks: the GitHub branch
  ruleset on the week09 team repo (PR required, no force-push, no deletion, 1
  approval). `clang-format` runs on save in the editor only.
- `code-principles.md:20-21` says the existing `clang-format` and
  `clang-tidy` "already cover those cases". The two enabled checks touch none
  of its rules, and nothing runs them automatically.
- `code-principles.md` absolute rule 2 ("every failure path releases what the
  function acquired") is prose only. No leak test or sanitizer is wired.
- `W9/CONVENTION.md:178` says itself that no tool catches its naming rules
  C1-C6.
- `W9/README.md:180` says 0 approvals; the live ruleset requires 1.
  `README.md:139` says merge commits only; the ruleset allows squash and
  rebase.
- Commit format conflicts: `K/skills/jungle-close/SKILL.md:38-52` vs
  `W9/README.md:194-215`.

## Main session positions after round 1 (attack these)

**P1. Classes of rules.** Sort each rule:
- A. Enforced: a tool blocks a violation automatically.
- B. Enforceable but not wired: a tool can check it; nothing runs the tool.
- C. Judgment: no tool can check it. Prose is the right home, but the rule
  must give a yes-or-no review question.
- D. Wrongly enforced (added after the user's push): a tool enforces a proxy
  that diverges from the intent (Goodhart). Examples: a 10-line function
  limit makes shallow wrappers; a coverage percentage rewards tests without
  assertions; a lint that always fails and blocks nothing trains people to
  ignore it.
"Sounds like a rule" = B + D + C-without-a-question.

**P2. Universal vs local principles (the user's push).** The user believes
universal principles exist even though conventions differ per project, and
that a rule's global placement must be proportional to its importance.
Main-session position: three layers.
- Universal principles: few, each with its "why" and a review question (for
  example name honesty, release on failure, locality, explicit inputs and
  outputs, readable shape). Global, short.
- Project conventions: local, mostly tool-enforced (layout, naming).
- Project instances: examples and accepted exceptions (`thread_current()` in
  Pintos). Local.
`code-principles.md` mixes layer 1 and layer 3 today.

**P3. Absolute rule needs a barrier.** If a document calls a rule absolute,
a tool must enforce it, and the barrier must be proven by mutation: break the
code on purpose and confirm the barrier fails. Otherwise the rule moves down
to a judgment question.

**P4. Ownership.** Human-owned, he reads and decides: specs and acceptance
criteria, `code-principles.md`, `CONVENTION.md`, ADRs, glossary.
Agent-owned, he need not read: handoffs, progress memos, survey notes,
memory files. (User agreed.)

**P5. Verbs for "correct" (user asked to separate them).**
- Wire: connect an existing tool to an automatic trigger (hook, CI).
- Fix: make code pass a rule, or make a document match reality (false claims,
  the README vs ruleset conflict).
- Rewrite: change a rule's wording or its class.
- Retire: delete a rule, or a tool that enforces wrongly (class D).
Default for class B: wire, not rewrite.

## Constraints the critics must respect

- He is a learner in a 5-month bootcamp with weekly team repos. Each week's
  repo lives about one week. Cost of a barrier counts.
- The team owns `W9`; he cannot change team tooling alone.
- In transcription and tutor modes the agent must not hand him solutions to
  exercises.
