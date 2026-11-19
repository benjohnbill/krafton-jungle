# Phase 1 테스트 설계 독립 최종 검토

검토일: 2026-11-09. 코드 생성과 테스트 실행은 하지 않았다. 소스·원본 산출물·Lark·GitHub를 변경하지 않았다. 아래 파일명은 같은 세션 artifacts 폴더 기준이며 줄 번호는 검토 시점 원본 기준이다.

## 결론

전체 코딩 착수를 막는 blocking 결함은 없다. 기존 재고와 책임별 설계, 실행 결과 구분, 무단 정책 변경 방지는 보존됐다. 다만 아래 두 부분은 해당 후보를 코드화하기 전에 좁혀야 한다. 한 항목은 기존 거절 입력의 History 보존 기대를 불필요한 결정 대기로 만들고, 다른 항목은 key 없는 위치 비교에서 잘못된 identity 기대를 만들 수 있다.

## 중요도순 substantive findings

### 1. P2 · 거절 입력의 redo 보존을 no-op 정책 질문과 함께 미정 처리한다

- 위치: **phase1-test-inventory.md, C §5, HR-N05, 537~543행**, 특히 541행과 543행. 관련 상위 연결은 **phase1-test-design.md, I-HR §3, 562~569행**, DEC-09 **754~759행**이다.
- 근거: 같은 inventory의 기존 **verify-empty-input 85행 사례(633~636행)**와 **verify-multi-top 86행 사례(638~641행)**는 실제 영역과 **history 그대로**를 요구한다. 원 조사보고서 tmp/design-history.md 155·160행 및 tmp/design-page.md의 행85·86 기록도 같은 기대다. 반면 HR-N05는 유효하지 않은 입력까지 포함한 하나의 후보에서 redo 가지를 자르지 않는 것을 권장 계약으로 채택할지 결정한다고 쓰고, 단순 현재·개수 보존만 기존 기대라고 축소한다.
- 영향: 거절 시 현재 View와 개수만 유지하지만 redo를 파괴하는 구현을, 기존 보존 기대 위반이 아니라 미정 범위로 분류할 수 있다. 현재·개수가 같은 다른 snapshots로 바꾸는 오류도 같은 약점이다.
- 고칠 방향: HR-N05의 assertion을 분리한다. 빈 입력·다중 root 거절은 현재·저장 내용·이동 가능 상태·기존 redo 재방문까지 보존하는 기존 계약의 보강으로 둔다. **정상 무변경 Patch를 과거 위치에서 누르는 조건만** DEC-09에 남긴다. DEC-09 자체를 폐기하거나 core 동일값 저장 정책 DEC-07을 대신 확정할 필요는 없다. 거절 입력 fixture와 no-op fixture가 같은 ID 아래 있어도 assertion별 의존은 분리해야 한다.

### 2. P2 · 혼합 삭제 후보의 생존 ref 기대에 위치 기준이 빠져 있다

- 위치: **phase1-test-inventory.md, B §6, DIFF-N05 303~305행**, **DP-N04 365~367행**. 비교 기준은 **phase1-test-design.md, U-DIFF §5, 343~350행** 및 기존 diff-child-insert-middle **inventory 250행**이다.
- 근거: 후보는 형제3개 중 하나 삭제와 살아남는 형제 변경을 결합하고, DP-N04는 생존 형제 및 중첩 target refs를 저장해 생존 불변 범위의 refs 유지를 검사한다고 쓴다. 그러나 어떤 old 위치가 어떤 new 위치를 맡는지 fixture와 identity 대응이 없다. 기본 계약은 key 없는 위치 비교다. ADR0006의 순서 절과 현재 src/diff.ts 62~80행은 같은 번호끼리 비교하고 남은 끝을 삭제한다.
- 구체 위험: old li(a),li(b),li(c) → new li(a),li(c)라면 정상 위치 비교는 두 번째 old li를 c로 갱신하고 세 번째 old li를 지운다. 내용상 남은 c라는 이유로 old 세 번째 li와 new 두 번째 li의 ===를 요구하면 정상 구현을 실패시키고 사실상 key 기반 보존을 강제한다. 직접 작성한 내용 oracle만으로 이 ref 대응의 모호함은 해소되지 않는다.
- 고칠 방향: 대표 old/new를 문서에 고정하고 old index→new index의 허용 ref 대응을 적는다. 중간 삭제를 쓰면 내용상 같은 항목의 identity를 요구하지 말고 위치 비교가 유지하는 노드와 변경 밖의 subtree만 검사한다. 또는 마지막 자식 삭제와 앞쪽 생존 위치 변경을 대표 fixture로 택해 보존 범위를 명시한다. Patch 단위의 수동 REMOVE[1] 후 c ref 유지(PATCH-N06)는 별개 계약이므로 이를 Diff 생성 결과에 그대로 적용하지 않는다.

## 통과한 검산과 분류

- canonical 색인 **91개**, 시트 **2~92행** 모두 정확히 한 번이며 ID·행 중복과 누락이 없다. 상세 본문에도 91개 ID가 모두 존재한다. 변환22·Diff16·Patch11·순수 변환 왕복1·Diff/Patch 연결8·History10·페이지23으로 합계가 맞는다.
- 선택은 정확히 **69 hist-max-size, 90 verify-back-partial, 91 verify-patch-log, 92 verify-highlight**의4개이며 나머지87개다. History 부분 복원의 identity를 필수로 승격하지 않았다.
- 별도 M9는 **93~97,100~102의8개**로 보존됐다. 98·99는 Phase2 h-key 영역으로 제외되며, 103부터 props 확장 경계를 기본 범위와 구분했다. M9 안 기본·엣지와 선택100~102도 구별한다. 원격 원문을 이번 검토에서 다시 전수 조사하지 않았으므로 이 경계 판정의 외부 근거는 제공된 조사와 산출물의 관찰 기록이다.
- **13대상=단위6·통합4·기능3**, **57갈래**가 문서와 phase1-model.json에서 일치한다. 공개 isTextInput도 생산 코드 reader/Patch 협력 함수로 존재한다. 각 갈래에 책임에서의 도출·성질·조건·기존 근거 또는 후보 연결이 있다. 후보 ID 총 **73개**, 정의 중복과 design의 명시적 미정의 후보 참조는 없다. 개수73을 신규 실행 테스트73개로 강제하지 않는다.
- Lark 기존과 로컬 T1~T37·T38 todo 및 P1~P28 선언, proposed ADR, 설계 후보와 실제 실행 결과를 구별한다. T38을 완료로 세지 않는다. ADR0006의 INSERT·[] View·순차 path·noRollback 구체안이 원격 #13의 과거 질문 때문에 모두 미정으로 되돌아가지 않았다.
- 두 왕복 방향을 구별한다. isEqualNode와 outerHTML의 live value·identity 맹점을 분리하고 .value 직접 확인, Node ===, MutationObserver를 제시한다.
- FUNC는 실제 브라우저이고 jsdom 페이지 검증은 보조 통합으로 분리한다. 입력 정제88의 script/onerror 제거와 literal Text escape를 혼동하지 않는다. 실제 입력·IME·focus 정책도 일괄 필수화하지 않는다.
- 공백, 루트 Text/Comment·null, value 정규형, 경로, History API의 영향 범위를 DEC-01~14에 연결한다. 위 finding1을 제외하면 초기저장1개·no-op80·분기84·안내85/86·정제88을 새로운 일반 정책 질문으로 되돌리지 않는다.
- 테스트 안의 가짜 페이지 orchestration, SUT로 계산한 단위 기대값, 테스트 전용 export, 무단 제품 변경과 원격 변경을 금지한다. 기존 코드 재사용과 assertion 보강 및 실제 추가를 구별해 대량 중복 생성 위험을 줄인다.

## handoff 실행 가능성과 남은 한계

- **별도 코딩 세션은 현재 문서로 착수 가능하다.** 실제 API와 기존 테스트를 매핑하고 영향 없는 단위부터 작성·실행할 수 있다. 모든13대상의 즉시 완성·통과를 보장하는 완결된 실행 명세는 아니다. 이 차이는 문서에도 명시돼 있다.
- 검토 중 현재 src에는 **diff.ts와 diff.test.ts도 추가된 상태**를 확인했고 diffViews 공개 구현을 읽었다. 설계의 Diff 부재는 과거 관찰이며 현재 부재 주장이 아니다. handoff의 시작 시 최신 목록·브랜치·작업 트리 재확인 규칙을 그대로 적용해야 한다. 새 Diff 테스트는 이번에 전수 매핑하거나 실행하지 않았다.
- 현재 src 목록에서 History·검증 페이지는 확인되지 않았다. 현재 package scripts는 typecheck, check, test, build를 제공하지만 browser runner 스크립트는 없다. 실제 History API·페이지 entry·selector·브라우저 runner 또는 수동 경로를 확보하기 전 해당 통합·FUNC는 blocked로 남는다. 테스트 안에서 제품 흐름을 대신 구현하는 해결은 허용되지 않는다.
- 미구현 모듈은 it.skip만으로 존재하지 않는 static import의 타입·모듈 오류가 해결되지 않는다. handoff가 이미 실행 import 강제를 금지하므로, 다음 세션은 API 부재를 case 상태표에 blocked로 기록하고 실행 불가능한 import를 생성하지 않아야 한다. 이는 현재 문서의 금지 경계를 구체적으로 적용하는 실행상 주의이며 별도 설계 결함으로 세지 않았다.
- 후보는 추적 단위다. 기존 canonical ID·T/P ID·후보 ID가 같은 실행 테스트와 assertion을 가리킬 수 있다. 코딩 세션의 case→파일·테스트명 표에서 다대일 매핑을 허용해야 한다. 실제 실행 수는 그 매핑 뒤 결정한다.
- 로컬 ADR의 proposed 지위와 Lark 충돌은 승인·적용 브랜치 확인 없이 해결된 것으로 보고할 수 없다. 승인 대기 때문에 무관한 변환·불변·빈 batch·기존 History 기대까지 막을 이유는 없다.
- 로컬 테스트 실행·CI·OS IME·실제 FUNC는 이번 검토의 증거가 아니다. 원격 변경도 하지 않았다. 브라우저 탭은 열지 않았다.
