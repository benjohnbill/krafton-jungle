# StateHistory와 History–View 복원 테스트 설계 handoff

조사 시점: 2026-11-09. 읽기 전용 조사이며 코드, GitHub, Lark를 변경하지 않았다. 이 문서는 별도 코딩 세션의 설계 입력이다. 현재 구현 또는 확정 API가 있다고 뜻하지 않는다.

## 1. 판정 요약과 근거 수준

- 조사 시작의 로컬 mini-react/src에는 vnode.ts, vnode.test.ts, setup.test.ts, main.ts만 있었다. 최종 재확인에서 다른 세션의 동시 작업으로 patch.ts와 patch.test.ts 및 ADR0006이 새로 생긴 것을 확인했다. history.ts, History 테스트, diff.ts, 검증 페이지 구현은 최종 확인에도 없다. main.ts는 시작 시 #app에 mini-react라는 글자만 썼다. Patch 구현 상태는 병행 작업 중이므로 코딩 세션이 다시 확인한다.
- CONVENTION.md는 src/history.ts의 State History 책임과 vnode 타입만 가져오는 의존 방향을 정한다. DOM 복원은 history가 아니라 test-pages에서 History, VNode 변환, Diff, Patch를 협력시키는 책임이다.
- ADR 0004는 createVNodeFromDom, createDomFromVNode, diffViews, applyPatchesToDom 이름만 명시한다. StateHistory 생성 방법과 메서드 시그니처는 없다. GLOSSARY.md에도 StateHistory, snapshots, current index 정의는 없다. 시작 때 읽은 ADR 0001~0005의 frontmatter는 모두 proposed이다. 최종 추가된 ADR0006도 아래 보충 관찰로 구분한다. 현 CONVENTION에 들어간 규칙과 ADR의 제안 상태를 섞지 않는다.
- Lark의 StateHistory, push(), current(), back(), forward(), canBack(), canForward(), size는 **기존 시트가 가정한 API 표기**이다. 공개 구현 또는 팀이 확정한 시그니처로 취급하지 않는다. 아래 후보는 ‘저장’, ‘현재 조회’, ‘뒤로 이동’ 등 의미상 동작으로 쓴다.
- Lark README 행5~8: UNIT는 함수 또는 클래스 하나, INTEG는 둘 이상 함수의 협력, 두 단계 모두 Node+jsdom. FUNC는 실제 브라우저에서 입력·클릭하는 Playwright 테스트. README 행13~15: 기본과 엣지는 필수, 선택은 요구사항 밖이며 미구현이면 skip.
- 로컬 vitest.config.ts는 jsdom 환경이다. src/vnode.ts의 VNode는 string 또는 {type, props: Record<string,string>, children: VNode[]}이며 현재 createVNodeFromDom은 텍스트 input의 실시간 .value를 props.value로 읽는다.
- lab/meeting-1110/plan.html은 State History 단위 테스트를 아직 할 일로 분류한다. 검증 페이지 버튼은 별도 기능 테스트 구분이다. lab/phase1-compare.html에 History 직접 명시는 발견하지 못했다.
- 부모의 LMS 원문 확인 결과를 전달받은 근거: Patch 후 새 VNode 저장, 뒤·앞 이동 시 실제 영역과 테스트 영역 동시 복원이 필수이다. 아래 Lark 셀은 본 담당이 직접 읽었다. LMS 페이지는 본 담당이 직접 열지 않았다.

## 2. 대상별 책임, 경계와 검증성질

### H1. 새 이력과 현재 조회
책임: View의 순서 있는 저장 집합에서 현재 View를 반환하고 앞뒤 이동 가능 여부와 저장 개수를 제공한다. 아직 저장하지 않은 새 이력과 저장 1개의 상태를 구별한다.
입력·출력: 새 인스턴스 또는 View 저장 → 현재 View 또는 빈 결과, 개수, 이동가능 여부. 저장상태: snapshots와 현재 위치의 논리적 대응. 협력: VNode 타입만. 범위: UNIT.
검증성질: 빈 이력은 현재가 없고 양방향 이동 불가이며, View 하나를 저장하면 그 View만 현재가 된다.

### H2. 저장과 분기
책임: 새 View를 현재 위치 다음에 저장하여 현재로 만들고, 과거 위치에서 새 View를 저장하면 이전 redo 가지를 버린다. DOM 갱신, Patch 생성, 페이지 no-op 판정은 이력 자체의 책임으로 단정하지 않는다.
입력·출력: View와 기존 이력 → 새 현재 View와 갱신된 개수·이동가능 여부. 저장상태: 과거 prefix 보존, 새 현재 추가, redo 제거. 협력: 없음. 범위: UNIT.
검증성질: A→B→C에서 A로 돌아가 D를 저장하면 접근 가능한 순서는 A→D이고 B와 C는 앞으로 이동으로 재등장하지 않는다.

### H3. 뒤·앞 이동과 경계
책임: 기존 저장 View 사이에서 현재 위치를 한 단계 이동하고 대상 View를 제공한다. 처음과 끝을 넘는 요청은 저장 내용과 현재 위치를 바꾸지 않는다.
입력·출력: 이동 요청 → 이동 대상 또는 실패 결과. 저장상태: 위치만 바뀌며 저장된 순서와 개수는 보존. 협력: 없음. 범위: UNIT.
검증성질: 유효 이동은 정확히 한 칸이며 경계의 연속 호출은 상태를 유지하고 반대 방향 이동을 망가뜨리지 않는다.

### H4. 저장·조회 참조 격리
책임: 저장에 사용한 View 또는 밖으로 내준 View를 외부에서 바꿔도 과거 snapshot의 내용은 유지한다. 복사 방식이나 내부 자료구조는 테스트가 정하지 않는다.
입력·출력: 중첩 View 저장 및 조회 → 내용이 맞고 외부 변이에 안전한 View. 저장상태: 과거 각 View 내용의 독립성. 협력: VNode 타입. 범위: UNIT.
검증성질: props, children, 깊은 자식의 외부 변이는 이미 저장한 현재와 과거 snapshot에 전파되지 않는다.

### HR1. Patch 완료와 History 저장 연결
책임: 성공적으로 반영한 새 View를 다음 이동에서 복원할 수 있게 저장하고, 페이지 초기 View를 복원 가능한 첫 상태로 둔다. 검증 페이지의 모든 버튼 배치나 안내 문구를 다시 검증하지 않는다.
입력·출력: 초기 View 및 유효 편집 → 실제 DOM 반영과 이력의 새 현재. 저장상태: 초기 1개, 변경 성공마다 새 상태, no-op 및 거절 입력에서는 보존. 협력: 페이지 코드, VNode 변환, Diff, Patch, History. 범위: INTEG, 버튼의 실제 클릭은 담당4 FUNC.
검증성질: 저장된 현재 View는 실제 반영된 View와 같고, 첫 변경 후 뒤로 가면 페이지를 처음 연 View가 복원된다.

### HR2. History 이동과 두 영역 복원 연결
책임: 이동으로 받은 View를 실제 영역과 편집용 테스트 영역에 함께 반영한다. 복원 자체를 새 저장으로 오인하지 않는다.
입력·출력: 저장된 A/B/C와 뒤·앞 이동 → 두 DOM의 대응 View. 저장상태: snapshot 개수 불변, 현재와 DOM 일치. 협력: History와 페이지 복원 경로, VNode 변환과 DOM 갱신. 범위: INTEG.
검증성질: 어느 방향을 반복해도 두 영역을 다시 읽은 값과 이력의 현재가 같고, 저장 개수는 이동 때문에 늘지 않는다. input은 .value까지 같아야 한다.

## 3. Lark 기존 History UNIT 전체
출처: React Tests sheet=ffbb46. 행은 실제 스프레드시트 행번호이다. ID=D열, 검증성질=G열, 시나리오=H열, 기대=I열, 구분=F열을 셀 단위로 읽었다.

### 행60 · hist-empty · 엣지
- 검증성질: 기록이 하나도 없을 때 앞뒤로 갈 수 없다고 정확히 알려 주는지 확인함
- 시나리오: 아무것도 push하지 않은 새 StateHistory를 사용함
- 기대: current()는 null, canBack()과 canForward()는 false, size는 0임

### 행61 · hist-push-one · 기본
- 검증성질: 기록 하나를 저장하면 그게 현재 화면이 되는지 확인함
- 시나리오: View A 하나를 push함
- 기대: current()가 A와 내용이 같고, canBack()과 canForward()는 false임

### 행62 · hist-back · 기본
- 검증성질: 뒤로 가면 이전 화면이 나오고, 다시 앞으로 갈 수 있게 되는지 확인함
- 시나리오: A, B를 push한 뒤 back()을 호출함
- 기대: A를 돌려주고 current()도 A이며, canForward()가 true임

### 행63 · hist-forward · 기본
- 검증성질: 뒤로 갔다가 앞으로 가면 최신 화면으로 돌아오는지 확인함
- 시나리오: A, B를 push하고 back()한 뒤 forward()를 호출함
- 기대: B를 돌려주고 current()도 B이며, canForward()는 false임

### 행64 · hist-back-at-start · 엣지
- 검증성질: 첫 기록에서 더 뒤로 가려 하면 아무 일도 일어나지 않는지 확인함
- 시나리오: A만 push한 상태에서 back()을 호출함
- 기대: null을 돌려주고 current()는 여전히 A임

### 행65 · hist-forward-at-end · 엣지
- 검증성질: 최신 기록에서 더 앞으로 가려 하면 아무 일도 일어나지 않는지 확인함
- 시나리오: A, B를 push한 상태(가장 최근 위치)에서 forward()를 호출함
- 기대: null을 돌려주고 current()는 여전히 B임

### 행66 · hist-push-truncates · 기본
- 검증성질: 뒤로 간 상태에서 새로 저장하면 앞쪽 기록이 지워지는지 확인함 (브라우저 뒤로가기와 같은 방식)
- 시나리오: A, B, C를 push하고 back()을 두 번 한 뒤 D를 push함
- 기대: 기록이 A, D 두 개가 되고 size는 2, canForward()는 false임

### 행67 · hist-isolation-input · 엣지
- 검증성질: 저장한 뒤 원본을 고쳐도 저장된 기록은 바뀌지 않는지 확인함
- 시나리오: A를 push한 뒤 밖에 있는 원본 A의 내용을 바꿈
- 기대: current()는 바꾸기 전 내용을 그대로 돌려줌

### 행68 · hist-isolation-output · 엣지
- 검증성질: 꺼낸 기록을 고쳐도 저장된 기록은 바뀌지 않는지 확인함
- 시나리오: current()로 받은 View를 바꾼 뒤 current()를 다시 호출함
- 기대: 두 번째 결과는 바꾸기 전 내용과 같음

### 행69 · hist-max-size · 선택
- 검증성질: 기록 개수에 상한을 두면 가장 오래된 것부터 지워지는지 확인함
- 시나리오: 최대 개수를 3으로 정하고 A, B, C, D를 push함
- 기대: 가장 오래된 A가 지워져 기록이 B, C, D가 됨

**중요:** hist-max-size(69)는 ‘선택’이다. 무한 이력, 기본 한도, 한도 초과 예외를 필수 정책으로 추가하지 않는다. capacity를 구현하기로 한 경우에만 max=3 기대를 적용한다.

## 4. 기존 History–View 관련 항목 전부와 범위
기존 INTEG 행51~59를 직접 확인했다. int-render-roundtrip, int-roundtrip-text, int-roundtrip-attr, int-roundtrip-children, int-roundtrip-replace, int-roundtrip-view-replace, int-roundtrip-sequence, int-preserve-identity, int-roundtrip-fuzz는 VNode 변환 또는 Diff→Patch의 협력이다. 이들 중 History 저장·이동을 포함한 항목은 없다. int-roundtrip-sequence(57)의 A→B→C→A는 연속 Diff→Patch이지 History 복원이 아니다.

따라서 다음 FUNC 항목은 History 연결 계약의 기존 근거이지만, Node+jsdom의 History 통합 테스트로 이미 존재한다고 세지 않는다. 버튼과 메시지 자체의 canonical 목록은 담당4 소유이다.

### 행71 · verify-load
- 시나리오: 페이지를 연 직후 두 영역을 비교함
- 기대: 테스트 영역의 HTML을 View로 바꾼 결과와 실제 영역을 View로 바꾼 결과가 같음
- History 연결: 초기 두 영역의 View 일치

### 행72 · verify-load-buttons
- 시나리오: 페이지를 연 직후 버튼 상태를 확인함
- 기대: 기록이 하나뿐이라 뒤로가기와 앞으로가기가 모두 비활성화되어 있음
- History 연결: 초기 기록 1개 명시. 초기 저장 여부 자체는 미정이 아님

### 행73 · verify-edit-no-apply
- 시나리오: 테스트 영역만 고치고 Patch는 누르지 않음
- 기대: 실제 영역은 전혀 바뀌지 않음
- History 연결: Patch 전 편집은 실제 View 및 저장 완료 상태와 구분

### 행76 · verify-patch-history
- 시나리오: 글자를 고치고 Patch를 누름
- 기대: 뒤로가기 버튼이 활성화되고 앞으로가기는 비활성 상태임
- History 연결: 첫 실제 변경을 저장한 뒤 초기 상태로 이동 가능

### 행80 · verify-patch-nochange
- 시나리오: 아무것도 고치지 않고 Patch를 누름
- 기대: 실제 영역의 DOM 변경이 0건이고 뒤로가기 버튼도 계속 비활성임
- History 연결: 페이지 no-op에서 새 이력을 만들지 않음. core의 동일값 저장 정책까지 확정하지 않음

### 행81 · verify-back
- 시나리오: 서로 다른 내용으로 Patch를 두 번 한 뒤 뒤로가기를 누름
- 기대: 실제 영역과 테스트 영역이 모두 첫 번째 Patch 직후 상태로 돌아감
- History 연결: 이동 대상 View가 두 영역에 복원됨

### 행82 · verify-forward
- 시나리오: 뒤로가기를 누른 뒤 앞으로가기를 누름
- 기대: 두 영역이 모두 두 번째 Patch 직후 상태로 돌아오고, 앞으로가기는 다시 비활성화됨
- History 연결: 이동 대상 View가 두 영역에 복원됨

### 행83 · verify-back-to-start
- 시나리오: Patch를 여러 번 한 뒤 뒤로가기를 더 이상 갈 수 없을 때까지 누름
- 기대: 두 영역이 페이지를 처음 연 상태가 되고 뒤로가기 버튼이 비활성화됨
- History 연결: 첫 페이지 상태까지 되돌아감

### 행84 · verify-back-then-patch
- 시나리오: 뒤로가기를 한 뒤 새로운 내용으로 Patch를 누름
- 기대: 새 내용이 반영되고, 이전의 앞쪽 기록은 사라져 앞으로가기가 비활성임
- History 연결: redo 가지 제거

### 행85 · verify-empty-input
- 시나리오: 테스트 영역을 모두 지우고 Patch를 누름
- 기대: 실제 영역과 history는 그대로이고, 최상위 노드가 하나 필요하다는 안내가 #message에 표시됨
- History 연결: 유효하지 않은 편집 거절 시 이력 보존

### 행86 · verify-multi-top
- 시나리오: 테스트 영역에 <p>a</p><p>b</p>처럼 최상위 요소를 두 개 입력하고 Patch를 누름
- 기대: 실제 영역과 history는 그대로이고, 최상위 노드가 하나 필요하다는 안내가 #message에 표시됨
- History 연결: 유효하지 않은 편집 거절 시 이력 보존

참고 행74 verify-patch-apply는 ‘글자 수정 후 Patch → 실제 글자 반영’, 행79 verify-many-tags는 input을 포함한 여러 태그 반영이다. 이들은 저장 성공을 만들 사전조건에 활용하지만 일반 Patch 기능을 여기서 중복 소유하지 않는다.

## 5. 보완 후보 stable ID
아래 ID는 이 문서의 고정 ID이다. API 이름이 아니라 동작을 기준으로 코딩한다. 기존 항목을 대체하지 않으며 기존 검증성질을 강화하거나 INTEG 공백을 메운다.

### HIST-N01 · 빈 이력 이동과 경계 연속 호출
- 입력: 아무 View도 저장하지 않은 이력, 그리고 A 1개인 이력.
- 사전상태: 각각 현재 없음과 현재 A.
- 동작: 뒤로 3회, 앞으로 3회 호출. A→B→C에서는 시작까지 뒤로 이동 후 추가 3회, 끝까지 앞으로 이동 후 추가 3회.
- 기대: 빈 상태는 개수0 및 이동불가 유지. 비어 있지 않은 경계는 해당 현재 유지. 반대 방향 유효 이동은 정상 작동하며 개수 보존. 경계 결과 null은 기존 hist-back-at-start/forward-at-end의 시트 기대에 맞춘다. 빈 상태 이동의 반환값은 D2 결정 뒤 고정한다.
- 필요성: hist-empty는 조회만 하고, 행64~65는 경계 호출 1회뿐이다. index의 음수화·범위 초과가 다음 호출에 남는 문제를 잡는다.
- 범위: UNIT. 결정의존: D1, D2.

### HIST-N02 · 여러 저장·이동에서 현재와 개수의 일치
- 입력: 내용이 뚜렷이 다른 A, B, C.
- 사전상태: 빈 이력.
- 동작: 순서대로 저장하고 뒤·앞을 B,A,B,C 순서로 이동.
- 기대: 저장 직후 현재는 각 저장값. 이동 반환과 현재 조회는 매번 동일 내용. 이동 중 개수는3. 시작과 끝의 가능 여부도 내용과 모순되지 않음.
- 필요성: hist-back/forward는2개만 사용한다. 내부 current index와 snapshots의 일치가 공개 출력에 나타나는지 검증한다.
- 범위: UNIT. 결정의존: D1. index와 snapshots를 테스트 때문에 공개하지 않는다. 공개 필드로 채택되면 추가로 직접 검사하되 내부 배열 구조를 필수화하지 않는다.

### HIST-N03 · 분기 뒤 과거 보존과 이전 redo 접근 차단
- 입력: A,B,C,D.
- 사전상태: A→B→C 저장 후 A로 이동.
- 동작: D 저장, 앞으로 이동 시도, 뒤로 이동, 다시 앞으로 이동.
- 기대: 현재 D, 개수2, 앞으로 불가. 이후 A→D만 이동 가능. B,C는 재등장하지 않음.
- 필요성: hist-push-truncates는 저장 직후 개수와 가능 여부만 명시하며 과거 A 유지와 실제 이동 결과를 함께 닫지 않는다.
- 범위: UNIT. 결정의존: D1,D2. redo 제거 정책 자체는 이미 시트명시이다.

### HIST-N04 · 중첩 참조 격리와 이동 반환 격리
- 입력: props와 2단계 children을 가진 A,B.
- 사전상태: A,B 저장.
- 동작: 원본 A/B의 props와 깊은 자식을 수정. 현재 조회 결과를 수정. 뒤로·앞으로 이동 결과도 수정한 뒤 동일 상태를 다시 조회·재방문.
- 기대: 저장 당시 손으로 적은 A/B 내용 유지. 단순 객체의 동일성은 요구하지 않음.
- 필요성: hist-isolation-input/output의 내용 수정이 얕은 필드만 검사할 수 있다. 이동 반환 경로가 현재 조회와 다른 alias를 노출하는 경우를 보완한다.
- 범위: UNIT. 결정의존: D1 및 D3의 이동 반환 격리 범위. 순환객체·함수·Date는 VNode 도메인 밖이므로 추가하지 않는다.

### HIST-N05 · 동일 내용 저장의 정책 고정
- 입력: 참조가 같은 A와 내용만 같은 새 A 객체, A→B에서 A로 이동한 상태.
- 사전상태: A 하나 및 redo가 있는 A 현재.
- 동작: 동일 내용 A를 다시 저장.
- 기대: D4 채택 전 미정. 대안① core는 호출마다 저장하여2개가 되고, redo 위치에서 저장하면 redo 제거. 대안② 같은 내용은 저장하지 않아 개수 유지, 이때 redo도 보존할지 별도 결정. 대안③ 참조 동일일 때만 생략은 내용 동일 객체와 결과가 갈려 별도 명시 필요.
- 필요성: 행80의 페이지 no-op은 명시됐지만 core 저장의 dedupe 계약은 없다. 필수 정책을 새로 강제하는 후보가 아니라 결정 뒤 회귀 테스트로 고정하는 후보이다.
- 범위: UNIT, 결정의존: D4. 무한 history limit 또는 임의 dedupe를 전제하지 않는다.

### HR-N01 · 초기 상태 저장과 첫 변경의 원자적 연결
- 입력: 초기 View A와 편집 View B.
- 사전상태: 페이지 초기화 전.
- 동작: 초기화 후 두 영역과 이력 조회, B 반영 완료 후 저장, 뒤로 이동.
- 기대: 초기 View A 1개, 양방향 불가. B 반영 뒤 현재 B이며 뒤로 A 복원. 실제 영역과 테스트 영역은 각각 A. 초기화·복원으로 같은 A가 중복 저장되지 않음.
- 필요성: 행72와83은 초기 이력1개를 이미 요구한다. 통합층에서 초기화 중복이나 첫 변경 후 처음 상태 유실을 잡는다.
- 범위: INTEG, FUNC 행72·76·83과 연결. 결정의존: D1,D5. 초기 저장 여부는 확정된 시트 기대이고, 구체적 저장 시점만 결정한다.

### HR-N02 · 재복원과 두 영역 및 현재 일치
- 입력: 텍스트·속성·중첩 자식이 다른 A,B,C.
- 사전상태: 초기 A 후 B,C 반영·저장.
- 동작: 뒤로 B, 뒤로 A, 앞으로 B, 앞으로 C를 2회 반복. 각 단계 두 영역을 VNode로 읽고 현재를 조회.
- 기대: 각 단계 세 결과가 손으로 적은 대상 View와 같음. 이동 때문에 개수는3에서 늘지 않음. B를 두 번 복원해도 이전 복원이 다음 복원값을 오염시키지 않음.
- 필요성: 행81~82는 한 번씩의 방향 이동이고 기존 int-roundtrip-sequence는 History가 없다. 복원 시 재저장, 한 영역만 갱신, 오래된 현재 View로 Diff하는 오류를 잡는다.
- 범위: INTEG. 결정의존: D1,D6. DOM 요소 identity 보존까지는 이 후보의 기대가 아님.

### HR-N03 · input 실시간 값 저장·복원
- 입력: input의 value 속성은 seed지만 .value는 typed인 A, 다음 저장값 B에서는 .value가 빈 문자열.
- 사전상태: ADR0005 범위의 텍스트 input, checkbox/radio 아님.
- 동작: A 캡처·저장, B 반영·저장, A로 뒤로, B로 앞으로 이동하고 두 영역의 input.value 확인.
- 기대: A에서는 typed, B에서는 빈 문자열. 현재 View.props.value도 각각 동일. 오래된 value 속성 seed나 innerHTML만으로 판정하지 않음.
- 필요성: 실시간 input 규칙은 ADR0005와 현 vnode 구현에 근거가 있다. History를 통과하면서 속성 문자열만 복원하면 눈에 보이는 값이 달라질 수 있다.
- 범위: INTEG. 결정의존: D1,D6. textarea/select/checked, focus, selection은 ADR 제외 범위이며 임의 추가하지 않는다.

### HR-N04 · 분기 후 저장·화면·redo 일치
- 입력: A,B,C와 새로운 D.
- 사전상태: A→B→C 저장 후 B 복원.
- 동작: D로 편집하고 유효 Patch 완료, 앞으로 이동 시도, 뒤로 B, 다시 앞으로 D.
- 기대: 실제 영역과 테스트 영역 및 현재가 D 또는 이동 대상과 일치. 이력은 A,B,D이고 C로 재진입 불가.
- 필요성: 행84와 hist-push-truncates가 각각 페이지와 core에서 말하는 분기를 실제 연결 경로로 검증한다.
- 범위: INTEG. 결정의존: D1,D6. 분기 제거 여부 자체는 시트에서 이미 결정됐다.

### HR-N05 · no-op 및 거절 편집의 저장 억제
- 입력: 초기 A, 그대로인 A, 빈 최상위 입력, 최상위2개 입력.
- 사전상태: 초기 또는 A→B→C의 B로 이동한 시점.
- 동작: 각각 Patch 처리 경로를 호출.
- 기대: 실제 변경 없는 A는 새 이력을 만들지 않음. 유효하지 않은 입력은 현재와 snapshots 및 실제 영역을 보존. redo가 있는 시점에서도 기존 가지를 실수로 자르지 않는 것을 권장 계약으로 채택할지 D7에서 결정.
- 필요성: 행80,85,86은 이미 no-op과 거절 시 이력 보존을 요구한다. 버튼 메시지는 이 테스트 소유가 아니며 이력 측면만 검증한다.
- 범위: INTEG. 결정의존: D7의 redo 보존과 no-op 비교 의미. 단순 현재/개수 보존은 기존 기대, redo 접근 유지까지는 보완 기대이다.

### HR-N06 · 미저장 편집 중 이동
- 입력: 저장 A→B→C에서 B 복원 후 테스트 영역만 X로 편집.
- 사전상태: 실제 B, 이력현재 B, 테스트 영역 X.
- 동작: 뒤로 또는 앞으로 이동.
- 기대: D8 전 미정. 대안① X를 버리고 대상 A/C를 두 영역에 복원. 대안② 이동 전에 명시적으로 X를 저장. 대안③ 이동을 거절하고 X를 유지. 부모 LMS 전달의 ‘이동하면 두 영역 변경’과 가장 단순하게 맞는 것은①이지만 확정하지 않음.
- 필요성: 행73은 Patch 전 실제 DOM 불변만 다루며 편집 후 이동의 계약은 다루지 않는다.
- 범위: INTEG. 결정의존: D8. 담당4의 실제 사용자 흐름 테스트에 같은 결정 전달 필요.

## 6. 결정필요와 영향

- D1 공개 API: 생성 형식, 저장·조회·이동의 실제 함수 또는 메서드명, null 표현, size와 가능여부의 필드/함수 형태. 현 시트의 이름은 설계 가정이다. 모든 UNIT·INTEG의 코딩 어댑터가 영향을 받는다. 테스트 전용 export는 금지.
- D2 경계 결과: 비어 있지 않은 시작/끝에서 null 및 현재유지는 시트명시이므로 별 이유 없이 다시 미정 처리하지 않는다. 빈 이력 이동도 null로 통일할지 시트가 명시하지 않은 반환만 결정. HIST-N01,N03 영향.
- D3 이동 반환의 참조 격리: 현재 조회 반환은 기존 시트가 격리 요구. 이동 결과도 밖에 주는 View라면 같은 격리를 권장한다. readonly/frozen을 택하면 외부 수정 시도 예외 또는 무시가 달라지므로 ‘저장 내용 보존’과 ‘수정 허용’을 분리. HIST-N04,HR-N02 영향.
- D4 동일 View 저장: 페이지 no-op 억제는 이미 확정, core dedupe는 미확정. core는 호출대로 저장하고 페이지에서 no-op을 거르는 편이 책임 분리가 단순하나 팀 결정 필요. HIST-N05와 분기 후 no-op의 redo 기대 영향.
- D5 초기 저장 시점: 페이지 처음 상태를1개 저장하는 것은 행72·83에 이미 근거. DOM 준비 후 초기 View 캡처·양쪽 반영 완료 지점 중 어느 시점을 기준으로 할지, 초기화 재호출 시 새 이력을 만들거나 같은 인스턴스를 재사용할지 정함. HR-N01 영향. 별도 reset API를 임의로 요구하지 않음.
- D6 복원 경로: 기존 Patch로 대상 View까지 갱신할지 DOM을 새로 그릴지 페이지가 결정. 이 담당의 기본 기대는 두 영역과 현재의 의미상 일치이며 복원 중 저장금지. ‘복원에서도 불변 노드 identity 유지’를 추가하려면 별도 요구 필요. HR-N02,N03,N04 영향.
- D7 no-op 비교와 redo: 정상 변경 후 같은 내용, 과거 위치에서 같은 내용, DOM은 달라도 캡처한 View가 같은 경우를 정의. 기존 행80은 페이지 최초 상태에서의 무변경만 명확하다. HR-N05와 담당4 확장 기대 영향.
- D8 미저장 편집 처리: 버림·자동저장·거절 중 선택. HR-N06과 담당4 흐름 영향. 경고창을 임의로 추가하지 않음.
- D9 capacity: hist-max-size는 선택. 구현하지 않으면 skip. 구현할 때 생성옵션과 기본 한도, 제거 후 현재 위치 일치까지 논의하되 본 Phase1 필수 목록에 임의 추가하지 않음.

## 7. 코딩 세션 실행 순서와 검증 경계

1. D1과 실제 export를 먼저 확인하고 의미상 테스트를 구현 API에 맞춘다. history.ts가 아직 없으므로 가짜 메서드명을 확정한 실행 테스트를 먼저 강요하지 않는다. CONVENTION에 따라 비어 있는 함수의 테스트는 skip 상태로 공통 테스트 PR에 둔다.
2. 기존 hist-* 기본·엣지9개를 기준으로 HIST-N01~N04를 보완한다. hist-max-size는 선택으로 분리한다. HIST-N05는 정책 결정 전 확정 assertion을 만들지 않는다.
3. History 공개 API가 생기면 테스트만을 위해 export를 추가하지 않고 초기화·Patch·복원 실제 연결 경로로 HR-N01~N05를 작성한다. 경로를 호출할 공개 entry가 없다면 페이지의 실제 초기화 경로 사용 또는 테스트 경계 설계가 먼저 필요하다. 가짜 orchestration을 테스트 안에서 새로 구현해 실제 페이지 통합을 검증했다고 보고하지 않는다.
4. 기대 View는 손으로 작성한다. 저장함수 출력으로 기대값을 만들지 않는다. 변환·Patch의 결과를 VNode로 다시 읽는 비교는 CONVENTION이 허용하지만 같은 잘못된 변환이 양쪽에 전파되지 않도록 고정 View와 .value 직접 assertion도 둔다.
5. History UNIT는 DOM을 만들지 않는다. HR INTEG는 Node+jsdom, 담당4 FUNC는 브라우저 클릭과 버튼·메시지 표시를 담당한다. current index와 snapshots는 논리적 불변식이며 비공개 필드를 캐스팅해서 검사하지 않는다.

## 8. 읽은 범위와 제한

직접 읽음: mini-react/CONVENTION.md, GLOSSARY.md, README.md, AGENTS.md, docs/adr/0001~0005, src/main.ts, src/vnode.ts, vitest.config.ts, src 파일 목록, lab/meeting-1110/plan.html의 History·테스트 구분 부분, lab/phase1-compare.html의 History 검색. Lark React Tests D/F/G/H/I의 History 행60~69, D/E/G/H/I의 INTEG 행50~59, D/G/H/I의 검증페이지 행70~86, README C/D/E 행4~8,12~15.

읽기법: 새 탭, snapshot 기반 이름상자 좌표 선택, Enter 후150~180ms 대기, 갱신 snapshot의 수식 textbox.textContent로 원문 수집. 캔버스 스크린샷은 행 배치 확인에만 사용했다. 소스와 시트는 수정하지 않았다. 조사 탭은 최종 보고 전에 닫았다.

제한: GitHub 원격 브랜치와 PR은 직접 조사하지 않았다. 로컬에 History가 없다는 사실을 원격 전체의 미구현으로 확장하지 않는다. 테스트 실행·코드 생성·Lark 수정은 하지 않았다. LMS 필수 내용은 부모의 직접확인 전달과 분리 표시했다.

### 최종 동시변경 보충 관찰
부모가 전달한 동시 작업을 계기로 src와 docs/adr 목록을 다시 읽었고 patch.ts, patch.test.ts와 ADR0006 추가를 확인했다. ADR0006 본문도 직접 읽었다. 이 문서가 정한 History 책임과 공개 API 미구현 판정은 바뀌지 않는다. Patch 세부 형식은 별도 담당 범위이며 기존 Lark 대비 충돌을 본 문서에서 임의로 해결하지 않았다. 코딩 세션은 구현 시작 시 실제 export와 최신 ADR을 다시 확인한다.
