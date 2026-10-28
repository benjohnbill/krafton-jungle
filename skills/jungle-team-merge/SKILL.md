---
name: jungle-team-merge
description: Pintos team weeks — verify my PR, a teammate's PR, or a broken develop on the latest base, and report; the user approves and merges.
disable-model-invocation: true
---

# jungle-team-merge

The team has no CI. This skill is his personal stand-in for it: a build on
the latest base before a merge, and a culprit report after a break. It reads
and reports. He types the code, approves, and merges.

## Boundaries — every mode

- **Read the team layer each run.** The PR template
  (`.github/pull_request_template.md`), the README branch, commit, and PR
  rules, and the merge rules from
  `gh api repos/<owner>/<repo>/rules/branches/<base>`. When the README and
  the ruleset disagree, the ruleset is the fact; list the gap under "team
  agenda" in the report.
- **Scratch only.** Every checkout, merge, build, and test runs in a
  detached worktree under the scratchpad. The week working tree stays as he
  left it: `git fetch` and read-only `git status` or `git log` only.
- **Container only.** Build and test in the container the week `CLAUDE.md`
  names, with the team's own targets (read the root `Makefile`):

  ```bash
  docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$WT":/work -w /work <image> make fast JOBS=<n>
  ```

  `make lint` runs where the week environment doc says. Two trees at once
  share the cores (`JOBS = nproc / 2`): `TIMEOUT` is wall time, and more
  QEMUs than cores turn passes into false `FAIL`s.
- **His hands only.** Code under `pintos/`, an approval, a merge, and any
  write to the ruleset, labels, projects, or issues are his. Push and
  `gh pr create` run only after he says yes in this run. Attribution follows
  the week `CLAUDE.md`.

## Mode

The line after `/jungle-team-merge` and the repo state pick the mode:

| Mode | Fits when |
|---|---|
| **A — open my PR** | his branch has commits not in `origin/<base>`, or he says he will open a PR, or asks the state of his open PR |
| **B — before I approve** | he names a teammate's PR number, or asks to check it before approval |
| **C — develop health** | the base fails to build or test, or he says it broke after a pull |

Two modes fit → one numbered question, then wait. The first output line names
the mode (`Mode B — before I approve #158`).

## Verify — the routine every mode uses

Input: a ref `X`, and whether to merge `origin/<base>` into it.

1. Worktree `X` (merged with `origin/<base>` when asked) and a **control**
   worktree at `origin/<base>`. A merge conflict ends the routine: report
   the files.
2. In both: `make lint`, then the container run. Keep both outputs.
3. Compare, and cite every line:
   - lint lines new in `X` (the base already fails lint, so compare, not
     require a clean pass);
   - tests `PASS` on the control and `FAIL` on `X` (regressions), and the
     reverse (progress);
   - build errors, conflict markers (`^(<<<<<<<|=======|>>>>>>>)`), and
     duplicate definitions, as `file:line`.
4. `git worktree remove` both.

## A — open my PR

1. If an open PR exists for his branch (`gh pr list --head <branch>`), go to
   step 5.
2. His branch behind `origin/<base>` → he syncs it by the README procedure in
   his own tree; wait. Verify his branch head merged with `origin/<base>`.
3. Draft the PR in the scratchpad. The body is the repo template, filled:
   - 🧪 table from step 2's lines (lint: "develop과 같은 N건, 신규 M건");
   - "주요 변경" holds the `diff` sketch of the `pr` skill
     (`~/.claude/skills/pr/SKILL.md`); the template stays the frame;
   - 담당 범위 and 🤝 공통 코드 영향 from the diff; a field only he can judge
     stays empty, marked for him.
4. One numbered message: the draft path, open questions, "push and open the
   PR?". On yes: `git push origin <branch>`, then
   `gh pr create --base <base> --title … --body-file …`.
5. **Status**: `gh pr view <n> --json reviews,commits,mergeable,mergedAt`.
   Report approvals against the ruleset count, and flag an approval older
   than the last commit.

## B — before I approve

1. `gh pr view <n> --json headRefName,baseRefName,files,reviews,body`, then
   `git fetch origin pull/<n>/head`.
2. Verify that head merged with `origin/<base>`.
3. Report `file:line` findings and where the measured lines differ from the
   PR's 🧪 table. The approval decision is his; post nothing on the PR.

## C — develop health

1. Verify `origin/<base>` alone.
2. Broken → find the culprit merge:
   `git bisect start --first-parent origin/<base> <last good>` in a scratch
   worktree, with the build or the failing tests as the bisect check.
3. Report the culprit merge (sha, PR number, author), the `file:line`, and a
   revert candidate as text (`git revert -m 1 <sha>`). Whether to revert or
   fix is the team's call.

## Report

Every mode ends with: the mode, what was measured (commands and shas), the
findings, and the team agenda when the README and the ruleset disagree.
