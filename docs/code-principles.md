---
role: Code principles — the structure and comment rules that he and the agent share for code in a week repository
truth: This file, for structure and comments. Names and layout belong to the project style guide (the team `CONVENTION.md` in a team week)
born: 2026-10-29 (settled by grilling, user said)
status: Draft. First run: week09 mmap production code. After mmap, he revises it from that run and then fixes it
read_when: before the agent generates code that he types (transcription mode), and before a refactoring pass over his code
edits: The agent proposes a change; he approves it before it lands (user said 2026-10-31). Mark findings from a run with their date
---

# Code principles

First reader: him. He wants to write code by these principles, and to practice
reading agent-written code that follows them. When a rule helps the agent but
makes the code harder for him to follow, his reading wins. Agent navigation
cost (lookups and calls followed) is the tie-breaker only.

This file does not repeat the style guide. Layout is fixed by `clang-format`.
Name shape, one name per concept, and named constants are in the team
`CONVENTION.md` (C1–C6). A mechanical check is accepted only when no
legitimate exception exists. No tool checks any rule in this file today:
`clang-format` checks layout, and `clang-tidy` checks name case and braces
only (`week09/.clang-tidy:5`). Each rule below names who or what detects a
violation, and what that detector cannot see.

## Absolute rules

No legitimate exception exists for these. A violation is fixed, not justified
(no `[CJG]` exception). "Absolute" states how strong the obligation is. It
does not claim that a tool catches every violation: each rule names its
detector and the detector's blind spots.

1. **A name and its contract do not lie.** A caller can tell the observable
   effects (state changed, resources taken, failure results) from the name
   and the comment at the declaration, without reading the body. A query
   name (`find`, `is_`, `has_`, `lookup`) changes no state. An upstream
   Pintos API keeps its name: `palloc_get_page` takes a page and a lock, and
   its contract says so (`week09/CONVENTION.md:192`).
   Why: a reader trusts a name and skips the body. A lying name makes the
   reader skip the line where the bug is.

   | Detector | Covers | Blind spots |
   |---|---|---|
   | Review at the transcription close; a `pintos-index` card that shows member writes under a query name | Functions he types or reviews | Effects through globals or deep callees; code nobody reviews |

2. **Every acquired resource has a responsible owner until release or an
   explicit transfer, on every path.** This includes memory, frames,
   page-table entries, locks, and open files. On a failure path, the function
   releases what it still owns. A transfer (for example a frame handed to the
   supplemental page table) is written at the transfer point.
   Why: a leak on a failure path does not fail a test until a later stage
   (swap, many processes) makes the path common.

   | Detector | Covers | Blind spots |
   |---|---|---|
   | Review question at close: "On each early return, what does this function still own?" A bin-2 `lab/` probe that forces the failure (see below) | Paths he reviews or forces | Failure paths no test reaches. No sanitizer runs inside the kernel. The leak test `multi-oom` is in the userprog suite only (`tests/userprog/no-vm`), not in the VM suite |

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
6. **Comment.** Does each comment add a necessary fact that the code does not
   show? The comment rule of transcription mode applies
   (`docs/transcription-mode.md`, "He writes code comments"). A contract
   comment at a declaration (rule 1) counts as a necessary fact.
   Why: a restating comment adds nothing, and it becomes false when the code
   changes. No tool can judge this; a similarity check would reward deleting
   useful comments.

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

An unchanged `make dfast` result is a regression observation, not proof that
behavior is kept: it says nothing about failure paths no test reaches. A fix
that changes behavior on such a path is bin 2 or bin 3 even when the suite
stays the same.

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

## Candidate universal intents

Status: local candidates (user said 2026-10-31). They move to
`~/.claude/docs/code-principles.md`, with a pointer in
`~/.claude/rules/agent-operating-model.md`, only after one attempt to falsify
them on a non-C task. A second language can falsify an intent; it cannot
prove one. Source: `docs/dialectic/2026-10-31-rules-barriers/critique-c-universal.md`.

1. **Resource responsibility.** Every resource retained during work has a
   responsible owner until release or explicit transfer, failure included.
   The barrier changes per language: review and probes in C; `with` in
   Python, `defer` in Go, `Drop` in Rust, `using` in TypeScript.
2. **Predictable contracts.** A caller can tell accepted inputs, observable
   effects, and outcomes without reading the body.
3. **Contained decisions.** Changing a private decision while the public
   agreement stays the same does not force unrelated callers to change.
4. **Evidence matches the claim.** Confidence matches what the observation
   could detect, in the actual working environment.

The five judgment questions above are aids to intents 2 and 3 in C. They are
not universal by themselves.
