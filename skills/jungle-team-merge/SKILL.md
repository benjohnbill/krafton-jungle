---
name: jungle-team-merge
description: Team weeks — verify my PR, a teammate's PR, or a broken base branch on the latest base, and report; the user approves and merges.
disable-model-invocation: true
---

# jungle-team-merge

This skill is his personal check before a merge: a build and test on the
latest base, and a culprit report after a break. It stands in for CI when the
team has none. It reads and reports. He approves and merges.

## Boundaries — every mode

- **Read the team layer each run.** `AGENTS.md`, the PR template
  (`.github/pull_request_template.md`), the branch, commit, and PR rules in
  `README.md` or `CONVENTION.md`, and the merge rules from
  `gh api repos/<owner>/<repo>/rules/branches/<base>`. `<base>` is the PR
  target that the README and the ruleset name. No branch name is fixed. When
  the README and the ruleset disagree, the ruleset is the fact; list the gap
  under "team agenda" in the report.
- **Scratch only.** Every checkout, merge, build, and test runs in a
  detached worktree under the scratchpad. The week working tree stays as he
  left it: `git fetch` and read-only `git status` or `git log` only.
- **Repo commands.** Read the install, build, lint, and test commands from the
  repo's README or `package.json`. Install dependencies in each worktree when
  the commands need them.

  A repo with a `pintos/` tree: build and test in the container the week
  `CLAUDE.md` names, with the team's own targets (read the root `Makefile`):

  ```bash
  docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$WT":/work -w /work <image> make fast JOBS=<n>
  ```

  `make lint` runs where the week environment doc says. Two trees at once
  share the cores (`JOBS = nproc / 2`): `TIMEOUT` is wall time, and more
  QEMUs than cores turn passes into false `FAIL`s.
- **His hands only.** An approval, a merge, and any write to the ruleset,
  labels, projects, or issues are his. The agent never approves. The agent
  merges only when he asks for that merge explicitly, by the repo's merge
  rule. Code is his when the week's mode says so (a Pintos week: code under
  `pintos/`). Push and `gh pr create` run only after he says yes in this run.
  Attribution follows the week `CLAUDE.md`.

## Mode

The line after `/jungle-team-merge` and the repo state pick the mode:

| Mode | Fits when |
|---|---|
| **A — open my PR** | his branch has commits not in `origin/<base>`, or he says he will open a PR, or asks the state of his open PR |
| **B — before I approve** | he names a teammate's PR number, or asks to check it before approval |
| **C — base health** | the base fails to build or test, or he says it broke after a pull |

Two modes fit → one numbered question, then wait. The first output line names
the mode (`Mode B — before I approve #158`).

## Verify — the routine every mode uses

Input: a ref `X`, and whether to merge `origin/<base>` into it.

1. Worktree `X` (merged with `origin/<base>` when asked) and a **control**
   worktree at `origin/<base>`. A merge conflict ends the routine: report
   the files.
2. In both: the repo's lint command, then its build and test commands. Keep
   both outputs.
3. Compare, and cite every line:
   - lint lines new in `X` (a base can already fail lint, so compare, not
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
3. Draft the PR in the scratchpad. The frame is the repo's PR template, and
   its comments say what each field holds:
   - Fill the fields with `diff` code blocks and Mermaid, by the visual
     guidance of the `pr` skill (`~/.claude/skills/pr/SKILL.md`, § Summary).
   - The verification fields hold step 2's measured lines, against the base.
   - A field only he can judge stays empty, marked for him.
   - The author-check boxes stay empty.
4. One numbered message: the draft path, open questions, "push and open the
   PR?". On yes: `git push origin <branch>`, then
   `gh pr create --base <base> --title … --body-file …`.
5. **Status**: `gh pr view <n> --json reviews,commits,mergeable,mergedAt`.
   Report approvals against the ruleset count, and flag an approval older
   than the last commit.

## B — before I approve

1. `gh pr view <n> --json headRefName,baseRefName,files,reviews,body`, then
   `git fetch origin pull/<n>/head`. `<base>` is `baseRefName`.
2. Verify that head merged with `origin/<base>`. After Verify step 1 and
   before the build, run the impact list on the merged worktree `$WT`, with
   the edge types for the language from `~/.claude/rules/change-impact.md`
   (C is shown):

   ```bash
   codebase-memory-mcp cli index_repository --repo-path "$WT" --name pr-<n>
   codebase-memory-mcp cli detect_changes --project pr-<n> \
     --since origin/<base> --fixpoint true --via true --seeds list \
     --edge-types '["CALLS","USAGE","IMPORTS","WRITES"]'
   codebase-memory-mcp cli delete_project --project pr-<n>
   ```

   - Index the worktree of this run. The project of the week tree reads its own
     checked-out tree, so it cannot answer for a PR ref.
   - Do not put `test` in the name. A name with `test` removes edges from the
     index and rows from the list.
   - Compare `changed_files` with the `gh pr view` files. Report any difference
     with the list.
   - If a `*_has_more` field is `true`, read the next page with its cursor.
3. Report `file:line` findings and where the measured lines differ from the
   PR's verification fields. The approval decision is his; post nothing on the
   PR.
4. Report the impact list as candidates to read, not as findings:
   - A zero is not absence. Function-pointer dispatch is not linked: in week09
     #166, `anon_swap_out` has 0 callers, but `evict_frame` calls it through
     `swap_out(page)`.
   - `Field` seeds match by name. Read `via_qn` to the seed, and confirm in the
     source: in week09 #165, 38 of 75 rows start at `load_info.ofs`, and
     `lookup` is on the list for its own local `ofs`.

## C — base health

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
