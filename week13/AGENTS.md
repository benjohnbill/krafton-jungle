Mode: team project (AI 함께하기), half personal. AI-together mode (`../docs/ai-together-mode.md`) until he refines the mode in a separate session.

# week13 (웹 서버 만들기)

One team repository, `mini-webserver`: a web server in C on POSIX sockets only, with a Forward Proxy or a Reverse Proxy. Each member builds on a personal branch with much autonomy, so the week is half a personal project. What must remain: he can explain each decision in his code in his own words (sockets, HTTP parsing, the concurrency model, the proxy), and the team keeps one merged code base with tests.

This file is the personal layer. It sits above the repository, so no teammate's clone has it.

## Mode

Course words (LMS `learning/1310`, read 2026-11-19): "결과물뿐만 아니라 과정도 중요합니다. AI가 작성한 코드를 완벽히 내 것으로 소화해 그 원리를 설명할 수 있어야 합니다." and "팀원 중 한 명이 대표로 레포지토리를 생성하고, 나머지 팀원을 초대하여 공동으로 사용합니다."

- His choice (2026-11-19): close to AI-together, but not the same. He refines the mode in another session. Until then, use the AI-together mode doc.
- AI-generated code goes on his personal branch `CJG` and can be pushed (user said 2026-11-19).
- `main` takes changes only through a PR, merged by merge commit. Ruleset `main 보호` (2026-11-19): requires a PR, 0 approvals, merge commit only, blocks deletion and force push, no bypass.
- D6 pilot: `week11-12/concepts_brief.md` § D6, "웹서버 주차 시험". One-paragraph key decision in each PR, one-paragraph ADR for the code the team keeps.

## Statement and spoilers

- Statement: https://jungle-lms.krafton.com/learning/1309 (웹 서버 만들기). Read it in Aside; the login is there.
- Week guide: https://jungle-lms.krafton.com/learning/1310 (schedule, CSAPP chapter 11, submissions).
- Spoiler list: none.

## Environment

- Repository: `mini-webserver/`, `origin` at `benjohnbill/mini-webserver` (public). He owns it and invites the team.
- Team board: https://github.com/users/benjohnbill/projects/8, linked to the repository.
- Stack: C with the standard library and POSIX APIs only. The course bans complete HTTP or event-loop libraries (libevent, libuv, nginx, Apache, mongoose). Build: a `Makefile` or `CMakeLists.txt`, TBD.
- His commits and PRs carry no Claude trace: no `Co-Authored-By: Claude` trailer, no "Generated with Claude Code" line.

Verify: TBD. He uses personal checks on `CJG`; none go to `main` yet. The course asks for unit tests, curl functional tests, a load test (ab, wrk, or hey), and a leak check (valgrind or `-fsanitize=address,leak`).

Board: 8

## Lab

`lab/` holds his hands-on probes in place of reading CSAPP chapter 11. It has its own `AGENTS.md` and its own mode (transcription, light). Settled 2026-11-19.

## Do not touch

No upstream or scaffolding exists. The agent changes the ruleset and team-tracked files only when he asks.
