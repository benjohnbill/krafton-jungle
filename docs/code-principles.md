---
role: Code principles — the structure and comment rules that he and the agent share for code in a week repository
truth: This file, for structure and comments. Names and layout belong to the project style guide (the team `CONVENTION.md` in a team week)
born: 2026-10-29 (settled by grilling, user said)
status: Draft. First run: week09 mmap production code. After mmap, he revises it from that run and then fixes it
read_when: before the agent generates code that he types (transcription mode), and before a refactoring pass over his code
edits: The agent may update this file (Tier 2). Mark findings from a run with their date
---

# Code principles

First reader: him. He wants to write code by these principles, and to practice
reading agent-written code that follows them. When a rule helps the agent but
makes the code harder for him to follow, his reading wins. Agent navigation
cost (lookups and calls followed) is the tie-breaker only.

This file does not repeat the style guide. Layout is fixed by `clang-format`.
Name shape, one name per concept, and named constants are in the team
`CONVENTION.md` (C1–C6). No new mechanical check is added here. A mechanical
check is accepted only when no legitimate exception exists, and the existing
`clang-format` and `clang-tidy` already cover those cases.

## Absolute rules

No legitimate exception exists for these. A violation is fixed, not justified.

1. **A name does not lie.** A function with a query name (`find`, `get`,
   `is_`, `has_`, `lookup`) does not change state. If a function has a side
   effect, its name shows the side effect.
   Why: a reader trusts a name and skips the body. A lying name makes the
   reader skip the line where the bug is.
2. **Every failure path releases what the function acquired before it.** This
   includes memory, frames, page-table entries, locks, and open files.
   Why: a leak on a failure path does not fail a test until a later stage
   (swap, many processes) makes the path common.
3. **No comment restates the code.** The comment rule of transcription mode
   applies (`docs/transcription-mode.md`, "He writes code comments"). He
   writes a comment only when the code does not show the fact and the reason
   is not obvious.
   Why: a restating comment adds nothing, and it becomes false when the code
   changes.

## Judgment questions

Each question has a "yes" answer for good code. When the answer is "no", fix
the code, or write down why the code stays (a `[CJG]` comment or a sheet row).

1. **Split.** Does each function satisfy at least one of these conditions?
   - It has two or more callers or entry points.
   - It names a step that would otherwise need a comment.
   - It isolates a unit that can be tested alone.

   If none applies, keep the code in the caller. There is no line limit. A
   function longer than about 40 lines is a signal to ask this question, not
   a limit.
   Example: `vm_do_claim_page()` passes by the first condition. It has two
   entry points: `vm_claim_page()` (from an address) and
   `vm_try_handle_fault()` (from a page it already found).
   Why: a wrapper that adds one call adds one jump to every reading.
2. **Mixing.** Does each function body stay at one level for each concern? A
   body that calls a named step for a concern does not also do raw work on the
   same concern.
   Example to check: `vm_do_claim_page()` gets the frame from `vm_get_frame()`,
   but on failure it takes the frame apart by hand (`palloc_free_page()` and
   `free()`).
   Why: when acquire and release live at different levels, a change to one
   side misses the other side.
3. **Locality.** Can a reader understand the function without opening another
   file? A `static` helper sits near its caller.
   Why: each file opened is one more place to hold in mind, for him and for
   the agent.
4. **Explicit inputs and outputs.** Is all state that the function reads or
   writes visible in its parameters, its return value, or its name?
   Accepted exception: `thread_current()` in Pintos.
   Example to check: `supplemental_page_table_copy(dst, src)` does not use
   `dst`. Its helpers write into `thread_current()->spt`.
   Why: hidden state is the state that a test does not set up and a reader
   does not see.
5. **Grep uniqueness.** When you search a new name with `grep`, do the results
   show one concept only?
   Why: a name is the search key. A generic name (`process`, `handle`, `data`)
   returns every unrelated use.

## Refactoring a past exercise

The procedure for applying these principles to code he already wrote.

Scope and order: week09 VM code that he wrote (by function, not by line), then
week06, week04, week05. Python weeks are decided later. A function that holds
teammate lines is in scope. A hunk that changes teammate lines is marked in the
PR. He gets team agreement.

Method: transcription mode. He decides whether to fix a candidate and the shape
of the fix (a D row). The agent writes the hunk. He types it and asks
questions.

Each candidate goes into one bin:

| Bin | Meaning | Verification | PR |
|---|---|---|---|
| 1. Behavior kept | The fix does not change what the code does | `make dfast` result is the same as the baseline | Refactoring PR |
| 2. Small behavior fix | The fix changes what the code does, usually on a failure path | First show the failure (test, `lab/` probe, or gdb). After the fix, the failure is gone and `make dfast` has no regression | Separate PR |
| 3. Not reachable yet | The path cannot run in the current stage | None now | Deferred to the stage that reaches it |

Do not put bin 1 and bin 2 changes in one PR. If the test result changes, a
mixed PR cannot tell which change caused it.

Steps for one pass:

0. Survey the candidates again against the rules above, and give each one a
   draft bin. Save a baseline `make dfast` result.
1. Discuss each candidate: why it breaks a rule, whether to fix it, and the
   shape of the fix. He decides.
2. Bin 2 only: show the failure before the fix. If no failure shows, move the
   candidate to another bin.
3. Hunk loop: the agent gives a hunk, he types it and asks questions.
4. Verify by the bin. If the change touches `userprog/` or `threads/`, also run
   the userprog and threads suites.
5. Commit, and open one PR for each bin. Follow the week's PR and commit rules.
