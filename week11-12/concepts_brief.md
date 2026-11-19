# Cross-repository carryover retrospective for the 나만무 first-day setup

* **Author:** benjohnbill
* **Date:** 2026-11-18 (Author Decisions 추가 2026-11-19)

## Reviewer Status

| Reviewer | Role title | Status |
| --- | --- | --- |
| `egm-design` | Skeptical Architect Brainstormer | completed |
| `egm-codebase-details` | Technical Accuracy and Reuse Brainstormer | completed |
| `egm-zoom-out` | Contrarian YAGNI Brainstormer | completed |
| `egm-comprehension` | Naive Reader Brainstormer | completed |
| `egm-implementation-readiness` | Implementation Readiness Brainstormer | completed |
| `egm-structural` | Structure Brainstormer | completed |
| `egm-inventive-catalyst` | Inventive Catalyst Brainstormer | completed |

근거 파일: `brainstorm-inputs/layer-table.md`, `brainstorm-inputs/carryover.md`, `brainstorm-inputs/tan-talk-report.md` (모두 `/home/benjohnbill/dev/krafton-jungle/week11-12/` 아래). 아래에서 `D#n`은 `carryover.md` § D의 n번 행, `B1`–`B3`은 `carryover.md` § B의 표입니다. `egm-codebase-details`는 mini 저장소 세 곳의 스크립트와 설정 파일도 직접 읽었습니다. 외부 저장소(matt-pocock skills, pstack)는 어느 reviewer도 읽지 않았습니다.

## Overview

**약점 먼저.** 이 회고는 지금 있는 근거로는 핵심 질문에 답할 수 없습니다. 핵심 질문은 "규칙이 다음 저장소의 첫날 상태에 어느 layer로 들어갔나"인데, 두 입력 표는 2026-11-18의 현재 상태를 적었습니다. 첫날 상태를 적은 표가 아닙니다. 그리고 회고가 바로잡으려는 실패, 곧 규칙이 다음 저장소로 이어지지 않은 것의 가장 큰 원인은 layer 선택이 아니었습니다. 저장소 파일 밖에 사는 것(GitHub 설정, 개인 `CLAUDE.md`)은 이어지지 않았고, 파일로 복사된 것은 Prose여도 이어졌습니다. 그래서 "더 높은 layer로 올리면 남는다"는 가정이 근거와 맞지 않습니다. 마지막으로, 목표인 "Human review 불필요"는 강의 규칙 "각자 코드를 자기 말로 설명"과 같은 Layer 5 칸에 섞여 있습니다. 둘을 나누지 않으면 성공 기준을 정할 수 없습니다.

**무엇을 하려는가.** 저자는 다섯 팀 저장소(R1 pintos-userprog, R2 Pintos VM, R3 mini-react, R4 mini-redis, R5 mini-dbms)를 시간 순서로 보고, 각 교정과 규칙이 다음 저장소의 첫날 상태에 이어졌는지, 다섯 layer(1 Codebase, 2 Static analysis, 3 Verification, 4 Prose, 5 Human review) 중 어디에 있었는지 판정하려고 합니다. 그 결과에서 언어에 묶이지 않는 부분을 골라 한 달 뒤 시작하는 나만무(5–6명, 5주, 스택 미정, AI 전면 허용)의 첫날 설정으로 만듭니다. 사용자는 나만무의 팀원 5–6명과 그들의 에이전트입니다. 팀원은 규칙을 따르지만 설계하지 않았습니다.

**리뷰가 남긴 핵심 가치.** 일곱 lens가 독립적으로 같은 결론에 닿았습니다. 나만무 첫날에 가장 값진 것은 규칙 목록이 아니라, (1) 저장소 설정을 git 안의 파일로 만들고 그 파일과 실제 설정의 차이를 검사하는 장치, (2) 언어에 묶이지 않는 계약(verify 진입점, required check 이름, test ID와 결정 인용 형식), (3) 교정을 모으는 장부(ledger)입니다. 근거로 보면 이 셋은 R3→R4→R5에서 실제로 끊긴 지점을 정확히 덮습니다.

## Author Decisions After Review (2026-11-19)

Goldfish 리뷰 뒤 저자와의 대화에서 정한 것입니다. 아래 Analysis와 충돌하면 이 절이 이깁니다. 이 절은 아직 Goldfish 리뷰를 받지 않았습니다.

### D1. 이 회고는 barrier-placement Trial의 첫 회고다

* `~/.claude/docs/tool-guides/barrier-placement.md`(2026-10-31 grilling 결정, 상태 "Trial. First run: the next jungle-week-init")가 Static layer를 만드는 방법을 이미 정했습니다. 이 회고는 그 규칙이 R3–R5에서 실제로 지켜졌고 작동했는지를 기존 사실로 판정합니다. 새 기준을 다시 만들지 않습니다.
* 이미 드러난 판정:

  | barrier-placement 규칙 | R3–R5의 사실 |
  | --- | --- |
  | § 1 `verify` 하나 | R4, R5에 `make verify` 있음(처음 R4 11-13, `carryover.md:128`). R3는 단일 진입점이 없고 CI job `code`가 네 명령을 돌림. § 1의 나머지 요구(도구가 죽으면 non-zero, `lint-diff` + `test-fast` 구성)는 판정하지 않음 |
  | § 1 "건너뛰고 통과라고 말하는 검사 금지" | R3 `check-decision-links`의 "인용 없는 새 테스트"가 CI에서 늘 `[건너뜀]` — 위반 |
  | § 2 팀을 묶는 것은 CI + required check뿐 | R3만 있음. R4, R5 없음. § 2는 사실 진술이고 R3–R5에 맞는 § 6 "week repo" 행은 required check를 요구하지 않으므로 "위반"이 아니라 "적용 안 함" (재리뷰 design 3, zoom-out 5). § 6 week repo 행의 첫 barrier(upstream 테스트 보호 hook)가 있었는지는 판정하지 않음 |
  | § 5 믿기 전에 증명(mutant) | 기록 없음 |
  | § 6 프로젝트 종류별 배치 | 나만무는 "Team or organization project" 행 |
* 새로 하는 일은 § 5 증명뿐이고, 나만무 후보 barrier에만 합니다(Key Decisions 6의 dry run과 같은 일).
* 이 회고의 결론으로 barrier-placement.md를 고칩니다. Trial을 끝낼지는 저자가 정합니다.

### D2. 저장소는 두 종류이고, Layer 5의 뜻이 다르다

* **학습 저장소** (앞으로 1달): 사람이 아는 것 자체가 결과물입니다. Layer 5는 줄일 비용이 아니라 목표입니다. 맞는 규칙의 예: PR #32 "설명할 수 없는 변경이라 파기".
* **프로젝트 저장소** (나만무): 아는 것은 수단입니다. 아래 D3의 것만 사람에게 남기고, 병합 gate는 Layer 1–3에 둡니다.
* barrier-placement.md § 6의 표가 이 구분의 자리입니다.

### D3. 에이전트가 코딩할 때 사람이 알아야 하는 것 (프로젝트 저장소)

A4의 "이해 범위" 질문에 대한 저자의 답입니다. 전체 코드도, 자기 코드의 함수 단위도 아닙니다.

| 무엇 | 누가 만드나 | 저장소에 남는 형태 |
| --- | --- | --- |
| 왜: 풀려는 문제, 요구분석 | 사람끼리 깊게 토론한 뒤 문서 | 요구분석 문서. 양이 적다 |
| 무엇과 증명: 기능, 상태, 작동한다는 증거 | 에이전트가 만들고 사람이 확인 | 시연, 테스트, 상태 다이어그램, feature map (Tan [9:40], [10:15], [12:58]) |
| 어떻게 | 코드 자체. 필요할 때 에이전트가 설명하거나 그림 (`code-map`) | 놀라운 것만 ADR |

* ADR 기준은 `domain-modeling` skill의 `ADR-FORMAT.md`(matt-pocock)를 따릅니다: 되돌리기 어렵다, 맥락 없이 놀랍다, 실제 tradeoff의 결과다 — 셋 다 참일 때만 씁니다. matt-pocock의 기준은 ADR을 "사람이 리뷰해야 한다"고 말하지 않습니다. 독자는 "나중에 코드를 보고 의아해할 사람"입니다.
* **사실:** R3 ADR은 94개이고 대부분 테스트와 ID로 묶인 동작 결정입니다. 이 기준으로 보면 ADR이라기보다 명세입니다. 나만무에서는 둘을 나눕니다.
* **반론 (아직 리뷰 전):**
  * Tan의 전제는 깊은 지식을 이미 프레임워크와 lint에 넣은 시니어들입니다. 나만무에서 그 가드를 설계할 사람이 저자 한 명이면 버스 팩터 1입니다.
  * 결정 기록을 쓰는 일 자체가 Layer 4라서, 안 써도 아무것도 막히지 않습니다. R4 ADR `결정` 행 인용 0개가 그 예입니다.
  * 결정과 코드를 잇는 장치(test ID ↔ 결정 인용, `check-ids.py`, `check-decision-links.mjs`)는 이미 있지만 위의 두 구멍이 있습니다.

### D4. 나만무는 공개 저장소다

* 저자의 계획은 정글 수강생끼리 쓰는 공개 저장소입니다. 무료 플랜에서도 공개 저장소는 ruleset을 쓸 수 있으므로 A3의 Blocker는 대부분 풀립니다.
* 남는 것: 비관리자 계정으로 시험하기(A8). 관리자인 저자는 우회 권한이 있어서 혼자 하는 시험은 막혀야 할 곳에서도 통과합니다.

### D5. ruleset의 실제 역할은 "사람이 읽게"가 아니라 "모두 CI를 거치게"다

* 저자: 시간이 없어 PR을 거의 읽지 않았습니다(R2 제외). R3, R4는 PR이 너무 많았습니다.
* 그러므로 "승인 1건"은 의미가 없었고, ruleset에서 쓸모 있는 것은 PR 필수, required check, force push 금지입니다. D#1(팀원 에이전트의 `main` 직접 push)은 CI를 건너뛴 사건입니다.
* 회의가 길고 잦았던 이유: 사람이 생성된 코드와 구조를 몰라서 판단을 내리지 못했고, 결정이 회의에서만 나와 저장소에 남지 않았습니다. D3의 "왜"와 "무엇과 증명"을 저장소에 남기는 것이 이 문제의 대응입니다.
* "설정을 코드로"(A1)는 확정 전입니다. CI 안에서 `GITHUB_TOKEN`으로 ruleset을 읽을 수 있는지 확인하지 않았습니다.

### D6. 설명 의무는 강의 규칙이 아니라 팀 책임으로 둔다 (재리뷰 R-1에 대한 답)

* 나만무에 설명 의무가 명시되지는 않을 것으로 봅니다. 그래도 각자 자기 코드가 "설명 가능한 상태"여야 합니다. 이유: 나중에 관련 문제가 터졌을 때 고치거나 소통할 수 있어야 하기 때문입니다.
* "내 말로 3줄"과 "소리 내어 설명"은 팀이 한 번도 해 본 적이 없습니다. 적혀 있기만 했습니다. 될지는 모릅니다. 그래서 확정하지 않고 시험할 가설로 둡니다.

**사례 (mini-redis, 2026-11 회고).** 설계를 정하는 자리에서 "왜 싱글 스레드인가" 같은 질문을 AI와 grilling했습니다. 팀은 잘 모르는 채로 결정했고, 근거는 긴 spec 문서에 남았습니다(`main`에 Markdown 110개, 5,802줄, 가장 긴 spec은 244줄). 아무도 다 읽지 못했고, 나중 회의와 성능 개선에서 같은 질문에 답하지 못했습니다. 구현은 에이전트가 끝냈습니다. 이 사례는 D3의 전제("'왜'는 사람이 깊게 토론해서 정한다")가 실제로는 지켜지지 않았음을 보여 줍니다.

**해석.** "설명 가능한 상태"의 단위는 코드가 아니라 결정입니다. 기준: 팀원 누구나 문서 없이 그 결정의 이유를 자기 말로 답할 수 있다.

| 요구 | 층 | 장치 |
|---|---|---|
| 결정 기록은 읽을 수 있는 크기다 | Static | ADR 한 문단(matt 형식), lint로 길이 상한 |
| 결정은 AI 혼자가 아니라 팀 자리에서 난다 | Human | grilling 결과를 한 문단 ADR로 줄여 회의에서 읽고 정함 (가설, 해 본 적 없음) |
| 구현 흐름은 레포에 미리 쓰지 않는다 | 해당 없음 | 필요할 때 code-map으로 생성 |

조건 차이: mini-redis는 사실상 이틀이었고 나만무는 5주입니다. 시간 부족이 원인인 부분은 나만무에서 줄어듭니다. 긴 spec이 결정 기록을 맡은 구조는 반복될 수 있습니다.

**웹서버 주차 시험 (2026-11 다음 주, 팀 레포, AI 함께하기).** 강의 원칙: 각자 AI로 먼저 구현하고, 자기 코드를 학습하고 검증한 다음, 팀이 서로의 코드를 리뷰해서 하나로 merge합니다. mini-redis와 달리 처음에 팀 설계 회의가 없습니다. 팀이 결정하는 순간은 리뷰에서 "누구 코드를 남기나, 왜"를 정할 때입니다. 이 순간에는 설명할 사람(구현한 본인)과 비교할 실제 대안(서로의 구현)이 있어서 D6을 시험하기에 맞습니다.

| 단계 | 할 일 |
|---|---|
| 개인 구현 후 | 각자 PR 설명에 핵심 결정 하나를 한 문단으로 씁니다 (AI가 쓴 긴 문서 말고) |
| 팀 리뷰 | 각자 자기 결정을 소리 내어 설명하고, 남길 코드를 고른 이유를 ADR 한 문단으로 남깁니다 |
| 며칠 뒤 | 문서 없이 "왜 이 구현을 남겼어?"에 팀원이 답할 수 있는지 봅니다 |

D7은 이 주차에서 시험하지 않습니다. 1주짜리 레포에서는 gate를 바꾸는 PR이 거의 나오지 않습니다. 나만무 첫날 §5 증명으로 확인합니다.

### D7. 판정받는 PR이 판정하는 파일을 고칠 수 없게 한다 (재리뷰 R-2에 대한 답)

**문제.** 팀원은 PR을 거의 읽지 않습니다(D5). 그래서 에이전트가 테스트를 지우거나 CI를 느슨하게 고쳐도 그대로 merge됩니다. CI가 모든 변경을 거치게 하는 장치라면(D5), CI 자체가 바뀌는 순간은 사람이 봐야 합니다.

**목적.** 기능 PR에는 사람이 0명 들어갑니다. 사람은 판정 규칙이 바뀌는 PR만 봅니다. 그런 PR은 드물고 작아서 실제로 읽을 수 있습니다.

**gate 파일.** PR의 통과 여부를 정하는 파일입니다. 판정받는 기능 코드는 아닙니다.

| gate 파일 | 의무 | 탐지기 | 덮는 것 | 사각지대 |
|---|---|---|---|---|
| CI workflow, `Makefile`의 verify, lint 설정, checker 스크립트, 커밋된 hook 설정, `CODEOWNERS`, ruleset JSON | 바꾸려면 owner 승인 | `CODEOWNERS` + ruleset "Require review from Code Owners" | 이 경로의 모든 수정과 삭제 | owner가 한 명이면 그 사람이 없을 때 막힙니다(버스 팩터 1). admin bypass가 켜져 있으면 무력해집니다 |
| `tests/` | 기존 테스트를 수정하거나 삭제하면 사람 승인 | CI의 diff 검사: 추가만 있으면 통과, 기존 줄이 바뀌면 실패 | 테스트 삭제, assert 완화 | 새 테스트가 약하게 쓰인 경우. 검사 스크립트 자체는 첫 줄에 있어서 `CODEOWNERS`가 지킵니다 |

**증명.** 나만무 첫날 barrier-placement §5대로 확인합니다: 테스트 한 줄을 고친 PR과 `ci.yml`을 고친 PR이 각각 막히는지 봅니다.

### Non-Goal 추가

* `~/.claude/rules/`를 신뢰 피라미드 기준으로 고치는 일. 저자가 나중 주제로 미뤘습니다.
* `jungle-week-init` 스킬(`../skills/jungle-week-init/`)에 이 brief의 결론(D2 학습 레포와 프로젝트 레포 구분, D6, D7)을 반영하는 일. 이 brainstorm이나 draft가 끝난 뒤에 합니다(저자, 2026-11-19).
* 다섯 레포를 "첫날 = 첫 작업 커밋 + 24시간" 시계로 엄밀히 채점하는 일(A2). 목적은 채점이 아니라 나만무에 쓸 장치이고, 그 장치는 D6과 D7에서 나왔습니다(저자, 2026-11-19).

### Re-review of D1–D5 (2026-11-19: zoom-out, design, inventive-catalyst)

세 reviewer가 D1–D5만 다시 봤습니다. D1 표의 사실 오류 두 개는 위에서 고쳤습니다. 나머지는 저자의 결정을 기다립니다.

**R-1. D2/D3이 강의 규칙과 이 brief의 Non-Goal에 맞선다 — Blocker (세 명 모두)**
* D3은 "어떻게"를 에이전트가 설명하게 두고 "자기 코드의 함수 단위도 아니다"라고 합니다. 강의 규칙 "각자 자기 말로 설명"과 Non-Goals "설명 의무를 없애거나 기계로 대신하는 것"에 어긋납니다. 에이전트의 설명은 이 규칙을 채우지 못합니다.
* 나만무에 강의 규칙이 적용되는지 확인한 기록이 없습니다. 저자가 말한 "AI 사용 규칙 없음"은 AI 사용에 관한 것이고, 설명 의무에 관한 것이 아닙니다.
* 적용된다면 함께 쓸 길: 설명 범위를 "자기 기능의 왜와 무엇"으로 좁히고, PR 본문에 작성자가 쓰는 "내 말로 3줄" 칸(CI는 칸 존재만 확인)을 두고, 주 1회 병합된 PR 하나를 무작위로 골라 작성자가 소리 내어 설명합니다(inventive-catalyst 4, 주당 약 10분).

**R-2. 기계 gate를 누가 바꿀 수 있는지 정하지 않았다 — Blocker (design 2)**
* 사람이 PR을 읽지 않으면, 에이전트는 같은 PR 안에서 실패하는 테스트를 지우거나 `ci.yml`, `verify`, checker를 약하게 하고 초록불로 병합할 수 있습니다. 테스트와 코드를 같은 에이전트가 쓰면 CI는 스스로를 인증합니다. barrier-placement.md:43은 테스트와 명세를 보호하라고 적습니다.
* 첫날에는 스택이 없어 `verify`가 빈 슬롯입니다. 그때 "CI를 거친다"는 빈 gate를 거친다는 뜻입니다.
* 제안: gate 파일(`ci.yml`, verify 진입점, checker, 테스트 디렉터리, `.github/rulesets/`)에만 CODEOWNERS 승인을 걸고 나머지 경로는 승인 0. bypass actor를 비우고 `strict: true`.

**R-3. D3의 "사람이 확인"에 확인 시점(detector)이 없다 — Major (design 4, zoom-out 2)**
* barrier-placement § 4는 사람 확인에도 고정된 review moment를 detector로 지정하라고 요구합니다. PR을 읽지 않는 팀에서는 "승인 1건"과 같은 길로 빈칸이 됩니다. 후보: 기능 시연 시점.

**R-4. D3의 두 반론에 대한 답 — Major (세 명)**
* 결정 기록이 Layer 4라는 반론: 인용 검사의 방향을 거꾸로 합니다. 요구분석 행마다 `R-n` ID를 붙이고 "모든 테스트 ID는 어떤 `R-n`이 인용해야 한다"를 CI가 검사합니다. 회의는 `requirements.md` PR이 병합되어야 끝납니다. "무엇과 증명"의 feature map은 테스트 이름에서 생성하고 CI가 커밋된 파일과 비교합니다. R3의 `[건너뜀]`은 CI에서 `fetch-depth: 0`으로 없어집니다(inventive-catalyst 1, zoom-out 3, design 5).
* 버스 팩터 1: 위험은 가드의 수가 아니라 가드가 잘못 막을 때 고칠 사람이 한 명이라는 점입니다. 답 셋:
  * 모든 가드의 실패 메시지가 규칙과 고치는 법을 말한다(A9). 지식이 실패 메시지에 남습니다.
  * 교정을 당한 사람이 그 교정의 guard PR을 쓰고, 본문에 § 5 증명(baseline, mutant, restore, neighbor)을 붙인다. 저자는 1주차에 checker 뼈대와 증명 방법만 만든다. guard PR이 곧 "자기 말로 설명"의 증거가 된다(inventive-catalyst 2).
  * 가드 수를 줄인다: 스택 scaffolder의 기본 lint + required check `verify` 하나(zoom-out 3).
* ADR은 같은 방법이 통하지 않습니다. "맥락 없이 놀랍다"는 누군가 코드를 읽어야 판정할 수 있습니다. 거의 안 쓰이는 것을 받아들이거나, ADR 제안 skill을 저장소에 커밋해 팀원 에이전트에게 닿게 합니다.

**R-5. D5의 진단과 D3의 처방이 어긋난다 — Major (zoom-out 4, design 8)**
* D5는 회의가 길었던 원인을 "구조를 몰라서"라고 적는데, D3은 구조("어떻게")를 요청이 있을 때만 설명하게 둡니다. 짧은 모듈 경계와 의존 방향 표 하나를 D3에 더합니다(A7 (b)).
* "PR을 읽지 않았다"는 저자 한 사람의 행동일 수 있습니다. PR이 많았던 원인이 PR 크기일 가능성도 있습니다. 기능 단위로 PR을 키우고 시연을 병합 조건으로 두는 길이 있습니다.
* 회의 결정은 새 문서보다 이미 있는 GitHub Project board의 이슈 댓글이 쌉니다(zoom-out 6).

**R-6. matt-pocock ADR 기준은 기존 검사와 부딪친다 — Major (design 6)**
* ADR-FORMAT.md는 한 문단과 `0001-` 번호를 씁니다. `check-ids.py`는 문단 형식 ADR을 실패시킵니다(D#5). 그대로 들이면 첫 ADR부터 CI가 빨갛습니다.
* "ADR과 명세를 나눈다"면서 명세의 자리를 정하지 않았습니다. 유일하게 작동한 결정–테스트 연결(R3 89/94 인용)을 잃을 위험이 있습니다. D3 표에 명세 칸을 더해야 합니다.

**R-7. D4는 검증 없이 Blocker를 닫았다 — Minor (design 7, zoom-out 7)**
* "공개 저장소는 ruleset을 쓸 수 있다"를 API 시험 없이 적었습니다.
* 공개 저장소에서는 유출된 비밀이 바로 공개됩니다. secret scanning과 push protection은 첫날 필수입니다.
* 소유자(개인 계정 또는 조직)와 관리자 수를 정하지 않았습니다. 관리자가 여럿이면 우회할 수 있는 사람도 여럿입니다.
* 비관리자 시험의 구체안: 비관리자 bot 계정으로 매일 `main` 직접 push와 CI 없는 병합을 시도하는 예약 workflow. 둘 다 거절되어야 green. ruleset을 읽는 권한 문제를 피합니다(inventive-catalyst 3).

**R-8. 범위와 YAGNI — Minor**
* drift job은 미룹니다. 나만무는 5주 동안 저장소 하나라, 커밋된 ruleset JSON과 적용 스크립트로 충분하고 매주 손으로 diff를 한 번 봅니다(zoom-out 8).
* 이어받는 checker(`check-ids.py`)도 § 5 dry run에 넣습니다. 특히 인용되지 않은 테스트 ID를 보지 않는 빈틈(D#23)을 mutant로 재현합니다(inventive-catalyst 5).
* D2의 학습/프로젝트 구분은 barrier-placement § 6에 넣지 않습니다. 그 문서는 자동 검사의 자리를 다룹니다(design 9). D1의 "새 기준을 만들지 않는다"와도 충돌합니다(zoom-out 5).
* D1은 규칙을 만든 사람이 자기 Trial을 채점하는 구조입니다. 판정은 아직 현재 상태 기준이고 A2 Blocker가 남아 있습니다.

## Analysis

### A1. 저장소 밖에 사는 guard는 이어지지 않았다 — Blocker

* **Lens:** design B1, inventive-catalyst 1, zoom-out 3, codebase-details 3, structural 6, implementation-readiness 8
* **반론 먼저:** 이 회고의 축은 layer입니다. 그런데 이어짐을 가른 것은 layer가 아니라 "규칙이 어디 사는가"였습니다.
  * 파일은 복사로 이어졌습니다. `check-ids.py`는 R4=R5 md5가 같고, `.clang-format`도 같습니다. `CONVENTION.md` 번호 규칙 2–6, 8은 R3, R4, R5에서 글자가 같습니다(B1, B2).
  * GitHub 설정은 단계마다 약해졌습니다. R3 ruleset은 PR 필수, 승인 1, stale 승인 무효, merge만, required check `code`였습니다. R4는 승인 0, 세 병합 방식 허용, 관리자 우회 `always`이고 첫날이 아니라 11-18 03:09에 생겼습니다. R5는 `[]`입니다(B1 "GitHub ruleset", B3).
  * 같은 사고가 두 번 났고 같은 방법으로 두 번 고쳤습니다. R3에서 PR 없는 커밋 4개 뒤 14:55에 ruleset을 만들었습니다(D#2). R4에서 팀원이 `main`에 직접 커밋 4개를 올렸고, 되돌림 1분 전에 ruleset을 만들었습니다(D#1). 첫 교정이 GitHub UI의 클릭으로만 남아서 다음 저장소에 가지 못했습니다.
  * 설정은 아무도 모르게 바뀝니다. `week11-12/CLAUDE.md`는 mini-react 관리자 우회를 지웠다고 적지만 지금 ruleset에는 `pull_request` 우회가 있고, PR #54–#56이 `REVIEW_REQUIRED` 상태로 병합됐습니다(`layer-table.md` "확인 못 한 것").
* **요구 사항:** 표의 각 행에 "어디 사는가"(저장소 파일 / 저장소 설정 / 개인 기기) 칸을 더합니다. 설정은 코드로 만듭니다. ruleset JSON을 `.github/rulesets/main.json` 같은 파일에 커밋하고, `gh api`로 적용하는 스크립트와, 실제 설정과 파일을 비교해 다르면 실패하는 CI 또는 예약 job을 둡니다. 이 비교 검사가 없는 설정은 아무리 엄격해 보여도 Layer 4로 칩니다(structural 4).
* **부작용:** 비교 job에는 관리자 읽기 권한 token이 필요하고, 그 token은 관리할 secret이 됩니다. 의도한 임시 우회도 커밋이 되어야 하므로 번거로워집니다.

### A2. "첫날 상태"가 정의되지 않았고, 입력 표는 현재 상태를 적었다 — Blocker

> 해결: 저자가 Non-Goal로 옮겼습니다(2026-11-19).

* **Lens:** structural 1, implementation-readiness 2, comprehension 5, codebase-details 2
* **반론:** 오늘 표의 Layer 2 ✓가 첫날의 Layer 4 ✗를 가릴 수 있습니다. R4의 "`main`은 PR로만"은 11-13에 문서로 들어왔지만 강제는 11-18에 시작했습니다(`carryover.md` B2). 시계도 셋입니다. R3–R5의 root commit은 GitHub의 `Initial commit`이라 작업 시작 7–11일 전이고, R2는 이력을 다시 써서 author date가 root보다 이릅니다(`carryover.md` § C). GitHub 설정에는 이력이 없고 생성 시각과 수정 시각만 있습니다. R2 설정은 403이라 읽을 수 없었습니다.
* **"이어졌다"의 뜻도 넷입니다:** 같은 파일(md5), 같은 문장, 같은 생각의 새 파일(`check-decision-links.mjs` → `check-ids.py`), 다른 layer의 같은 생각(comprehension 4). B3의 끊김에는 이유가 없습니다. `.devcontainer`와 `.editorconfig`가 끊긴 것은 맞는 끊김이고(Pintos 환경 파일), PR 템플릿, required check, 새 세션 리뷰가 끊긴 것은 잃은 것으로 보입니다.
* **요구 사항:** 점수를 매기기 전에 세 가지를 고정합니다.
  1. 첫날 = 첫 작업 커밋 + 24시간. 파일은 git에서, 설정은 생성 시각에서 읽습니다. 복원할 수 없는 칸(R2 설정 전체)은 `?`로 두고 판정에서 뺍니다. 0으로 세지 않습니다.
  2. "이어짐"의 단위를 file / text / intent 중 하나로 기록합니다.
  3. 끊김마다 이유 코드를 붙입니다: 해당 없음 / 대체됨 / 잊음 / 일부러 뺌.
* 다른 기준점 제안: "저자가 아닌 첫 팀원이 커밋한 때의 `main`"(comprehension 5). 어느 쪽이든 다섯 저장소에 같은 시계를 씁니다.

### A3. GitHub 플랜이 Layer 2 병합 보호를 막을 수 있다 — Blocker

* **Lens:** implementation-readiness 1, design B2, zoom-out 8, inventive-catalyst 1
* R2(조직 소유 private)는 ruleset, branch protection, rules API 모두 403 "Upgrade to GitHub Pro or make this repository public"이었습니다(`carryover.md` § A, § E). 나만무 저장소가 무료 플랜 조직 소유 private이면 A1의 핵심 수단이 첫날부터 없습니다. R1(사용자 소유 private)이 ruleset을 만들 수 있었는지도 확인하지 않았습니다.
* private 저장소는 Actions 시간도 quota입니다. R5의 macOS matrix와 TSan job은 PR마다 비쌉니다(design B2).
* **요구 사항:** 다른 어떤 결정보다 먼저 나만무 저장소의 소유자, 공개 여부, 플랜을 정하고, 같은 종류의 throwaway 저장소에서 ruleset과 required check가 실제로 만들어지는지 API로 확인합니다. 안 되면 대안을 미리 적습니다: 공개 저장소, 유료 플랜, 또는 `main` push에서 실패하고 되돌림 PR을 여는 CI job(사후 탐지라 더 약함).
* 이 확인은 이번 주에 할 수 있고, 결과에 따라 회고의 결론 일부가 달라집니다. inventive-catalyst는 이것을 가장 급한 확인으로 꼽았습니다.

### A4. "Human review 불필요"와 "자기 말로 설명"이 같은 Layer 5에 섞여 있다 — Blocker

* **Lens:** 일곱 lens 모두 (design M3, inventive-catalyst 3, zoom-out 4, comprehension 2, structural 8, implementation-readiness 7, codebase-details Q2)
* **반론:** 목표를 글자대로 따르면 강의가 요구하는 유일한 규칙을 지우게 됩니다. 지금 Layer 5에는 세 가지가 섞여 있습니다: (a) 병합 gate로서의 승인, (b) 학습 결과로서의 이해, (c) Copilot이나 새 세션 리뷰 같은 에이전트·bot 리뷰.
* **근거가 보여 주는 것:** (a)는 이미 비어 있습니다. R2 승인은 "LGTM", "lgtv"였고, R1은 사람 승인 0건, Copilot 리뷰는 quota로 거의 모두 실패했습니다(실제 리뷰는 R4 #47 하나). R3 #54–#56은 우회로 병합됐습니다. 반대로 실제로 작동한 Layer 5 규칙은 (b) 하나였고, 그것도 리뷰어가 아니라 작성자 자신의 확인이었습니다: PR #32 "제가 원리를 설명할 수 없는 변경이라 파기합니다"(D#3).
* **해결 방향 (Separation):** 품질 gate는 Layer 1–3으로 옮기고 사람 승인을 병합 경로에서 뺍니다. 이해는 gate가 아니라 작성자의 의무로 둡니다. 구체안 두 가지:
  * PR 본문에 작성자가 직접 쓰는 "설명" 칸. CI는 칸이 있고 비어 있지 않은지, 바뀐 함수 이름이나 ID를 참조하는지만 봅니다. 내용은 사람의 것입니다.
  * 강한 확인을 PR마다가 아니라 기능 시연 때로 옮깁니다. Tan의 검증 산출물(영상, statechart, feature map)이 설명의 발판이 됩니다(`tan-talk-report.md` § 3 Verification).
* **약점:** 작성자의 설명도 AI가 쓸 수 있습니다. 기계 검사는 칸이 있다는 것만 증명합니다. 시연이 마지막 방어선이고, 시연은 팀의 동시 시간을 씁니다.
* **회고에서 정해야 할 모호함:** "각자 코드를 이해한다"는 전체 코드인가, 자기가 쓰거나 병합한 코드인가. mini-react 문장은 "병합된 코드의 원리"라 둘 다로 읽힙니다(`layer-table.md` mini-react). 6명, 5주에 리뷰 없이 "전체 코드"는 어렵고 "자기 코드"는 됩니다. 이 결정 하나가 저자가 열어 둔 human review 경계의 대부분을 정합니다(inventive-catalyst 3).

### A5. layer 표시와 ✓ 표시가 자기 범례를 따르지 않는다 — Major

* **Lens:** comprehension 1, 7, 8, 10; codebase-details 1, 5; design M4
* **layer 경계:**
  * 범례는 컴파일러를 Layer 2에 둡니다. 그런데 컴파일러가 강제하는 `struct store`, `struct engine` 불완전 타입은 1로만 표시됐습니다.
  * 실행 중 `throw`는 "1 + 2", ASan과 UBSan은 "2 + 3"입니다.
  * 단위 테스트는 2, jsdom 예제 테스트는 3입니다. Tan은 테스트를 Verification에 둡니다. 저자의 2와 3 경계는 Tan과 다르고, 어디에도 적혀 있지 않습니다.
  * ruleset은 정적 분석이 아니라 병합 gate인데 2로 들어가 있습니다.
* **✓의 과장:** R4, R5 CI는 "✓ 실패는 표시되지만 병합을 막지 않음"입니다. 범례대로면 △입니다. 그 밖의 경우:
  * R5 ADR 이름 검사는 ADR 0개를 검사합니다.
  * R4 ADR `결정` 행에는 인용이 0개입니다.
  * mini-react의 "인용 없는 새 테스트" 검사는 CI에서 `origin/main`이 없어 늘 `[건너뜀]`입니다.
  * `[확인]` 줄은 출력만 합니다.

  이런 "출력만 하는 검사"는 Prose처럼 동작합니다. 실패하는 줄 알았는데 조용히 안 도는 자동 리뷰어(Copilot quota)는 없는 것보다 나쁩니다. 사람들이 돌았다고 믿기 때문입니다.
* **"사람이 읽어야 하나" 칸:** Layer 4 행에 "사람"이 많습니다. 팀원은 이를 Layer 5 리뷰로 읽습니다. 실제 뜻은 "규칙을 지키려면 알아야 하는 사람"입니다.
* **"올린다"의 방향:** Tan의 "higher" guard는 Codebase, 곧 1번입니다. "Prose를 올린다"는 번호를 줄인다는 뜻이라고 글로 적어야 합니다.
* **요구 사항:**
  * 각 layer를 행에 적용할 수 있는 판정 문장으로 정의하고 모든 행을 다시 표시합니다. 예: "1 = 잘못된 코드를 쓸 수 없거나 컴파일되지 않음, 2 = 프로그램을 실행하지 않고 도구가 거절, 3 = 프로그램이나 시연을 실행".
  * 강제 칸은 "병합을 막음 / 실패를 보이기만 함 / 출력만 / 빈 검사 / 누가 우회 가능"으로 나눕니다.
  * 다섯 칸을 직교로 둡니다: layer(사는 곳의 성격), 강제, 우회자와 모드, 적용 주체(git 파일 / 사람이 적용하는 설정 / 로컬), drift 검사 유무(structural 4).
  * 층별 개수는 한 행을 두 층에 세므로 버리거나, 행당 주 layer 하나로 다시 셉니다.

### A6. 교정 근거는 하한이고, 측정 단위가 갈린다 — Major

* **Lens:** design M1, comprehension 3, implementation-readiness 3, structural 3, zoom-out 2, codebase-details 7
* **반론:**
  * Tan의 "교정"은 세션 안에서 에이전트를 바로잡는 것입니다. § D는 커밋 메시지와 PR 댓글만 찾았고, PR 본문, Slack, 회의록, 보드 카드, 에이전트 세션은 보지 않았습니다(`carryover.md` § E). 에이전트로 만든 R3–R5의 교정은 대부분 채팅에서 일어났고 흔적이 없을 것입니다.
  * 저자가 기억하는 팀원 에이전트 교정이 하나(D#1)라는 것은 교정이 드물었다는 증거가 아니라, 저자가 팀원 세션을 볼 수 없다는 증거입니다.
  * § D의 25행 대부분은 저자가 자기 문서나 검사를 고친 것입니다.
  * 손으로 쓴 Pintos의 교정(D#24, D#25)과 에이전트 출력의 교정은 실패 원인이 다릅니다. 나만무가 겨냥하는 것은 후자입니다.
* **단위에 대한 이견:**
  * zoom-out: 규칙 수는 잘못된 단위입니다. mini-dbms의 행이 적은 것은 하루이틀에 끝냈기 때문이지 더 나아서가 아닙니다. 단위는 "Rn의 상태 X에 있던 검사가 Rn+1 첫날에 없었고, 무엇이 통과했나"이고, B3이 이미 약 20행을 적었습니다.
  * structural: 두 단위가 다른 질문에 답합니다. 교정 사건(§ D)은 열린 질문 1, 2에 답하고, 규칙 계보(B1–B3)는 이어짐과 첫날 kit에 답합니다. 둘을 rule ID로 잇습니다.
* **요구 사항:**
  * § D를 하한으로 표시합니다.
  * 각 교정에 붙일 칸: 사람이 쓴 코드인지 에이전트 출력인지, 결과 유형(닫힌 목록: Layer 1 범주 제거 / 2 결정적 검사 / 3 실행 검증 / 4 Prose / 5 사람 / 없음), 나중에 다시 났나, rule ID.
  * 실행되지 않은 규칙(위반도, 교정도, 검사 발동도 관찰되지 않은 규칙)은 순위에 넣지 않고 "모름"으로 둡니다. R5에서 다시 나지 않았다는 것은 그 규칙이 쓰일 일이 없었다는 뜻일 수 있습니다(codebase-details 7).
  * 나만무에는 첫날부터 교정을 모으는 싼 통로를 둡니다. 예: `correction` 이슈 label과 `layer?` 칸이 있는 이슈 템플릿.

### A7. 언어 독립은 코드가 아니라 계약으로만 이어졌다 — Major

* **Lens:** codebase-details 4, design M6, comprehension 6, implementation-readiness 6, inventive-catalyst 5
* **반론:** TS→C 전환(R3→R4)에서 실행 가능한 산출물은 하나도 이어지지 않았습니다. ID 검사는 다른 언어로 다시 썼고 CI도 다시 썼습니다. 이어진 것은 생각, 그리고 같은 언어 저장소 사이의 파일뿐입니다. "언어 독립 부분을 고르면 첫날이 싸다"는 인상은 스택을 고른 뒤 각 검사를 다시 만드는 비용을 가립니다.
* **`check-ids.py`의 숨은 가정 (codebase-details가 코드에서 확인):**
  * test ID가 `"[T1]`처럼 큰따옴표 바로 뒤에 와야 합니다(`check-ids.py:19`). pytest, Go, JUnit처럼 테스트 이름이 함수 이름인 스택에서는 `[T1]`을 쓸 수 없습니다.
  * 테스트는 `tests/` 아래에만 있다고 가정하고, 모든 파일을 UTF-8로 읽습니다.
  * `docs/requirements.md`가 없으면 죽습니다. 그래서 빈 새 저장소에서는 첫날 실패합니다.
  * ID 문법이 `T[0-9]+`뿐입니다. mini-react의 `[A-Z][A-Z-]*\d+[a-z]?`(`check-decision-links.mjs:11`)와 호환되지 않으므로 나만무는 하나를 골라야 합니다.
* **세 묶음으로 나눕니다** (implementation-readiness 6):
  * (a) 스택 없이 지금 바로 쓸 수 있는 것: ruleset JSON과 적용 스크립트, secret scanning과 push protection, `.gitattributes`, PR 템플릿, `CONVENTION.md` 절차 규칙, `retarget-stacked-prs.yml`, Markdown 물결표 검사(`convention.py:172-234`에서 떼어 냄), `CLAUDE.md` = `@AGENTS.md`, `docs/agents/` 세 파일.
  * (b) 생각은 이어지지만 스택마다 다시 만들 것: test ID와 결정 인용 계약, 하나의 verify 진입점, 모듈 경계를 불투명하게 두는 방식, 의존 방향 표. 이 계약은 지금 문서로 정합니다.
  * (c) 스택에 묶여 미룰 것: lint, type, 이름 검사, 실행 검증 CLI와 feature map. 각 항목에 trigger("스택을 고른 날")와 목표 layer를 붙입니다.
* **해결 방향 (Segmentation):** 스택 없는 core와 버릴 수 있는 stack adapter로 나눕니다. 첫날 `verify`는 정확히 한 이유, "adapter 미선택"으로 실패합니다. 슬롯 표시를 `<<SLOT:verify-command>>` 같은 한 문법으로 통일하고, 표시가 남아 있으면 첫날 검사가 실패하게 하면 슬롯 채우기 자체가 Layer 2가 됩니다(structural 6c).
* **이견:** inventive-catalyst는 팀이 고를 법한 스택 2–3개의 adapter stub을 미리 만들자고 했고, zoom-out은 스택별 기본값은 그 스택의 scaffolder와 권장 lint 설정에서 받으라고(미리 손으로 만들지 말라고) 했습니다. 쓰이지 않을 adapter는 버리는 일입니다.

### A8. 한 사람에 묶인 운영, 그리고 우회가 규칙을 약하게 한다 — Major

* **Lens:** design M2, structural 7, implementation-readiness 4, 5, comprehension 9
* **반론:**
  * 규칙을 가장 많이 벗어난 사람은 규칙 설계자입니다. 오너 예외는 PR #1, #2가 승인 없이 병합된 뒤 문서를 실제에 맞춰 넣은 것이고(D#8), R5로 복사됐습니다. 관리자 우회는 남아 있습니다(D#17).
  * 저자가 관리자라서, 저자 혼자 하는 시험은 팀원이나 팀원의 에이전트가 막힐 곳에서도 통과합니다. 실제 실패(D#1)는 팀원에게서 나왔습니다.
  * required check 이름이 CI job 이름과 정확히 같아야 하므로, 스택 전환 중 job이 없어지면 모든 PR이 막힙니다. 이것을 푸는 길이 오너의 설정 변경 하나뿐입니다.
  * 보이는 예외는 팀원에게 "규칙은 선택 사항"이라고 가르칩니다.
* **요구 사항:**
  * 첫날 설정을 관리자가 아닌 계정(두 번째 GitHub 계정이나 동의한 팀원)으로 시험합니다.
  * ruleset의 bypass actor는 없애거나, 이유와 만료를 적은 기록으로 둡니다. 오너 예외는 문장이 아니라 label과 CI 기록처럼 보이는 장치로 바꿉니다.
  * gate마다 되돌리는 길을 적습니다: 누가 끄고, 어디에 기록하고, 얼마나 꺼 둘 수 있나.
  * required check 이름을 지금 `verify` 하나로 고정하고, 안의 내용만 스택에 따라 바꿉니다.
  * 성공 기준 후보: 저자가 아닌 팀원이 빈 저장소에 첫날 설정을 적용해 목표 상태에 닿습니다(design M2).

### A9. Prose는 저자의 에이전트에만 닿는다 — Major

* **Lens:** zoom-out 7, design M7, comprehension 9, structural 6d, inventive-catalyst 4
* **반론:**
  * Pintos `CLAUDE.md`와 `GLOSSARY.md`는 `.git/info/exclude`로 git에서 빠져 있었습니다.
  * R3의 issue tracker와 skill 설정은 저자의 개인 `CLAUDE.md`에 있습니다.
  * "AI 공동 작성자 표시를 넣지 않음"은 R3부터 개인 메모리에만 있습니다(B3).
  * 팀원의 에이전트가 `AGENTS.md`를 읽는지는 그 도구에 달렸고 아무도 확인하지 않았습니다. D#1을 막은 것은 문서가 아니라 설정이었습니다.
* **요구 사항:**
  * 이월하는 모든 규칙을 두 묶음으로 나눕니다: "팀원을 묶는 것"과 "내 에이전트를 안내하는 것". 앞의 묶음은 CI, required check, ruleset이어야 합니다.
  * 팀원의 에이전트가 따라야 하는 것은 모두 저장소에 커밋하거나 설정으로 강제합니다. 개인 파일은 규칙을 더할 수는 있지만 팀 규칙을 실어 나르지는 못합니다.
  * 개인 `~/.claude`의 skill로 kit을 나르면 같은 실패를 되풀이합니다. skill을 쓴다면 팀 저장소에 넣습니다.
* **해결 방향 (Self-Service):** Layer 1–3 규칙은 미리 알 필요가 없습니다. 실패 메시지가 그때 규칙을 가르칩니다. Tan의 lint 메시지가 근본 원인 수정을 알려 주는 방식입니다(`tan-talk-report.md` 8:49). 각 규칙을 "`CONVENTION.md`를 안 읽은 팀원이 막히고, 무엇을 할지 들었나"로 잽니다.

### A10. 범위: 조사는 이미 대부분 끝났다 — Major (이견 있음)

* **Lens:** zoom-out 1, 9, 10
* **zoom-out의 반론:**
  * `carryover.md`가 이미 R1–R5의 파일과 규칙을 모두 추적했습니다(B1, B2, B3, D). 모든 저장소의 모든 규칙에 질문을 다시 하면 약 170행의 행 단위 함정에 빠집니다. 그중 상당수는 측정 기록, Redis 대조 절, Pintos icount처럼 나만무에 갈 수 없는 것입니다.
  * Pintos(R1, R2)는 AI 규칙이 달랐고, CI도 `AGENTS.md`도 없었으며, 에이전트 파일은 로컬뿐이었습니다. 각주 하나로 두고 R3→R4→R5 전환만 봅니다. 하루로 시간을 자릅니다.
  * 교정 뒤 판정할 것은 약 15–20행이고, 결과는 keep-as-prose / raise / drop과 한 줄 이유입니다.
* **이미 있는 기준을 다시 만들지 말라:**
  * `/home/benjohnbill/dev/krafton-jungle/docs/dialectic/2026-10-31-rules-barriers/JUDGMENT.md` "Accepted 3": "거짓 주장부터 고치고, 그다음 그가 소유한 싼 연결, 그다음은 위험이 보일 때까지 아무것도 하지 않음".
  * 같은 파일 "Accepted 2": "주장했지만 없는" 칸이 해로운 칸입니다.
  * `/home/benjohnbill/.claude/docs/tool-guides/barrier-placement.md` § 4: obligation, detector, covers, blind spots의 네 부분 형식. "도구 detector가 없는 규칙도 review moment를 detector로 지정하면 절대 규칙이 될 수 있다". § 6: "Team project: CI with a required check first".
  * 2026-10-31 결정 O2는 "universal intents"를 "C가 아닌 과제에서 반증 시도 한 번까지" 로컬에 두었습니다. mini-react(TS)가 그 시도였으므로 그 결과를 기록해야 합니다(zoom-out 12).
* **다른 lens와의 긴장:** structural과 implementation-readiness는 칸을 더 늘리자고 합니다(시점 두 개, 직교 칸 다섯, 비관리자 계정 replay). zoom-out은 줄이자고 합니다. 이 brief의 종합은 이렇습니다. 칸을 늘리는 것은 **나만무로 가져갈 후보 행에만** 적용하고, 나머지 행은 zoom-out의 세 갈래 판정으로 끝냅니다. 그러면 두 쪽 모두 지킬 수 있습니다.

### Contradictions and Ideal Final Result

* **inventive-catalyst가 이름 붙인 모순 넷과 변환:**

  | 모순 | 변환 | 결과 |
  | --- | --- | --- |
  | Human review 없음 vs 각자 설명 | Separation in subject, Inversion | 품질 gate는 기계, 이해는 작성자의 설명과 시연 (A4) |
  | 한 명의 설계자 vs 설계하지 않은 팀 | Self-Service, Blessing in Disguise | 규칙은 실패 메시지로 가르치고, 팀원은 교정을 보고만 함 (A9) |
  | 스택 미정 vs 첫날 준비 | Segmentation, Cheap Dispensables | 스택 없는 core와 버릴 수 있는 adapter (A7) |
  | 일주일짜리 저장소 vs 쌓여야 하는 교정 | Extraction | 규칙이 아니라 교정을 쌓는 장치를 이월. 나만무는 5주 한 저장소라 그 안에서 쌓을 수 있음 |
* **Ideal Final Result:** 나만무 저장소가 첫 커밋부터 스스로를 지킵니다.
  * 설정은 코드이고, drift는 빨간 check가 됩니다.
  * 모든 병합 gate가 기계입니다.
  * 규칙은 기록된 교정이 필요를 보인 곳에만 있고, 실패 메시지로 가르칩니다.
  * 팀원이 알아야 하는 것은 "교정을 보고하기"와 "자기 기능을 설명하기" 둘뿐입니다.
  * 사람의 시간은 승인이 아니라 설명에만 씁니다.
* **IFR의 약점:**
  * 교정 장부 관리는 여전히 저자 혼자의 일입니다.
  * 승격 결정도 저자가 하므로 병목이 남습니다. 5주에는 받아들일 만하지만 적어 둡니다.
  * A3의 플랜 확인이 실패하면 IFR의 첫 줄이 무너집니다.

### Open question answers (reviewer synthesis)

**Q1. 어떤 Prose 규칙을 먼저 올리나.** lens 다섯이 거의 같은 순서를 냈습니다. 기준은 "관찰된 실패 또는 재발 × guard의 싼 정도"입니다.

1. **거짓 주장부터.** 문서는 강제한다고 적지만 설정이 강제하지 않는 것들입니다.
   * 문서는 "승인 1건"인데 R4 ruleset 승인은 0이고, R5에는 ruleset이 없습니다.
   * 문서는 "merge commit으로"인데 R4는 세 방식을 다 허용합니다.
   * 문서는 "`main`은 PR로만"인데 R5에는 ruleset이 없습니다.
   * `CONVENTION.md` 8은 R4, R5에서 강제되지 않습니다.

   해결은 settings-as-code와 drift 검사(A1)입니다. 이 규칙은 두 번 실패했습니다(D#1, D#2).
2. **secret scanning과 push protection.** R3–R5 `disabled`, R1, R2 `null`입니다. 짝이 되는 규칙 "생성 파일과 비밀 정보 확인"은 모든 저장소에서 Layer 5입니다. 설정 하나로 켭니다.
3. **required check `strict: true`.** R1–R5 모두 ✗인 "PR 전에 `origin/main`을 병합"을 Layer 2로 바꿉니다. `retarget-stacked-prs.yml`은 `GITHUB_TOKEN`으로 base를 바꿔 CI를 다시 돌리지 않으므로, 옛 base의 CI 결과로 병합될 수 있는 틈도 같이 닫힙니다(codebase-details 6).
4. **출력만 하는 검사를 실패로 바꾸거나 지우기:** 인용 안 된 ID(D#23), superseded만 인용, ADR 이름 중복(Set이라 알리지 않음), CI `fetch-depth`.
5. **재발했고 싸게 검사할 수 있는 것:**
   * `Status:` 줄 형식: R4는 `Status:` 15개와 `**Status:**` 23개가 섞였고, R5도 섞였습니다.
   * 측정 기록 번호 충돌(D#11).
   * 마지막 `return` 앞 빈 줄: R5에서 손으로 61곳을 고쳤습니다(D#22). 다만 이 검사는 언어마다 따로 만들어야 합니다.
   * 개념 이름 표의 "쓰지 않는 이름" 칸: 이미 deny-list 데이터라 token grep으로 언어와 상관없이 강제할 수 있습니다. R1부터 Layer 4였던 C4 규칙의 일부가 Layer 2로 갑니다(codebase-details).
6. **모듈 의존 방향.** Tan의 대표 사례입니다. 스택에 묶이므로 지금은 "방향 표 + graph 검사"라는 계약만 이월합니다.

나중에 올리거나 Prose로 둡니다:
* 동사 표, `모듈_동사`, `typedef` 같은 이름 규칙. 언어에 묶여 지금은 올릴 수 없습니다.
* "ADR 이유 칸은 팀원이 말한 문장만". 스크립트로 판정할 수 없습니다.
* 설명 규칙.

**Q2. Prose나 Human review에서 멈춰도 되는 기준.** Tan은 기준을 주지 않았습니다(`tan-talk-report.md` § 4, § 9). 비용이 5로 갈수록 오른다는 주장도 설명 없는 슬라이드 축뿐이므로, 기준은 저자가 자기 사례에서 정해야 합니다. lens들의 후보를 합치면 다음이 모두 참일 때만 멈춥니다.

* (a) 저장소 텍스트, git 이력, 설정만으로 지켰는지 판정할 수 없습니다. 판정할 수 있으면 Layer 4에 남기지 않습니다. 이 기준으로 기존 ✗ 행을 점검할 때의 예:
  * "ADR 이유 칸은 팀원이 말한 문장만"은 판정할 수 없어서 남습니다.
  * "`return` 앞 빈 줄"은 판정할 수 있어서 남지 않습니다.
* (b) 재발이 문턱 아래이거나, 재발을 모르지만 교정을 모으는 통로가 있습니다.
* (c) 놓쳐도 일주일 안에 되돌리기 쌉니다. 비밀 정보 유출과 `main` 직접 push는 이 기준을 통과하지 못합니다.
* (d) 규칙이 커밋된 파일에 삽니다.

이와 별개로, 설명 규칙은 강의 규칙이라 기준과 상관없이 Layer 5에 남습니다. 출력만 하는 검사는 이 판정에서 Prose로 칩니다. 사람 확인으로 남기는 규칙은 barrier-placement.md § 4대로 "review moment"를 detector로 지정합니다.

**Q3. 외부 저장소의 역할.** 다음 진술은 검증되지 않았습니다. 어느 reviewer도 외부 저장소를 읽지 않았습니다.

* **matt-pocock skills:** 이미 R4, R5의 작업 흐름 layer로 쓰이고 있습니다(`docs/agents/*`, B1). 그대로 두되 version을 고정합니다. upstream에서 바뀐 skill은 기록되지 않은 Prose drift입니다.
* **pstack:** `/no-comments`, `/statechart`, `/create-verification-skill`은 슬라이드 각주로만 알려졌습니다(`tan-talk-report.md` § 6). `/no-comments`는 현재 팀 규칙 "주석은 이유만"과 충돌하므로 들이기 전에 하나를 골라야 합니다. 스택이 정해지기 전에는 후보로만 둡니다.
* **큰 agent 저장소:** Tan의 outer loop(수백–수천 cloud agent, fuzz와 auto-merge, 227명)는 6명, 5주와 맞지 않습니다. Tan 자신이 "don't automate a bad loop"라고 말했습니다.
* **들이는 규칙:** 외부 skill은 Layer 3 산출물을 내거나(실행 검증 CLI, feature map) Prose를 줄일 때만 들입니다. 규칙을 더하려고 들이지 않습니다. 들이는 항목마다 어느 교정을 다루는지 적고, 저장소에 vendor하거나 고정합니다.

**Q4. 이번 주 산출물.** lens마다 이름은 다르지만 세 부분으로 모입니다.

1. **Correction ledger + rule lineage**(행은 나만무 후보만). 칸:
   * rule ID, 언어 독립 intent 한 문장
   * 저장소별 첫날 layer와 강제
   * 어디 사는가, 우회
   * 끊김 이유
   * 연결된 § D 교정과 재발 여부
   * 판정(raise / keep / drop)과 Q2 기준, 스택 묶음 (a)(b)(c)
   * 덮지 않은 근거 출처
2. **나만무 first-day kit:**
   * A7 (a) 묶음을 담은 template 저장소
   * 설정 적용과 drift 검사 스크립트
   * `verify` 고정 이름의 CI 뼈대와 슬롯 표시
   * 텍스트 기반 ID 인용 계약
   * template commit을 기록하는 version stamp. 다음 회고는 이력을 다시 짓지 않고 diff로 이어짐을 잴 수 있습니다(structural 6e).
   * 정리 방식은 lifecycle 순간별입니다: 저장소 생성, 스택 선택, 첫 PR, 매 PR, 단계 끝, 규칙 변경, 주말. B3의 끊김 대부분이 "저장소를 만들 때 빠뜨림"이었기 때문입니다(structural 5).
   * `jungle-week-init`에 팀 최종 가지를 더해 이 셋을 한 단계로 돌리는 방안도 있습니다(zoom-out 10). R5처럼 서두르는 날에 설정이 빠지기 때문입니다.
3. **Dry run:** 나만무와 같은 소유자 종류, 같은 플랜의 throwaway 저장소에서 비관리자 계정으로 과거 실수를 일부러 다시 만듭니다.
   * D#1, D#2: `main` 직접 push
   * D#6: 이스케이프 안 한 물결표
   * D#5: 문단 형식 ADR
   * D#11: 같은 기록 번호
   * D#23: 인용 안 된 ID
   * D#3: 설명할 수 없는 변경

   각 실수가 실제로 어느 layer에서 멈췄는지 적습니다. 통과한 replay는 시험 실패가 아니라 그 규칙을 올릴 근거입니다.

### Nits

* mini-redis를 두 입력이 다른 SHA로 읽었습니다(`layer-table.md` `9e1812d`, `carryover.md` `1a64bd7`). 저장소마다 SHA 하나로 고정합니다.
* `carryover.md`는 R1–R5를, `layer-table.md`는 저장소 이름을 씁니다. 산출물에서는 key 하나로 통일합니다.
* "강제 칸이 ✗로 시작"하는 개수는 "규칙 없음" 행과 "문서는 있고 강제는 없는" 행을 섞습니다.
* `week11-12/CLAUDE.md`가 실제 ruleset 상태와 다릅니다. 회고가 이 파일을 인용하므로 먼저 맞춥니다.
* 문서와 실제의 차이(`CLAUDE.md`와 설정, PRD의 함수 넷과 `engine.h`의 다섯)를 독립된 사례 종류로 기록합니다. 설계자에게도 Layer 4는 믿을 수 없다는 증거이고, Q2에 바로 쓰입니다.
* Tan의 교정 계단 그래프(0→167)는 단위가 설명되지 않았으므로 목표 숫자로 쓰지 않습니다.
* R5의 빈틈(ruleset 없음, ADR 0개)은 설계 선택이 아니라 서두른 결과로 다룹니다. "첫날은 명령 하나여야 한다"의 근거로는 쓰되, 어떤 규칙이 중요한지의 근거로는 쓰지 않습니다.

## Goals vs. Non-Goals

**약점 먼저:** 성공 기준은 저자가 2026-11-19에 세 개로 정했습니다(아래 첫 항목). 첫째 기준은 사람의 대답을 보는 Human 층이라 가장 약합니다. 아래의 리뷰어 후보는 참고로 남깁니다.

* **In-Scope Goals:**
  * **성공 기준 (저자 결정, 2026-11-19):**
    | 언제 | 기준 | 무엇을 판정하나 |
    |---|---|---|
    | 웹서버 주차 끝 | 며칠 뒤 "왜 이 구현을 남겼어?"에 팀원 과반이 문서 없이 답한다 | D6 가설이 맞나 |
    | 나만무 첫날 | 테스트를 고친 PR과 `ci.yml`을 고친 PR이 둘 다 막힌다 (§5) | D7 장치가 실제로 동작하나 |
    | 나만무 끝 | owner 승인 없이 merge된 gate 변경 PR이 없다 | D7이 5주 동안 유지됐나 |

    "회의가 길고 잦았다"는 원래 문제는 숫자로 재기 어려워 뺐습니다. 첫째 기준이 그 원인(결정을 모르는 상태)을 직접 봅니다.
  * ~~첫날 정의, "이어짐" 단위, 근거 출처 범위를 회고 시작 전에 고정한다.~~ Non-Goal로 옮김 (A2, 2026-11-19).
  * R3→R4→R5 전환과 § D 교정을 rule ID로 이은 ledger를 만든다. Pintos는 각주와 C 이름 규칙 계보로만 다룬다.
  * Layer 5를 병합 gate / 이해(강의 규칙) / 에이전트·bot 리뷰로 나누고, "human review 경계"는 병합 gate에 대해서만 정한다.
  * "각자 이해"의 범위(전체 코드 또는 자기 코드)를 정한다.
  * 나만무 저장소의 소유자, 공개 여부, 플랜을 정하고 ruleset이 되는지 확인한다.
  * 스택 없는 first-day kit(template, 설정 코드와 drift 검사, `verify` 계약, ID 인용 계약)을 만든다.
  * 비관리자 계정 dry run으로 kit을 시험한다.
  * 리뷰어의 성공 기준 후보(참고, 포함 조건):
    * Layer 2 목표 행마다 dry run 기록에 비관리자 계정에서 관찰한 거절이 있다.
    * 모든 gate 항목에 되돌리는 길이 있다.
    * `CONVENTION.md`의 모든 규칙이 detector 또는 "review moment" 중 하나를 가진다.
    * 첫날 kit 적용 결과에서 저장소 밖에만 사는 guard가 없다.
    * 병합된 PR 중 작성자 설명 칸이 없는 것이 없다.
* **Out-of-Scope Non-Goals:**
  * 다섯 저장소의 모든 규칙(약 170행)을 다시 판정하는 것.
  * 스택 미정 상태에서 lint, type, 이름 검사를 미리 손으로 만드는 것.
  * 강의 규칙인 설명 의무를 없애거나 기계로 대신하는 것.
  * Tan 규모의 outer loop(대량 cloud agent, auto-merge, fuzz)를 들이는 것.
  * 외부 skill을 규칙집으로 통째로 들이는 것.
  * mini-redis, mini-dbms의 설계 문제에 실제 Redis나 DBMS가 쓰는 답을 적는 것.
  * 지금 저장소(R3–R5)의 설정을 이번 회고에서 고치는 것. 고칠지는 저자가 따로 정합니다.

## Alternatives Weighed

아래는 reviewer들이 반대한 선택지입니다. 저자가 직접 거절한 항목은 아직 없습니다. 각 항목은 reviewer 근거이고, 채택이나 거절은 저자의 결정입니다.

* **rule × repository × layer 표만으로 회고:** reviewer들이 반대했습니다(structural 2, 3; zoom-out 2). 규칙은 저장소마다 문장이 바뀌고, 쪼개지고, 합쳐집니다. 그래서 문장을 key로 한 표는 비교할 수 없고, 행 수는 기간과 서두름을 잽니다. 대신 rule ID로 이은 교정 ledger와 계보 표를 씁니다.
* **층별 개수를 성공 지표로 사용:** reviewer들이 반대했습니다(comprehension 11, implementation-readiness Nit, design N2). 두 층 행을 두 번 세고, 행이 묶는 규칙 수가 저장소마다 다릅니다.
* **GitHub 설정을 손으로 적용하고 문서에 적기 (지금 방식):** reviewer들이 반대했습니다(A1). 두 번 실패했고, 저장소마다 약해졌고, 아무도 모르게 drift가 생겼습니다.
* **`check-ids.py` 또는 `check-decision-links.mjs`를 그대로 복사:** codebase-details가 반대했습니다(A7). 따옴표, 경로, 파일 존재, ID 문법을 하드코딩했습니다. 설정 파일을 받는 checker 하나로 뽑아내고, 이월하는 것은 계약입니다.
* **개인 `~/.claude` skill로 kit 전달:** structural 6d, design M7이 반대했습니다. 팀원과 팀원 에이전트에게 닿지 않습니다.
* **Human review를 모두 없애기:** 모든 lens가 반대했습니다. 강의 규칙과 충돌합니다. 병합 gate만 줄입니다.
* **"승인 1건"을 품질 gate로 유지:** zoom-out 4가 반대했습니다. 근거상 이미 비어 있었습니다(LGTM, 우회 병합, quota 실패). 대신 작성자 설명과 시연을 둡니다. 다만 R3 ruleset의 승인 1건은 stale 승인 무효와 함께 실제로 강제됐던 유일한 사례이므로, 지울지 저자가 정해야 합니다.
* **Pintos 두 저장소를 같은 비중으로 분석:** zoom-out 1이 반대했습니다. AI 규칙이 다르고 CI가 없었으며, 에이전트 파일이 로컬뿐이었습니다. structural은 R2 설정과 이력을 "모름"으로 두고 판정에서 빼자고 했습니다.
* **스택 후보별 adapter stub을 미리 만들기:** inventive-catalyst는 찬성, zoom-out은 YAGNI로 반대했습니다. 결정은 열려 있습니다.

## Key Decisions & Staging for Next Steps

**약점 먼저:** 아래 결정 대부분은 저자가 정할 몫이고, 이 brief는 순서만 제안합니다. 1번이 실패하면 3–5번의 모양이 바뀝니다.

1. **(D4로 대부분 해결: 공개 저장소. 비관리자 계정 시험만 남음) 플랜 확인.** 나만무 저장소의 소유자 종류, 공개 여부, 플랜을 정하고, 같은 조건의 throwaway 저장소에서 ruleset과 required check가 만들어지는지 API로 확인합니다. 안 되면 대안(공개, 유료, 사후 탐지 CI)을 고릅니다. — 저자의 결정
2. **측정 정의 고정.** 다음을 문서 첫머리에 적습니다.
   * 첫날 = 첫 작업 커밋 + 24시간, 또는 다른 기준점 하나
   * "이어짐" 단위(file / text / intent)
   * 끊김 이유 코드
   * layer 판정 문장, 그리고 테스트를 2와 3 중 어디에 둘지
   * 근거 출처 범위와 § D가 하한이라는 표시
   * 저장소별 고정 SHA
   — 저자의 결정
3. **(D2, D3으로 저자가 답함) Layer 5 분리와 "이해 범위" 결정.** 병합 gate / 이해 / 에이전트·bot 리뷰로 나누고, "각자 이해"가 전체 코드인지 자기 코드인지 정합니다. 그 결과로 human review 경계를 병합 gate에 대해서만 적습니다. — 저자의 결정
4. **Ledger 작성 (하루 시간 제한).** R3→R4→R5 전환, B3 끊김, § D 교정, 거짓 주장 목록을 rule ID로 잇습니다. 판정은 raise / keep / drop과 Q2 기준입니다. 2026-10-31 O2의 반증 시도 결과(mini-react)를 한 줄로 기록합니다. — 저자 작업, 에이전트 보조 가능
5. **Kit 초안.**
   * A7 (a) 묶음
   * ruleset JSON, 적용 스크립트, drift 검사
   * `verify` 고정 이름 CI와 슬롯 표시
   * 텍스트 기반 ID 인용 checker의 계약. 구현은 스택을 고른 뒤 config로 맞춥니다.
   * secret scanning과 push protection
   * `strict: true`
   * PR 설명 칸 검사
   * template version stamp
   — 저자 작업
6. **Dry run.** 비관리자 계정으로 D#1, #2, #3, #5, #6, #11, #23을 replay하고, 멈춘 layer를 기록합니다. 가능하면 팀원 한 명이 kit을 빈 저장소에 적용하게 합니다. — 저자와 동의한 팀원
7. **스택을 고른 날의 trigger 목록.** 다음 항목마다 목표 layer와 시한을 적습니다:
   * lint, type, 이름 검사
   * 의존 방향 graph 검사
   * `return` 앞 빈 줄
   * 실행 검증 CLI와 feature map
   * pstack 후보, 그리고 `/no-comments`와 "주석은 이유만" 중 하나 고르기
8. **나만무 운영 중.** `correction` label이나 이슈 템플릿으로 교정을 모읍니다. 관찰된 교정만 승격의 trigger로 씁니다. 판정할 수 있으면 Layer 1–3으로, 판단이 필요하면 Prose에 "관찰된 위반" 한 줄을 붙여 둡니다. 우회는 기록된 사건으로만 허용합니다.

`/egm-draft`로 넘길 때 이 brief의 A1–A10이 문제 정의가 되고, Q1–Q4 답이 설계 후보가 됩니다.
