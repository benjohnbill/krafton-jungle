---
name: jungle-week-init
description: Day-1 bootstrap of a new Krafton Jungle week repository (build layer, editor config, issue board in solo weeks, week CLAUDE.md draft).
disable-model-invocation: true
---

# jungle-week-init

A conditional checklist. Each item runs when its condition holds and is
skipped aloud when it does not: the upstream layout changes every week. The
previous week's files are the templates: `LATEST` = the highest-numbered
sibling `weekNN/` that has a `GNUmakefile`.

**Team week** (question 2): the repository is the team's. Everything this
skill makes is his personal layer, so it stays local: add each path to
`.git/info/exclude`, and the repo's own config, rules, and issues stand as
the team keeps them. §3, §4, §5, and §8 are skipped aloud.

## 0. Facts, then questions

Facts (look, do not ask): the new repository's path, `git remote -v`
(upstream vs origin), the build system upstream ships (`Makefile`, CMake,
none), the exercise layout, a README that states the order (and
`README.upstream.md` when it exists). Upstream test for the README: with an
`upstream` remote, `git log upstream/HEAD..HEAD -- README.md` is empty;
otherwise `git log --format=%h -- README.md` lists only the root commit, and
that commit holds a file other than README, LICENSE, and `.gitignore` files
(with only those files, the README is his own).

Then one message, numbered, and wait:

1. Week number and title ("Week N"; also the board title in a solo week).
2. Solo tutoring or a team project? A team week gets `Mode:` on the first
   line of its CLAUDE.md.
3. The course guide's words on AI use (he pastes them), and the mode they
   lead to: tutor mode (`docs/tutor-mode.md`), concept tutor
   (`docs/concept-tutor-mode.md`), transcription
   (`docs/transcription-mode.md`), or AI-together
   (`docs/ai-together-mode.md`).
4. Where AI-generated code may go: which branches, and whether it is ever
   pushed.
5. Tutor mode only: what step 2 is this week (the representation he must
   draw).
6. Where the problem statement lives, and which blocks are spoilers.
7. What "verify" means this week (the exit-0 check, a test runner, a grader).
8. The velog WIL post URL of the previous week, and this week's name for
   the study index heading (for example `C언어(2) [Debugging lab]`).

## 1. Build layer — if upstream ships a Makefile

Copy `LATEST/GNUmakefile` and keep its shape: `include Makefile`, a
hand-written exercise list (tab completion needs literal names), the labels
`r_` `g_` and, when a container exists, `dr_` `dg_` `dcheck` `dshell` with
`DOCKER_TTY ?= -it`. Upstream files stay untouched. Criterion:
`make <first exercise>` builds and `make` alone prints the label help.

When upstream `make check` runs each test in its own emulator (Pintos), add
`dfast` too: the whole suite with `-j$(nproc)`, `-icount shift=N,sleep=off`
and a short `TIMEOUT`. `LATEST/GNUmakefile` holds the rule and, in its
comments, why each part is there. Criterion: `make dfast` exits, and every
`.output` it judged is newer than the run's start.

Without a Makefile: a minimal one with the same labels.

## 2. `.clangd` — if the language is C or C++

Copy `LATEST/.clangd`; set its flags equal to the build's `CSTD` + `WARN`.
When the repo ships its own editor or style config (`.clangd`,
`.clang-format`, `compile_flags.txt`), that config is the source: add only
what it lacks, and lint and format results stay the team's.

When the copied `GNUmakefile` has a `compiledb` rule (Pintos weeks), run
`make compiledb` and exclude `compile_commands.json`: without it Ctrl+T finds
only opened files. He re-runs it after adding or removing a `.c` file.
Criterion: the command prints a file count, and `git status` does not show
the file.

## 2b. Barriers — trial from 2026-10-31

Read `~/.claude/docs/tool-guides/barrier-placement.md` first.

1. **Test protection.** If the repo has `pintos/tests/`, write
   `.claude/settings.local.json` with the `PreToolUse` hook that runs
   `~/dev/krafton-jungle/.claude/hooks/protect-upstream-tests.py` (copy it
   from `week09/.claude/settings.local.json`). Criterion: a real `claude -p`
   session started in the week repo is blocked when it edits an upstream
   test, and a new test file passes.
2. **`convention.py` fix — once.** If he brings `scripts/convention.py`
   forward, fix it before its first use: read each tool's `returncode`,
   report a tool failure apart from findings and exit 2, and label
   `clang-diagnostic-error` as a compiler error, not "naming". Defect and
   repro: `docs/dialectic/2026-10-31-rules-barriers/team-issue-draft.md`.
   Criterion: with fake `clang-format` and `clang-tidy` that exit 2 silently,
   `make lint` exits non-zero. Delete this item after the fix lands.
3. **`make verify`.** Propose `verify` = lint on the diff + the fastest full
   test runner. Lint-only CI only with the team's agreement.

## 3. `.gitignore`

Build outputs (`build/`, `build-docker/`, binaries beside sources).

## 4. Issues — solo week, if `issue-template/weekN_issues_complete.csv` exists

Copy `~/dev/krafton-jungle/make_week05_issues.py` to `make_weekNN_issues.py`
beside it; adapt `REPO`, `WEEK`, `ROOT`, `CSV`, and the collector that pulls
each exercise's statement (question 6). The five `공통 -` rows are the same
every week. `--dry-run`, then run. Criterion: `gh issue list --limit 100`
count equals the CSV row count.

## 5. Board — solo week

```
gh project create --owner benjohnbill --title "Week N" --format json
gh project item-add N --owner benjohnbill --url <issue url>   # each issue
```

Note the project number; it becomes `Board: N` in the week CLAUDE.md. IDs are
never cached (`jungle-close` looks them up). Criterion: `item-list` shows
every issue as Todo.

## 6. Week CLAUDE.md — the four slots

A week's `CLAUDE.md` is thin. It carries a one-paragraph purpose (what the
exercises are, and what must remain after them) and four slots:

1. **Step 2 and the ladder rungs** — tutor mode only
   (`docs/tutor-mode.md`): the week's representation, and the
   after-it-passes rungs in the week's terms.
2. **Where the statement and the spoilers live** — the file, block, or PDF
   that is the specification, and the blocks that are spoilers.
3. **Environment** — toolchain, build labels, container, custom commands,
   the verify chain (`Verify:` — the commands whose exit 0 means done), and
   the line `Board: <GitHub Project number>` (`Board: none` in a team week).
4. **Do not touch** — upstream-tracked files and fixed scaffolding.

Plus, for a team or build week, `Mode:` on the first line.

Draft from the answers to questions 2–7; the Mode section records the
course words and his answers to 3–4. `LATEST/CLAUDE.md` is the shape
reference. In a team week the file is local: an excluded `CLAUDE.md`, or
`CLAUDE.local.md` when the repo tracks a `CLAUDE.md` or `AGENTS.md`.
CLAUDE.md is user scope: write the draft to
`~/dev/krafton-jungle/docs/proposals/weekNN-claude-md.md` and give him the
copy command. Criterion: he confirms the file is in place.

## 6b. Transcription layer — if question 3 chose transcription mode

Create `notes/sheets/` and a `GLOSSARY.md` skeleton (`domain-modeling`
format) for the week's domain words; add both to `.git/info/exclude`. In
the week CLAUDE.md draft, Slot 2 names the sheet location. Criterion: both
paths exist and `git status` does not show them.

## 6c. README — core only

Read `~/.claude/skills/readme/SKILL.md` and follow it for the core only,
with `Status: active`.

- Solo week: the Map includes the personal layer from §1 to §6b. Commit
  the README with §8.
- Team week: write `~/dev/krafton-jungle/docs/proposals/weekNN-readme.md`
  only when the repo has no README or the upstream test from §0 holds. Its
  Map lists only paths a teammate's clone has, and it also carries the team
  sections. Otherwise skip aloud. When he owns the repo and asks, commit the
  README directly to the team repo instead of the proposal.

Criterion: `~/.claude/scripts/readme-check <readme> <repo>` exits 0.

## 7. Study index — the previous week's WIL link and this week's heading

In `~/dev/krafton-jungle/benjohnbill.github.io/index.html` (rules: that
repository's `AGENTS.md`):

- Add `<a class="wil" href="<URL>">WIL →</a>` inside the previous week's
  `<div class="gh">`, after its `<h2>`. Skip aloud when he has no post yet.
- Add an empty group for this week with the heading `N주차 · <name>` only
  when he wants it shown before its first page; otherwise the first card
  creates it. Either way, the heading text is wrapped in
  `<a class="wk-repo" href="https://github.com/<owner>/<repo>">`, the
  `origin` of this week's repository.

Commit in that repository (`Link the week N-1 WIL post from the study
index`). Push when he confirms; he reviews it on the live site. Criterion:
the live index shows the link.

Then the README of `LATEST`: run the `freeze` guards of
`~/.claude/skills/readme/SKILL.md` first. Only when they pass, write
`Learning log: <URL>` in that README, then follow `freeze`, push included.
When a guard fails, skip aloud with the guard that failed.

## 8. First commit — solo week

In the week repository: `Add local build layer, clangd config, and tutoring
protocol for week N`, listing in the body what was skipped and why. Then push.

## Report

Numbered: what ran, what was skipped (with the condition that failed), the
board number, the proposal paths and their copy commands, the README result
(this week's core, and the `LATEST` freeze or the guard that skipped it).
