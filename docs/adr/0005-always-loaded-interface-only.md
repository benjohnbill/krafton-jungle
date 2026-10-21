# Always-loaded files hold only the interface; the spine is a router

An always-loaded file (a `CLAUDE.md`, the tutor spine) holds only the interface and what must not be touched: "CLAUDE.md 는 interface 및 핵심적인 내용들(혹은 건드리면 절대 안 되는 것)만 들어잇는게 맞다고 보거든?" (L807). Detail moves to on-demand docs behind pointers (L863). He applied the same standard to this repository, because the spine is always loaded too (L930). So `docs/tutor-spine.md` became a router: it selects the mode, and each mode has its own doc (`docs/*-mode.md`) (agent Q42; "OK", L988). A week file can select the mode per branch, and the mode does not change inside a session. He liked this: "별도 브랜치하고 서로 코드하고 문서 동기화만 잘 시키면, 다른 모드로 각각 사용 가능하잖아" (L1163). Do not move mode bodies back into the spine or the week `CLAUDE.md`.

Source: session 9a9b8353 (2026-10-22), L807, L863, L930, L988, L1163.
