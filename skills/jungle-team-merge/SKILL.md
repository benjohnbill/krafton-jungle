---
name: jungle-team-merge
description: Pintos team weeks — merge teammates' personal branches into the shared base branch. Measure each branch (lint, the feature's tests plus every test the base already passes), judge it against the team criteria, integrate the best part of each on one local branch with history kept, verify and trace every hunk, then ask everything at one gate; after it, push, open the PR, and sync his personal branch. Use when he says "팀원 브랜치 합치자", "develop 구성", "머지 판정", "브랜치 비교해서 머지", "~ 구현했어, 팀끼리 머지 준비중", or asks which teammate's code to take.
---

# jungle-team-merge

**One gate.** Steps 0–5 run locally; nothing leaves the machine before the
gate. The gate asks everything at once in one numbered message, and he
answers by number. **Never ask mid-run.** A failure stops the work and goes
to the gate early as "stopped at step N: reason, state, rollback". After the
gate, a failure ends with no push and the same report.

A judgement call before the gate takes the default written here and goes into
the gate as "decided: …".

The course rule (week `CLAUDE.md`) forbids the agent to write logic under
`pintos/`. Default: before the gate the agent only assembles lines teammates
already wrote (merges and side-picks); renames and cleanup wait for gate
approval; logic fixes are written as findings, never as code.

Waiver: when he says "알아서 해줘" (or names a fix) at the gate, the agent may
write the code for the logic fixes listed there, in this run only. Each fix
is still its own commit and goes through the re-verify in "After the gate".

Scratch files go in the scratchpad. `run-tests.sh` (this folder) is the judge;
its header defines the verdicts `PASS | PASS* | FAIL | UNJUDGED | STALE`.

## 0. Facts — look, do not ask

- `git fetch --prune`. Every remote branch: `git log --oneline <base>..<b>` and
  `git diff --stat <base>...<b>`. The base is `develop` if it exists, else
  `main`.
- The week `CLAUDE.md`: `Verify:`, the do-not-touch list, the course rule.
- `CONVENTION.md` at the repository root and its rule IDs.
- The week `GNUmakefile` and its `dfast` label. Missing → stop.
- **Test scope** — from his words ("argument passing 구현했어", "write/exit
  머지 준비중"):
  - **Scoped tests**: the tests of the feature he named, by the test names in
    the week `GNUmakefile` lists (argument passing → `args-*`; write/exit →
    `exit`, `write-*`).
  - **Regression set**: every test that is `PASS` or `PASS*` on the control's
    full run (step 1). That is "what already passed", measured, not
    remembered.
  - Both lists go into the gate as "decided: scope".

## 1. Measure

1. `run-tests.sh --selftest <any tree>`. A mismatch stops the run.
2. One scratch worktree per branch, plus the **control** (the base), each with
   the week `GNUmakefile` copied in.
3. The control's full run: `run-tests.sh [--wait-loop] <control> <nproc> 5`
   with no test list (week08: 95 tests, about 30 s). Its `PASS`/`PASS*` lines
   are the regression set.
4. Write the expected verdict of each scoped test per branch before running.
5. `make lint` in each tree.
6. Every branch tree at once, from one Bash call (`&` per tree, then `wait`),
   each with `nproc / trees` jobs:
   `run-tests.sh [--wait-loop] <tree> <jobs> 5 <scoped ∪ regression>`.
   `TIMEOUT` is wall time; oversubscribed QEMUs turn passes into timeouts.
7. `--wait-loop` only for a tree whose `process_wait` loop is cited by
   `file:line` in the judge table.
8. A branch that cannot run the scoped tests alone (it lacks the syscall that
   prints): graft the missing part from another branch, in its scratch tree
   only, and say so in the table.

Any `STALE`, a build failure, or a selftest mismatch goes to the gate early.

## 2. Judge

One table per criterion he gave; default: CONVENTION.md fidelity, stability
for the next milestone, time and space cost, readability. Every cell cites a
test line, a lint line, or `file:line`. A rewritten pass shows as `PASS*`. The
stability column carries known windows the tests cannot see yet, with the
tests that will show them.

## 3. Plan

- **Pick list**: per function or block, which branch it comes from.
- **Function-overlap list**: for each file both sides change, the functions
  both sides touched since the merge base. Each is taken whole from one side
  or listed as a hand-merge. git folds one side's non-conflicting hunks into
  the other side's function silently, and `merge-tree` does not report it.

  ```bash
  printf '*.[ch] diff=cpp\n' > "$S/attrs"; mb=$(git merge-base A B)
  for s in A B; do git -c core.attributesFile="$S/attrs" diff -U0 "$mb" "$s" -- <file> |
    sed -n 's/^@@.*@@ //p' | sort -u > "$S/$s.fn"; done
  comm -12 "$S/A.fn" "$S/B.fn"
  ```

  Limit: a hunk that starts at a signature line is named after the previous
  function. Step 5's provenance check is the real test; this list is the
  early warning.
- **Rename list**: every name that breaks CONVENTION.md, old → new,
  `file:line`, rule ID.
- **Cleanup list**: marker comments, commented-out code, planning notes.
- **Logic fixes**: numbered findings — the property violated, the test that
  shows it, where to look. No code.
- **Conflict preview**: `git merge-tree --write-tree` of the merges in order.

## 4. Integrate

Branch `integrate/<topic>` from the base. Merge each personal branch with
`--no-ff --no-commit` in pick order. Resolve per the pick list and the overlap
list, and commit each merge with a body that names what it kept and what it
left out. No renames, cleanup, or logic fixes yet. Attribution follows the
week `CLAUDE.md`.

## 5. Verify and trace

- `make lint`, and the same `run-tests.sh` command as step 1, so the
  before/after columns compare.
- **Provenance check**: per changed file,
  `git diff <picked-source> integrate/<topic> -- <file>`. Every remaining hunk
  maps to a row: another pick, a rename, a cleanup item, an approved fix. The
  rows are the provenance table. An unmapped hunk is an unplanned fold: stop.
- **Sync preview** of his personal branch: `git status --porcelain` and
  `git merge-tree --write-tree <his-branch> origin/<base>`.

## The gate — one message

1. The base: the integration was built on `<base>` at `<sha>`. May it serve as
   the branch this meeting/PR certifies stable? If `develop` is absent: create
   it from `main`?
2. "decided: scope" (scoped tests, regression set), the judge tables, the pick
   list, the provenance table, and the before/after test and lint lines.
   `PASS*` caveat: a hang after the last output line is not detected.

   | Part | From | Changed in integration | Evidence |
   |---|---|---|---|
   | `load()` arg passing | JSY | merge only | args-* 5/5 `PASS*` |

3. The rename list and the cleanup list. Approval = consent to exactly those
   edits.
4. Logic fixes as numbered findings. Default: not applied. Applied when he
   names its number, or says "알아서" for all of them. Silence = no.
5. Every other "decided: …".
6. Push `integrate/<topic>` and open the PR into the base?
7. The sync preview: clean / dirty / conflicting files. On conflict: (a) he
   resolves, or (b) the whole-file base side for the named files, with the
   discarded diff shown (history keeps his commit).
8. After his merge: may I sync his branch, delete the integration branch
   (local and remote), and remove the worktrees?
9. Slack text for teammates, ready to paste: commit first, then on their
   personal branch `git pull --no-rebase origin <base>` and
   `git push origin <branch>`. Parts not in the provenance table disappear on
   this pull; push them first to keep them.

Stop until he answers.

## After the gate

1. Apply the approved renames and cleanup as one commit, and each approved
   logic fix as its own commit. Run step 5 again.
2. Push only when every line equals the gate's line, or differs exactly as an
   approved item says. Otherwise: no push, report.
3. Push, then open the PR with the body from the `pr` skill. The Summary
   carries the provenance table.
4. Hand off: `! gh pr merge <N> --merge`, then tell me. (`gh pr merge` is
   denied to the agent.)
5. **Sync** his branch:
   - Confirm that `origin/<base>` contains the merge commit.
   - Re-run `git status --porcelain` and `merge-tree`. Different from the
     gate's report → skip the sync and report. A gate answer never applies to
     a different conflict set.
   - Else `git pull --no-rebase origin <base>`; the whole-file base side only
     for the files approved at gate item 7. No stash, no `-X theirs`. Push.
6. Delete `integrate/<topic>` only after `git merge-base --is-ancestor` shows
   it is in the base. `git worktree prune`. Report each new head.
