---
scope: Document roles and layout for mini-redis and mini-dbms, learned from mini-react
decided: 2026-11-12 (grilling session; his decisions, not yet team rules); mini-redis section and Roles revised 2026-11-13
status: 확정 (개인 층). 팀 합의 전이므로 팀 레포에는 아직 적용하지 않음
read_when: before setting up the docs or file tree of mini-redis or mini-dbms
---

# Doc structure decisions

mini-react에서 ADR 하나가 요구사항 구체화, 설계 결정, edge case, 팀 절차를 모두 맡아서 과중해졌어요. 이 메모는 mini-redis와 mini-dbms에서 문서마다 한 가지 역할만 맡기기 위한 결정이에요. mini-react 레포는 고치지 않아요(Q1).

## Why

mini-react의 살아 있는 ADR 102개를 분류한 결과예요(대체된 3개 제외, 제목과 CAUTION으로 판단).

| Bucket | 개수 | 예 |
|---|---|---|
| Requirement reading (R) | 24 | `root-only-function-component` |
| Design decision (D) | 24 | `render-cursor-in-module-cells-in-instance` |
| Edge case (E) | 43 | `empty-text-node-stays-empty-string` |
| Team process (P) | 11 | `personal-branches-no-forks` |

세 조건을 통과한 ADR은 16개였어요. 원인은 셋이에요.

1. 형식: "결정 한 문장 + CAUTION"에는 맥락과 대안 칸이 없어서, 어떤 동작 문장이든 ADR이 될 수 있었어요. 이게 뿌리예요. `domain-modeling`의 기본 형식에서 벗어난 시험 형식이었어요.
2. `CONVENTION.md`의 "결정하지 못한 경우는 ADR과 테스트로 정하고" 때문에 `it.todo`가 ADR로 갔어요.
3. 요구사항 표의 `근거` 칸이 ADR 이름만 받아서, 판정을 받쳐야 하는 동작은 ADR이 되어야 했어요.

## Doc roles

뼈대는 matt-pocock 흐름이에요(Q20). 과정 때문에 더한 것은 요구사항 표와 ID 결합 둘뿐이에요.

```
 grill-with-docs  ── "why?" answers ──┬─► big why (architecture) ──► docs/adr/      (repo, stays)
   (team, 1 PC)                       ├─► words ─────────────────► GLOSSARY.md   (repo, stays)
                                      │
 to-spec  ────────────────────────────┼─► requirements ──────────► spec issue: User Stories
                                      ├─► small why ─────────────► spec issue: Implementation Decisions
                                      └─► edge cases to test ────► spec issue: Testing Decisions
 to-tickets ──► tickets (blocking edges)
 implement-spec ──► tdd ──► tests: edge case = test name (repo, stays)
                            local why = code comment   (repo, stays)
```

| Role | grill 중에 생김 | 레포에 남는 곳 |
|---|---|---|
| Requirement | spec의 User Stories | 요구사항 표 `해석`과 `근거` |
| Design (big why) | ADR 후보 | `docs/adr/` (두 겹 기준 통과분만) |
| Design (small why) | spec의 Implementation Decisions | 코드 주석 |
| Edge case | spec의 Testing Decisions | 테스트 이름 |
| Known limit | spec의 Out of Scope | 표의 `남은 일`, 없으면 `README.md`의 "알려진 한계" |
| Team rule | — | `CONVENTION.md` 줄과 이유 한 구절 |

## ADR (Q5, Q17, Q19)

- 형식은 `~/.claude/skills/domain-modeling/ADR-FORMAT.md`예요. 맥락, 결정, 이유를 1~3문장으로 쓰고, Consequences와 Considered Options는 쓸 가치가 있을 때만 써요.
- 거름망은 두 겹이에요. 둘 다 통과해야 ADR이에요.
  - Pocock의 세 조건: 되돌리기 어렵고, 맥락 없이 보면 놀랍고, 실제 트레이드오프의 결과예요.
  - Nygard의 "아키텍처에 중요함": 구조, 비기능 요구, 의존성, 인터페이스, 만드는 방법에 닿아요. 한 모듈 안의 표현 선택은 여기서 걸러져요.
- `docs/adr/` 하나에 평평하게 둬요. 하위 폴더는 없어요. 폴더를 나누던 이유(102개 찾아가기)가 사라지고, 역할 분배는 폴더가 아니라 `area`가 맡아요.
- 파일 이름에 번호를 붙이지 않아요. 브랜치마다 쓴 ADR의 번호가 병합 때 겹치기 때문이에요(`domain-modeling` 기본값과 다른 점).
- 결정 하나의 결과를 따로 ADR로 쓰지 않아요. 그 ADR의 Consequences에 한 줄로 써요.
- 이유 칸에는 팀원이 자기 말로 말할 수 있는 문장만 써요. 에이전트의 추론은 쓰지 않아요(Q17의 사례).

## Edge cases (Q9)

- 테스트 이름(한국어 동작 문장)이 기준이에요. 별도 문서는 두지 않아요.
- 테스트 이름에 없는 "왜"는 그 코드 줄의 주석으로 써요. `CONVENTION.md`의 "주석은 이름으로 말할 수 없는 이유만"과 같아요.
- 테스트를 비교하는 방법의 결정(예: 왕복을 `.value`로 비교)은 그 테스트 파일 맨 위 주석으로 써요.

## Requirements table (Q10, Q18)

칸은 `ID | area | LMS 문장 | 해석 | 충족 | 근거 | 남은 일`이에요.

- `해석`: LMS 문장이 여러 뜻으로 읽힐 때 우리가 고른 뜻이에요. 문장이 분명하면 `—`예요. 예: L9 "Hook 은 최상위 컴포넌트에서만" → "Root Component만 Hook을 부른다"(React의 "함수 본문 최상위"와 다름).
- `근거`: 테스트 ID를 직접 받아요. ADR 이름은 진짜 설계 결정일 때만 함께 적어요.
- `남은 일`: 일부러 지원하지 않는 것도 여기 적어요. 관련된 LMS 문장이 없는 한계는 `README.md`의 "알려진 한계" 절에 적어요.

## Coupling (Q15)

- ID 결합은 두 곳에만 둬요. ADR의 `결정:` 줄과 요구사항 표의 `근거` 칸이에요.
- 테스트 ID는 이 두 곳이 인용하는 테스트에만 붙어요. 나머지 테스트는 동작 문장만 가져요.
- 검사 스크립트는 두 곳의 ID가 실제 테스트로 있는지, ADR 이름이 실제 파일로 있는지 확인해요. 언어가 정해지면 만들어요.
- 결합은 다대다예요. 결정 하나를 여러 기능 파일의 테스트가 지켜요. 폴더 이름을 맞추는 건 사람을 위한 길 안내이고, 진짜 연결은 ID가 맡아요.

## Tests (Q14)

- 테스트 파일 하나는 기능 하나예요. Redis의 `tests/unit/expire.tcl`처럼 기능 이름으로 지어요. 소스 파일과 1대1이 아니어도 돼요.
- 여러 기능을 가로지르는 위험(동시성, 영속화, 크래시, Error)은 별도 파일로 둬요.
- `describe` 이름은 동작으로만 지어요. ID나 문서 형식(CAUTION)을 넣지 않아요.
- `CONVENTION.md`에 "모듈 → 테스트 파일" 지도 표를 한 번 적어요.

## Team rules (Q11)

- `team/` ADR 폴더를 만들지 않아요.
- 규칙의 이유는 `CONVENTION.md`의 그 줄에 한 구절로 붙여요.
- 과정 문구의 해석(예: "외부 프레임워크 금지" → 런타임 의존성 0개)은 팀 규칙이 아니라 요구사항 표의 `해석`이에요.

## Roles (Q6, 2026-11-13에 바뀜)

- 담당자 배정은 하지 않아요. 6단계는 팀 전체가 spec과 ADR을 같이 읽고 화이트보드 앞에서 "이렇게 작동하고, 우리는 이걸 배웠다"를 요약하는 자리예요. 양이 적으면 리뷰도 나누지 않아요.
- `area`라는 단어는 쓰지 않아요. 그 자리를 마일스톤 이름(`store`, `api`, `concurrency`, `expire`, `cache`, `persist`)이 맡아요. 이 이름이 마일스톤 폴더, ADR frontmatter, 요구사항 표의 칸, 테스트 파일 이름에 똑같이 붙어요.
- 옛 결정: `area`마다 담당자 한 명이 ADR, 표의 행, 테스트를 설명한다. mini-redis grilling(2026-11-13)에서 위 내용으로 바꿨어요.

## mini-redis 적용 (2026-11-12~13 grilling)

그의 결정이에요. 팀 규칙이 되려면 `CONVENTION.md` PR과 승인 1건이 필요해요. 근거와 마일스톤별 문제 초안은 `lab/redis/milestone-review.md`(로컬)에 있어요.

### 깊이

- 언어는 C예요. 해시 테이블은 Pintos `hash.c`를 가져다 쓰고, 인터페이스(`hash_insert`, `hash_find`, `hash_delete`)와 "버킷, 체이닝, 가득 차면 rehash"까지만 알아요(팀과 코치 합의). 해시 함수는 FNV-1 64비트예요(SHA-256 아님). 이 해석은 요구사항 표의 LMS #4 `해석` 칸에 코치 합의를 근거로 적어요.
- 범위는 LMS 1306 문장이 이름 붙인 것뿐이에요. eviction은 넣지 않고, 영속화(#12)는 선택이에요. 서버 프레임워크는 써도 되고 권장해요.
- grill 방식은 문제 먼저예요. AI가 문제를 내고, 팀이 답하고, AI가 고려할 점을 물어 유도해요. Redis의 실제 방식은 2단계 grill 끝, ADR을 쓰기 전에 공개해요. "Redis는 이래요, 여러분은요?"로 시작하지 않아요.

### 마일스톤

목록은 지금 고정하고, 마일스톤마다 `overview.md`는 앞 마일스톤의 6단계 끝에 실제 코드를 보고 써요. 사이클 하나는 약 3시간이고, 시간이 아니라 개념, 기능, 필요성 단위로 나눠 의존 순서대로 놓아요.

| M | 이름 | 주제 | LMS |
|---|---|---|---|
| M0 | — | 배관: `hash.c` 이식, 요청을 하나씩 받는 블로킹 서버, 테스트 도구, 검증 명령, CI, ID 검사 스크립트(Q15). grill 없음, 드라이버 한 명 | — |
| M1 | `store` | SET, GET, DEL | #2 #4 #13 |
| M2 | `api` | HTTP로 부르기 | #3 #10 #14 |
| M3 | `concurrency` | 서버 프레임워크 선택, 원자성, 느린 연산 | #8 |
| M4 | `expire` | TTL과 만료 | #9 |
| M5 | `cache` | cache-aside, 무효화, 캐시 유무 성능 비교 | #15 #11 #17 |
| M6 | `persist` | 영속화 (선택) | #12 |

- #16(엣지 케이스)은 매 사이클의 테스트 단계에 들어가요.
- 서버 프레임워크는 M3 grill에서 골라요. M0에서 고르면 M3에서 풀 문제가 사라져요.
- M0의 테스트 도구는 테스트마다 한국어 설명 문자열을 받을 수 있어야 해요. C 함수 이름에는 문장을 쓸 수 없어요.

### 사이클 (팀 워크플로 6단계)

1. 각자 공부하고 만나요.
2. grill-with-docs를 해요. 문제 먼저 받고, 끝에 Redis를 공개해요.
3. to-spec으로 `spec.md`를 쓰고, ADR을 써요.
4. to-tickets(작으면 생략)와 테스트를 만들어요.
5. implement-spec으로 코드를 만들어요.
6. `overview.md`, `spec.md`, ADR을 같이 읽고 Redis와 대조하고, 다음 `overview.md`를 써요.

ADR의 이유 칸에는 2단계에서 팀원이 말한 문장만 써요. AI가 이유를 지어내면 Q17 사례가 반복돼요.

### 문서: 기록 층과 현재 층

```
 HISTORY (written once, never rewritten)      CURRENT STATE (always true now)
 docs/milestones/<name>/                      src/, tests/
   overview.md  problems, deps, links         GLOSSARY.md
   spec.md      to-spec + "Redis와 대조"       docs/requirements.md
   issues/NN-*.md  to-tickets                 README.md  (links into history)
 docs/adr/      big why, superseded not edited
```

- 마일스톤 폴더는 그 시점의 생각을 남긴 기록이에요. 지난 폴더는 고치지 않아요. 결정이 바뀌면 다음 마일스톤의 `spec.md`가 밝히고, 새 ADR을 쓰고 옛 ADR의 `status`를 `superseded`로 바꿔요.
- 기능의 현재 모습은 코드, 테스트, `README.md`가 맡아요.
- 이슈 tracker는 GitHub Issues가 아니라 로컬 마크다운이에요(`setup-matt-pocock-skills/issue-tracker-local.md`의 형식, 경로만 `docs/milestones/<name>/`). spec이 레포 안에 남아야 6단계와 발표에서 다시 읽혀요. 팀 보드에는 마일스톤 카드만 두고 폴더를 링크해요. 이 설정은 팀이 쓰므로 팀 `AGENTS.md`에 넣어요.
- `overview.md`에는 Redis 답을 넣지 않고, LMS 문장은 다시 쓰지 않고 요구사항 표의 ID만 인용해요.
- `spec.md`의 "Redis와 대조" 절은 "우리 생각 → Redis → 우리가 고른 것" 순서예요. `README.md`가 이 절들을 링크해 발표 뼈대로 써요.
- ADR은 두 겹 거름망 그대로예요. "놀랍다"는 맥락 없이 코드를 보는 독자 기준이라, Redis와 같은 답도 큰 결정이면 ADR이 돼요. "Redis는 X" 같은 고정 칸은 두지 않아요(원인 1 반복).

### 파일 트리

```
mini-redis/
├─ AGENTS.md          read CONVENTION.md, GLOSSARY.md; issue tracker = local markdown
├─ CLAUDE.md          @AGENTS.md
├─ CONVENTION.md      team process + doc roles
├─ GLOSSARY.md
├─ README.md          milestone order, links to "Redis와 대조"
├─ Makefile           build, test, verify (M0)
├─ docs/{requirements.md, milestones/<name>/, adr/}
├─ src/               hash.c, list.c (ported), store, server
├─ tests/             <name>_test.c, functional/ (#14)
└─ .github/           ci.yml, pull_request_template.md
```

- `CONVENTION.md`는 mini-react의 번호 붙은 팀 규칙(브랜치, PR, 커밋)만 복사해요. 테스트 절의 "결정하지 못한 경우는 ADR로"(원인 2)와 `docs/adr/team/` 링크는 가져오지 않고, 링크는 이유 한 구절로 바꿔요(Q11). 코딩 스타일 컨벤션은 나중에 해요.
- 코드 주석, 알려진 한계, 테스트 ID 규칙은 위 절들의 결정 그대로예요.

## Open

- **Q8, Q13:** 팀이 확신하고 책임질 수 있는 결정의 기준과 grill 진행 속도예요. 첫 grill 세션 뒤에 정해요. 후보 기준은 "팀원 한 명이 버린 대안과 버린 이유를 말할 수 있으면 짧은 검색으로 충분하고, 말할 수 없으면 보류 목록에 올린다"예요. 보류 목록은 흩어져 조사한 뒤 `docs/research/<주제>.md`로 남기는 안이 있어요.
- **비판자 grill의 깊이 (2026-11-13):** grill AI가 이해도 확인이 아니라 비판자로 팀 설계를 공격하는 방향(깨지는 경우, 엣지 케이스, 다른 저장소와 비교, Redis 답을 우리 `hash.c`·C·HTTP에 옮겼을 때)에 그가 동의했어요. 공격의 양과 시간은 첫 grill(M1 `store`)을 해 본 뒤 정해요. 정해지면 `docs/agents/grill.md`로 레포에 넣는 안이 있어요. Q8, Q13과 함께 봐요.
- **팀 합의:** 이 메모는 그의 결정이에요. 팀 레포에 적용하려면 첫 grill에서 팀에게 보여 주고 `CONVENTION.md` PR과 승인 1건을 받아야 해요.
- **검사 스크립트:** 언어는 C로 정해졌어요. mini-redis M0에서 만들어요.

## Evidence

로컬에만 있어요(`lab/`은 `.git/info/exclude`로 추적하지 않음).

- `lab/doc-structure-trial/README.md`: mini-react `vnode` ADR 14개를 이 규칙으로 옮긴 시험이에요. 결과는 14 → 1이고, 정보가 사라진 곳은 없었어요. 빠진 "왜" 다섯 개는 코드 주석이 받아요.
- `lab/doc-structure-trial/requirements-sample.md`: `해석` 칸이 있는 요구사항 표 예시(S4, S24, S27)예요.
- `lab/doc-structure-trial/research/doc-roles-prior-art.md`: 문서 역할의 선행 사례예요. Nygard, arc42, Spec Kit, Kiro, Gherkin 등 출처 URL이 있어요.
- `lab/doc-structure-trial/research/test-layout-prior-art.md`: 테스트 파일 단위의 선행 사례예요. Redis, SQLite, CockroachDB, bbolt 등이 있어요.
- `lab/doc-structure-trial/research/cls.txt`, `map.py`: ADR 102개 분류와, ADR 인용을 테스트 파일에 대응시킨 스크립트예요.
