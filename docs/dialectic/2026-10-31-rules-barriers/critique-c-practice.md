---
role: Critique of the rules-barriers case from the practitioner lens
truth: One critic's view on 2026-10-31. Not a decision
born: 2026-10-31
status: Open
---

# Critique: c-practice (practitioner lens)

Named public practices below come from my training knowledge (cutoff June 2026). I did not re-fetch them. Each is marked "known practice" or "judgment".

## 1. P3 is the right instinct, but "absolute rule needs a mutation-proven barrier" is the wrong unit

- **Claim**: Strong agentic engineers prove a barrier with one deliberate failure, not with a mutation framework. Full mutation proof for every absolute rule costs more than the rules are worth in a one-week repo.
- **Evidence**: Known practice: the "red first" step of TDD, and Anthropic's Claude Code docs, which tell users to add a hook and then trigger it once. Repo evidence: `tools/pintos-index/src/pintos_index/mutate.py:1-9` already does mutation proof for the index tool. The user paid that cost once, for a tool that lives across weeks. Judgment: a `W9` rule lives one week.
- **Change**: Rewrite P3 to "show the barrier red once, by hand, and paste the output in the PR or the doc." Keep scripted mutation only for tools that outlive a week (`tools/pintos-index`).
- **Test**: For each absolute rule, the doc links one command and its failing output. A reviewer can rerun the command on a broken line.

## 2. Absolute rule 2 (release on failure) cannot get a barrier in Pintos. Demote it, do not fake a tool

- **Claim**: No sanitizer or leak test runs inside the Pintos kernel under QEMU, so P3 forces rule 2 down to a judgment question.
- **Evidence**: Judgment, with a check: `pintos/threads/palloc.c` has `palloc_free_page` but I found no leak report. ASan and LeakSanitizer need a hosted libc; the kernel has none. Known practice: kernel teams use KASAN or kmemleak, and Pintos has neither. A partial barrier exists: a stress test that fails allocation (a `palloc` fault-injection counter) and then checks the free count. That is real work in an upstream file the team owns.
- **Change**: Retire the word "absolute" from rule 2. Move it to judgment question form: "On each early return, list what this function acquired. Is each item freed?" Add one probe in `lab/` per bin-2 candidate, as `code-principles.md` already says (bin 2 requires the failure to show first).
- **Test**: The doc has no "absolute" rule without a command. Bin-2 PRs each carry a failing-then-passing probe.

## 3. A senior agentic engineer drops the "No new mechanical check is added here" stance and wires the existing check first

- **Claim**: The cheapest real barrier is already written and not triggered: `make lint` exits non-zero at `W9` HEAD and nothing runs it.
- **Evidence**: Case facts: `W9/.git/hooks` holds only samples; no CI. Known practice: Claude Code `PostToolUse` and `Stop` hooks that run lint and test commands, and `PreToolUse` hooks that block commits; Husky and `pre-commit` for human commits. Anthropic's own guidance says rules in `CLAUDE.md` are advisory and hooks are deterministic. Judgment: `make lint` failing at HEAD means a hook that blocks would block every commit today, so wire it as a diff-only check.
- **Change**: Wire. Add a project-local `.claude/settings.json` hook in `K` (the user owns it, no team consent needed) that runs `make -C week09 lint` after the agent edits C files and feeds the output back. A git `pre-push` hook is a second option. Do not touch team tooling.
- **Test**: Make an agent edit that breaks a brace rule. The hook output names the line in the same turn. Remove the break and the output goes empty.

## 4. P5 is correct but the default "wire, not rewrite" hides a ranking: fix false claims first

- **Claim**: A false document costs more than a missing tool, because the agent reads the document as true and acts on it.
- **Evidence**: `code-principles.md:20-21` says `clang-format` and `clang-tidy` "already cover those cases"; the case shows two enabled tidy checks that touch none of its rules. Known practice: strong teams treat `AGENTS.md` or `CLAUDE.md` like code with review, because a wrong line misleads every session (Anthropic's memory docs and the `AGENTS.md` convention both say keep it short and accurate). The `W9/README.md:180` vs ruleset conflict is the same class.
- **Change**: Fix, before any wiring: delete or correct the sentence at `code-principles.md:20-21`; correct `README.md:180` to 1 approval (it is the team's file, so send the team a one-line PR).
- **Test**: `rg` each "already enforced" claim in the doc set and match it to a command that exits non-zero on a violation. Zero claims without a command.

## 5. P4 (ownership) is sound but incomplete. The missing owner is the test and spec set

- **Claim**: The article's central barrier is "a human owns the spec and the agent cannot edit it." P4 lists the spec but gives the agent no mechanical lock on it.
- **Evidence**: Known practice: agentic engineers mark test and acceptance files read-only to the agent (permission `deny` rules on `Edit` for `tests/`, or a `PreToolUse` hook that blocks edits to them). Here the spec is the upstream Pintos `tests/` directory (`pintos/tests/vm`, 115 entries) and `Rubric.*`. Judgment: in this repo the barrier that already works is the upstream test suite; the agent editing it would void the grade.
- **Change**: Wire. Add a `deny` permission for edits under `week09/pintos/tests/**` in the `K` project settings. This costs one line.
- **Test**: Ask the agent to edit a file under `pintos/tests`. The harness refuses. `git diff -- pintos/tests` stays empty after a normal session.

## 6. Class D is real, and the main case already contains one example: the always-failing lint

- **Claim**: A check that fails at HEAD and blocks nothing trains everyone to ignore it. Fix HEAD or scope the check, not both neglected.
- **Evidence**: Case fact: 21 layout lines and 7 naming errors at HEAD `e542179`. Known practice: teams adopt a lint "ratchet" (fail only on new violations in the diff), as reviewdog and `git diff`-scoped `clang-format-diff.py` do. Judgment: with a one-week repo, a diff-scoped check is the only version that pays back.
- **Change**: Rewrite `make lint` usage in the hook to check only changed files and changed lines (`clang-format-diff`), not the whole tree. Leave `scripts/convention.py` alone; it is team-owned.
- **Test**: A new violation in a changed hunk fails the hook. The 28 old errors do not.

## 7. P2's universal layer should shrink to what a reviewer asks, and the global file should not hold it

- **Claim**: Practitioners keep universal principles out of always-loaded files unless a failure repeatedly forced them in. A principle with no observed failure is theater.
- **Evidence**: Known practice: Anthropic's docs and the `AGENTS.md` convention advise a short file and adding a line only after the agent errs. Repo evidence: `~/.claude/rules/agent-operating-model.md` already carries a retention test (non-derivable, needed at decision time, asymmetric error cost). Judgment: "name honesty" and "locality" pass none of the three tests in a global file; they are derivable and cheap to get wrong.
- **Change**: Retire the idea of promoting the five judgment questions to global. Keep them in `K/docs/code-principles.md`, loaded by `read_when`. Promote a line only after the same miss happens in two weeks.
- **Test**: The global rule set does not grow. A promotion appears with two dated incidents.

## 8. The question to change: not "is each rule a barrier" but "what fails first, and who sees it"

- **Claim**: The user's real goal is to see how expert agentic engineers work. Their loop is: test red, agent fixes, human reads the diff shape. The case audits prose and misses that the user's actual barrier is his own reading in transcription mode.
- **Evidence**: `docs/tutor-spine.md` and `docs/transcription-mode.md`: he types every line. Judgment: typing is a stronger barrier than any tool in this repo for the rules the agent writes into code he types, and it is also the learning channel. The article's tooling assumes an agent that writes unseen.
- **Change**: None to the documents. Rewrite the panel question to "for code the agent writes without his typing (probes in `lab/`, scripts, the index tool), which barriers exist?" Those are the places for hooks and tests.
- **Test**: The next panel lists barriers per code path (typed by him, written by the agent) and finds the unbarriered paths.

## What a senior agentic engineer drops as theater

- "Absolute" on rules 1 and 3 of `code-principles.md`: no tool checks name honesty or comment restatement. They are judgment questions. Keep them as such.
- Scripted mutation proof for week-lived rules (claim 1).
- Promoting principles to the global file without incidents (claim 7).

## What they do first in this repo

1. Fix the false sentence at `code-principles.md:20-21` (claim 4). Ten minutes.
2. Add the project-local hook that runs diff-scoped lint on agent edits, and the `deny` rule for `pintos/tests/**` (claims 3, 5, 6). Under one hour.
3. Run `make lint` and `make check` once on a broken line, and paste the red output in the doc (claim 1).

Verdict on the core question: The rule documents are mostly rules that sound good, and the fix is to correct false claims first, wire the existing lint with a diff-scoped hook second, and demote rules that no tool can check, not to build new barriers.
