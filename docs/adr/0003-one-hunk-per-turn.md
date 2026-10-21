---
status: proposed
---

# One hunk per turn, a 보류 line on a switch, and no row named first

The agent shows code one hunk per turn (about one spec sentence); a short function can go whole (L239). The limit on information is itself a source of questions: "'정보가 제한됌' 혹은 '미구현된 개념에 대한 궁금증' 등이 하나의 질문 소스가 될 수 있다고 봐서" (L239). When he switches to another hunk in the middle of a question, the agent writes one line `보류: <question>` in chat and in the sheet: "돌아갈 주소를 interrupt_frame 처럼 남겨두는 것" (L256). The hunk size and the 보류 line are his decisions.

The agent does not name the sheet row that a hunk closes. He names it, and the agent confirms or corrects it, so the sheet works as his checklist. He accepted this only provisionally: whether it limits his thinking or supports it is "'빈칸 채우기 세션'에서 적용한다고 보는게 맞겠고" (L383). Decide it after the fork trial.

Source: session 9a9b8353 (2026-10-22), L239, L256, L383.
