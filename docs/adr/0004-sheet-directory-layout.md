# Sheets live in notes/sheets/<stage>/, one file per function

Layout: `notes/sheets/<stage>/INDEX.md` for the stage, and `notes/sheets/<stage>/<func>.md` for each function, named with the C identifier. Uppercase names are role files (`INDEX.md`); lowercase names are subjects (`fork.md`). The reason is his: "sheet 문서 디렉토리 구조가 곧 내가 '무엇을 / 어떤 단위로' 구현했는 지에 대한 그래프가 된다고 봐서" (L445). His first idea was an uppercase name for every sheet; the agent narrowed uppercase to role files only (Q38, Q39), and he agreed: "38, 39 모두 동의" (L464). Do not rename sheets to a flat or uppercase scheme; the directory itself is the record of units.

Source: session 9a9b8353 (2026-10-22), L445, L464.

**Superseded** by ADR 0006 (2026-10-25): one stage sheet; the directory no longer holds one file per function. The record of units is the Function task list.
