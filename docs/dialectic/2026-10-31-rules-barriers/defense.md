---
role: Defense for the rules-barriers panel. Answers all 37 critic claims
truth: Defender's view on 2026-10-31. Facts marked "checked" were re-read or re-run today. Not a decision
born: 2026-10-31
status: Open
---

# Defense

`K` = workspace root, `W9` = `K/week09`, `G` = `~/.claude/rules/agent-operating-model.md`.

## 1. Verdicts

| Critic | # | Label | Verdict | Reason |
|---|---|---|---|---|
| problem | 1 | Frame is shape control, not enforcement | NARROW | Right for code he types. Unread code (teammate PRs, Q4) still needs detectors. Add, do not replace. |
| problem | 2 | Compare sheet row with index card | CONCEDE | Facts hold (sheet fields at `mmap/memory-mapped-files.md:9-14`, `model.py:22`). One line, retire if it finds nothing. Pintos-local. |
| problem | 3 | Article premise fails in transcription mode | CONCEDE | `transcription-mode.md:26-29`: he types every line. Barriers belong on paths he does not type. |
| problem | 4 | Class C is the asset for Q4 | CONCEDE | Q4 is reading foreign code. Write rules do not transfer; review questions do. |
| problem | 5 | P1 mixes three axes | CONCEDE | A vs B is a state. The always-red lint is B with a broken baseline, not D. |
| problem | 6 | False assurance is the worst class | CONCEDE | `code-principles.md:20-21` claims coverage that does not exist. `CONVENTION.md:178` is the honest form. |
| problem | 7 | P3 converse error; name the detector | CONCEDE | "Absolute" at `code-principles.md:25` means "no `[CJG]` exception", a review decision. Demotion would legalize a justified leak. |
| practice | 1 | Red once, not a mutation framework | NARROW | Cost point holds. Add goodhart's two cheap steps (green baseline first, neighbor passes); `make lint` is already red, so a bare "red once" proves nothing. |
| practice | 2 | Demote rule 2, no barrier possible | REBUT | Sanitizer part is true. "No leak test" is false: `multi-oom` is one. Demotion confuses obligation with detection. |
| practice | 3 | Wire a K-local lint hook now | NARROW | In transcription mode the agent rarely edits `W9` C files; he types them. And `convention.py` reports "no violations" when tools crash. Fix the script before wiring. |
| practice | 4 | Fix false claims first | CONCEDE | Agrees with problem 6 and learner 5. Note `README.md:181` already says the table is policy, not the live setting. |
| practice | 5 | Deny agent edits to `pintos/tests/**` | CONCEDE | One line in `K` settings, which he owns. Zero upkeep. The risk (a voided grade) is asymmetric. |
| practice | 6 | Diff-scoped lint ratchet | NARROW | `jungle-team-merge` SKILL.md:60-65 already compares to base. Goodhart 7: line-equality comparison is fragile. |
| practice | 7 | Do not promote principles to global | NARROW | Right for always-loaded files. A global on-demand doc costs no tokens per session. Placement is the user's value choice. |
| practice | 8 | Ask "what fails first, who sees it" per code path | CONCEDE | Same as problem 3. Adopt "barriers per code path". |
| universal | 1 | A second language falsifies, never proves | CONCEDE | Change the Scope wording from "check" to "try to falsify". |
| universal | 2 | Responsibility and transfer, not "release what you acquired" | CONCEDE | Rule 2 wording breaks on legitimate ownership transfer. |
| universal | 3 | Contracts, not verbs; `palloc_get_page` | CONCEDE | Checked: rule 1 forbids state change under `get`; the team approves `palloc_get_page`, which locks and flips a bitmap. |
| universal | 4 | Containment of decisions, not adjacency | NARROW | Right as the universal intent. Locality stays a useful local reading heuristic (universal 6 says so too). |
| universal | 5 | Falsifiable evidence; wire CI | NARROW | Intent holds. CI in a one-week team repo fails the cost test; team has deferred CI (`README.md:189`). |
| universal | 6 | Shape rules are heuristics | CONCEDE | Ousterhout and Martin dispute split and comment rules. Keep them as aids. |
| universal | 7 | Retire `G:138` placement rule | NARROW | Accept "importance does not decide scope" (`W9/CLAUDE.md:20` is local and critical). Reject retiring `G:138` here: out of scope, and it is a placement heuristic, not a claim of universality. |
| universal | 8 | Explicit bindings, authority, disk homes | NARROW | Layer table is useful. Creating the global doc now is premature; keep its "one non-C task first" test. |
| goodhart | 1 | Obligation and detection are independent | CONCEDE | Strongest claim. P3 must split them. |
| goodhart | 2 | Lint report hides tool failure | CONCEDE | Checked in code: no exit status read; a crash gives exit 0. |
| goodhart | 3 | Rule 1 contradicts team vocabulary | CONCEDE | Same fact as universal 3. |
| goodhart | 4 | Bounded failure injection | NARROW | Correct design. Hours of work: do it only for a bin-2 candidate, which `code-principles.md:102` already requires. |
| goodhart | 5 | Sanitizers measure the emulator | CONCEDE | Pintos has its own allocator (`malloc.c`). Rule 2 is not "B awaiting CI". |
| goodhart | 6 | Rule 3 has no runtime barrier | CONCEDE | Keep it as a review question. |
| goodhart | 7 | Exact lint-line diff is fragile | CONCEDE | Output embeds line numbers (`convention.py:84-86`). Low priority. |
| goodhart | 8 | Equal tests do not prove refactor | CONCEDE | Relabel bin 1 check as a regression observation. Cheap. |
| learner | 1 | Default "none until a risk is shown" | NARROW | Right for team tooling. Wrong for near-zero-cost changes he owns (deny rule, doc fixes). |
| learner | 2 | Lead with "which decision improves next PR" | CONCEDE | Agrees with problem 3 and 4. |
| learner | 3 | P3 confuses strength and reach | CONCEDE | Same as goodhart 1. |
| learner | 4 | Read by decision, not by document type | NARROW | Good trigger. User already agreed P4; keep the type list as the default home, add the trigger. |
| learner | 5 | Truth repairs pay back first | CONCEDE | Same as practice 4. |
| learner | 6 | Failing lint can be advisory | CONCEDE | The base comparison already uses it. Condition: it must report tool failure (goodhart 2). |

Totals: 23 CONCEDE, 13 NARROW, 1 REBUT.

## 2. Fact checks

| Claim | Result | Evidence |
|---|---|---|
| goodhart: `W9` is on branch CJG, HEAD `3c39884` | True | `git rev-parse` gives CJG; `git log` gives `3c39884`; `pintos/include/vm/file.h` is modified. `e542179` exists elsewhere in history. The case's HEAD fact is branch-dependent. |
| goodhart: `convention.py` discards exit status | True | `:63-64` and `:98-105` never read `returncode`. `lint()` (`:136-145`) returns 0 with "lint: 위반 없음" when no output line matches. A crashed tool reads as clean. |
| goodhart: every non-brace diagnostic is "naming" | True | `:131`. Compiler errors get the "naming" label. |
| practice: no sanitizer runs inside Pintos | True | No KASAN or kmemleak; own arena allocator `threads/malloc.c`. |
| practice: no leak test runs inside Pintos | False | `tests/userprog/no-vm/multi-oom.c:17` is a guest leak test. |
| problem: `multi-oom` is in the userprog set, not the VM set | True | `userprog/Make.vars:6` includes `tests/userprog/no-vm`; `vm/Make.vars:6` does not. It tests process leaks, not VM failure paths. |
| problem: `pintos-index` records member writes | True | `model.py:22` `member_writes`; `cards.py:137-140` prints "Field writes through parameters". |
| goodhart/universal: `palloc_get_page` approved and changes state | True | `CONVENTION.md:192`; `palloc.c` takes `pool->lock` and calls `bitmap_scan_and_flip`. |
| problem: template has only a name line | True | `docs/templates/stage-sheet.md:7`. |
| practice: `pintos/tests/vm` has 115 entries | True | `ls | wc -l` gives 115. |
| practice: `mutate.py` does mutation proof | True | `mutate.py:1-9`. |
| case: README says 0 approvals | True, with nuance | `README.md:178`; `:181` says the live setting is checked separately. A ruleset named CSY is active (`gh api .../rulesets`); I did not read its parameters. |
| case: only sample hooks, no hooksPath, no CI | True | `.git/hooks` all `*.sample`; `core.hooksPath` unset; `.github/` holds only the PR template. |

## 3. Conflicts between critics

1. **Wire a hook now (practice 3) vs "none until risk" (learner 1).** Evidence favors learner for the lint hook. The agent does not write `W9` C files in transcription mode, so a post-edit hook seldom fires. And the script can false-green. Evidence favors practice for the `pintos/tests` deny rule: one line, no upkeep, asymmetric risk.
2. **Demote rule 2 (practice 2) vs keep it unconditional (goodhart 1, learner 3, problem 7).** Evidence favors keeping it. Three critics agree, the "no leak test" premise is false, and demotion permits a justified leak.
3. **Red once (practice 1) vs four-step mutation (goodhart 1).** Compatible. Goodhart's extra steps cost minutes and catch the real trap: a check that is red before the mutation.
4. **CI after agreement (universal 5) vs none (learner 1).** Learner wins for a one-week team repo. Universal's intent holds for long-lived code.
5. **Global on-demand doc (universal 8) vs local until two incidents (practice 7).** User's value choice. Both agree: nothing new in always-loaded files.
6. **Lint as advisory (learner 6) vs "trains people to ignore it" (case P1, practice 6).** Evidence favors learner: the merge skill already uses a base comparison, so the red lint informs a decision.

## 4. What the case must change

**Edits.**

- **Core question.** Replace with: "For each code path (typed by him, written by the agent unseen, teammate PR, foreign code), what holds the intended shape and obligations, what shows the actual shape, what detects a gap and when, and is every document's claim about that true?"
- **Scope.** "Check the intent against a second language" becomes "try to falsify it in a second language". Drop "plus sanitizers in C" as the release example; sanitizers do not reach Pintos.
- **P1.** Two axes. Checker: exact tool, proxy tool, human question. State: wired, unwired, claimed but absent. Class D keeps only true proxy cases. Add "claimed but absent" as the most harmful cell.
- **P2.** Universal layer becomes four intents: resource responsibility with transfer, predictable contracts, contained private decisions, evidence matched to what it can detect. Shape rules become heuristics. No placement change until one non-C trial.
- **P3.** Rewrite: an absolute rule names its obligation, its detector (tool, test, or fixed review moment), what the detector covers, and its blind spots. Prove a tool detector with green baseline, red mutant for the right reason, green restore, neighbor passes. Never demote an obligation for lack of a tool.
- **Rule texts (input to the grilling).** Rule 1: advertised effects, upstream names exempt. Rule 2: discharge locally owned obligations on failure, transfer allowed. Rule 3: review question.
- **P4.** Add the decision trigger: he reads what his next approval or re-entry depends on. Fix an unattacked contradiction: P4 calls `code-principles.md` human-owned, but its own header says "The agent may update this file (Tier 2)" (`code-principles.md:7`). One of the two must change.
- **P5.** "Fix" must include tool defects (`convention.py` false-green). Default order: fix false claims, then near-zero-cost wiring he owns, then nothing until a risk is shown.
- **Verified facts.** State the branch with each HEAD. Note `README.md:181`'s self-declaration.

**Keep.** The verb set of P5. P4's split of human and agent documents. The finding that `code-principles.md:20-21` is false. The three-layer idea of P2, with intents in place of rules. The demand that a barrier be proven to fail.
