# 담당 2: Phase 1 diff·patch·연결 테스트 설계

## 0. 결론과 범위

기존 canonical inventory는 diff UNIT 16개(행24~39), patch UNIT 11개(행40~50), INTEG 8개(행52~59), 합계35개예요. 기존 Lark 기대를 보존하되, 조사 중 새로 생긴 현재 로컬 ADR0006·patch.ts·P1~P28을 우선 별도 기록해요. 로컬안은 구체적이지만 ADR status는 proposed이며 팀 승인 여부는 확인하지 않았어요. #13 원문이 질문 상태라는 사실만으로 현재 로컬까지 형식 미정이라고 단정하지 않아요.

이 문서는 읽기 전용 조사와 보완안이에요. 코드·테스트·Lark·GitHub를 수정하거나 테스트를 실행하지 않았어요. 모든 후보는 설계일 뿐 구현 누락 판정이 아니에요. 기존 목록에 직접 사례가 없다는 판단도 읽은 diff/patch/INTEG 범위로 한정해요.

### 읽은 출처
- React Tests: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=ffbb46
- README: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=Ojre1q
- 현재 #13 본문과 유일 댓글: https://github.com/benjohnbill/mini-react/issues/13 (이번 조사에서 Open 확인)
- 로컬 읽기: mini-react/CONVENTION.md, GLOSSARY.md, docs/adr/0004-one-file-per-feature-and-patch-format-later.md, docs/adr/0005-dom-and-vnode-conversion-rules.md, docs/adr/0006-patch-format-and-path.md, src/patch.ts, src/patch.test.ts. 읽은 ADR front matter는 status: proposed예요. 승인·병합 여부를 이 로컬 파일만으로 추정하지 않아요.
- Lark 행24~59는 시나리오와 기대를 셀 단위로 읽었어요. 행24~39 원문은 앞선 연속 조사, 행40~59는 이번 조사에서 원문 재대조했어요. native 검색으로 diff- 22건, patch-20건, int-9건을 확인해 기본과 확장을 구분했어요. 177개 전체를 다시 조사하지 않았어요.
- 읽는 기법: 이름 상자에 셀 주소 입력→Enter→전체 snapshot→값이 바뀌는 동안 약180ms 대기→수식 textbox scoped snapshot. canvas는 screenshot으로 구조를 확인해요. scoped snapshot 이후 다음 셀 전에 전체 snapshot으로 ref를 갱신해요. 이 기법은 즉시 부모에게 전달했어요.

### 중복집계 경계
- 행51 int-render-roundtrip(INTEG)은 변환 담당의 canonical inventory예요. 본 보고서에서는 연결 전제만 참조해요.
- 페이지 담당 소유: 행74 verify-patch-apply, 75 verify-patch-partial, 76 verify-patch-history, 80 verify-patch-nochange, 91 verify-patch-log. 본 보고서의35개에 포함하지 않아요. UI 이벤트·로그·History 저장은 여기서 설계 소유하지 않아요.
- key확장: 행96 diff-key-change, 97 diff-key-added, 100 diff-keyed-reorder, 101 diff-keyed-insert; 100·101 분류는 선택. 행102 patch-move도 별도 key 확장. 행96 등의 Phase는 'Phase 1 · key 확장', Milestone M9예요. 기본 index diff와 혼합하지 않아요.
- Phase2 props확장: 행106 diff-event-same,107 diff-event-change,108 patch-props-false,109 patch-event-swap,110 patch-event-remove. Phase1 보장으로 세지 않아요.

## 1. 출처의 시점과 현재 로컬 계약

### Lark README
M5 VNode는 문자열 또는 태그·속성·자식을 가진 객체, M6 View는 최상위 VNode, M7 Patch는 두 View의 차이를 DOM에 반영하기 위한 지시, M8 container는 View를 그려 넣는 DOM 요소예요. N14 초기 VNode는 type/문자열 props/children, N15는 key:string|null 확장, N16은 Phase2 숫자·boolean·null·undefined·함수 props 확장이에요.

### 원격 #13과 Lark
이번에 직접 읽은 #13은 Open이며 평평한 목록 표현, 변경 전 트리 path 선해결과 뒤에서 삭제 순서보장 중 선택, []가 container 첫자식인지 모두 질문 상태였어요. 댓글은 HTML 주석을 번호에서 제외한다고 명시해요. Lark는 TEXT/REPLACE/PROPS/CREATE/REMOVE와 root [], 삭제역순·생성정순을 구체 기대해요. 이 둘만으로 팀 합의를 추정하지 않아요.

### 조사 중 동시 추가된 현재 로컬안: ADR0006 + 구현 + 테스트
초기 읽기 뒤 부모가 동시변경을 감지했고 재독했어요. ADR0006은 status: proposed지만 실제 patch.ts와 P1~P28 테스트도 존재해요. 승인 미확인과 로컬안 부재는 다른 말이에요. 현재 CONVENTION.md에는 'Patch 형식이 정해지기 전에는 내용을 읽지 않는다' 문구가 삭제됐어요. 따라서 과거 읽기 결과를 현재 금지규칙으로 쓰지 않아요.
- Patch 종류: TEXT, REPLACE, PROPS, INSERT, REMOVE. Lark CREATE와 현재 INSERT가 달라요.
- []는 View 자신. 실제 patch.ts는 container의 첫 Text 또는 Element에서 시작하고 주석을 제외해요. container 자체는 root 교체 대상이 아니에요.
- 각 path는 앞 Patch를 적용한 뒤 트리에서 해석해요. 받은 순서대로 적용하고 patch 함수가 정렬하지 않아요.
- diff의 로컬안 순서: 같은 index 자식 비교 먼저, 증가분 INSERT는 앞부터, 감소분 REMOVE는 뒤부터. old-tree 전체 선해결 방식이 아니에요.
- TEXT는 Text.data를 바꾸며 HTML로 해석하지 않음. PROPS는 같은 Element에 반영, 입력칸 value는 live .value에 씀. 일반 속성 remove는 removeAttribute.
- 실패는 path를 담은 Error. 앞서 적용한 Patch는 rollback하지 않아요. TEXT/PROPS의 대상 종류도 검사해요.
- input value 제거는 일반 removeAttribute만 함. DOM읽기 View는 value를 항상 포함하므로 그런 diff는 생기지 않는다는 전제예요. 임의 VNode의 value 필드 삭제를 표시값 초기화 계약으로 확대하지 않아요.
- INSERT []는 구현에서 위치가 없다며 Error. 비어 있거나 여러 root가 있는 container 전체지원은 명시적 설계범위가 더 필요해요.
- 위 사항은 현재 로컬안/정적 구현 관찰이며 팀 승인·main 반영·테스트 pass를 주장하지 않아요. 스키마 확인만을 이유로 후보를 모두 차단할 필요는 없고 승인 추적과 Lark 정합성을 별도로 남겨요.

### 변환과 인덱스
ADR0005 proposed는 공백·빈 Text 보존, 주석 제외, 주석 양옆 Text를 합치지 않음, 입력칸 .value를 빈값까지 포함한다고 적어요. Lark fromdom-skip-whitespace 행9의 공백 제거 기대와 차이가 있어요. 현재 patch안은 whitespace도 번호에 세며 P19로 시험해요. 현재안 대상 설계에서는 이를 사용하고 Lark와의 충돌을 별도 이력으로 표시해요. #13 주석 제외 조건은 직접 확인했어요.


## 2. 대상별 책임·입출력·상태·협력

### diffViews
두 View를 비교해 새 View로 바꾸는 데 필요한 변경을 반환하며 입력 View를 바꾸지 않아요. Phase1의 기본 비교는 key 없는 구조를 대상으로 하고 Patch 표현·경로 기준은 현재 ADR0006 proposed 안으로 구체화하되 승인 추적을 남겨요.
- 입력: currentView,newView. 출력: Patch 목록(현재 로컬안). DOM 상태를 직접 변경하지 않아요.
- 상태: 입력 트리와 공유 중첩 객체 불변. DOM·History 부수효과 없음은 책임에서 도출한 검증 후보이며 기존38의 직접 범위는 두 View 내용 불변이에요.
- 협력: vnode 타입과 patch의 타입. Patch의 소비자는 applyPatchesToDom. Phase1 문자열 props와 Phase2 확장을 구분해요.

### applyPatchesToDom
주어진 container 안 View DOM에 변경을 적용하고 변경 대상 밖의 Node를 보존해요. VNode 기준 위치와 실제 DOM Node의 차이를 처리하며 live 입력값과 문자열을 올바른 DOM 상태로 반영해요.
- 입력: container,patches. 출력: void는 현재 patch.ts 시그니처. 상태: container 내부 DOM과 입력칸 .value가 변경됨.
- 협력: Patch 계약, vnode의 DOM 생성 규칙. container 자체 보존은 기존46, 기존42의 대상 요소 보존·기존40의 이웃 보존이 직접 근거예요.
- Patch 목록 내용 불변성은 현재 P25가 시험해요. 잘못된 batch는 앞 변경을 되돌리지 않는 현재 ADR0006/P28이 있어요. 같은 batch 재적용의 멱등성은 보장으로 추정하지 않아요.

### diff→patch 연결
이전 View와 새 View의 diff를 이전 DOM에 적용한 뒤 새 View와 같은 관찰 상태가 되게 하며, 변경되지 않은 실제 Node 참조를 유지해요.
- 입력: old/new View, old DOM/container. 출력은 최종 DOM과 다시 읽은 View. 협력: diffViews,applyPatchesToDom,createVNodeFromDom; createDomFromVNode는 독립 기대 DOM 비교를 돕되 같은 버그의 상쇄를 막는 직접 assertion을 병행해요.

### DOM 읽기→Diff→Patch 연결
실제 DOM에서 현재 입력과 구조를 읽고 기준 View와 비교하여 필요한 변경만 실제 DOM에 반영해요. 읽기에서 제거한 주석·보존한 공백·빈 Text·live .value가 patch의 위치와 값 해석에 일치해야 해요.
- 두 View의 어느 쪽이 '이전'인지 호출자 흐름에 따라 명시해야 해요. LMS의 Patch 클릭 흐름과 History 저장은 부모/페이지 담당이 소유하며 이 보고서가 no-op History 정책을 정하지 않아요.

## 3. 기존 canonical inventory

행 번호는 시트 행 번호예요(No. 값은 한 칸 작음). 아래 Patch 표현은 시트의 기록을 보존한 것이며 팀 계약 확정 선언이 아니에요.

### 3.1 diff UNIT 16
- 행 24 · UNIT · `diff-same`: 내용이 완전히 같은 두 View 비교 → 빈 배열 [].
- 행 25 · UNIT · `diff-text`: <p>a</p> → <p>b</p> → [{ type: 'TEXT', path: [0], text: 'b' }]만 반환, REPLACE 없음.
- 행 26 · UNIT · `diff-tag`: <p>a</p> → <span>a</span> → path [] REPLACE 하나, 내부 글자 Patch 없음.
- 행 27 · UNIT · `diff-text-to-elem`: 같은 위치의 문자열 VNode → <b> 요소 VNode → 해당 path REPLACE 하나.
- 행 28 · UNIT · `diff-attr-change`: class x → y → [{type:'PROPS',path:[],set:{class:'y'},remove:[]}].
- 행 29 · UNIT · `diff-attr-add`: 속성 없는 요소에 id="a" 추가 → PROPS set={id:'a'}, remove=[].
- 행 30 · UNIT · `diff-attr-remove`: id 속성 삭제 → PROPS set={}, remove=['id'].
- 행 31 · UNIT · `diff-child-add`: 자식 1개 → 2개 → CREATE path [1] 하나.
- 행 32 · UNIT · `diff-child-remove`: 자식 3개 → 1개 → REMOVE [2], REMOVE [1] 순서.
- 행 33 · UNIT · `diff-child-insert-middle`: key 없는 ul의 li a,c 사이에 li b 삽입 → index 비교. TEXT [1,0]('b')와 CREATE [2](li c). 최소 변경은 아니지만 결과 화면은 맞음.
- 행 34 · UNIT · `diff-deep`: <div><section><p>a</p><p>b</p></section></div> 두 번째 p 글자 변경 → TEXT path [0,1,0] 하나.
- 행 35 · UNIT · `diff-multi`: 서로 다른 위치의 글자 하나와 속성 하나 변경 → TEXT 하나와 PROPS 하나만, 다른 Patch 없음.
- 행 36 · UNIT · `diff-remove-all`: 자식 3개 → 없음 → REMOVE [2], [1], [0] 순서.
- 행 37 · UNIT · `diff-from-empty`: 자식 없음 → 3개 → CREATE [0], [1], [2] 순서.
- 행 38 · UNIT · `diff-no-mutate`: 변경 전후 두 View 비교 → 두 View 모두 내용 불변.
- 행 39 · UNIT · `diff-invalid-arg`: 인자로 null 또는 undefined → TypeError 발생.

### 3.2 patch UNIT 11
- 행 40 · UNIT · `patch-text`: View가 <div><p>a</p><p>x</p></div>인 container에 첫 p의 글자를 바꾸는 TEXT를 적용함 → 첫 p의 글자만 바뀌고, 두 번째 p는 적용 전과 같은 요소(===)임.
- 행 41 · UNIT · `patch-replace`: p가 있는 위치에 span으로의 REPLACE를 적용함 → 그 위치가 span이 되고 내용은 Patch의 node와 같음.
- 행 42 · UNIT · `patch-props-set`: class를 y로, title을 t로 바꾸는 PROPS를 적용함 → 두 속성이 새 값이고, 요소 자체는 적용 전과 같은 요소임.
- 행 43 · UNIT · `patch-props-remove`: remove가 ['id']인 PROPS를 적용함 → id 속성이 없어짐.
- 행 44 · UNIT · `patch-create`: 자식이 1개인 ul에 path [1] CREATE를 적용함 → ul의 두 번째 자식으로 새 li가 추가됨.
- 행 45 · UNIT · `patch-remove`: 자식이 3개인 ul에 REMOVE [2], REMOVE [1]을 적용함 → 첫 번째 li만 남음.
- 행 46 · UNIT · `patch-view-replace`: path []인 REPLACE를 적용함 → container 안의 View DOM이 새 DOM으로 바뀌고, container는 같은 요소이며 자식은 여전히 하나임.
- 행 47 · UNIT · `patch-empty`: 빈 배열을 적용함 → MutationObserver 기록이 0건이고 DOM이 전혀 바뀌지 않음.
- 행 48 · UNIT · `patch-value-prop`: input의 value를 'new'로 바꾸는 PROPS를 적용함 → input.value가 'new'임.
- 행 49 · UNIT · `patch-invalid-path`: 존재하지 않는 path [9, 9]에 TEXT를 적용함 → 메시지에 [9, 9]가 들어 있는 Error가 발생함.
- 행 50 · UNIT · `patch-mutation-count`: 글자 하나만 바꾸는 TEXT를 적용하면서 MutationObserver로 기록함 → 기록이 그 텍스트 노드의 글자 변경(characterData) 1건뿐임.

### 3.3 연결 INTEG 8
- 행 52 · INTEG · `int-roundtrip-text`: 글자만 다른 두 View로 이전 View DOM에 diffViews와 applyPatchesToDom을 적용함 → 다시 읽은 결과가 새 View와 같음.
- 행 53 · INTEG · `int-roundtrip-attr`: 속성의 추가, 변경, 삭제가 섞인 두 View로 같은 순서를 수행함 → 다시 읽은 결과가 새 View와 같음.
- 행 54 · INTEG · `int-roundtrip-children`: 자식의 추가, 삭제, 가운데 끼워 넣기가 섞인 두 View로 같은 순서를 수행함 → 다시 읽은 결과가 새 View와 같음.
- 행 55 · INTEG · `int-roundtrip-replace`: 중간 깊이의 태그가 바뀌고 그 아래 구조도 달라진 두 View로 같은 순서를 수행함 → 다시 읽은 결과가 새 View와 같음.
- 행 56 · INTEG · `int-roundtrip-view-replace`: 최상위 태그가 div에서 section으로 바뀐 두 View로 같은 순서를 수행함 → 다시 읽은 결과가 새 View와 같고, container의 자식은 여전히 하나임.
- 행 57 · INTEG · `int-roundtrip-sequence`: View A → B → C → A 순서로 계속 바꿈 → 단계마다 다시 읽은 결과가 그 단계의 View와 같고, 마지막에는 A와 같음.
- 행 58 · INTEG · `int-preserve-identity`: 한 곳만 다른 두 View로 같은 순서를 수행함 → 바뀌지 않은 모든 요소가 적용 전과 같은 요소(===)임.
- 행 59 · INTEG · `int-roundtrip-fuzz`: 무작위로 만든 View 쌍 500개로 같은 순서를 수행함. 무작위 시드는 고정해 재현할 수 있게 함 → 500개 모두 새 View와 같고, 실패하면 그 시드와 두 View를 출력함.

기존 INTEG의 '다시 읽은 결과==새 View'만으로 DOM identity와 live .value를 전부 보장하지 않아요. 기존58은 모든 바뀌지 않은 요소의 ===를 별도로 요구해요. 기존51은 변환 전용이고 diff 보장이 아니에요.

## 4. diff 7묶음: 한줄 성질·기존·보완·결정

1. D1 무변경: 같은 내용은 변경 없음이고 차이 밖 변경을 만들지 않아요. 기존24/25/26/35, DIFF-N01·DP-N01 보강. 최소변경은 전역 최소 Patch 개수 강제가 아니며33이 반례예요.
2. D2 종류·태그: 종류나 태그 교체는 그 subtree 자손을 중복 갱신하지 않아요. 기존26/27, DIFF-N02 역방향·깊은 교체 보강. root []는 현재 ADR0006의 View 자신으로 설계하고 승인추적 D-03.
3. D3 텍스트·빈값: 문자열을 HTML로 해석하거나 임의 trim하지 않고 대상 위치에 전달해요. 기존25/34, DIFF-N03. 현재로컬 공백·빈Text 보존안과 Lark 변환행9 차이는 D-04.
4. D4 속성: 문자열 값 설정과 속성 삭제를 구별하고 영향 없는 속성은 남겨요. 기존28~30, DIFF-N04/PATCH-N05. Phase2 undefined/boolean은 기본 문자열 props에 섞지 않아요.
5. D5 자식·경로·순서: 각 patch가 순차 적용된 트리의 올바른 위치에 도달하고 바깥 Node를 보존해요. 기존31~37, DIFF-N05/PATCH-N06/DP-N04. 현재 INSERT·next-tree path 안으로 구체화하며 old-tree path로 fixture를 작성하지 않아요. key MOVE는 별도.
6. D6 input.value: live 입력값의 변경과 빈값이 연결 전체에서 소실되지 않아요. diff16 직접사례 없음, patch48 및 현재P23/P24 있음. DIFF-N06/PATCH-N03/DP-N03은 특히 empty를 보강. attribute==property 기대 금지.
7. D7 입력불변·잘못된입력: 비교는 두 View를 바꾸지 않고 정의한 실패를 드러내요. 기존38/39, DIFF-N07 중첩freeze·공유참조 보강. null/undefined는 첫인자·둘째인자별 대표로 명확화하되 임의 malformed shape로 무제한확장하지 않아요.


## 5. patch·연결 묶음과 현재 테스트 중복 방지

- P1 Node 보존: 텍스트·속성 갱신은 대상 밖 실제 refs를 보존해요. Lark40/42/50/58, 현재P10/P11/P12/P14. 실제===가 oracle이며 isEqualNode만으로 identity를 판정하지 않아요.
- P2 구조·root: 생성/삭제/교체 후 목표구조와 container를 유지해요. Lark41/44~46/54~56, 현재P3/P4/P7/P8/P9/P15/P20/P21/P22. CREATE→INSERT와 순차트리 기준을 반영해요.
- P3 인덱스: VNode 위치가 주석을 제외하고 공백·빈Text를 포함한 실제 DOM 위치에 대응해요. Lark11patch와8연결에는 직접명시없지만 현재P17/P18/P19가 이미 있어요. PATCH-N01은 신규가 아닌 ref보강, N02는빈Text·주석양옆Text 잔여조건이에요.
- P4 값·문자열: .value와 attribute를 별도관찰하고 텍스트를 HTML로 해석하지 않아요. Lark43/48, 현재P2/P23/P24. PATCH-N03은dirty nonempty 중복을제외하고 empty를추가, N04는P2/P14의ref보강으로분류해요.
- P5 noop·반복·실패: 빈batch는무변경,비어있지않은batch재적용은정책구분,실패시앞변경은남아요. Lark47/49/57, 현재P13/P25/P26/P27/P28. N08 noRollback은이미P28이므로중복신규금지.
- I1 의미·연속성·독립관찰: Lark52~59 최종내용·일련변경·보존·고정seed가있어요. DP-N01~06은property·refs·mapping을대표조합으로보강하고전수cross-product는만들지않아요.


## 6. Stable 보완 후보

후보ID는 이 보고서에서 고정해 부모가 병합할 때 이름을 바꾸지 않아도 되게 해요. '결정 의존'이 있는 기대는 확정 oracle이 아니에요. 단위 fixture는 현재 ADR0006/patch.ts의 INSERT 및 순차 path 안을 기준으로 설계할 수 있어요. 팀 승인 상태는 별도로 남겨요. 아래 후보ID는 신규필요 여부가 아니라 설계추적ID이며 현재 P1~P28과 매핑해 중복 신규를 피해야 해요.

### DIFF-N01 내용 동일과 참조 동일
- 입력: 같은 old 객체를 두 번, 깊은 복사지만 같은 내용인 old/new 두 경우. 사전상태: 값·props·children snapshot. 동작: diffViews 호출.
- 기대: 의미상 변경 없음; 현재 로컬안의 빈 Patch[]를 기대할 수 있고 승인 추적을 남김. 왜:24의 '같은 내용'이 객체 참조 shortcut과 구조동등을 구별하지 않음. 범위:UNIT D1. 결정 의존:D-01.

### DIFF-N02 교체 역방향과 자손 억제
- 입력: 자손이 있는 요소→문자열, 동일 위치 태그교체 두 대표. 사전상태: old/new 불변. 동작:diff.
- 기대:교체되는 범위만 반영하며 자손 Patch 중복 없음. 왜:27은 문자열→요소만,26은 동일 글자의 태그 변경만. 범위:UNIT D2. 결정 의존:D-01,D-03(루트 버전은 보류).

### DIFF-N03 빈 텍스트와 공백
- 입력:children의 'a'→'', ''→'a', ' '→'  ' 두 방향을 대표표로 구성. 사전상태:VNode 문자열은 이미 생성된 입력이며 DOM 읽기 정책과 분리. 동작:diff.
- 기대:문자열 차이가 실제 대상 위치에 전달, 주변 형제 삭제/재번호화 없음은 보존계약 채택 시. 왜:25·34에는 빈값/공백 사례 없음. 범위:UNIT D3. 결정 의존:D-01,D-04. 임의 trim 기대 금지.

### DIFF-N04 빈 속성과 삭제의 구별
- 입력:{title:'x'}→{title:''}, {}→{title:''}, {title:''}→{} 대표3개. 사전상태:Phase1 문자열 props. 동작:diff.
- 기대:빈문자열 설정과 속성 삭제가 다른 의미로 전달됨. 현재 로컬안의 PROPS set/remove로 표현함. 왜:28~30은 비어 있지 않은 값만. 범위:UNIT D4. 결정 의존:D-01. undefined는 이 후보에 넣지 않음.

### DIFF-N05 구조 변경과 다른 위치 변경의 혼합
- 입력:형제3개 중 하나 삭제, 살아남는 형제의 text/prop 변경, 중첩 자식 하나 추가를 한 대표쌍으로 구성. 사전상태:명명한 old 위치별 refs와 기대 new를 직접 작성. 동작:diff.
- 기대:각 대상 의미와 최종 new가 맞고 바깥 변경 없음; 현재 로컬안대로 앞 patch 적용 후 path와 비교→INSERT정순→REMOVE역순으로 설계함. 왜:35는 글자+속성만,32는 삭제만. 범위:UNIT D5,DP-N04와 짝. 결정 의존:D-01,D-02.

### DIFF-N06 value의 빈값 변화
- 입력:input props.value 'old'→'new', 'old'→'', ''→'' 대표. 사전상태:문자열 props, value 필드 존재. 동작:diff.
- 기대:두 변경이 전달되고 마지막은 무변경. 빈값을 속성 부재로 축약하지 않음은 ADR 채택 상태 확인 후. 왜:diff16에는 value 직접 사례 없음. 범위:UNIT D6. 결정 의존:D-01,D-05. DOM .value 자체 판정은PATCH/DP에서 함.

### DIFF-N07 중첩 입력과 공유 참조 불변
- 입력:props·children·손자객체를 공유하거나 각각 가진 old/new. 사전상태:recursive freeze 가능한 fixture와 깊은 snapshot, 참조목록. 동작:diff.
- 기대:throw 없이 유효입력을 비교하고 모든 입력 내용·기존 참조 유지. 왜:38은 내용 불변만 서술해 검증 강도가 모호. 범위:UNIT D7, 기존38 보강. 결정 의존:freeze된 입력도 유효입력으로 허용할지 확인; 결과 Patch가 old/new 참조를 담는 것 자체는 금지하지 않음.

### PATCH-N01 comments 위치: 현재P17/P18 보강
- 입력:hello<!--x--><span>world</span>의span내Text변경 및 주석사이INSERT. 사전상태:기존Text/comment/span refs저장. 동작:현재ADR0006fixture적용.
- 기대:주석을제외한위치에만반영,주변Node refs유지. 왜:내용mapping은이미P17/P18에있고현재테스트는ref검사가없음. 범위:UNIT P3,새동일내용테스트를중복생성하지않음. 결정의존:로컬안승인추적D-01,주석수명D-08(현재P17/18은댓글존재도기대).


### PATCH-N02 공백·빈Text·주석양옆Text 잔여조건
- 입력:DOM API로[Text(''),Text(' '),Comment,Text('a'),span]을생성해span또는공백Text한곳을수정. 사전상태:전체실제refs,parser의Text병합을피함. 동작:순차pathfixture적용.
- 기대:현재로컬안대로빈Text·공백을세고주석은빼며의도한Node만갱신. 왜:P19는공백만이미다루므로빈Text·주석양옆분리Text가잔여조건. 범위:UNIT P3. 결정의존:D-04는Lark와현재안정합성,현재안관찰기대는구체적.


### PATCH-N03 dirty input의 live 빈값: 현재P23/P24 보강
- 입력:attribute value='initial',.value='typed'인input에set.value='' 및반복동일빈값대표. 사전상태:input ref와attribute/property별도기록. 동작:PROPS적용.
- 기대:같은input의.value='',attribute동일성은강제안함. 왜:nonempty new는P23/P24가이미있어중복제외,empty만추가. 범위:UNIT P4. 결정의존:현재코드는set.value를property에쓰며remove.value는attribute만삭제함. remove로live값초기화를기대하지않음.


### PATCH-N04 문자열안전성과Text identity: 현재P2/P14 보강
- 입력:HTML모양문자열로Text갱신. 사전상태:targetText·부모·이웃refs,setup후observer큐비움. 동작:TEXT적용.
- 기대:요소생성없이문자그대로,동일Text ref,characterData record의target===기존Text. 왜:P2는HTML비해석을이미검증,P14는record개수와type만검사하므로targetref를보강. 범위:UNIT P1/P4. 결정의존:현재ADR0006·구현에근거,pass주장아님.


### PATCH-N05 빈 PROPS와 빈 문자열
- 입력:일반 div에 title='', title삭제, set/remove 모두 빈 PROPS 대표. 사전상태:div·이웃 refs,기존 title. 동작:patch.
- 기대:title=''은 hasAttribute true와 getAttribute ''; 삭제는 hasAttribute false. 빈 PROPS는 DOM 무변경을 후보로 둠. 왜:43삭제·42비빈설정·47빈batch와 다른 조건. 범위:UNIT P4/P5. 결정 의존:D-01,빈PROPS 허용/거부는D-06.

### PATCH-N06 순차path와삭제혼합: 현재P21/P22 재사용
- 입력:a,b,c에서b삭제후현재index[1]인c의글자를변경. 사전상태:a와c refs저장. 동작:REMOVE[1]→TEXT[1,0]순으로적용.
- 기대:c수정,a/c생존refs동일. 왜:P21은앞삭제후새index수정,P22는수정후끝삭제를이미검증하므로같은의미의새테스트를중복작성하지않고ref/대표깊이보강만고려. 범위:UNIT P2. 결정의존:현재next-tree계약채택,old-tree전체선해결기대는사용안함.


### PATCH-N07 동일 nonempty batch 재적용
- 입력:TEXT/PROPS 1개 batch와 CREATE 1개 batch를 각각 분리. 사전상태:첫 적용 후 DOM. 동작:동일 목록 재적용.
- 기대:미정. TEXT/PROPS의 재설정, CREATE의 중복/거부,stale path 처리 중 계약이 먼저 필요. 왜:57은 매 단계 새 diff이며 재사용batch멱등 보장이 아님. 범위:UNIT P5 정책 probe. 결정 의존:D-06. 통과조건을 임의로 '멱등'으로 정하지 않음.

### PATCH-N08 invalid batch noRollback: 현재P28 재사용
- 입력:valid TEXT뒤invalid path TEXT. 사전상태:DOM refs와내용. 동작:batch적용후Error포착.
- 기대:현재ADR0006·P28대로앞TEXT반영은남고Error발생. 왜:이전초안의원자성미정표현은동시변경후stale이며이미P28에있음. 범위:UNIT P5,신규중복없음. 결정의존:로컬안승인추적만. 추가로PROPS가Text를가리키는오류는현재구현분기에는있지만P1~P28직접케이스는없어보강후보;Lark49의invalid위치와다름.


### DP-N01 no-op 연결의 참조와 부수효과
- 입력:서로 다른 객체지만 동일한 old/new View. 사전상태:container,root,모든Element와Text refs;DOM조립후 observer기록비움. 동작:diff→patch→readback.
- 기대:readback 동일,실제Node refs 동일,MutationObserver0건. 왜:24·47은 분리,58은 한 곳 변경일 때임. 범위:INTEG D1/P5. 결정 의존:구체Patch내부를읽지않음;History저장/로그는범위밖.

### DP-N02 subtree 교체와 바깥 보존
- 입력:중간 section→article 교체와 내부구조변경,바깥형제는동일. 사전상태:container·root·교체대상·이웃refs 저장. 동작:diff→patch→readback.
- 기대:교체대상은새ref,바깥동일Node들은===,최종내용new와일치. 왜:55최종내용+58보존을한대표구조로연결. 범위:INTEG P1/P2. 결정 의존:교체범위최소성계약;root버전은D-03.

### DP-N03 DOM 읽기에서 dirty value→빈값
- 입력:attribute='initial',.value='typed'인실제input에서읽은current View와props.value=''인new View. 사전상태:inputref·속성·property기록. 동작:read→diff→patch→read.
- 기대:실제 .value='',같은inputref,다시읽은value=''. attribute동일성은기대하지않음. 왜:fromDom과patch가각각맞아도빈값소실/잘못된읽기로연결실패가능. 범위:INTEG D6/P4. 결정 의존:D-05와ADR승인상태. 변환담당의개별UNIT과중복집계하지않음.

### DP-N04 구조·삭제·중첩수정의 한 혼합회귀
- 입력:DIFF-N05와동일한대표old/new. 사전상태:생존형제및중첩targetrefs,사람이직접쓴new기대. 동작:diff→patch→readback.
- 기대:내용new와일치,생존불변범위refs유지,엉뚱한형제변경없음. 왜:32·35·54가개별성공해도batch경로실패가능. 범위:INTEG D5/P2. 결정 의존:Patch내부읽지않음,기본index와key최적화를혼동하지않음.

### DP-N05 comment·whitespace·빈Text mapping 연결
- 입력:DOM API로만든emptyText,공백Text,주석,일반Text,span이있는실제DOM과span글자만다른new View. 사전상태:각실제ref와DOM구조기록. 동작:read→diff→patch→read.
- 기대:의도span만바뀌고주변Text·Element참조유지;주석제외VNode기준위치가정확. 왜:readback내용만보면주석누락과동일내용노드교체를놓침. 범위:INTEG P3. 결정 의존:D-04,D-08;주석보존그자체는별도정책. DOM전체isEqualNode를주석제거왕복oracle로쓰지않음.

### DP-N06 연속갱신과 fuzz 관찰 보강
- 입력:기존57 A→B→C→A에한번의빈text/value및구조변경대표를넣고,기존59고정seed생성기는유효Phase1범위로제한. 사전상태:단계별기대View와변경밖refs. 동작:매단계새read/diff/patch,실패seed출력.
- 기대:각단계내용·.value·생존refs를독립관찰. 왜:최종A만맞는상쇄실패와isEqualNode의property맹점방지. 범위:INTEG기존57/59보강,새500×모든edge곱금지. 결정 의존:D-04,D-05;같은batch재적용은이후보아님.

## 7. 현재 결정·잔여 질문·차단 범위

- D-01 형식:현재 ADR0006 proposed와patch.ts는TEXT/REPLACE/PROPS/INSERT/REMOVE로구체적. Lark CREATE와차이있음. 차단은'스키마부재'가아니라팀승인/기존시트정합성추적. 현재안fixture설계는가능.
- D-02 시간기준·순서:현재안은앞Patch후트리,받은순서,같은index비교→INSERT앞부터→REMOVE뒤부터. #13의old-tree선해결대안과다름. old-tree기준을확정oracle로쓰지않음. M9 MOVE가들어오면다시정해야한다는ADR명시.
- D-03 root:현재안[]는View자신,container유지. 구현은첫Text/Element부터시작,INSERT[]는Error. container내비어있는상태·추가root·rootREMOVE후후속Patch범위는추가질문. 일반단일Viewrootfixture는계속설계가능.
- D-04 공백:현재로컬은공백·빈Text보존,댓글제외,P19로공백mapping시험. Lark행9와차이는해결필요하나현재안내용까지미정이라고쓰지않음.
- D-05 value·emptyprops:현재set.value는liveproperty,remove.value는attribute만삭제. read로만든View는항상value포함전제. empty문자열직접사례는P23/24에없어보강. set/remove같은key충돌은현재코드상set후remove이나공개계약의유효입력여부를확인. undefined/boolean은Phase2.
- D-06 repeated:동일nonemptybatch재적용과빈PROPS허용을명시계약으로일반화하지않음. 현재코드는받은대로다시적용하므로CREATE/INSERT멱등기대금지. 빈batch는기존47/현재P13.
- D-07 실패:현재ADR0006은noRollback,현재P28은부분반영을확인하는테스트가있음. 과거미정표현폐기. PROPS대상종류오류·INSERT범위오류및메시지대표추가는기존P26/P27과중복구분해서검토가능.
- D-08 주석수명:현재코드는주석을세지않고P17/P18의innerHTML기대에주석보존이들어있음. root전체REPLACE의subtree주석까지보존하라는보장은아님. 외부불변Node는실제refs로검사.
- 승인/실행:ADRproposed,localcodeexists,localtestexists는각기다른사실. 승인·merge·CI·pass는이번조사로확인하지않았어요. 본보고서후동시변경가능성을남겨요.


## 8. 실행 관찰 기준과 부모 통합 요약

- Node보존:실제Node참조를변경전저장하고변경후직접===로비교. querySelector로새로찾아구조만비교하거나isEqualNode만쓰지않음. 변경대상밖모든Element는기존58,Text참조강화는관련계약과기존50근거를명시.
- MutationObserver:fixture조립과초기렌더기록을먼저비우고,동작후microtask전달또는takeRecords로회수해판정. characterData와childList·attributes를구분. .value변경은observer무기록일수있으므로별도propertyassertion필수.
- 기대 독립성:diff출력을기대값계산기로사용하지않음.독립수기목표와직접DOMassertion,허용된별도공개변환함수비교를함께사용. readback같음만으로주석·.value·identity를보장하지않음.
- fixtures:지원HTML단일root,Phase1문자열props,기본indexdiff. input은checkbox/radio제외. textarea/select/SVG/template및이벤트·key최적화는다른범위.
- 부모 통합:diff는D1~D7에기존16과DIFF-N01~N07;patch는P1~P5에기존11과PATCH-N01~N08;연결은I1및P3에기존8과DP-N01~N06. 후보총21개(기존보강포함)이며전수곱이아닌대표조건이에요. canonical기존35개,51·페이지·key·Phase2는중복집계제외. D-01~D-08은현재로컬안과잔여정책을분리하며,이미P1~P28에있는조건은중복신규가아닌보강/재사용으로분류해요.

## 9. 현재 로컬 P1~P28 정적 inventory와 매핑

아래는새로읽은src/patch.test.ts의선언·assertion관찰이에요. 실행결과가아니며Lark35개집계와별도예요.

- P1 TEXT 일반변경→Lark40. P2 문자열HTML비해석→PATCH-N04이미존재.
- P3 요소REPLACE→Lark41. P4 Text→Element REPLACE→Lark27의patch측확장.
- P5 PROPS set→Lark42. P6 PROPS remove→Lark43.
- P7 INSERT끝추가→Lark44(CREATE→INSERT차이). P8 속성·중첩자식INSERT→추가로컬범위. P9 REMOVE역순→Lark45.
- P10 TEXT옆형제===→Lark40보존. P11 PROPS대상===와명시안한속성보존→Lark42. P12 REPLACE/INSERT/REMOVE뒤형제===→PATCH구조보존이미존재.
- P13 빈목록observer0→Lark47. P14 characterData1건→Lark50. record.target/ref정밀assertion은없음.
- P15 []rootREPLACE와childNodes1→Lark46. P16 깊은path→Lark34의patch측직접범위.
- P17 주석제외TEXT path→PATCH-N01이미존재. P18 주석제외INSERT index→PATCH-N01이미존재. P19 whitespace번호포함→PATCH-N02일부이미존재. 빈Text·주석양옆Text는별도잔여.
- P20 INSERT[0],[1],[2]정순→Lark37의patch측. P21 앞삭제후현재트리path→PATCH-N06이미존재. P22 index수정후끝삭제→PATCH-N06이미존재.
- P23 input.value=new→Lark48. P24 dirty.value=typed후new→PATCH-N03nonempty이미존재. empty설정은잔여.
- P25 patches내용불변(structuredClone비교)→추가로컬기존범위. 리스트/내부객체freeze나참조불변까지검증했다고확대안함.
- P26 없는path Error메시지→Lark49. P27 TEXT가Element가리킬때Error→추가로컬기존범위.
- P28 valid다음invalid일때앞변경유지→PATCH-N08이미존재.

### 후보 상태 최종표현
- DIFF-N01~N07:이번읽기에서는diff테스트소스전체를읽지않았으므로Lark보강후보. 기존소스부재단정금지.
- PATCH-N01/N04/N06/N08:각각P17·18/P2·14/P21·22/P28기존조건재사용,refs보강만필요한부분구분.
- PATCH-N02:공백은P19재사용,빈Text·분리Text잔여. N03:dirty nonempty는P24재사용,empty잔여. N05:빈문자열/빈PROPS직접케이스잔여. N07:반복batch정책probe.
- DP-N01~N06:Lark52~59를기반으로한연결관찰보강. 이번에는연결테스트소스의존재/실행은확인안함.
- 현재patch구현에있는PROPS의Text대상오류,INSERT[]·out-of-range실패분기는추가보강후보지만새stableID를무제한늘리지않고PATCH-N08의유형별실패대표로흡수가능. 음수/noninteger path는유효입력범위결정전확대금지.
