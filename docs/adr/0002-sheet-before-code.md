# A spec sheet, written before the code, is the judging standard

He judges generated code against a sheet written before the code, as "코더들이 … 설계 명세서나 api 디자인 정리본을 별도로 만들어서 참고하는 것처럼" (L366). D (design decision) and I (invariant) rows come from dialogue with him: "그거 적는 과정에서도 너하고 대화를 하지 않을까 싶어 … 너는 원문/URL 등을 바탕으로 … 내 생각을 정리 및 검증해주는 느낌" (L366). If the generator also wrote the whole standard, its misreading would enter both the code and the sheet, and they would agree. Before the agent gives a relevant invariant, it asks one pointer question; if he does not reach it in that turn, it gives the answer (agent Q31, "31번 동의", L383).

**Status**: S rows (spec sentences judged T/F) are drafted by the agent with the source quote and URL, and he audits them. This part was an agent proposal (Q27) that he did not object to, but he did not approve it explicitly. Confirm it in the trial.

Source: session 9a9b8353 (2026-10-22), L332, L366, L383.

**Superseded in part** by ADR 0006 (2026-10-25): the S rows and T/F status were dropped after the trial.
