# The agent generates code; he types it as the critic

The course says to implement "직접", without AI code generation. He reads "직접" as this: he types every line himself, after its questions and hypothesis checks pass. The agent generates the code. He questions it and judges it. The failure to prevent is copy-paste ("가장 경계할 것은 '무지성 복사/붙여넣기'이지", L205). A unit is done when he can explain why each line exists and is needed, and when, with an agent at hand, he could produce the same code again (L205; he said "기준이 될 수도 있다", so this is a working criterion). Teammate PRs get the same treatment: "일종의 AI-generated Code와 본질적으로 다르지 않다" (L205). He sees this as a study method and also as a base method for AI coding: "사실상 내가 비판자로서 존재하는 거지" (L332). Basis: Shen & Tamkin, arXiv 2601.20245. Method: `docs/transcription-mode.md`.

**Considered Options**: Closed-book retyping (type from memory, then diff). Rejected: he does not want memorization; he types with the code visible. A ref branch that holds the agent's code. Rejected: the code is shown in chat only.

Source: session 9a9b8353 (2026-10-22), lines L205, L332.
