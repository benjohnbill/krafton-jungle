# Phase 1 설계 독립 검토 후속 확인

검토일: 2026-11-09. 요청된 수정 부분만 읽었다. 소스·산출물·모델은 수정하지 않았고, 테스트 실행 및 Lark 재조사는 하지 않았다. 이 후속 보고서만 새로 작성했다.

## 결론

앞선 P2 finding 두 건은 모두 해소됐다. 이번 수정 범위에서 남은 blocking이나 substantive 결함은 없다. 전체 설계 재감사 또는 실행 성공 판정은 아니다.

### Finding 1: HR-N05의 거절 입력 History 보존 축소 · 해소

- phase1-test-inventory.md 537~543행: 빈 입력·다중 root 거절이 현재 View, 저장된 내용 전체, 이동 가능 상태, 실제 영역 및 기존 redo 재방문을 보존한다고 명시한다. 내부 snapshots 공개 대신 공개 이동 결과로 관찰하도록 정했다.
- 같은 문서 541·543행: 정상 무변경 Patch의 비교 의미와 과거 위치 redo만 D7/DEC-09로 한정한다.
- phase1-test-design.md 569행 및 757행: 같은 경계를 반영한다. 758행의 'HR-N05의 redo 부분'은 바로 앞 757행에서 거절 입력을 제외하므로 더 이상 거절 입력 전체를 미정으로 만들지 않는다.
- tmp/phase1-model.json 850행의 I-HR 결정 문구도 같은 경계다. phase1-coding-handoff.md 52행도 일치한다.

### Finding 2: 위치 비교와 생존 노드 identity의 모호함 · 해소

- phase1-test-inventory.md 303~305행: DIFF-N05의 old/new 대표쌍을 고정했다. old section의 마지막 p(c)를 삭제하고, section class 추가, 첫 p의 a→A 및 b(new) 자식 추가를 결합한다. 삭제되는 기존 형제는 tail이므로 내용상 항목 이동의 identity를 요구하지 않는다. Diff 단위에는 불필요한 실제 DOM refs도 제거했다.
- 같은 문서 365~367행: DP-N04의 old root div, section[0], p[0,0], p[0,1], aside[1]를 같은 new 위치의 노드와 ===로 비교하고, p[0,2]만 제거되며 b는 새 노드라고 명시한다. 이 대응은 key 없는 위치 비교와 맞는다. 중간 삭제에서 내용상 같은 항목의 ref 보존을 강제하지 않는다는 경계도 있다.
- phase1-test-design.md 832~833행 및 phase1-coding-handoff.md 53행은 수정된 재고의 고정 fixture와 위치별 대응을 참조한다. 모델은 상세 fixture를 중복 저장하지 않고 기존 DIFF-N05·DP-N04 ID로 재고에 연결하므로 충돌하지 않는다.

## 함께 요청한 실행상 보정

- phase1-coding-handoff.md 54행: 미구현 모듈 static import에 it.skip만 붙여도 타입 오류가 해결되지 않는다는 점, scaffolding 부재 시 실행 불가능한 import를 만들지 않고 이유 있는 todo·blocked로 남긴다는 점을 반영했다. 임의 새 API·제품 구현도 금지한다.
- 같은 문서 55행: canonical·로컬 T/P·후보 ID의 다대일 매핑을 허용하고 설계 항목 수만큼 실행 테스트를 복제하지 않도록 명시했다.
- 같은 문서 14행과 phase1-test-design.md 815·835행: diff.ts·diff.test.ts 동시 추가 관찰과 코드 생성 전 재매핑 필요를 반영했다. 과거 부재를 현재 상태로 일반화하지 않는다.

## 남은 한계

기존 DEC의 실제 미확정 계약, 현재 API와 작업 트리 재확인, 브라우저 runner와 실제 FUNC·IME 증거 확보는 그대로 남는다. 이는 이번 두 finding의 미해소 사유가 아니라 다음 코딩·실행 단계의 이미 분리된 작업이다. 이번에는 기존91행·73후보 전체를 다시 검산하거나 새 Diff 테스트를 읽고 실행하지 않았다. 브라우저 탭은 열지 않았다.

추가 재확인: inventory DIFF-N05 305행은 수기 Patch 종류·경로·payload와 바깥 변경 지시 없음으로 단위 oracle를 한정했다. 실제 DOM 내용과 refs는 DP-N04의 통합 책임으로 분리해 단위에서 apply까지 호출할 오해도 해소했다.
