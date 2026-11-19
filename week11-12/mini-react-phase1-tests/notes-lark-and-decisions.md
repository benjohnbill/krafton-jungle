# Lead notes (raw, for the final summary)

## Lark rewording proposals
- Row 3 fromdom-text → child case: `<p>` with Text hello → children ['hello'] (DEC-02).
- Row 12 fromdom-comment-node → `<div><!-- 메모 --></div>` → children [] (DEC-02). Rename idea: fromdom-skip-comment-only.
- Row 8 fromdom-bool-attr: expected for `<input disabled>` is { disabled: '', value: '' } (ADR 0005).
- Row 51 int-render-roundtrip: add "View는 정규형: 입력칸 props에 value가 있고 주석이 없음".
- CREATE→INSERT (31, 33, 37, 44, maybe 101), row 44 ID patch-insert, row 9 fromdom-keep-whitespace: delegated to Lark agent (pending).

## Conversion unit (commit after 94b0e59)
- T39-T53 new, T34-T37 moved to round-trip.test.ts, R1-R5 new, T38 todo removed (covered by P17/P18 + I-READDP). No vnode.ts change.
- CONV-N021 not written (DEC-02 keeps Element input).

## History unit (94b0e59)
- H1-H17 pass, H18 todo (Lark 69 optional). ADR 0007. Verbs can/push/back/forward added. GLOSSARY StateHistory.

## Diff+Patch unit (commit below)
- D36 strengthened (frozen inputs, refs), D39 = DIFF-N05. P29-P37 new, P2/P14/P15/P17/P18/P21 strengthened. I1-I12 in diff-patch.test.ts (Lark 52-59 → I1-I7, I10 fuzz 500 seeded).
- Decisions: frozen Views valid input; empty PROPS = no change (ADR 0006 line added); PATCH-N07 idempotence not written (DEC-13); DIFF-N06 value ""→"" only partly covered.
- Trap: container leading whitespace makes path [] point at Text → told page agent.
