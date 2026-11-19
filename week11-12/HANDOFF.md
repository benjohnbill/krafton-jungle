# Handoff

> Generated: 2026-11-10
> Project: krafton-jungle/week11-12/product (the team "product" repository, local only)
> Session summary: Settled and built the control version (no framework) of the product "나만무 팀 판독기"; next is v1.1, a Belbin team-fit feature.

## Goal

The team builds three libraries (mini-react, mini-redis, mini-dbms). `week11-12/product/`
holds one product built twice: `control/` with no framework, `experiment/` with the
team libraries. The difference is measured with the three course comparisons. This
session finished control v1. The next session adds **v1.1: team fit by Belbin team
role**: "would a person of role A fit well in this team?", answered from fake past
records of several cohorts. The feature exists because a team-matching site's owner
would want it (not to manufacture a measurement gap), and it makes two course
comparisons natural: find past teams by role mix = linear scan; open one team by id =
index; the same role-mix question repeated = the cache slot.

## Current State

**Working:**
- `product/` commit `1ac5070`: control v1 in `control/` (server, domain, web), shared
  contract in `shared/` (`types.ts`, `participants.ts`, `scenarios/` with S1–S7 tests,
  `CHECKS.md`), `SPEC.md` at the root. `npm ci`, `typecheck`, `check`, `test`, `build`,
  `test:functional` (48 tests) all pass; `git status --porcelain` empty after them.
- `CHECKS.md` 7 browser rows: all PASS on 2026-11-10, run through the Aside browser
  (S5 live update 24–25 ms after the 201).
- Scripts take `APP` (default `control`): `npm run start`, `npm run reset`,
  `npm run build` use `${APP:-control}/…`. Data per `INSTANCE` (default `main`).

**Known limits (not broken, record them):**
- `control/server/config.ts` puts `dist/` and `.data/` at the repo root
  (`new URL("../../", import.meta.url)`). When `experiment/` exists, the two versions
  will share them. Give each version its own folder then.
- `product/` has no remote. Creating one is the user's call (team decision 3).

## Files in Play

| File | Why It Matters |
|------|---------------|
| `week11-12/product-plan.md` | Decisions: product, answer-key separation, layout, comparison plan, v1.1 section, deferred items. Read first |
| `week11-12/product/SPEC.md` | The control spec v1 (contract, error table, score rule, S1–S7, P1–P5). v1.1 spec is an addition to it |
| `week11-12/product/shared/types.ts`, `shared/participants.ts` | The fixed contract and the 32 fake people. v1.1 adds types here |
| `week11-12/product/shared/scenarios/` | Black-box tests; `harness.ts` spawns the server in a process group per test file |
| `~/.claude/plans/product-control-spec/FINAL.md` | Full record of the agent-grilling run: decision log J1–J89, verification plan, isolation flags |
| `~/.claude/plans/product-control-spec/containment.py`, `deliver.py` | Leak check (exit 1 on hit; `--delivery` mode) and the SPEC delivery stripper |
| `~/build/najungle-app` | The neutral, isolated build repo (commit `78b91be`). v1.1 is built here on top of v1, then copied back |

## What Has Been Tried (and Why It Failed)

### Change cards + pain journal
- **What:** apply "requirement change" cards to the control one by one and journal the pain.
- **Why dropped:** the user has at most 2 days, nobody had a concrete answer for who writes cards, who feels the pain (an AI does the edits), and who writes the journal. Replaced by the three course comparisons plus an optional 30-minute hands-on change per library.

### Project `.claude/settings.json` deny list for the builder
- **What:** ship a deny list in the build repo.
- **Why it failed:** a PreToolUse hook blocks writing settings files (protected boundary). Do not bypass. CLI `--disallowedTools` flags work instead (see Constraints).

### Measuring index and cache at 32 rows
- **Why it fails:** at the real class size the differences are near zero. The user chose to get scale from a real feature (v1.1 past records), not from adding data only for the measurement.

### Spec lines chosen by predicted pain
- Typing/cursor preservation, a 32-way simultaneous submit, evaluation history, and a body-less `/events` route were cut: they copied the study page's measurement list (answer key). Rule kept: every requirement is an owner need.

## Current Best Theory

Write the v1.1 spec as an addition to `SPEC.md` (the user agreed: no 6-round panel,
only the leak check and the question agent), build it in `~/build/najungle-app` with the
same isolation, verify, and copy back to `product/control/`. Keep the statistic simple:
"mean past satisfaction of teams with the same role mix" — anything more breaks the
2-day budget.

## Next Steps

1. Read `week11-12/product-plan.md` (sections v1.1, Comparison, Deferred) and `product/SPEC.md`.
2. Confirm the 9 Belbin role names from a primary Belbin source (not done yet; the
   user was told this would be checked). Present them in English with short Korean notes.
3. Design with the user (ask, do not assume): what "past record" holds (cohort, team id,
   members with role, one satisfaction score?), how many fake past records (the scale
   must be large enough for the index and cache comparisons, honest as "several
   cohorts"), where a participant's own role comes from (survey field?), the route
   shape (for example `GET /team-fit?…`), and the page behavior.
4. Write the v1.1 addition in `~/.claude/plans/product-control-spec/` style: draft →
   `python3 -I containment.py` (HITS 0) → `deliver.py` → `--delivery` (DELIVERY 0).
5. Run the question agent in `~/build/najungle-app` (read-only flags, prompt asks for a
   numbered question list or "NO QUESTIONS"); fix the spec until NO QUESTIONS.
6. Commit the new `SPEC.md` (and any new `shared/` files you ship) in the build repo,
   run the isolated build session, run the post-build audit, rerun the five commands
   and porcelain, run the new browser checks (Aside, the user asked for this last time).
7. Copy back to `product/` exactly as in `FINAL.md` § Verification plan step 5
   (`app/` → `control/`, scripts keep `${APP:-control}`), run all checks, commit.

## Key Constraints

- Language: reply in Korean (해요체, call the user 오라버니); documents for agents in English.
- Every reply ends with the two-line `› 한 일:` / `› 다음:` block (`~/.claude/rules/closing-report-block.md`).
- No Claude trace in the user's commits or PRs (no Co-Authored-By, no "Generated with").
- Answer-key separation: the builder never sees `benjohnbill.github.io/study/week11/framework-control.html`, `product-plan.md`, the plan folder, or claude-mem. claude-mem observation 48067 holds the page's diff tree and measurement list verbatim.
- Builder session flags (proven in `~/.claude/plans/product-control-spec/evidence/ptest3.jsonl`, `ptest4.jsonl`):
  `claude -p "<task>" --setting-sources project --strict-mcp-config --allowedTools "Bash" "Edit" "Write" --disallowedTools "WebSearch" "WebFetch" "Read(//home/benjohnbill/dev/**)" "Read(//home/benjohnbill/.claude/**)" "Read(//tmp/claude-1000/-home-benjohnbill-dev*/**)" "Grep(//home/benjohnbill/dev/**)" "Glob(//home/benjohnbill/dev/**)" "Bash(*benjohnbill/dev/*)" "Bash(*~/dev/*)" "Bash(*krafton*)" "Bash(*claude-1000/-home-benjohnbill-dev*)" "Bash(*https://*)" "Bash(*github.io*)" --output-format stream-json --verbose > <plan>/evidence/build-v1.1.jsonl`
  For the read-only question agent, add `"Edit" "Write"` to the deny list.
- Post-build audit: scan tool_use inputs and tool_results of the build transcript for `benjohnbill/dev`, `krafton`, `claude-1000/-home-benjohnbill-dev`, `github.io`, `framework-control`, `ranking-cache`, `csv-store`, `dbms-client`, `evaluations.csv`, `mini-react`, `mini-redis`, `mini-dbms`, `store-file`, `users.csv`, `people.csv`, `대조군`, `실험군`, and web tools. Any hit discards the build.
- Keep `ls -A ~/build` = `najungle-app` only (probe files go to `<plan>/evidence/`).
- Stack: TypeScript, Node v26 runs `.ts` directly (`.ts` imports), Vite page, `node:http`, Vitest, Biome, no runtime dependencies, no new dev dependencies (an automated browser test of S5 is deferred until the experiment).
- Fake data only. Present Belbin as a frame for team composition, not a validated predictor (its validity research is mixed; its questionnaire is proprietary, the role names are fine to use).
- Time budget: at most 2 days for the whole product work. Keep v1.1 small.
- The study site and team conventions: change only when the user asks.

## Memory Pointers

- Observations: #48067 — the study page's answer key in claude-mem (why the builder runs with claude-mem off).
- Searches worth re-running: `search "product control spec agent-grilling"`, `search "Belbin team fit v1.1"`.
