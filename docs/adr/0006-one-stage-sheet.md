# One stage sheet replaces the per-function sheets and the S rows

A stage has one sheet, `notes/sheets/<stage>/<stage-title>.md`, made from `docs/templates/stage-sheet.md`. It has four sections: Function (task list), Decision (table `ID | 선택 | 이유`), Invariant (list), Delayed (task list). He keeps it open in a narrow Zed preview pane. Its job is the missing link between his flow diagram, his structure diagram, and the code: "흐름도/구조도/코드를 보면서 공부하는 나를 돕는게 목표잖아" and "남 보이려고 공부하는거 아니잖아". The questions themselves stay in the conversation; only the unresolved ones go to Delayed at session close. His reason: a document that is less accessible than the chat, not very readable, and not written by him is worse than asking the agent at once ("내가 쓴 것도 아니라고 한다면 … 그냥 너한테 즉각적으로 물어보는게 더 나은 것 같다").

Evidence from the trial (week09 Memory Management, 2026-10-24): he never opened the function sheets ("함수 단위는 내가 볼 생각도 안 했던 것 같거든"). An audit of about 60 questions found none answered by an existing row. Every T/F status stayed F.

Who writes what: he writes code comments, and only a comment that meets both of his conditions — the code alone does not show it, and the why is not obvious. He also writes the reason cell of a Decision row. The agent writes the rest. A sheet points at a comment by function name and the team tag (`` `hashing()` › [CJG] ``), not by `file:line`, because "나중에 내가 해당 파일을 바꾸거나 팀원의 다른 코드로 merge 당하는 것에 너무 취약". Line style (his): noun-ending fragments with an explicit subject and object, short names `_<core action>()`, no filler marks.

**Considered Options**: Keep per-function sheets and fill T/F at the end. Rejected: he did not know what to fill or how, and he never looked at them. One stage file with a full question log per function. Rejected: about half of the questions (hash.c internals, C syntax, git) would overflow the pane. A stage file with plain line lists. Rejected: the preview joins bare lines into one paragraph.

Supersedes ADR 0004, and the S-row part of ADR 0002. The rest of 0002 (Decision and Invariant rows come from dialogue; one pointer question) stays.

Source: session 00156fb9 (2026-10-24 to 2026-10-25).
