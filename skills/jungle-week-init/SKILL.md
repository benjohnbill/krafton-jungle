---
name: jungle-week-init
description: Day-1 bootstrap of a new Krafton Jungle week repository — build labels, .clangd, .gitignore, the issue script and GitHub Project board, and the week CLAUDE.md four-slot draft. Use when a new weekNN/ repository appears under ~/dev/krafton-jungle or he says "새 주차", "N주차 세팅", "이번 주 세팅", "주차 시작".
---

# jungle-week-init

A conditional checklist. Each item runs when its condition holds and is
skipped aloud when it does not: the upstream layout changes every week. The
previous week's files are the templates: `LATEST` = the highest-numbered
sibling `weekNN/` that has a `GNUmakefile` (week05 today).

## 0. Facts, then questions

Facts (look, do not ask): the new repository's path, `git remote -v`
(upstream vs origin), the build system upstream ships (`Makefile`, CMake,
none), the exercise layout, a README that states the order.

Then one message, numbered, and wait:

1. Week number and title for the board ("Week N").
2. Solo tutoring or a team project? A team week gets `Mode:` on the first
   line of its CLAUDE.md.
3. What step 2 is this week (the representation he must draw).
4. Where the problem statement lives, and which blocks are spoilers.
5. What "verify" means this week (the exit-0 check, a test runner, a grader).
6. The velog WIL post URL of the previous week, and this week's name for
   the study index heading (for example `C언어(2) [Debugging lab]`).

## 1. Build layer — if upstream ships a Makefile

Copy `LATEST/GNUmakefile` and keep its shape: `include Makefile`, a
hand-written exercise list (tab completion needs literal names), the labels
`r_` `g_` and, when a container exists, `dr_` `dg_` `dcheck` `dshell` with
`DOCKER_TTY ?= -it`. Upstream files stay untouched. Criterion:
`make <first exercise>` builds and `make` alone prints the label help.

Without a Makefile: a minimal one with the same labels.

## 2. `.clangd` — if the language is C or C++

Copy `LATEST/.clangd`; set its flags equal to the build's `CSTD` + `WARN`.

## 3. `.gitignore`

Build outputs (`build/`, `build-docker/`, binaries beside sources).

## 4. Issues — if `issue-template/weekN_issues_complete.csv` exists

Copy `~/dev/krafton-jungle/make_week05_issues.py` to `make_weekNN_issues.py`
beside it; adapt `REPO`, `WEEK`, `ROOT`, `CSV`, and the collector that pulls
each exercise's statement (question 4). The five `공통 -` rows are the same
every week. `--dry-run`, then run. Criterion: `gh issue list --limit 100`
count equals the CSV row count.

## 5. Board

```
gh project create --owner benjohnbill --title "Week N" --format json
gh project item-add N --owner benjohnbill --url <issue url>   # each issue
```

Note the project number; it becomes `Board: N` in the week CLAUDE.md. IDs are
never cached (`jungle-close` looks them up). Criterion: `item-list` shows
every issue as Todo.

## 6. Week CLAUDE.md — the four slots

Draft from the spine's slot list (`~/dev/krafton-jungle/docs/tutor-spine.md`,
last section) and the answers to questions 2–5. `LATEST/CLAUDE.md` is the
shape reference. CLAUDE.md is user scope: write the draft to
`~/dev/krafton-jungle/docs/proposals/weekNN-claude-md.md` and give him the
copy command. Criterion: he confirms the file is in place.

## 7. Study index — the previous week's WIL link and this week's heading

In `~/dev/krafton-jungle/benjohnbill.github.io/index.html` (rules: that
repository's `AGENTS.md`):

- Add `<a class="wil" href="<URL>">WIL →</a>` inside the previous week's
  `<div class="gh">`, after its `<h2>`. Skip aloud when he has no post yet.
- Add an empty group for this week with the heading `N주차 · <name>` only
  when he wants it shown before its first page; otherwise the first card
  creates it.

Commit in that repository (`Link the week N-1 WIL post from the study
index`). Push when he confirms; he reviews it on the live site. Criterion:
the live index shows the link.

## 8. First commit

In the week repository: `Add local build layer, clangd config, and tutoring
protocol for week N`, listing in the body what was skipped and why. Push only
when he asks.

## Report

Numbered: what ran, what was skipped (with the condition that failed), the
board number, the proposal path and its copy command.
