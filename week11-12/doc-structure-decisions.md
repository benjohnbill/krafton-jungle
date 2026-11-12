---
scope: Document roles and layout for mini-redis and mini-dbms, learned from mini-react
decided: 2026-11-12 (grilling session; his decisions, not yet team rules)
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

## Roles (Q6)

- 담당 영역 `area`는 LMS의 핵심 로직으로 나눠요. 주차 `CLAUDE.md`의 "Core logic to explain"이 후보 목록이에요. mini-redis라면 해시 테이블, 만료와 무효화, 동시성이에요.
- `area`는 세 곳에 똑같이 붙어요. ADR frontmatter(`area: expire`), 요구사항 표의 `area` 칸, 테스트 파일 이름이에요.
- 담당자 한 명은 자기 `area`의 ADR, 표의 행, 테스트 파일을 함께 설명해요.
- 정확한 `area` 목록은 첫 grill에서 팀이 정해요.

## Open

- **Q8, Q13:** 팀이 확신하고 책임질 수 있는 결정의 기준과 grill 진행 속도예요. 첫 grill 세션 뒤에 정해요. 후보 기준은 "팀원 한 명이 버린 대안과 버린 이유를 말할 수 있으면 짧은 검색으로 충분하고, 말할 수 없으면 보류 목록에 올린다"예요. 보류 목록은 흩어져 조사한 뒤 `docs/research/<주제>.md`로 남기는 안이 있어요.
- **팀 합의:** 이 메모는 그의 결정이에요. 팀 레포에 적용하려면 첫 grill에서 팀에게 보여 주고 `CONVENTION.md` PR과 승인 1건을 받아야 해요.
- **검사 스크립트:** 언어가 정해진 뒤에 만들어요.

## Evidence

로컬에만 있어요(`lab/`은 `.git/info/exclude`로 추적하지 않음).

- `lab/doc-structure-trial/README.md`: mini-react `vnode` ADR 14개를 이 규칙으로 옮긴 시험이에요. 결과는 14 → 1이고, 정보가 사라진 곳은 없었어요. 빠진 "왜" 다섯 개는 코드 주석이 받아요.
- `lab/doc-structure-trial/requirements-sample.md`: `해석` 칸이 있는 요구사항 표 예시(S4, S24, S27)예요.
- `lab/doc-structure-trial/research/doc-roles-prior-art.md`: 문서 역할의 선행 사례예요. Nygard, arc42, Spec Kit, Kiro, Gherkin 등 출처 URL이 있어요.
- `lab/doc-structure-trial/research/test-layout-prior-art.md`: 테스트 파일 단위의 선행 사례예요. Redis, SQLite, CockroachDB, bbolt 등이 있어요.
- `lab/doc-structure-trial/research/cls.txt`, `map.py`: ADR 102개 분류와, ADR 인용을 테스트 파일에 대응시킨 스크립트예요.
