# mini-react Phase 1 테스트 설계

관찰일: 2026-11-09, Asia/Seoul. 대상 프로젝트: week11-12/mini-react. 이 문서는 팀 확정 규칙을 새로 만드는 문서가 아니라, Lark 기존 테스트와 보완 후보를 연결한 코드 생성 전 설계다. 코드·Lark·GitHub를 변경하지 않았고 테스트를 실행하지 않았다.

## 1. 목표와 범위

함수 또는 기능의 책임을 1~2줄로 정의하고, 그 책임과 입력·상태·협력 관계에서 검증할 성질을 도출한다. 각 성질에 기존 사례와 정상·경계·연속 실행 조건을 대응시킨다. 기대가 미정이거나 자료가 충돌하면 결정표에 따로 남긴다.

- 기본 범위: M1 DOM↔VNode, M2 Diff, M3 Patch, M4 StateHistory와 검증 페이지.
- 실제 공개 협력 함수 isTextInput도 단위 대상에 추가했다. 처음 제시한12개는 고정 목록이 아니었다.
- Phase 1 key 확장 M9는 별도 부록. Phase 2 Component·hooks·이벤트 props·h key는 기본 목록 밖이다.
- 단위6개, 통합4개, 기능3개의 **상위 대상 묶음13개**, 검증 갈래57개다. History의 의미상 동작과 실제 메서드 수는 별개다.
- canonical Lark 재고91개: 변환22, Diff16, Patch11, 순수변환왕복1, Diff·Patch연결8, History10, 페이지23. 이 중 hist-max-size와 verify-back-partial/log/highlight 4개는 선택이므로 기본·엣지87개다.
- 별도 Phase 1 key 확장8개. 기본 재고91개는 시트2~92행을 누락·중복 없이 대응했다. 행98·99는 Phase 2,103부터 props 확장임을 경계 원문으로 추가 확인했다.최종 사이트의 Phase 1 검색99건이 기본구간91+key8과 일치했다. 이는 문자열 검색 대조이며177개 전체 문장을 정밀 검증한 것은 아니다.
- 보완·재사용 추적항목73개는 신규 실행 테스트73개가 아니다. 기존 T/P 테스트 재사용, assertion 보강, 기존 Lark 코드화, 정책 probe가 섞여 있다. 사례별 분할과 중복 제거 뒤 실제 실행 개수를 정한다.

## 2. 함께 사용할 산출물

- phase1-test-design.md: 대상 정의·성질·공통 결정·판정 기준.
- phase1-test-inventory.md: 기존 시트 행·ID·시나리오·기대, 로컬 T/P 매핑, 보완 후보 ID와 조건·이유·범위·결정의존.
- phase1-coding-handoff.md: 별도 코딩 세션에 전달할 실행 지침.
- 채팅의 visualize 도식: 아래13대상과57갈래를 같은 이름으로 탐색. 도식은 상세 oracle를 대신하지 않는다.

## 설계와 구현 상태를 구분하는 표기

- **Lark 기존**: 시트에 사례와 기대가 기록되어 있다. 코드가 존재하거나 테스트가 통과했다는 뜻은 아니다.
- **로컬 구현**: 관찰한 CJG 브랜치에 테스트 코드가 있다. 이번 설계 작업에서는 실행하지 않았다. 다른 브랜치 상태로 일반화하지 않는다.
- **추가 후보**: 기존 책임에서 새 조건이나 오류 검출 목적을 도출했다. 새 제품 정책을 승인한 것은 아니다.
- **결정 필요**: 기대 결과를 정할 계약이 없거나 자료가 충돌한다. 영향받는 사례를 연결하고, 관련 없는 사례까지 막지 않는다.
- **선택 확장**: Phase 1 key 확장 등 필수 범위와 별개다. Phase 2 hooks·컴포넌트·이벤트 비교는 본 기본 설계의 대상이 아니다.

## 테스트 레벨과 판정 방법

- **단위**: 해당 공개 함수나 객체의 책임을 직접 확인한다. 수동 fixture와 직접 쓴 기대값을 사용한다. applyPatchesToDom의 단위 테스트는 DOM을 사용해도 단위 테스트다.
- **통합**: 실제 협력 함수들을 연결하고 값·노드 위치·상태에 대한 해석이 맞는지 확인한다. 함수 호출 횟수 mock만으로 연결의 정확성을 대신하지 않는다.
- **기능**: Lark README의 FUNC 기준에 따라 실제 브라우저의 사용자 입력과 클릭, 화면 결과를 검증한다. jsdom의 UI 시뮬레이션은 보조 통합 검증으로 분리하고 실제 FUNC 완료로 세지 않는다.
- **구조**: 명시한 태그·속성·childNodes·textContent를 확인한다. isEqualNode만으로 입력의 현재 property나 노드 identity를 보장하지 않는다.
- **현재 상태**: input.value 같은 property를 직접 확인한다. getAttribute('value')는 초기/직렬화된 속성 확인과 구분한다.
- **변경 범위**: 변경 전 노드 참조와 변경 후 참조를 ===로 비교한다. 결과 화면만 같아도 전체 재생성한 구현은 이 검증을 통과하지 못해야 한다.
- **호출 독립성**: 연속 실행 전후 입력과 기존 반환값이 바뀌지 않는지 확인한다. 이것을 모든 반환 payload의 깊은 복사 요구로 확대하지 않는다.

## 충분함을 판단하는 기준

요구사항 → 대상 책임 → 검증 성질 → 입력·상태·실행 순서 → 사례 → 판정 방법의 연결을 남긴다. 대표 조건의 조합은 서로 다른 오류를 잡을 이유가 있을 때 추가한다. 모든 조건의 기계적 곱집합, 근거 없는 성능·무한깊이·모든 HTML 요소 지원을 완료 조건으로 삼지 않는다.


## 3. 테스트 대상 정의

### U-FROM · 단위 · createVNodeFromDom

지원하는 DOM을 합의된 VNode 표현으로 읽고, 입력 DOM은 변경하지 않는다.

- 입력: 현재 계약은 Element; 시트는 루트 Text·Comment도 가정
- 결과·상태: VNode; 루트 Comment의 null은 충돌 확인 필요
- 책임을 나누는 기준: DOM의 종류·속성·자식·글자·입력 상태를 읽되 원본은 보존

### U-TO · 단위 · createDomFromVNode

VNode의 구조와 값을 새 DOM으로 만들고 문자열을 HTML로 해석하지 않으며 입력 VNode를 보존한다.

- 입력: string 또는 요소 VNode
- 결과·상태: 새 Text 또는 Element
- 책임을 나누는 기준: VNode의 type·props·children을 새 DOM으로 표현

### U-INPUT · 단위 · isTextInput

reader와 Patch가 현재 value를 다룰 input 대상을 같은 규칙으로 분류한다.

- 입력: Element
- 결과·상태: boolean과 타입 가드
- 책임을 나누는 기준: 현재 value를 상태로 읽고 쓸 대상인지 분류

### U-DIFF · 단위 · diffViews

두 View의 차이를 Patch 목록으로 반환하고, 입력 View와 DOM은 바꾸지 않는다. 기본 비교는 key 없는 위치 비교다.

- 입력: 이전 View·새 View
- 결과·상태: Patch 목록
- 책임을 나누는 기준: 두 View의 차이를 판단하고 위치를 표현하되 입력은 보존

### U-PATCH · 단위 · applyPatchesToDom

합의된 Patch를 container 안의 View에 적용하고 변경 대상 밖의 노드와 container를 보존한다.

- 입력: container·Patch 목록
- 결과·상태: DOM과 live input 값 변경; 현재 반환 void
- 책임을 나누는 기준: 각 변경 지시를 올바른 노드에 적용하고 나머지는 유지

### U-HISTORY · 단위 · StateHistory

View의 저장 순서와 현재 위치를 관리하고 저장·조회·이동·격리의 약속을 지킨다.

- 입력: View와 저장·조회·이동 동작
- 결과·상태: 현재 View·이동 결과·개수·이동 가능 여부
- 책임을 나누는 기준: 저장된 View와 현재 위치를 일관되게 관리

### I-ROUND · 통합 · 변환 왕복

두 변환을 연결했을 때 지원하는 정규형의 구조와 현재 상태가 합의한 범위에서 보존된다.

- 입력: 정규형 VNode 또는 지원 DOM
- 결과·상태: 다시 읽은 VNode 또는 새 DOM
- 책임을 나누는 기준: 두 변환의 표현 약속이 서로 맞는지 확인

### I-DP · 통합 · Diff → Patch

이전 DOM에 두 View의 diff를 적용하면 목표 View의 상태가 되고 변경 없는 노드는 유지된다.

- 입력: old·new View와 old DOM
- 결과·상태: 목표 내용·참조·변경 범위
- 책임을 나누는 기준: 차이 지시의 생성자와 소비자가 같은 약속을 쓰는지 확인

### I-READDP · 통합 · DOM 읽기 → Diff → Patch

DOM에서 읽은 구조와 현재 입력값을 diff와 Patch가 같은 의미로 해석해 정확한 대상을 바꾼다.

- 입력: 실제 DOM에서 캡처한 old View·new View
- 결과·상태: 정확한 노드와 현재 상태의 갱신
- 책임을 나누는 기준: 읽기·비교·반영 사이의 데이터와 위치 계약 확인

### I-HR · 통합 · History → 화면 복원

반영한 View를 저장하고 선택한 이력을 두 영역에 복원하며 이력과 화면의 현재 상태를 일치시킨다.

- 입력: 실제 초기화·커밋·이동 경로
- 결과·상태: 현재 View·이력·두 영역 상태
- 책임을 나누는 기준: 저장과 복원의 협력 관계를 실제 경로로 검증

### F-INIT · 기능 · 최초 표시

페이지 로드 시 실제 영역의 샘플을 독립된 테스트 영역에 표시하고 초기 이력과 버튼을 준비한다.

- 입력: 실제 브라우저 페이지 로드
- 결과·상태: 두 영역·버튼·초기 상태
- 책임을 나누는 기준: 로드 동작 → 초기 화면·독립성·이력 준비

### F-PATCH · 기능 · Patch 버튼

현재 테스트 편집을 읽어 바뀐 부분만 실제 영역에 반영하고 유효한 새 View를 저장한다.

- 입력: 실제 브라우저 편집·Patch 클릭
- 결과·상태: 실제 영역·이력·버튼·안내
- 책임을 나누는 기준: 현재 편집을 검증한 뒤 부분 반영하고 저장

### F-NAV · 기능 · 뒤로가기·앞으로가기

선택한 저장 상태로 실제 영역과 테스트 영역을 함께 바꾸고 이동 가능 상태와 분기를 일치시킨다.

- 입력: 실제 브라우저 이동 버튼 클릭
- 결과·상태: 두 영역·이동 버튼·이력 재생 결과
- 책임을 나누는 기준: 이력 이동 → 두 화면 동기화·경계·분기

## 4. 대상에서 도출한 검증 갈래

### U-FROM · createVNodeFromDom

#### 1. 노드 표현과 입력 범위

- 검증할 성질: 빈 요소와 지원 노드 종류를 정해진 형태로 반환한다.
- 도출: DOM 노드 종류 → 지원 입력과 반환 형태
- 기존 근거: fromdom-elem · text · empty · tag-lowercase · comment-node
- 보완 조건: 루트 Text·Comment와 Element-only의 차이 명시
- 추적 후보: CONV-N021
- 결정과 범위: DEC-02: 시트의 Node 입력·null과 로컬 Element→VNode 충돌

#### 2. 속성의 존재와 값

- 검증할 성질: 여러 문자열 속성과 빈 값 속성을 빠뜨리지 않는다.
- 도출: attributes → 없음·하나·여럿·빈 값
- 기존 근거: fromdom-attrs · bool-attr
- 보완 조건: 기존 T7~T9 재사용; 명시 value 속성과 자동 property 추출 구분
- 추적 후보: 기존 재고의 사례·assertion 재사용
- 결정과 범위: 속성 순서는 검사하지 않음

#### 3. 자식 구조와 경계

- 검증할 성질: 중첩·순서·빈 요소와 합의한 Text 경계를 유지한다.
- 도출: childNodes → 깊이·형제·종류·빈 자리
- 기존 근거: fromdom-nested · mixed-children · empty · deep
- 보완 조건: 빈 자식 요소; 주석 양옆 Text 분리; 빈 Text 노드
- 추적 후보: CONV-N001, CONV-N003, CONV-N005, CONV-N022
- 결정과 범위: DEC-01·DEC-04: 공백·빈 Text와 경로 대응

#### 4. 글자와 공백 정책

- 검증할 성질: 엔티티가 해석된 글자를 읽고 합의한 공백 정책을 적용한다.
- 도출: Text.data → 일반 글자·공백-only·pre
- 기존 근거: fromdom-special-chars · skip-whitespace · keep-pre-space
- 보완 조건: 앞뒤 공백과 공백-only 구분; inline 사이 한 칸과 들여쓰기 구분
- 추적 후보: CONV-N004, CONV-N006, CONV-N022
- 결정과 범위: DEC-01: Lark 공백 제거와 로컬 보존 충돌

#### 5. 주석 제외

- 검증할 성질: 주석은 VNode에서 제외하되 입력 DOM에서는 지우지 않는다.
- 도출: 주석 제외 → VNode 표현과 원본 보존 분리
- 기존 근거: fromdom-skip-comment
- 보완 조건: 여러 깊이·여러 주석; 원본 주석 참조 유지
- 추적 후보: CONV-N002, CONV-N013
- 결정과 범위: 루트 Comment 반환은 DEC-02로 분리

#### 6. 현재 입력값

- 검증할 성질: 초기 속성이 아니라 입력칸의 현재 value를 읽는다.
- 도출: attribute와 property 차이 → 초기·입력·지움
- 기존 근거: Lark reader 현재값 직접 사례 없음; 로컬 T16~T21 있음
- 보완 조건: 초기값·속성 없는 타이핑·속성과 현재값 충돌; 모두 지움·빈 입력칸·비입력 요소 제외
- 추적 후보: CONV-N007, CONV-N008, CONV-N009, CONV-N010, CONV-N011, CONV-N012
- 결정과 범위: DEC-03: 입력 대상과 빈 value 정규형의 팀 채택 확인

#### 7. 입력 DOM 보존

- 검증할 성질: 읽기 전후 구조·참조·현재 입력값을 바꾸지 않는다.
- 도출: 읽기 책임 → outerHTML 밖의 상태도 보존
- 기존 근거: fromdom-no-mutate · 로컬 T5
- 보완 조건: child 참조·Text.data·주석·input.value 전후 확인
- 추적 후보: CONV-N013
- 결정과 범위: outerHTML만으로 참조·현재값 불변을 보장하지 않음

### U-TO · createDomFromVNode

#### 1. 노드 생성

- 검증할 성질: 문자열은 Text, 요소는 해당 태그의 새 노드로 만든다.
- 도출: VNode 종류 → DOM 노드 종류
- 기존 근거: todom-elem · text
- 보완 조건: 같은 입력으로 두 번 만든 결과의 참조 독립성
- 추적 후보: CONV-N020
- 결정과 범위: reader의 루트 입력과 별개

#### 2. 속성 반영

- 검증할 성질: 속성값뿐 아니라 빈 속성의 존재도 반영한다.
- 도출: props → attribute 존재와 값
- 기존 근거: todom-attrs
- 보완 조건: hidden 등 빈 문자열 속성
- 추적 후보: CONV-N014
- 결정과 범위: 문자열 props 기본 범위

#### 3. 자식 구조와 순서

- 검증할 성질: 중첩·혼합·빈 자식을 적힌 순서대로 만든다.
- 도출: children → nodeType·개수·순서
- 기존 근거: todom-nested
- 보완 조건: mixed children·빈 요소; 공백 Text·빈 Text
- 추적 후보: CONV-N015, CONV-N016, CONV-N017
- 결정과 범위: DEC-01·DEC-04와 reader 정규화는 분리

#### 4. 문자열은 글자

- 검증할 성질: HTML 모양과 엔티티 표기도 문자열 그대로 만든다.
- 도출: 문자열 VNode → Text 하나
- 기존 근거: todom-text-escape
- 보완 조건: 앞뒤 공백·&amp;·태그 모양을 함께 검증
- 추적 후보: CONV-N018
- 결정과 범위: 스크립트 실행을 유도하지 않고 노드 종류로 검증

#### 5. 입력 표시값

- 검증할 성질: props.value가 새 입력칸의 현재 value로 보인다.
- 도출: input VNode → input.value
- 기존 근거: todom-value-prop · 로컬 T33
- 보완 조건: 새 input과 이미 타이핑한 input 갱신은 구분
- 추적 후보: 기존 재고의 사례·assertion 재사용
- 결정과 범위: dirty input 갱신은 U-PATCH의 책임

#### 6. 입력 보존과 새 결과

- 검증할 성질: VNode를 바꾸지 않고 서로 독립된 새 DOM을 반환한다.
- 도출: create 책임 → 입력 비변경·결과 독립
- 기존 근거: todom-no-mutate
- 보완 조건: 중첩 props·children 보존; 한 결과 수정이 다른 결과나 입력을 바꾸지 않음
- 추적 후보: CONV-N019, CONV-N020
- 결정과 범위: Patch의 기존 노드 보존과 반대되는 책임

### U-INPUT · isTextInput

#### 1. 기본 입력칸

- 검증할 성질: 기본 input과 text input을 포함한다.
- 도출: 입력 요소 → 현재값 적용 대상
- 기존 근거: 직접 대응 Lark 사례 없음. 현재 공개 협력 책임에서 도출.
- 보완 조건: 기본 input·type=text → true
- 추적 후보: U-INPUT-N001
- 결정과 범위: 모든 input subtype 지원으로 확대하지 않음

#### 2. checked 계열 제외

- 검증할 성질: checkbox와 radio를 value 상태 대상으로 오인하지 않는다.
- 도출: 현재 상태가 checked인 요소 → 제외
- 기존 근거: 직접 대응 Lark 사례 없음. 현재 공개 협력 책임에서 도출.
- 보완 조건: checkbox·radio → false
- 추적 후보: U-INPUT-N002
- 결정과 범위: 해당 컨트롤의 상태 복원을 구현하는 테스트 아님

#### 3. 비입력 요소 제외

- 검증할 성질: value를 가진 li·button을 입력칸으로 오인하지 않는다.
- 도출: property 존재와 입력 역할은 별개
- 기존 근거: 직접 대응 Lark 사례 없음. 현재 공개 협력 책임에서 도출.
- 보완 조건: li·button → false
- 추적 후보: U-INPUT-N003
- 결정과 범위: 생산 코드가 공개해 사용하는 helper; 테스트만을 위한 export 아님

### U-DIFF · diffViews

#### 1. 변경 없음

- 검증할 성질: 내용이 같으면 참조나 속성 순서가 달라도 Patch가 없다.
- 도출: 내용 비교 → 동등함과 참조 동일성 구별
- 기존 근거: diff-same
- 보완 조건: 동일 참조·별도 동일 객체·속성 나열 순서
- 추적 후보: DIFF-N01
- 결정과 범위: 전체 최적화나 전역 최소 Patch 수를 강제하지 않음

#### 2. 노드 종류와 태그

- 검증할 성질: 종류·태그가 바뀌면 해당 범위만 교체하고 자손 변경을 중복 생성하지 않는다.
- 도출: VNode 종류와 type → 유지 또는 교체
- 기존 근거: diff-tag; diff-text-to-elem
- 보완 조건: 요소→문자열; 자손도 달라진 subtree 교체
- 추적 후보: DIFF-N02
- 결정과 범위: DEC-05: CREATE와 INSERT 및 현재 로컬안 승인 추적

#### 3. 문자열 내용

- 검증할 성질: 빈 글자와 공백을 포함한 새 문자열을 정확히 전달한다.
- 도출: 문자열 VNode → 내용 차이
- 기존 근거: diff-text
- 보완 조건: 일반↔빈 글자·빈 글자 유지; 공백·줄바꿈·한글·특수문자
- 추적 후보: DIFF-N03
- 결정과 범위: DOM 읽기 정규화와 diff의 문자열 비교를 혼동하지 않음

#### 4. 속성의 존재와 값

- 검증할 성질: 속성 없음과 빈 값을 구분하고 추가·변경·삭제를 빠뜨리지 않는다.
- 도출: props의 키와 값 → 설정 또는 삭제
- 기존 근거: diff-attr-add; diff-attr-change; diff-attr-remove
- 보완 조건: 빈 문자열 설정·유지·삭제; 속성 여러 개의 혼합 변경; value 변경·지움·빈 값 유지
- 추적 후보: DIFF-N04, DIFF-N06
- 결정과 범위: DEC-03: live value의 빈 값 정규형; Phase 2 props 제외

#### 5. 자식 개수와 위치

- 검증할 성질: 자식의 추가·삭제와 남은 위치의 변경을 함께 찾는다.
- 도출: children 순서와 길이 → 위치별 비교
- 기존 근거: diff-child-add; diff-child-remove; diff-child-insert-middle; diff-remove-all; diff-from-empty
- 보완 조건: 맨 앞 삽입·각 위치 삭제; 남은 자식 변경과 끝 삭제 혼합
- 추적 후보: DIFF-N05
- 결정과 범위: 현재 로컬안: 같은 위치 비교→INSERT 정순→REMOVE 역순; key는 별도

#### 6. 중첩 위치와 변경 조합

- 검증할 성질: 여러 가지의 변경을 충돌 없는 정확한 경로에 표현한다.
- 도출: 재귀 비교 → 경로와 batch 순서
- 기존 근거: diff-deep; diff-multi
- 보완 조건: 구조 변경과 다른 가지 내용 변경; 부모 속성과 자식 변경; 경로 배열 공유로 덮어쓰기 방지
- 추적 후보: DIFF-N05
- 결정과 범위: DEC-05: 현재 로컬안은 앞 Patch 적용 뒤 트리 기준

#### 7. 입력 보존과 호출 독립성

- 검증할 성질: 입력을 바꾸지 않고 호출 사이에 결과가 섞이지 않는다.
- 도출: 비교 결과만 반환 → 입력과 호출 영향 제한
- 기존 근거: diff-no-mutate; diff-invalid-arg
- 보완 조건: 중첩·공유 참조 불변; A→B 뒤 A→C, 이전 결과 불변; null·undefined는 인자별 대표 오류
- 추적 후보: DIFF-N07, DIFF-N08
- 결정과 범위: 잘못된 모든 객체 형태를 지원 요구로 확대하지 않음

### U-PATCH · applyPatchesToDom

#### 1. 변경 범위와 노드 보존

- 검증할 성질: TEXT·PROPS는 대상과 이웃의 필요한 참조를 유지한다.
- 도출: 부분 갱신 → 내용뿐 아니라 Node identity
- 기존 근거: patch-text; patch-props-set; patch-mutation-count
- 보완 조건: Text·부모·형제 ref; MutationRecord.target 확인
- 추적 후보: PATCH-N04
- 결정과 범위: 기존 P2·P10~P14를 보강하고 중복 생성하지 않음

#### 2. 구조와 루트

- 검증할 성질: 삽입·삭제·교체는 정확한 구조를 만들고 container는 유지한다.
- 도출: Patch 종류 → 구조 변화와 유지 범위
- 기존 근거: patch-replace; patch-create; patch-remove; patch-view-replace
- 보완 조건: 교체 역방향·중첩 생성; 순차 삭제 뒤 새 위치 갱신의 참조 보강
- 추적 후보: PATCH-N06
- 결정과 범위: DEC-05: Lark CREATE와 로컬 INSERT; root []는 로컬안에서 View

#### 3. VNode와 DOM의 위치 대응

- 검증할 성질: 주석을 제외하고 합의한 Text 노드를 세어 의도한 대상을 수정한다.
- 도출: VNode children 번호 → 실제 childNodes 대응
- 기존 근거: 현재 로컬 P17·P18·P19
- 보완 조건: 주석 앞뒤의 Text·빈 Text; 공백·주석 혼합에서 ref 보존
- 추적 후보: PATCH-N01, PATCH-N02
- 결정과 범위: DEC-01·DEC-04: Lark 공백 제거와 로컬 보존의 정합성

#### 4. 글자·속성·현재 입력값

- 검증할 성질: 글자는 HTML이 아니며 빈 속성과 live 빈 입력값을 구분해 반영한다.
- 도출: TEXT·PROPS → Text.data·attribute·property
- 기존 근거: patch-props-remove; patch-value-prop; 현재 로컬 P2·P23·P24
- 보완 조건: dirty input을 빈 값으로; 빈 속성 설정과 삭제; 빈 PROPS의 허용 범위
- 추적 후보: PATCH-N03, PATCH-N04, PATCH-N05
- 결정과 범위: remove.value는 현재 로컬안에서 attribute만 삭제; 표시값 초기화로 확대 금지

#### 5. 무변경·순차 적용·실패

- 검증할 성질: 빈 batch는 무변경이고 순차 적용과 실패는 정해진 약속을 따른다.
- 도출: 목록 처리 → 순서·불변·오류 경계
- 기존 근거: patch-empty; patch-invalid-path; 현재 로컬 P25~P28
- 보완 조건: PROPS가 Text를 가리키는 오류; INSERT 위치 오류 대표; 동일 batch 재적용은 별도 정책 probe
- 추적 후보: PATCH-N05, PATCH-N07, PATCH-N08
- 결정과 범위: DEC-05·DEC-13: 현재 로컬안은 noRollback; 멱등성을 임의 요구하지 않음

### U-HISTORY · StateHistory

#### 1. 초기와 현재 조회

- 검증할 성질: 빈 상태와 첫 저장 후의 현재·개수·이동 가능 여부가 일치한다.
- 도출: 저장 집합과 현재 위치 → 공개 조회
- 기존 근거: hist-empty · push-one
- 보완 조건: 빈 이력에서 이동을 반복
- 추적 후보: HIST-N01
- 결정과 범위: DEC-06: 실제 API와 빈 상태 이동 반환 확인

#### 2. 이동과 경계

- 검증할 성질: 앞뒤 이동은 정확한 View를 선택하고 경계에서는 현재를 유지한다.
- 도출: 순서 있는 이력 → 이전·다음·범위 경계
- 기존 근거: hist-back · forward · back-at-start · forward-at-end
- 보완 조건: A·B·C 반복 이동; 경계 초과 연속 호출 후 유효 이동
- 추적 후보: HIST-N01, HIST-N02
- 결정과 범위: 시트의 비어 있지 않은 경계 null은 기존 기대

#### 3. 새 저장과 분기

- 검증할 성질: 과거에서 새 View를 저장하면 redo를 버리고 과거 prefix를 보존한다.
- 도출: 현재 위치에서 저장 → 새 가지
- 기존 근거: hist-push-truncates
- 보완 조건: 분기 후 실제로 A↔D만 재방문
- 추적 후보: HIST-N03, HIST-N05
- 결정과 범위: 분기 정책은 기존; core 동일값 저장은 DEC-07

#### 4. 스냅샷 격리

- 검증할 성질: 원본과 조회 결과를 수정해도 저장 당시 내용은 유지된다.
- 도출: View 참조의 입출력 → 외부 변경 차단
- 기존 근거: hist-isolation-input · isolation-output
- 보완 조건: 중첩 props·children 격리; back·forward 반환값의 격리
- 추적 후보: HIST-N04
- 결정과 범위: DEC-08: 이동 반환의 보호 방식; 깊은 복사 구현을 강제하지 않음

#### 5. 선택: 용량 제한

- 검증할 성질: 선택한 상한을 넘으면 오래된 이력부터 제거한다.
- 도출: 선택 capacity → 보관 범위
- 기존 근거: hist-max-size · 선택
- 보완 조건: 선택 구현 시 이동 위치와 개수 함께 확인
- 추적 후보: 기존 재고의 사례·assertion 재사용
- 결정과 범위: 미구현이면 선택 제외; 필수 완료를 막지 않음

### I-ROUND · 변환 왕복

#### 1. VNode→DOM→VNode

- 검증할 성질: 정규형 VNode를 만들고 다시 읽으면 같은 내용을 얻는다.
- 도출: 두 변환 합성 → 표현 정합성
- 기존 근거: int-render-roundtrip
- 보완 조건: mixed children·속성의 대표 정규형
- 추적 후보: ROUND-N001
- 결정과 범위: 루트 문자열과 input value 정규형은 DEC-02·03 확인

#### 2. DOM→VNode→DOM

- 검증할 성질: 지원 DOM의 구조와 글자가 합의한 정규화 후 보존된다.
- 도출: 반대 방향 합성 → 구조 보존
- 기존 근거: 로컬 T34·T35·T36
- 보완 조건: 빈 요소·한글 mixed·엔티티
- 추적 후보: ROUND-N002, ROUND-N003
- 결정과 범위: Lark 51행과 반대 방향; 원본 Node identity 보존 요구 아님

#### 3. 입력 상태와 의도적 정보손실

- 검증할 성질: 현재 입력값은 보존하고 주석·정규화 예외는 명시적으로 검사한다.
- 도출: 합성의 보존 범위 → equality 예외
- 기존 근거: 로컬 T37
- 보완 조건: 현재 value와 지운 값 직접 검사; 빈 input 정규형 안정; 주석 제외와 원본 주석 보존
- 추적 후보: ROUND-N004, ROUND-N005, ROUND-N006
- 결정과 범위: DEC-01~04: isEqualNode 하나로 현재값을 보장하지 않음

### I-DP · Diff → Patch

#### 1. 목표 상태 도달

- 검증할 성질: 텍스트·속성·자식·교체를 연결했을 때 목표 구조가 된다.
- 도출: diff 결과 → 실제 Patch 반영
- 기존 근거: int-roundtrip-text; int-roundtrip-attr; int-roundtrip-children; int-roundtrip-replace; int-roundtrip-view-replace
- 보완 조건: subtree 교체와 바깥 보존; 여러 종류 변경을 섞은 회귀
- 추적 후보: DP-N02, DP-N04
- 결정과 범위: 기대 구조는 직접 작성; readback만을 유일한 oracle로 쓰지 않음

#### 2. 불필요한 변경 없음

- 검증할 성질: no-op과 국소 변경에서 바꾸지 않을 Node는 그대로 남는다.
- 도출: 목표 내용 외의 보장 → identity·mutation
- 기존 근거: int-preserve-identity
- 보완 조건: 동일 내용의 별도 객체 no-op; Element·Text refs와 observer 0
- 추적 후보: DP-N01, DP-N02
- 결정과 범위: 단위 검사 성공을 연결 보장으로 대신하지 않음

#### 3. 연속 변경과 재현성

- 검증할 성질: 매 단계 새 diff를 계산해도 내용·live 값·보존 범위가 맞는다.
- 도출: 반복 사용 → 기준 View 갱신과 오류 재현
- 기존 근거: int-roundtrip-sequence; int-roundtrip-fuzz
- 보완 조건: 기존 고정 seed 500쌍 유지; 빈 글자·value·구조 변화 대표 보강
- 추적 후보: DP-N06
- 결정과 범위: 같은 batch 재적용과 다른 요구; 모든 edge의 곱집합은 아님

### I-READDP · DOM 읽기 → Diff → Patch

#### 1. 주석·공백·빈 Text의 경로

- 검증할 성질: reader가 만든 children 번호와 Patch의 노드 탐색이 일치한다.
- 도출: 정규화 → VNode 번호 → 실제 DOM 위치
- 기존 근거: 연결 52~59를 바탕으로 보완
- 보완 조건: DOM API로 빈 Text·공백·주석·분리 Text 구성; 의도한 span만 갱신하고 주변 ref 유지
- 추적 후보: DP-N05
- 결정과 범위: DEC-01·04: 공백 제거와 보존 충돌부터 연결

#### 2. live value의 빈 값

- 검증할 성질: 현재 value를 읽고 비교해 지운 빈 값까지 같은 input에 반영한다.
- 도출: property 읽기 → value Patch → property 쓰기
- 기존 근거: patch-value-prop는 단위 근거
- 보완 조건: attribute는 initial, 현재는 typed; 빈 값 갱신 뒤 readback와 input.value 직접 검사
- 추적 후보: DP-N03
- 결정과 범위: DEC-03: value 정규형; attribute 동일성은 강제하지 않음

### I-HR · History → 화면 복원

#### 1. 초기 저장과 커밋 연결

- 검증할 성질: 처음 상태를 한 번 저장하고 첫 변경 뒤에도 처음으로 돌아갈 수 있다.
- 도출: 초기화·반영·저장 → 첫 상태 보존
- 기존 근거: verify-load-buttons; verify-patch-history; verify-back-to-start
- 보완 조건: 초기화 중복 저장 방지; 첫 변경 뒤 뒤로 초기값 복원
- 추적 후보: HR-N01
- 결정과 범위: 시트의 초기 이력 1개는 이미 명시; 실제 API만 확인

#### 2. 두 영역과 현재의 일치

- 검증할 성질: 앞뒤 이동을 반복해도 두 화면과 현재 View가 선택 상태와 같다.
- 도출: 이력 선택 → 두 영역 복원
- 기존 근거: verify-back; verify-forward
- 보완 조건: A·B·C 반복 재생; 현재 input.value와 지운 값; 이동 때문에 저장 수 증가하지 않음
- 추적 후보: HR-N02, HR-N03
- 결정과 범위: History 부분 갱신은 선택; 전체 재생성도 기본 결과 요구를 충족 가능

#### 3. 분기·no-op·거절 입력

- 검증할 성질: 새 분기는 redo를 버리고 no-op과 거절 입력은 저장을 만들지 않는다.
- 도출: 커밋 가능 여부 → 저장·redo 관계
- 기존 근거: verify-back-then-patch; verify-patch-nochange; verify-empty-input; verify-multi-top
- 보완 조건: 분기 뒤 B↔D 재생; 되돌린 위치 no-op의 redo; 미저장 편집 후 이동
- 추적 후보: HR-N04, HR-N05, HR-N06
- 결정과 범위: 거절 입력은 redo까지 보존하는 기존 기대. DEC-07·09는 core dedupe와 정상 과거 no-op, DEC-10은 미저장 편집만 적용

### F-INIT · 최초 표시

#### 1. 필수 UI와 초기 내용

- 검증할 성질: 두 영역과 세 버튼이 있고 두 영역의 View가 초기 기대와 같다.
- 도출: 페이지 준비 → 관찰 가능한 UI
- 기존 근거: verify-layout; verify-load
- 보완 조건: 직접 적은 초기 내용도 확인
- 추적 후보: 기존 재고의 사례·assertion 재사용
- 결정과 범위: 실제 selector와 편집 UI는 DEC-11 확인

#### 2. 복사 독립성과 미적용 편집

- 검증할 성질: 테스트 영역만 편집해도 실제 영역과 저장 상태는 바뀌지 않는다.
- 도출: 독립된 편집 사본 → 참조 비공유
- 기존 근거: verify-edit-no-apply
- 보완 조건: 대응 Node 비공유 또는 편집 모델에 맞는 격리 확인
- 추적 후보: PAGE-N01
- 결정과 범위: 편집 UI가 HTML 문자열 컨트롤이면 해당 모델로 조정

#### 3. 초기 이력과 버튼

- 검증할 성질: 초기 기록 하나에서 양방향 이동 버튼은 비활성이다.
- 도출: 저장된 첫 상태 → 이동 가능 여부
- 기존 근거: verify-load-buttons
- 보완 조건: 첫 Patch 뒤 한 번만 뒤로가서 초기 상태 확인
- 추적 후보: HR-N01
- 결정과 범위: 기본 기대는 기존 시트에 명시

### F-PATCH · Patch 버튼

#### 1. 현재 편집과 반복 반영

- 검증할 성질: 매번 현재 테스트 상태를 읽어 글자·속성·구조를 반영한다.
- 도출: 입력·클릭 → 읽기·비교·반영
- 기존 근거: verify-patch-apply; verify-attr-edit; verify-delete-node; verify-many-tags
- 보완 조건: 혼합 구조 A→B→C; 브라우저의 보정 구조와 실제 표시
- 추적 후보: FLOW-N01, PAGE-N04
- 결정과 범위: 기대 결과는 양쪽이 같다는 것 외에 직접 지정

#### 2. 부분 갱신과 no-op

- 검증할 성질: 한 곳 변경은 그곳만 바꾸고 무변경은 DOM과 이력을 유지한다.
- 도출: 변경 유무 → 실제 갱신 범위
- 기존 근거: verify-patch-partial; verify-patch-nochange
- 보완 조건: no-op 반복 뒤 B 커밋과 한 번의 뒤로 이동; 실제 영역 refs와 mutation 확인
- 추적 후보: PAGE-N02
- 결정과 범위: observer 범위는 실제 영역으로 제한

#### 3. 반영과 이력 저장

- 검증할 성질: 변경 완료 후 그 상태를 복원 가능한 새 이력으로 만든다.
- 도출: 커밋 완료 → 저장과 버튼 갱신
- 기존 근거: verify-patch-history
- 보완 조건: 저장 뒤 여러 번 편집해도 과거 스냅샷 유지
- 추적 후보: FLOW-N02
- 결정과 범위: 미저장 편집 이동은 DEC-10

#### 4. 유효성·브라우저 파싱·안전

- 검증할 성질: 빈 입력과 다중 루트는 거절하고 보정 HTML과 정제 결과는 시트 기대를 따른다.
- 도출: 사용자 HTML → 검사·파싱·정제 → 반영
- 기존 근거: verify-empty-input; verify-multi-top; verify-invalid-html; verify-no-script-exec
- 보완 조건: 거절 뒤 상태·이력 유지; script 요소와 onerror 제거를 직접 확인
- 추적 후보: PAGE-N04
- 결정과 범위: DEC-11·12: 안전한 입력 경로·정제 책임; 변환 Text escape만으로 대체 불가

#### 5. 실제 입력과 조합

- 검증할 성질: 실제 입력의 완성값이 Patch와 이력 이동 후에도 맞게 나타난다.
- 도출: 브라우저 키 입력 → 현재값 캡처
- 기존 근거: 기존 단위 값 대입은 브라우저 입력 증거 아님
- 보완 조건: text input 실제 typing; 지원 도구 또는 수동 IME 완료값 확인
- 추적 후보: PAGE-N03
- 결정과 범위: DEC-14: IME·조합 중 Patch·focus/caret 범위; 합성 event를 OS IME 증거로 세지 않음

#### 6. 빠른 조작의 재현성

- 검증할 성질: 정해진 빠른 조작열 뒤 두 영역과 기대 최종 상태가 맞고 오류가 없다.
- 도출: 연속 이벤트 → 완료 순서와 상태 일관성
- 기존 근거: verify-rapid-click
- 보완 조건: B Patch→뒤→앞→뒤→D Patch→앞
- 추적 후보: FLOW-N05
- 결정과 범위: 성능 시간 제한이나 비동기 정책을 임의 추가하지 않음

### F-NAV · 뒤로가기·앞으로가기

#### 1. 두 영역 동기화

- 검증할 성질: 뒤로와 앞으로 이동하면 두 영역이 해당 저장 상태를 보여준다.
- 도출: 이력 선택 → 사용자 화면 결과
- 기존 근거: verify-back; verify-forward
- 보완 조건: 반복 재생·현재 입력값; 저장 후 편집이 과거를 오염시키지 않음
- 추적 후보: HR-N02, HR-N03, FLOW-N02
- 결정과 범위: 기본 History 복원에 Node identity 유지까지 강제하지 않음

#### 2. 시작·끝과 버튼

- 검증할 성질: 처음까지 돌아갈 수 있고 시작·끝 버튼 상태가 이동 가능 여부와 맞다.
- 도출: 현재 위치 → 경계와 UI
- 기존 근거: verify-load-buttons; verify-back-to-start; verify-forward
- 보완 조건: 반복 경계 조작 뒤 유효 이동
- 추적 후보: 기존 재고의 사례·assertion 재사용
- 결정과 범위: 빈 History의 core 반환과 페이지 초기 상태는 구분

#### 3. 분기 후 재생

- 검증할 성질: 과거에서 새 변경을 반영하면 예전 redo는 재등장하지 않는다.
- 도출: 뒤로 이동 후 커밋 → 새 가지
- 기존 근거: verify-back-then-patch
- 보완 조건: A→B→C→뒤B→D 뒤 A·B·D만 재생
- 추적 후보: FLOW-N03, FLOW-N04
- 결정과 범위: 현재 B에서 무변경 Patch의 redo는 DEC-09

#### 4. 미저장 편집과 선택 복원

- 검증할 성질: 미저장 편집 후 이동의 결과는 합의된 정책으로 고정한다.
- 도출: 편집 중 이동 → 버림·저장·거절의 정책
- 기존 근거: 직접 대응 Lark 사례 없음. 현재 공개 협력 책임에서 도출.
- 보완 조건: 미저장 X 상태에서 뒤로·앞으로 각각
- 추적 후보: HR-N06, FLOW-N02
- 결정과 범위: DEC-10; 부분 복원·로그·강조는 선택 90~92

## 5. 공통 결정과 구현 확인 목록

새로운 정책을 정할 질문과, 이미 시트에 있는 기대의 구현/API를 확인할 작업을 구분한다. 기존 no-op 저장 억제, 초기 이력1개, 분기 절단, 경계 null, 오류안내, 안전정제 자체는 시트 명시다. 로컬 ADR의 proposed 표시는 제안 지위이며 코드·테스트 존재나 mtime만으로 승인·병합을 추론하지 않는다.

### DEC-01 · 공백-only 정규화

- 상태: 자료 충돌
- 확인한 사실: Lark fromdom-skip-whitespace(9)는 공백-only 제거, keep-pre-space(10)는 pre 보존. 현재 로컬 ADR0005·T13 및 Patch P19는 공백 보존·번호 포함.
- 영향 범위: U-FROM의 공백·pre·빈 Text, I-ROUND, PATCH-N02, DP-N05와 페이지 readback.
- 처리: 기존 기대를 보존한 채 한 정규화·인덱스 계약으로 맞춘다. 들여쓰기와 inline 사이 한 칸을 같은 것으로 취급하지 않는다.

### DEC-02 · reader 루트 입력과 null 반환

- 상태: 자료 충돌
- 확인한 사실: Lark 3은 루트 Text→string, 12는 루트 Comment→null. 현재 createVNodeFromDom은 Element→VNode.
- 영향 범위: fromdom-text, fromdom-comment-node, CONV-N021, 문자열 루트의 VNode 왕복.
- 처리: Node 입력·null 반환으로 넓힐지, 시트의 입력을 child 사례로 조정할지 근거 확인. 캐스팅으로 타입 충돌을 숨기지 않는다.

### DEC-03 · 현재 input.value와 빈 값 정규형

- 상태: 로컬 제안 채택 확인
- 확인한 사실: Lark todom-value-prop는 현재 표시값을 요구. 로컬 ADR0005·reader T16~21·Patch P23/24는 text input 현재값·빈 value 키 유지와 .value 쓰기를 구체화.
- 영향 범위: CONV-N007~012, ROUND-N004~005, DIFF-N06, PATCH-N03, DP-N03, HR-N03.
- 처리: 현재값·입력 대상 범위·빈값 정규형의 채택 근거를 확인한다. checkbox/radio/textarea/select 지원으로 확대하지 않는다. remove.value는 현재 로컬에서 속성 삭제일 뿐 표시값 초기화가 아니다.

### DEC-04 · Text 경계·빈 Text·주석과 위치 대응

- 상태: 정합성 확인
- 확인한 사실: 로컬은 한 Text당 한 문자열, 빈 Text와 공백 포함, 주석 제외. Lark는 child 주석 제외를 명시하나 Text 경계와 빈 Text는 직접 기대가 없다.
- 영향 범위: CONV-N003/005/017, ROUND-N006, PATCH-N01/02, DP-N05.
- 처리: reader와 Patch가 같은 노드를 세도록 정한다. root 또는 subtree 교체에도 모든 주석을 보존하라는 새 요구는 추가하지 않는다.

### DEC-05 · Patch 형식·path·순서·실패의 현재안

- 상태: 로컬 구체안과 시트 차이
- 확인한 사실: Lark는 CREATE, 로컬 ADR0006 proposed와 구현·P1~28은 INSERT. 현재안은 []=View, 앞 Patch 적용 후 트리, 받은 순서, 비교→INSERT 정순→REMOVE 역순, Error의 앞 변경은 rollback하지 않음. 원격 #13은 질문 상태.
- 영향 범위: diff·patch의 구체 기대와 새 테스트 adapter. 스키마 부재로 모든 작업을 막지는 않음.
- 처리: 현재안의 승인·적용 브랜치를 확인하고 CREATE↔INSERT 차이를 명시적으로 처리한다. 입력과 기대를 몰래 자동변환해 호환된 것처럼 보고하지 않는다. 과거 문구를 현재 금지규칙으로 사용하지 않는다.

### DEC-06 · History 실제 API와 빈 상태 이동

- 상태: 구현 표면 확인
- 확인한 사실: Lark는 push/current/back/forward/canBack/canForward/size 표기를 사용. 빈 current=null, 시작·끝 이동=null과 현재 유지, 초기 페이지 이력 1개는 이미 명시. 로컬 History API는 조사 시 미구현.
- 영향 범위: History 단위와 HR 통합의 실행 연결. 빈 상태 이동 반환만 기존 시트에 직접 명시되지 않음.
- 처리: 실제 API를 확인하거나 API 합의 후 코드화한다. 이미 명시된 초기 저장·비어 있지 않은 경계 반환을 다시 미정으로 만들지 않는다.

### DEC-07 · core의 동일 내용 저장

- 상태: 계약 추가 필요
- 확인한 사실: 페이지 no-op 저장 억제(80)는 기존. core push 자체의 동일값 생략은 미정.
- 영향 범위: HIST-N05. 일반 저장·분기·이동 테스트는 영향 없음.
- 처리: 매 호출 저장과 내용 동등 시 생략을 구분한다. 권장: 페이지에서 no-op을 걸러 core 책임을 단순하게 유지하되 확정하지 않는다.

### DEC-08 · History 이동 반환의 격리

- 상태: 반환 범위 확인
- 확인한 사실: hist-isolation-input/output은 저장 입력과 current() 결과의 격리를 이미 요구. back/forward 반환에도 같은 보호를 적용할지 확인 필요.
- 영향 범위: HIST-N04의 이동 반환 보강.
- 처리: 저장 내용 보존을 검사한다. deep clone 구현이나 외부 수정 허용을 강제하지 않고 frozen/readonly 방식도 구분한다.

### DEC-09 · 과거 위치 no-op의 redo 보존

- 상태: 교차 조건 결정
- 확인한 사실: 80은 초기 no-op,84는 새로운 내용의 분기를 명시. 뒤로 간 B에서 무변경 Patch를 누를 때 C가 남는지는 직접 사례 없음. 빈 입력·다중 root 거절의 history 그대로에는 기존 redo도 포함되며 이 결정의 대상이 아니다.
- 영향 범위: HR-N05의 redo 부분, FLOW-N04.
- 처리: 권장: 의미있는 변경이 없으면 이력과 redo도 유지. 확정 전 미래 접근 유지 assertion은 분리.

### DEC-10 · 미저장 편집 후 이력 이동

- 상태: 사용자 동작 정책
- 확인한 사실: 73은 Patch 전 실제 영역 불변만 명시. 미저장 X가 있을 때 뒤·앞 이동의 버림·자동저장·거절은 미정.
- 영향 범위: HR-N06, FLOW-N02의 미저장 부분, F-NAV.
- 처리: 한 정책을 정하고 두 방향을 검증한다. 새 경고창이나 자동저장을 임의로 도입하지 않는다.

### DEC-11 · 편집 UI·페이지 API·루트 추출

- 상태: 구현 표면 확인
- 확인한 사실: 시트85/86은 빈 입력·다중 root 거절과 #message 안내,87은 브라우저 보정 HTML 반영을 이미 요구. 편집기 종류·초기화 entry·일부 selector는 조사 시 없음.
- 영향 범위: F-INIT·F-PATCH·F-NAV와 페이지를 실제 호출하는 HR 통합.
- 처리: 실제 entry와 사용자 입력 경로를 사용한다. 테스트 안에 별도 orchestration을 만들어 제품 통합이라고 보고하지 않는다.

### DEC-12 · 사용자 HTML의 안전 경계

- 상태: 구현 책임 확인
- 확인한 사실: verify-no-script-exec(88)은 실행 없음과 실제 영역 script 요소·onerror 제거를 이미 요구. literal Text 생성 안전성과 HTML 입력 정제는 다른 책임.
- 영향 범위: F-PATCH의 안전 사례, PAGE-N04, 혼합 입력 경로.
- 처리: 정제 여부 자체는 기존 기대다. 정제 위치와 실행 전 안전한 입력 경로를 확인하고 무해한 테스트 표식으로 검사한다. 새 보안 범위를 임의 확대하지 않는다.

### DEC-13 · 추가 Patch 입력 범위

- 상태: 필수와 정책 probe 분리
- 확인한 사실: 빈 batch·없는 path 오류는 기존, 현재안 noRollback도 구체적. 동일 nonempty batch 재적용의 멱등성, 빈 PROPS, set/remove 동일키, 비정상 container는 별도 범위.
- 영향 범위: PATCH-N05의 빈 PROPS, PATCH-N07, 추가 malformed 입력.
- 처리: 지원 계약 없이 멱등성이나 모든 잘못된 입력 처리를 필수화하지 않는다. 현재 구현의 guard 대표와 정책 probe를 분리한다.

### DEC-14 · 브라우저 runner·IME·focus 범위

- 상태: 실행 환경과 추가 보장
- 확인한 사실: README FUNC는 실제 브라우저. 조사 시 package에는 Vitest·jsdom만 있고 browser runner 없음. 합성 composition은 OS IME 증거가 아님.
- 영향 범위: 모든 FUNC의 실행환경, PAGE-N03의 IME·조합 중 Patch·focus/caret.
- 처리: runner와 수동 보완 경로를 확인한다. 조합 완료 입력 검증과 조합 중 정책을 나누고 버튼 클릭 뒤 focus 불변을 임의 요구하지 않는다.

## 6. 출처와 관찰 한계

### 과제 원문

https://jungle-lms.krafton.com/learning/1307 를 부모 세션이 직접 읽었다. Phase 1 필수 흐름은 초기 실제DOM→VNode→테스트영역 생성, Patch클릭→현재 테스트DOM 재읽기→이전View와Diff→변경부분만 실제영역반영→새View History저장, 이력이동→두영역 함께변경이다. unit·functional·edge 검증 요구가 있다.

### Lark

- React Tests: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=ffbb46
- README: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=Ojre1q
- 셀 본문을 이름상자와 수식 textbox snapshot으로 읽었다. 시각적 캔버스는 행 배치 보조다. G열은 쉬운 설명, H열은 시나리오, I열은 예상 동작이다. 상세 재고의 일부 원문 머리글은 설명을 시나리오라고 표현하지만 데이터 열은 위 기준으로 해석한다.
- README는 기본·엣지 필수, 선택은 미구현 skip. UNIT/INTEG는 Node+jsdom, FUNC는 실제 브라우저 사용자 입력·클릭으로 구분한다.

### 로컬과 과거 M1

- 브랜치 관찰: .git/HEAD의 CJG. 시작(2026-11-09T03:49:23.692Z)에는 src/vnode.ts,vnode.test.ts,main.ts,setup.test.ts. T1~T37 it와 T38 todo 선언을 읽었다.
- 조사 중 다른 변경으로 patch.ts,patch.test.ts(P1~P28),ADR0006이 추가되고 isTextInput이 production Patch에서 쓰이는 export가 됐다. CONVENTION의 과거 Patch내용검사금지 문구는 제거됐고 GLOSSARY에 []=View path가 추가됐다. 후속 관찰 2026-11-09T03:58:04.544Z. 이 작업의 조사자들은 소스를 수정하지 않았다.
- ADR0005·0006 frontmatter는 proposed. 원격 #13 https://github.com/benjohnbill/mini-react/issues/13 은 관찰 시 Open 질문 기록이다. 현재 로컬 구체안과 구별한다.
- lab/m1-test-draft/M1-test-grilling.md와 초안, 취소 PR18 https://github.com/benjohnbill/mini-react/pull/18 은 개인 설계와 도출 방식의 근거다. 현 팀 합의로 자동 승격하지 않는다.
- History·검증 페이지의 실제 구현과 브라우저 runner는 조사 범위에서 확인하지 못했다. 독립 검토 시 diff.ts와 diff.test.ts도 추가된 것을 확인했다. 새 Diff 테스트는 전수 매핑하거나 실행하지 않았으므로 다음 세션이 재사용 여부를 다시 확인한다. 이는 모든 원격 브랜치의 부재를 뜻하지 않는다. 코딩 시작 때 최신 상태를 다시 확인한다.

## 7. 레벨별 구현과 완료 기준

1. 현재 API와 결정 의존을 대조한다. 제품 정책을 새로 정하지 않아도 되는 사례부터 작성한다.
2. 기존 코드와 매핑한 단위 테스트를 먼저 보강한다. 테스트만을 위한 export나 비공개 필드 캐스팅은 피한다.
3. 실제 협력 경로로 통합 테스트를 작성한다. 테스트 안에 새 페이지 orchestration을 만들어 제품 통합이라고 주장하지 않는다.
4. 실제 브라우저에서 FUNC를 검증한다. 페이지 init·편집기·selector·runner를 실제 구현에 맞춘다.
5. 각 case ID의 구현파일·테스트명·판정·근거를 기록한다. blocked는 어떤 결정이 필요한지 명시하고 무관한 사례까지 중단하지 않는다.
6. typecheck·lint·tests·build와 브라우저 실행 결과를 분리한다. 통과하지 않은 TODO·skip·설정확인을 제품 통과로 계산하지 않는다.
7. 테스트 전부 통과가 가독성·구조·모든 미래 입력의 정확성까지 보장하지 않는다. 이름·책임·의존성 리뷰는 별도로 한다.


## 8. 독립 검토와 반영

별도 세션이 기존91개·선택4·필수87·key8,13대상·57갈래·73추적항목을 검산했다. 전체 설계 착수를 막는 결함은 없었고, 다음 두 부분을 코드화 전에 보정했다.

1. 거절 입력은 redo를 포함한 이력 전체 보존이 기존 기대임을 HR-N05에 명시했다. 정상 과거 위치 no-op의 redo만 DEC-09에 남겼다.
2. DIFF-N05와 DP-N04의 old/new 대표쌍을 고정했다. 마지막 자식 삭제와 앞쪽 위치 변경을 섞고, old index→new index의 보존 refs를 적었다. 내용상 같은 항목이 다른 위치로 옮겨도 key 없는 비교에 key 기반 identity를 강요하지 않는다.

코드 생성·테스트 실행·CI·OS IME·실제 기능 검증은 이 설계 검토의 증거가 아니다. 새 Diff 파일을 포함한 병행 변경이 있으므로 시작 시 최신 작업 트리를 확인한다.
