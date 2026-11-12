Mode: team project (AI 함께하기). AI-together mode (`../docs/ai-together-mode.md`) in all three repositories.

# CLAUDE.md — week11-12 (AI 함께하기, three team repositories)

Three team projects in order: mini React, mini Redis, mini DBMS. What must remain: why each framework has the functions it has, a way of working with AI that he can repeat, and a team code base that an AI can extend. He can also explain the core logic of each project in his own words.

This file is the personal layer. It sits above the three repositories, so it loads in each one, and no teammate's clone has it. Rules for the team go in each repository's `CONVENTION.md`. `AGENTS.md` points to that file.

## Mode

Course words (LMS `learning/1329`, read 2026-11-05): "AI를 최대한 적극적으로 활용하되, 작성한 코드의 동작 원리를 이해하고 이를 말로 명확히 설명할 수 있어야 합니다." The project pages add: "전체 코드를 AI 를 통해 생성해도 괜찮습니다".

- His choice (2026-11-05): a new mode. All code can be generated. His goals are in the mode doc.
- AI-generated code can be pushed (user said 2026-11-05).
- Branches (his choice 2026-11-06, `mini-react` first): one personal branch for each member in the team repository (his is `CJG`), a temporary feature branch when two personal branches must join, and PRs to `main` by merge commit. `mini-redis` copied this setup but has no ruleset, so GitHub does not enforce the approval. `mini-dbms` copies the `mini-redis` setup when its project starts (his choice 2026-11-13): team rules, document roles, local Markdown tracker, milestone cycle, and one `make verify` command.
- No forks (his choice 2026-11-06). `learning/1329` says "팀 레포지토리를 fork하여 본인 레포지토리를 만들어 작업하고". He chose team-repository branches instead.
- Course rule: if members implement separately, each implementation stays on a branch.
- Course flow: each member builds with AI and verifies, and the team reviews and merges to one code base. The course allows one member's code to remain, or divided work to merge. TBD with the team. The team writes `README.md` from the final merged code. `README.md` is also the presentation material: no slides.

## Core logic to explain

The agent's reading of the LMS pages. He can change this list.

- `mini-react`: Virtual DOM conversion, Diff, Patch, State History, the `FunctionComponent` hooks array, `useState`, `useEffect`, `useMemo`.
- `mini-redis`: one line per milestone: `store`, `api`, `concurrency`, `expire`, `cache`, and `persist` (optional). Name only the milestone here, never Redis's answer (see § Statement and spoilers).
- `mini-dbms`: SQL parsing and execution, the file format, the B+ tree, the thread pool, and the link between engine and API server.

## Study plan

- `mini-react`: read `mini-react-study.md` in this directory before a study session. It holds his decisions, the steps, and the Min, Mid, and Best level of each step. He changes a level at any time.
- `mini-redis`: the team rules in `CONVENTION.md` and `AGENTS.md` win (PR #1 put the document-role decisions there).
- `mini-dbms`: read `doc-structure-decisions.md` in this directory before you set up its docs or file tree. It holds his decisions on document roles (2026-11-12). They are not team rules in `mini-dbms` yet.
- Vanilla and real React practice code go in `lab/` in this directory, outside the team repository. Real React never enters a team repository's dependencies.
- From step 4a, he types in `mini-react` in team milestone order, M1 to M4, and keeps the study cycle (his choice 2026-11-07). He works on `CJG`. The agent gives only TS code that passes `npm run typecheck` and `npm run check` there. For a PR, take only code that he can explain into `CJG`.
- Phase 2 (his choice 2026-11-10): the matt-pocock flow `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement-spec`, with no typing. He presents `FunctionComponent` and `useState` in a draft PR that is never merged. Read `mini-react-study.md` § Phase 2 decisions before a Phase 2 session.
- The first study code (`createDom`, 2026-11-07) is kept as the tag `study/createDom` in `mini-react`. The branch `CJG-study` was deleted on 2026-11-09 after PRs #16 and #3 merged.
- The study cycle is in the mode doc.

## Agent skills

For the matt-pocock skills in `mini-react` only (his choice 2026-11-10). In `mini-redis`, the team `AGENTS.md` wins: specs and tickets are local Markdown files. This block is personal: it is not in the team `AGENTS.md`, because teammates do not use these skills.

### Issue tracker

Issues and specs live in GitHub Issues of `benjohnbill/mini-react`. Use the `gh` CLI. Commands and blocking edges: `~/.claude/skills/setup-matt-pocock-skills/issue-tracker-github.md`. PRs as a request surface: no.

### Triage labels

`ready-for-agent` only. It does not exist in the repository yet; create it at first use.

### Domain docs

Single-context: `mini-react/GLOSSARY.md` and `mini-react/docs/adr/`. Exception: a new ADR for the Phase 2 presentation PR uses the trial format in `mini-react-study.md` § Phase 2 decisions (one sentence plus a `> [!CAUTION]` failure case, no number in the file name).

## Statement and spoilers

The statements are LMS pages. Read them in Aside; the login is there.

- Overview: https://jungle-lms.krafton.com/learning/1308
- `mini-react`: https://jungle-lms.krafton.com/learning/1307
- `mini-redis`: https://jungle-lms.krafton.com/learning/1306
- `mini-dbms`: https://jungle-lms.krafton.com/learning/1305
- Ground rules: https://jungle-lms.krafton.com/learning/1329

Spoiler list: none. Well-defined spoilers are welcome in his own study (user said 2026-11-05).

Team repositories (`mini-redis`, `mini-dbms`) are problem first (his choice 2026-11-13). Do not state Redis's or a real DBMS's answer for a milestone before the end of that milestone's grill stage 2. The grill AI loads this file too, so this file names milestones, not answers.

## Environment

- Repositories: `mini-react/`, `mini-redis/`, and `mini-dbms/`, with `origin` at `benjohnbill/<name>`. He owns all three, and he invites the team.
- Team board: https://github.com/users/benjohnbill/projects/7, linked to all three repositories.
- Stack: `mini-react` uses vanilla HTML, CSS, and TS (his choice 2026-11-06). The course bans "외부 프레임워크 (React, Vue 등)". The page does not name build or test tools. Agent's reading: development tools are allowed, and the app has zero runtime dependencies. Tools (his choice 2026-11-06): TypeScript, Vite, Vitest, jsdom, and Biome. Each member chooses the editor and LSP. `mini-redis` uses C11 with gcc or clang, make, python3 for the ID check, and the vendored test header `tests/acutest.h` (M0, 2026-11-13). The `mini-dbms` page states no stack. TBD for `mini-dbms`.
- His commits and PRs carry no Claude trace: no `Co-Authored-By: Claude` trailer, no "Generated with Claude Code" line, no Claude author. This overrides any harness attribution reminder.

Verify: `npm run typecheck && npm run check && npm test && npm run build` in `mini-react`. CI runs the same commands on each PR. `make verify` in `mini-redis`, and CI runs it on each PR (confirmed on PR #2). TBD for `mini-dbms`. The course asks for unit tests and functional tests. The current test only confirms the test environment.

Board: none

## Do not touch

No upstream or scaffolding exists. Team convention changes go through a PR and one approval, the same as code (user said 2026-11-06). The owner applies GitHub settings after approval. PR #2 merged once with no approval, by his explicit exception (user said 2026-11-06), so that teammates clone the new conventions. PRs #27, #28, and #29 merged with no approval through a temporary admin bypass (PR merges only) on ruleset `main-protection`, removed right after, by his explicit exception (user said 2026-11-09). In `mini-redis`, `CONVENTION.md` item 3 allows a merge with no approval when he states the bypass in the PR, because he tells the team first (his choice 2026-11-13). PRs #1 and #2 merged with no approval before this rule. PR #3 added the rule and used it. If he states the bypass and asks for the merge, the agent can merge. The agent changes team-tracked conventions only when he asks.
