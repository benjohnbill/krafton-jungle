---
role: Pintos notes for transcription mode — how the sheet fits the KAIST Pintos gitbook
truth: This file, for Pintos weeks only. The method is `docs/transcription-mode.md`
born: 2026-10-22 (moved out of transcription-mode.md "Open items")
status: Trial. The P2 trial was skipped (2026-10-23, user said); P3 (week09) is the first real run, and its first function doubles as the trial
edits: The agent may update this file (Tier 2). Mark trial findings with their date
---

# Transcription mode — Pintos notes

## Bindings

- Spec text = the KAIST Pintos gitbook (64-bit text). Test file = the test's
  `.c` and `.ck`. Debugger = gdb in the container.
- A stage = one gitbook stage.

## P3 (VM) — sheet shape

Every stage uses the one stage-sheet shape (2026-10-25; the earlier plan of
mixed tables per stage was dropped with the `S` rows). Hard limits from the
gitbook (mmap/munmap rules, the stack-growth limit) go in as I lines.

Make each stage's sheet when the stage starts, in gitbook order.

The P3 text has errors (for example, `vm/page.h` does not exist). Record
interpretations in the sheet, not quotes.
