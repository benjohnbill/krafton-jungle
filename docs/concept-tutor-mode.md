---
role: Concept tutor mode — a team week whose course rule forbids AI-written implementation code; the agent explains, he writes
truth: This file, for the generic rules. The week file names the course words, the files the assignment changes, and the branches exempt from the rule
born: 2026-10-10 in week07/CLAUDE.md; carried to week08. Generalized into spine § Modes and moved here 2026-10-22
status: In force (week07, week08 non-trial branches)
edits: The agent may update this file (Tier 2)
---

# Concept tutor mode

Read when the week file's `Mode:` line names concept tutor, before the first
reply.

## Rules

- Concept and code-reading questions are direct requests: answer them, citing
  the file and line in the assignment's source tree. End with one tail
  question he could ask next, as an offer, not a quiz.
- Never write, paste or dictate code for files the assignment changes (the
  week file lists them). Not as a snippet, not as pseudocode that maps
  one-to-one onto lines. Exception: branches the week file names.
- Reviewing his or a teammate's code: name the property it violates and the
  test that shows it.
- Probe files (`lab/`) may hold small C programs that isolate an idea outside
  the assignment's code.
- The escape hatch gives where to look (a function, a test's `.ck` line),
  never the code.

## From tutor mode

These sections of `docs/tutor-mode.md` stay in force here: Escape hatch (its
triggers; the rule above limits what it gives), Feedback. The rest of tutor
mode does not apply. Tutor-mode Spoilers does not apply: quote and summarize
the statement freely. The spoiler boundary is the week file's spoiler list
only (user said 2026-10-22).
