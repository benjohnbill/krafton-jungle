---
name: jungle-team-merge
description: Team-week merge of teammates' personal branches into the shared base branch — measure each branch (lint, scoped tests, regressions), judge it against the team criteria, pick the best part of each, integrate on one branch with history kept, verify, open the PR, then sync his personal branch. Use when he says "팀원 브랜치 합치자", "develop 구성", "머지 판정", "브랜치 비교해서 머지", or asks which teammate's code to take.
---

# jungle-team-merge

Two **gates**, and nothing asked between them. Work runs to a gate, the gate
asks everything at once in one numbered message, and he answers by number.
A judgement call between gates takes the default written here and goes into
the gate B report as "decided: …".

## 0. Facts

Look, do not ask:
- `git fetch --prune`; every remote branch with `git log --oneline <base>..<b>`
  and `git diff --stat <base>...<b>`.
- The week `CLAUDE.md`: `Verify:`, the do-not-touch list, the course rule on
  writing code under `pintos/`.
- `CONVENTION.md` at the repository root, if present.

## 1. Measure each branch

One scratch worktree per branch plus one for the base (the **control**), each
with the week's local `GNUmakefile` copied in. Per tree:

- `make lint` (exit code and the lines it names).
- The scoped tests, plus the regression suite the week names (Pintos: the 18
  threads tests), through `run-tests.sh` in this folder:
  `run-tests.sh <tree> <jobs> 5 threads/alarm-single userprog/args-none …`.
  Its header says what `timeout-judged` and `STALE` mean.
- When a branch cannot run the scoped tests alone (for example, it lacks the
  syscall that prints), graft the missing part from another branch in its
  scratch tree only, and say so in the table.

**Cores**: trees run at once share `nproc`; give each `nproc / trees` jobs.
`TIMEOUT` is wall time, so oversubscribed QEMUs turn passing tests into
timeouts.

**Subagents**: with three or more branches, measure each branch in its own
subagent, run in parallel, so the diffs and logs stay out of this context.
Each returns: lint result, the per-test lines from `run-tests.sh`, and for
each criterion the property the branch violates with the test or line that
shows it. With fewer branches, measure inline.

Criterion: the control fails every scoped test it should fail, and no line
reads `STALE`. A control that passes means the judge is broken, not the code.

## 2. Judge

One table per criterion set he gave, default: CONVENTION.md fidelity,
stability for the next milestone, time and space cost, readability. Every
cell cites evidence: a test line, a lint line, or `file:line`. Review names
the property violated and the test that shows it.

## 3. Plan the integration

Prepare, do not execute:
- **Pick list**: per function or block, which branch it comes from.
- **Rename list**: every name that breaks CONVENTION.md (C3 `_cnt`, C4 the
  syscall argument names, C6 named constants), old → new, `file:line`.
- **Cleanup list**: marker comments, commented-out code, planning notes.
- **Logic fixes**: lines that must be newly written (a guard, a moved call).
  The course rule forbids writing these unless he waives it at gate A.
- **Conflict preview**: `git merge-tree --write-tree` of the merges in order.
  Where git would fold one side's non-conflicting hunks into the other
  side's version of the same function, plan to take that function whole
  from one side.

## Gate A — one message

1. The base branch: does `develop` (or the named base) exist, and may it
   serve as the branch whose merged state this meeting/PR certifies stable?
   If it does not exist, propose creating it from `main`.
2. The judge tables (step 2).
3. The pick list, the rename list, the cleanup list.
4. Logic fixes, each with the test that needs it: write them, or leave them
   to their authors?
5. Push the integration branch and open the PR into the base?

Stop until he answers.

## 4. Integrate

Branch `integrate/<topic>` from the base. Merge each personal branch with
`--no-ff --no-commit` in the gate A order, resolve per the pick list, and
commit each merge with a body that names what it kept and left out. Then
one commit for renames and cleanup, one for each approved logic fix.
Attribution in commits and the PR follows the week `CLAUDE.md`.

## 5. Verify

`make lint` exits 0, and `run-tests.sh` on the integration tree gives every
scoped and regression test the expected verdict. Run the same command as in
step 1 so the before/after columns compare.

## 6. PR

Push, then write the body with the `pr` skill. The Summary carries the
**provenance table** (below). `gh pr merge` is denied to the agent here; it
goes to gate B.

## Gate B — one message

1. The provenance table:

   | Part | From | Changed in integration | Evidence |
   |---|---|---|---|
   | `load()` arg passing | JSY | `count_arg`→`arg_cnt`, markers removed | args-* 5/5 |

2. Before/after test lines and lint.
3. Every "decided: …" taken between the gates.
4. For him to run: `! gh pr merge <N> --merge`.
5. After that merge, may I: sync his personal branch (step 7), delete the
   integration branch, local and remote, and remove the worktrees?
6. The Slack text for teammates, ready to paste:
   commit first, then on their personal branch
   `git pull --no-rebase origin <base>` and `git push origin <branch>`.

## 7. Sync his branch — after his gate B answer

Confirm `origin/<base>` contains the PR merge commit. On his personal branch
with a clean tree: `git pull --no-rebase origin <base>`, then push it. Delete
`integrate/<topic>` only after `git merge-base --is-ancestor` shows it is in
the base. `git worktree prune`. Report the new head of each.
