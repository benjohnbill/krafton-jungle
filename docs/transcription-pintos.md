---
role: Pintos notes for transcription mode — how the sheet fits the KAIST Pintos gitbook
truth: This file, for Pintos weeks only. The method is `docs/transcription-mode.md`
born: 2026-10-22 (moved out of transcription-mode.md "Open items")
status: Trial. The P3 part is a plan, settled after the P2 trial
edits: The agent may update this file (Tier 2). Mark trial findings with their date
---

# Transcription mode — Pintos notes

## Bindings

- Spec text = the KAIST Pintos gitbook (64-bit text). Test file = the test's
  `.c` and `.ck`. Debugger = gdb in the container.
- A stage = one gitbook stage.

## P3 (VM) — sheet shapes (open)

The P3 gitbook mixes requirement shapes, so the sheet mixes tables:

- T/F rows (S): mmap/munmap and the stack-growth limits.
- Function contracts: Memory Management, Anonymous Page, Swap.
- An invariant list and a design-decision log: the introduction, the fault
  handler, eviction, COW.

Make each stage's sheet when the stage starts, in gitbook order.

The P3 text has errors (for example, `vm/page.h` does not exist). Record
interpretations in the sheet, not quotes.
