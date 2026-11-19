# Phase 1 테스트 코드 생성 handoff

## 작업 위치

- 프로젝트(WSL): /home/benjohnbill/dev/krafton-jungle/week11-12/mini-react
- 문서 폴더(Windows): C:\Users\benjohnbill\.aside\u\0\sessions\2026-11-09_C1EEOU2nGJ87YfII\artifacts
- 문서 폴더(WSL): /mnt/c/Users/benjohnbill/.aside/u/0/sessions/2026-11-09_C1EEOU2nGJ87YfII/artifacts
- 문서를 다른 위치로 복사했다면 같은 폴더의 세 파일을 함께 읽는다.

## 목적
Lark 기존 사례와 보완 설계를 실제 테스트 코드로 옮긴다. Phase 1의 책임에서 도출한 검증 성질을 보존한다. 테스트가 통과하도록 기대 동작이나 제품 코드를 임의로 바꾸지 않는다.

## 먼저 읽을 자료
- 같은 폴더의 phase1-test-design.md
- 같은 폴더의 phase1-test-inventory.md
- 프로젝트 mini-react/AGENTS.md, CONVENTION.md, GLOSSARY.md, package.json, vitest.config.ts
- Lark React Tests와 README. 문서의 관찰 시각 이후 수정됐을 수 있으므로 관련 범위를 다시 확인한다.

## 코드 생성 전 확인
1. 현재 branch, 작업 트리, 실제 공개 API와 구현 상태를 확인한다. 기존 작업을 덮어쓰지 않는다.
2. 이 설계는 시점별 로컬 관찰을 근거로 했다. 시작에는 vnode.ts·vnode.test.ts·main.ts·setup.test.ts만 있었고, 조사 중 patch.ts·patch.test.ts(P1~P28)·ADR0006이 추가됐다. T1~T37·T38 todo와 P1~P28을 먼저 매핑한다. 독립 검토 중 diff.ts와 diff.test.ts도 추가됐으므로 해당 테스트도 새로 만들기 전에 매핑한다. Diff·History·검증 페이지의 부재 관찰을 모든 브랜치나 현재 상태로 일반화하지 않는다.
3. [결정 필요] 목록을 최신 계약과 대조한다. 합의된 자료가 없으면 영향받는 기대값은 임의 확정하지 않는다. 해당 사례를 blocked로 기록하고, 영향 없는 사례를 먼저 구현한다.
4. 후보 case는 자동으로 팀 합의가 된 것이 아니다. 사례의 성질이 기존 계약에서 도출되는지 확인하고 설계와 구현을 연결한다.

## 구현 원칙
- 단위와 통합: 현재 Vitest와 jsdom 설정을 사용한다. Lark의 FUNC는 실제 브라우저 입력과 클릭으로 판정한다. jsdom의 UI 시뮬레이션을 FUNC 완료로 세지 않는다.
- 테스트는 내보낸 함수를 호출한다. 테스트만을 위해 내부 함수를 export하지 않는다.
- VNode fixture와 기대값을 직접 작성한다. 검사 대상 함수로 자기 기대값을 계산하지 않는다.
- 통합에서는 수동 기대 구조를 우선하고, 별도 생성 함수 결과를 비교하더라도 공통 오류를 숨길 수 있다는 한계를 보완한다.
- 구조, 실시간 input property, DOM identity를 각각 검사한다. outerHTML 또는 isEqualNode 하나로 세 가지를 모두 검증했다고 보고하지 않는다.
- 텍스트/주석/공백이 섞인 DOM은 확정된 정규화 및 경로 계약으로 준비한다.
- 동일 case를 여러 레벨에 복제하지 말고 각 레벨에서 추가로 검증할 약속을 적는다.
- 기존 테스트를 삭제하거나 기대값을 약하게 바꿔서 통과시키지 않는다.
- 미구현 함수 때문에 임시 skip 또는 todo를 두면 정확한 이유와 case ID를 남긴다. skipped/todo를 통과 수로 보고하지 않는다.
- 실제 제품 코드 수정이 필요하면 실패 재현과 원인을 먼저 분리한다. 이 handoff만으로 기능 변경이나 미정 정책 선택을 승인받은 것은 아니다.
- Lark, GitHub, 팀 규칙, 공개 API의 정책을 임의 수정하지 않는다. commit, push, PR은 이번 handoff의 기본 실행 범위가 아니다.

## 실행과 완료 보고
- 가능한 환경에서 npm run typecheck, npm run check, npm test, npm run build를 실행한다. 실행하지 못한 항목은 원인과 함께 명시한다.
- 브라우저 기능 검증은 실제 실행 환경과 자동/수동 여부를 적고, 실제 키 입력·IME·focus/caret 확인을 jsdom property대입으로 대체하지 않는다.
- case ID → 테스트 파일·테스트명 → passed/failed/skipped/blocked 대응표를 남긴다. 매개변수화 전 설계 항목 수와 실제 실행 테스트 수를 구분한다.
- 변경 파일, 재현된 결함, 미정 사항, 남은 검증 범위를 보고한다. 모든 테스트 통과를 코드 품질 전체의 보장으로 표현하지 않는다.

## 이 작업의 정확한 범위

- 기본 M1~M4: 상위13대상(단위6·통합4·기능3),57검증갈래. 기존 Lark91개 중87개 기본·엣지,4개선택. M9 key8개는별도.
- 73개 추적 후보를 신규73개로 만들지 않는다. 기존 코드 재사용·assertion보강·기존시트코드화·결정대기 조건을 구분한다.
- DEC-01~14와 후보별 의존만 연결한다. 기존 시트가 정한 초기저장·no-op·분기·거절안내·정제를 새 정책 질문으로 되돌리지 않는다.
- 현재 로컬 Patch안은 INSERT, path=[]는View,앞Patch적용후트리,받은순서적용,noRollback이다. Lark CREATE와 차이가 있으므로 최신 채택 계약을 확인한다. 과거#13질문만으로 모든 Patch가미정이라고 하지 않는다.
- Lark int-render-roundtrip은 VNode→DOM→VNode. 로컬T34~37은 DOM→VNode→DOM이므로 같은 한 사례로 대체하지 않는다.
- History push/current 등의 이름은 시트 가정이다. 실제 API 확인없이 새 실행 import를 강제하거나 any캐스팅으로 계약 충돌을 숨기지 않는다.

## 시작 프롬프트

/mnt/c/Users/benjohnbill/.aside/u/0/sessions/2026-11-09_C1EEOU2nGJ87YfII/artifacts 폴더의 phase1-test-design.md와 phase1-test-inventory.md를 읽고 /home/benjohnbill/dev/krafton-jungle/week11-12/mini-react의 Phase1 테스트를 코드로 옮겨 주세요. 문서를 옮겼다면 전달받은 새 경로를 사용하세요. 위 구현 경계와 팀 규칙을 지키고, 먼저 현재 브랜치·작업트리·공개API·기존테스트를 확인해 case ID별 구현계획을 정리하세요. 미정 항목은 영향받는 사례만 blocked로 기록하고, 나머지 단위→통합→실제브라우저기능 순서로 구현·실행하세요. 테스트를 통과시키려고 제품 코드나 정책을 임의로 바꾸지 마세요. 최종에는 기존과추가 case ID별 파일·테스트명·결과와 실행명령, 남은 결정·미구현·수동검증을 보고하세요.

## 독립 검토 후 추가 주의

- HR-N05의 거절 입력은 기존 redo를 포함한 이력 전체 보존을 검사한다. 정상 무변경 Patch의 과거 위치 redo만 DEC-09에 의존한다.
- DIFF-N05·DP-N04는 재고 문서에 고정한 마지막 자식 삭제 fixture와 위치별 참조 대응을 사용한다. 중간 항목 삭제 뒤 내용상 같은 항목의 identity를 요구해 key 없는 Diff를 잘못 실패시키지 않는다.
- 미구현 모듈에 static import를 만들어 놓고 it.skip만 붙이면 typecheck 오류가 사라지지 않는다. 실제 공개 scaffolding이 없다면 해당 사례는 이유가 있는 todo·blocked 명세로 남기고 실행 불가능한 import를 생성하지 않는다. 새 API나 제품 구현을 임의로 만드는 해결은 금지한다.
- canonical ID·로컬 T/P ID·후보 ID가 같은 실행 테스트 또는 assertion으로 매핑될 수 있다. 다대일 대응을 허용하고 단순히 설계 항목 수만큼 테스트를 복제하지 않는다.
