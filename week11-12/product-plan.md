---
role: product (대조군과 실험군) 계획. 개인 층이며 팀원은 읽지 않아요
truth: 2026-11-09 grilling 세션의 합의. 근거 페이지는 benjohnbill.github.io/study/week11/framework-control.html
status: Draft. 대조군 명세는 확정(2026-11-10, agent-grilling). 빌드는 오라버니 승인 뒤. 실험군을 시작할 때 이 파일의 Deferred부터 다시 열어요
---

# product plan

## Decided

- **Product**: 나만무 팀 판독기 (잠정). 시연과 측정에는 가짜 데이터만 써요. 각 라이브러리가 필요한 이유가 제품 기능에서 자연스럽게 드러나는 것이 선택 기준이에요.
- **Variable**: 실험 변수는 "우리 프레임워크가 있는가 없는가" 하나예요. 진짜 React, Svelte, Vue와의 비교와 그쪽에서 아이디어를 가져오는 작업은 product 밖(`lab/`, mini-react PR)에서 팀이 해요.
- **Library interface**: mini-redis와 mini-dbms는 product 서버가 HTTP로 부를 수 있어야 해요. 과정 원문도 요구해요: 1306 "외부에서 해당 프로젝트를 사용", 1305 Phase 3 API 서버.
- **Answer-key separation**: 대조군은 페이지의 diff 트리, 측정 목록, 약점 주석을 보지 않고 기능 명세와 시나리오만으로 만들어요. 페이지는 "예측"으로 봉인해요. v1은 맥락 없는 새 에이전트나 팀원이 짜요.
- **Control quality**: 프레임워크 없이 보통 개발자가 짤 법한 합리적인 코드예요. 일부러 약하게 만들지 않아요.
- **Fixed contract**: `shared/types.ts`, `shared/participants.ts`(가짜 참가자 32명), 라우트, `shared/scenarios/`의 기능 시나리오 테스트를 고정해요. 파일 트리 전체는 고정하지 않아요. 실험군의 `+` 파일은 미리 만들지 않아요.
- **Spec**: 확정본은 `~/.claude/plans/product-control-spec/SPEC.delivered.md`, 과정과 근거는 같은 폴더의 `FINAL.md`예요. 라우트는 `GET /`, `GET /participants`, `PUT /surveys/me`, `POST /evaluations`, `GET /evaluations/me`, `GET /ranking?track=`예요. framework-control 페이지의 `POST /surveys`, `POST /preferences`, `GET /events`는 쓰지 않아요. 실시간 전달 방식은 계약에 없고 각 버전이 정해요 (답안지 분리).
- **Location**: `week11-12/product/` 로컬 git 레포로 시작해요. 원격 레포는 팀 결정 3(폴더 2개 또는 레포 2개)이 나온 뒤 오라버니가 만들어요.
- **Stack**: product는 TS예요. 개발 도구와 테스트 환경은 우리 라이브러리들과 맞추고, 런타임 의존성은 우리 라이브러리뿐이에요. Node v26은 `.ts`를 직접 실행해요.
- **Data scale**: `tools/seed.ts`는 고정 시드값을 쓰고 크기를 인자로 받아요. 100만 건 측정(인덱스 대 선형 탐색)은 mini-dbms 레포 안의 벤치마크로 해요. product에서 mini-dbms가 필요한 근거는 규모가 아니라 새 조건 추가와 동시 쓰기예요. 데이터는 현실 규모(반 32명)로 둬요.
- **Layout**: product 레포 하나에 `control/`과 `experiment/`를 최상위 폴더로 둬요 (오라버니 결정 2026-11-09). 팀 결정 3의 A안과 같아요. 두 버전이 함께 쓰는 계약과 테스트는 세 번째 최상위 폴더 `shared/`에 둬요. 버전 폴더가 아니라서 이 결정과 충돌하지 않아요.
- **Build**: 대조군 v1은 `~/build/najungle-app`(중립 레포)의 `app/`에서 격리된 세션이 빌드하고, 검증 뒤 `product/control/`로 옮겨요. 절차는 `FINAL.md` § Verification plan이에요.
- **Timing**: 실험군은 mini-redis와 mini-dbms를 완성한 뒤에 만들어요. 대조군은 우리 라이브러리가 필요 없으니 더 일찍 시작할 수 있어요. 처음 grilling의 Q13 답은 대조군과 실험군을 헷갈린 답이었어요 (오라버니 정정 2026-11-09).

## Deferred

대조군을 시작할 때 정해요. 그 전에는 팀 워크플로우로 제안하지 않아요. 오라버니가 변경 카드 한두 장으로 먼저 혼자 시험해요.

- **불편 일지**: 일지가 생긴 이유는 불편이 처음 쓸 때가 아니라 변경할 때 생기기 때문이에요. 변경 요청 카드를 하나씩 대조군에 적용하고 일지에 적어요. 카드 내용은 팀이 써요.
  - 기록 순서 (Q4): 있었던 일부터 적고, 분류는 나중에 붙여요. 어디에도 맞지 않는 장면은 "기타"로 남겨요.
  - 분류 축 (Q1): "누가 겪나". 후보 이름은 ISO/IEC 25010의 performance efficiency(사용자), reliability(데이터), maintainability(바꾸는 사람)예요. 표준 이름은 아직 원문으로 확인하지 않았어요.
  - 변경 비용 (Q2): Ousterhout, *A Philosophy of Software Design* 2장의 세 증상, change amplification, cognitive load, unknown unknowns로 기록해요.
- **AI 변경 비용 (Q3)**: 같은 모델, 새 세션, 같은 카드 문장으로 두 버전에 적용해요. 재는 항목은 `git diff --stat`, 읽은 파일 수, 카드 범위 밖에서 깨진 테스트, 사람 개입 횟수예요. 타이핑 시간은 재지 않아요. 카드 하나당 한 번 실행하니까 결과는 증명이 아니라 관찰이에요. 방향 근거는 DORA 2024 보고서(AI 도입과 delivery stability 하락의 상관관계, 설문 기반)예요.
- **예측 → 측정 → 판정 형식**: 카드마다 역사에서 나온 예측(출처는 프레임워크 공식 문서의 "왜")을 한 줄 붙이고, 측정한 뒤 판정해요. 예측이 맞으면 "그 이유는 지금도 살아 있다", 틀리면 "AI가 그 비용을 지웠다"가 발견이에요. 비용은 카드 다섯 장이면 AI 실행 열 번이에요.
- **S5 자동 테스트**: 실시간 반영의 브라우저 자동 테스트는 v1에서 빠졌어요. 새 개발 의존성(브라우저 실행기)이 필요해서, 실험군을 만들 때 정해요.
- **측정 코드 위치 (Q6)**: 잠정안은 측정 코드를 앱 밖에 두는 거예요. 측정 1은 기능 테스트의 `MutationObserver`, 측정 2, 3, 5는 `tools/load.ts`, 측정 4는 `git diff --stat`로 재요. 측정을 붙일 때 오라버니에게 다시 보여 드려요.
- **설명 책임**: 대조군에서 오라버니가 설명할 범위는 불편 일지에 적힌 곳이에요. 미리 약점 목록을 정하지 않아요.
- **Open**: 동료를 순위로 세워도 되는지, 점수순 정렬은 누가 하는지(mini-dbms ORDER BY 또는 mini-redis 정렬 집합). 둘 다 framework-control 페이지의 "아직 열린 것"이에요.
