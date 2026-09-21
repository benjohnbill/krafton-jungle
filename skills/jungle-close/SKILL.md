---
name: jungle-close
description: Day-close routine for a Krafton Jungle week repository — verify the touched exercises, commit (Solve or WIP), push, set the GitHub Project board, give the next exercises as hints, print the two Logseq lines, rewrite the progress memo. Use when he wraps up — "커밋/push", "보드 갱신", "진도 반영", "프로젝트 보드 최신화", "오늘 마무리", "커밋하고 보드" — or asks for any subset of those.
---

# jungle-close

One pass, no pauses between steps. The only stop: a verify that fails on an
exercise he calls done (step 1). Report at the end as a numbered list.

## 0. Facts

- `WEEK` = `git rev-parse --show-toplevel`. Its `CLAUDE.md` slot 3 gives the
  lines `Verify:` (the verify chain) and `Board: N`.
- Touched exercises = paths under the exercise directory in
  `git status --porcelain` (week05: `challenges/NN_name/`), plus what he
  named in the request.
- Memory dir = `~/.claude/projects/<WEEK with every "/" replaced by "-">/memory/`
  (`/home/benjohnbill/dev/krafton-jungle/week05` →
  `-home-benjohnbill-dev-krafton-jungle-week05`).

## 1. Verify

For each touched exercise, run the week's verify chain. Week05: `make r_<name>`
on the host, then `make dr_<name> DOCKER_TTY=-i` in the container.

Criterion: every command exits 0 → the exercise is **Solve**. Any other exit →
it is **WIP**. If he called it done and it is WIP, stop here and show him the
failing output; nothing is committed yet.

## 2. Commit

One commit per exercise. Several exercises share one commit only when he asked
for that ("오늘치 다 커밋"); then the body is a numbered list, one item per
exercise, each item in the four-part shape.

Solve title: `Solve NN_name: <the cause, as one clause>`. Body: four parts,
prose, no headers.

1. What the buggy code did (which pointers, which order).
2. Why that produced the observed signal. Quote the glibc or signal text
   verbatim.
3. What the fix changed and what it deliberately left alone.
4. Where it was verified and the exit code ("Verified on the host and in the
   container (glibc 2.39): exit 0.").

Reference: `git -C ~/dev/krafton-jungle/week05 show eca29f3`.

WIP title: `WIP NN_name: <where he stopped>`. Body: what was confirmed, what
was killed, the next step.

Stage only the exercise files and `lab/` files he touched. Criterion:
`git status` is clean of those paths and `git log -1` shows the title.

## 3. Push

`git push origin master` when his request names push or 마무리. When it names
neither, commit, and end the report with "push도 할까요?". Criterion: the push
exits 0 and `git status -sb` shows no `ahead`.

## 4. Board

```
gh project item-list N --owner benjohnbill --format json --limit 100
gh project field-list N --owner benjohnbill --format json
gh project item-edit --id <item id> --project-id <project id> \
  --field-id <Status field id> --single-select-option-id <option id>
```

Match items by title suffix (`… - NN_name`). Solve → `Done`. WIP → `In
Progress`. The exercise he says he takes next → `In Progress`. Look every ID
up each time; cache nothing. Criterion: a fresh `item-list` shows the new
status for every changed item.

## 5. Next hints

Take the board's `Todo` items in board order, `구현 -` titles only, three of
them (or the number he asked). For each, read only the statement blocks that
slot 2 of the week file names (week05: `[시나리오]`, `[기대 동작]`) and give:
the name, the statement in one line, the concept it exercises (ownership,
lifetime, bounds, realloc, stack frame). The spoiler blocks stay unread.

## 6. Logseq lines

Two lines, chat only: line 1 = the invariant broken today, or the lesson;
line 2 = next. He pastes them.

## 7. Blog card

Only when he names the blog (`benjohnbill.github.io/` beside the week
repositories). Ask for the card's target when it is unclear.

## 8. Progress memo

Overwrite `<memory dir>/progress.md`:

```markdown
---
name: progress
description: Where he stopped at the last close — exercise, step, confirmed, next
metadata:
  type: project
---

**Exercise:** NN_name · **Step:** N of 5 · **Status:** Solve | WIP
**Confirmed:** …
**Killed:** …
**Next:** …
**Drill mode:** none | 03, 09, 19
**Closed:** YYYY-MM-DD
```

Ensure `MEMORY.md` in the same dir carries the line
`- [Progress](progress.md) — where he stopped at the last close`; the first
close adds it. Criterion: `progress.md` carries today's date and
`grep progress.md MEMORY.md` finds the line.

## Report

Numbered: commits (hash, title), push result, board changes, the hints, the
two Logseq lines.
