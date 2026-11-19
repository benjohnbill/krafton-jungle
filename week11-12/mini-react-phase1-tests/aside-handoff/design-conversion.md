# Phase 1 변환 단위 및 왕복 통합 테스트 설계

작성 관측일: 2026-11-09, 읽기 전용 조사. 소스, 테스트, Lark를 수정하지 않았고 테스트도 실행하지 않았습니다. 이 문서의 '기존'은 **현재 Lark에 있는 정의**와 **로컬 코드에 이미 있는 테스트**를 구별합니다. PR #18 취소 사실은 위임 맥락으로만 받았고 GitHub PR을 직접 확인하지 않았습니다. M1 개인 합의를 현재 팀 합의로 승격하지 않습니다.

## 1. 대상 책임과 입출력

- createVNodeFromDom: 주어진 DOM 요소의 태그, 문자열 속성, 자식 구조 및 합의된 입력칸 현재값을 새 VNode 값으로 읽습니다. 읽는 과정에서 원래 DOM을 바꾸지 않습니다. 공백, 빈 글자, 주석의 정규화 정책은 아래 결정 목록을 따로 확정해야 합니다.
- createDomFromVNode: 문자열 또는 요소 VNode를 읽어 새 DOM Node를 만듭니다. 문자열은 HTML이 아닌 Text 한 개이며, 요소의 props와 children을 순서대로 반영하고 입력 VNode를 변경하지 않습니다.

| 대상 | 현재 입력 계약 | 현재 출력 | 보존 대상 | 관련 함수와 사용 경계 |
|---|---|---|---|---|
| createVNodeFromDom | Element 하나, HTML 일반 요소 중심 | VNode(실제 현 구현 최상위는 객체), null 반환 없음 | localName, 문자열 attributes, 자식 순서와 깊이, Text.data, 대상 input.value | 재귀 자기호출, createPropsFromElement, isTextInput. Diff 입력의 기준값이지만 Diff와 Patch 정확성은 이 테스트의 책임 아님 |
| createDomFromVNode | string 또는 {type:string, props:Record<string,string>, children:VNode[]} | 새 Node, 문자열이면 Text, 객체이면 HTML Element | literal 문자열, 속성 존재와 값, 자식 순서와 깊이, input의 표시 .value | 재귀 자기호출. History 복원 등에 사용 가능하지만 History 저장·독립성 테스트는 담당 외 |
| 왕복 A | 지원 범위의 Element | DOM→VNode→DOM | 합의한 화면 표현과 노드 구조 | 로컬 T34~T37 방향. 주석 제거와 input value 추가 때문에 무조건 isEqualNode를 요구할 수 없음 |
| 왕복 B | 정규형 요소 VNode | VNode→DOM→VNode | 지원 범위에서 정규화 후 같은 값 | **Lark 51행의 실제 방향**. 최상위 문자열을 reader에 넘기는 것은 현 시그니처와 맞지 않음 |

현재 src/vnode.ts 1~3행의 VNode에는 key, 함수 props, hooks가 없습니다. 5~18행이 DOM 생성, 20~37행이 reader, 39~48행이 속성 추출, 50행 이후가 input 분류입니다. 최초 읽을 때 isTextInput은 비공개였고 후속 읽기에서는 export가 붙어 있었습니다. 조사 도중 다른 작업의 로컬 변경이 관찰되므로 코딩 세션은 시작할 때 현 diff를 다시 확인해야 합니다. 이 조사자는 변경하지 않았습니다.

DOM을 전부 보존한다는 표현은 사용하지 않습니다. 이벤트 리스너, focus, selection, dirty value flag, checked, selected, JS 객체 동일성은 VNode의 기본 type·props·children만으로 복원하는 계약이 아닙니다. 이들을 근거 없이 필수로 추가하지 않습니다.

## 2. 근거의 지위와 정확한 출처

1. 현 Lark React Tests: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=ffbb46 . D열=ID, G열=시나리오, H열=입력, I열=기대. 이 문서의 inventory는 이름상자로 셀 이동 후 수식 textbox scoped snapshot으로 각 셀을 읽었습니다. 2~23행, 51행, 93~95행을 본 범위로 삼습니다. 검색 roundtrip은 8건으로 51~57행과 59행이며 52행부터는 Diff와 Patch 연결 테스트입니다.
2. 현 Lark README: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=Ojre1q . B5:E6은 UNIT와 INTEG 정의 및 Node + jsdom 실행 환경입니다. B13:C15는 기본·엣지 모두 필수, 선택은 미구현 시 skip입니다. L14:N14는 기본 type·문자열 props·children, L15:N15는 key 확장, L16:N16는 Phase 2 props 확장입니다.
3. mini-react/CONVENTION.md, '테스트': 기대값은 검사 대상 함수로 계산하지 않고 직접 적기, 내보낸 함수 호출로 동작 확인. '이름과 함수 > 이름' create=새로 만들어 돌려주기. 문서 역시 로컬에서 조사 중 변경이 관찰되어 절 제목을 인용합니다.
4. mini-react/GLOSSARY.md 'VNode': 문자열 또는 태그·속성·자식을 가진 객체. 문자열은 글자 노드 하나이며 HTML로 해석하지 않음. 'View': 최상위 VNode.
5. mini-react/docs/adr/0005-dom-and-vnode-conversion-rules.md: **frontmatter status: proposed**. 7행 책임, 11~15행 공백·주석·분리·빈 글자·소문자, 19행 literal Text, 23~25행 input 현재 .value 및 비입력 요소 제외, 35~40행 비교와 제외 범위. 로컬에 있다고 팀 승인된 것으로 간주하지 않습니다.
6. lab/m1-test-draft/M1-test-grilling.md: Decided D1~D19, Background B1~B8, Tests T1~T38, Open의 '오라버니의 브랜치와 로컬에서만 합의된 내용'과 보류를 읽었습니다. D19에 과거 Requirement의 ADR0004 변환 규칙을 ADR0005로 옮겼다고 명시합니다. 이 문서의 Closed는 개인 grilling 종료이지 팀 승인 상태가 아닙니다.
7. lab/m1-test-draft/vnode.test.draft.ts와 mini-react/src/vnode.test.ts: import 이후 본문이 줄바꿈을 정규화하면 동일함을 직접 비교했습니다. 로컬 T1~T37은 it, T38만 todo입니다. 통과 여부는 이번 조사에서 확인하지 않았습니다.

## 3. 검증성질 그룹

- **표현과 입력계약:** 빈 요소도 type·props·children이 있는 객체이고, children은 항상 배열입니다. creator의 루트 문자열 허용과 reader의 Element-only를 별도로 판단합니다.
- **태그와 속성:** HTML type 소문자, 속성 없음·하나·여럿·빈 값의 존재를 빠뜨리지 않으며 props 값은 문자열입니다. 속성 순서는 요구하지 않습니다.
- **자식의 구조:** 여러 형제와 재귀 깊이, mixed Text·Element 순서, 빈 요소의 위치를 보존합니다. 실제 DOM childNodes를 기준으로 하며 Text 합치기 여부는 명시합니다.
- **글자 의미:** DOM 엔티티는 파서가 이미 해석한 글자를 읽고, VNode의 &amp;나 <b>는 재해석하지 않는 literal입니다. 공백만·앞뒤 공백·빈 Text는 서로 다른 변수입니다.
- **주석 정책:** VNode에서 주석을 제외하더라도 입력 DOM 주석은 남깁니다. 주석 양옆 Text 경계를 보존할지 합의해야 하고, Patch의 주석 건너뛰기는 M2·M3입니다.
- **입력칸 상태:** 초기 value 속성, 현재 .value, 지운 빈 값, value 속성 없음은 독립 조건입니다. 속성을 복사한 뒤 현재값이 이겨야 한다는 순서 버그도 잡습니다.
- **비변경과 새 결과:** reader는 DOM의 값과 참조를 유지하고 creator는 VNode를 유지합니다. 같은 입력으로 두 번 만들 때 서로 다른 Node 및 하위 Node를 반환하는지를 별도로 봅니다.
- **왕복의 합성:** 두 함수를 이었을 때 정해진 정규형이 보존되는지만 확인합니다. 단독 기대값을 수기로 쓴 테스트와 짝지어 공통 오류가 숨는 것을 막습니다.
- **경계와 한계:** 일반 HTML과 문자열 props가 기본 범위입니다. 기존 Lark 깊이 500은 보존하되 무제한 깊이·폭·잘못된 입력·SVG 지원 요구로 확대하지 않습니다.

## 4. 현재 Lark inventory: 변환 단위 22건

아래 G·H·I는 inspected 셀 원문입니다. 현재 Lark 정의가 로컬 구현과 충돌해도 고치지 않고 그대로 보존했습니다.

| 행 | ID | 시나리오 원문(G) | 입력 원문(H) | 기대 원문(I) |
|---|---|---|---|---|
| 2 | fromdom-elem | 빈 div 하나를 VNode로 바꾸면 태그 이름만 담긴 깔끔한 객체가 나오는지 확인함 | 속성과 자식이 없는 <div></div>를 바꿈 | { type: 'div', props: {}, children: [] }을 돌려줌 |
| 3 | fromdom-text | 그냥 글자는 객체가 아니라 문자열 그대로 나오는지 확인함 | 글자가 hello인 텍스트 노드를 바꿈 | 문자열 'hello'를 돌려줌 |
| 4 | fromdom-attrs | 태그에 붙은 속성들(href, class, id)이 빠짐없이 옮겨지는지 확인함 | <a href=\"/x\" class=\"btn\" id=\"go\">를 바꿈 | props가 { href: '/x', class: 'btn', id: 'go' }이고 값은 모두 문자열임 |
| 5 | fromdom-nested | 태그 안에 태그가 있을 때 그 구조가 그대로 옮겨지는지 확인함 | <ul><li>a</li><li>b</li></ul>를 바꿈 | ul의 children에 li 두 개가 순서대로 있고, 각 li의 children은 ['a'], ['b']임 |
| 6 | fromdom-mixed-children | 글자와 태그가 섞여 있어도 순서가 바뀌지 않는지 확인함 | <p>안녕 <b>세상</b>!</p>를 바꿈 | p의 children이 ['안녕 ', b 요소 VNode, '!'] 순서임 |
| 7 | fromdom-empty | 자식이 없으면 '없음(null)'이 아니라 '빈 목록'으로 나오는지 확인함 | 자식이 없는 요소를 바꿈 | children이 null이나 undefined가 아닌 빈 배열 []임 |
| 8 | fromdom-bool-attr | 값 없이 이름만 있는 속성(disabled)도 사라지지 않는지 확인함 | 값 없이 적힌 속성이 있는 <input disabled>를 바꿈 | props.disabled가 빈 문자열 ''이어서 속성이 있다는 사실이 남음 |
| 9 | fromdom-skip-whitespace | 코드를 보기 좋게 하려고 넣은 줄바꿈과 띄어쓰기는 내용으로 치지 않는지 확인함 | 줄바꿈과 들여쓰기로 작성된 여러 줄짜리 HTML을 바꿈 | 공백만 있는 문자열은 어느 children에도 들어 있지 않음 |
| 10 | fromdom-keep-pre-space | 띄어쓰기가 화면에 그대로 보이는 pre 태그 안에서는 공백을 지우지 않는지 확인함 | <pre> 안에 들여쓰기와 줄바꿈이 있는 글을 바꿈 | pre 안의 공백과 줄바꿈이 글자 그대로 남음 |
| 11 | fromdom-skip-comment | HTML 주석은 화면에 안 보이므로 VNode에서 빠지는지 확인함 | <div><!-- 메모 --><span></span></div>를 바꿈 | 주석은 빠지고 div의 children에는 span 하나만 있음 |
| 12 | fromdom-comment-node | 주석 하나만 넣으면 '아무것도 없음'을 돌려주는지 확인함 | 주석 노드 자체를 넘김 | null을 돌려줌 |
| 13 | fromdom-tag-lowercase | 태그를 대문자로 써도 소문자 이름으로 통일되는지 확인함 | HTML 문서에서 대문자로 적힌 <DIV>를 바꿈 | type이 소문자 'div'임 |
| 14 | fromdom-special-chars | &lt; 같은 특수 표기가 실제 글자 <로 바뀌어 저장되는지 확인함 | 글자에 a &lt; b &amp; c처럼 HTML 특수 문자 표기가 들어 있음 | 문자열이 화면에 보이는 글자 그대로인 'a < b & c'임 |
| 15 | fromdom-deep | 태그가 아주 깊게 겹쳐 있어도 멈추거나 오류가 나지 않는지 확인함 | div가 500단계로 겹쳐 있는 DOM을 바꿈 | 오류 없이 깊이 500의 VNode를 돌려줌 |
| 16 | fromdom-no-mutate | 읽기만 해야 하는 함수가 원래 화면을 건드리지 않는지 확인함 | 바꾸기 전과 후에 원래 DOM의 outerHTML을 비교함 | 두 값이 같아서 원래 DOM이 바뀌지 않았음을 알 수 있음 |
| 17 | todom-elem | div VNode로 진짜 div 요소가 만들어지는지 확인함 | type이 div인 요소 VNode로 DOM을 만듦 | tagName이 DIV인 요소를 돌려줌 |
| 18 | todom-text | 문자열 VNode로 진짜 글자 노드가 만들어지는지 확인함 | 문자열 VNode 'hello'로 DOM을 만듦 | 글자가 hello인 텍스트 노드를 돌려줌 |
| 19 | todom-attrs | VNode의 속성들이 진짜 요소에 그대로 붙는지 확인함 | props에 class, id, href가 있는 VNode로 DOM을 만듦 | 세 속성이 모두 같은 값으로 요소에 붙어 있음 |
| 20 | todom-nested | 안쪽 자식까지 순서대로 전부 만들어지는지 확인함 | ul 아래 li가 세 개 있는 VNode로 DOM을 만듦 | ul 아래에 li 세 개가 같은 순서와 내용으로 있음 |
| 21 | todom-text-escape | 글자 안에 태그 모양이 있어도 태그가 아니라 글자로 보이는지 확인함 | 문자열 VNode '<b>x</b>'로 DOM을 만듦 | b 요소는 생기지 않고 화면에 <b>x</b>라는 글자가 그대로 보임 |
| 22 | todom-value-prop | 입력창의 값을 정하면 화면의 입력창에도 그 값이 실제로 들어가는지 확인함 | props가 { value: 'abc' }인 input을 만듦 | input.value가 'abc'임 |
| 23 | todom-no-mutate | 화면을 만드는 동안 설계도(VNode)를 건드리지 않는지 확인함 | DOM을 만들기 전과 후의 VNode를 비교함 | 두 VNode의 내용이 완전히 같음 |

### 현재 Lark 순수 왕복 통합 1건

| 행 | ID | 시나리오(G) | 입력(H) | 기대(I) |
|---|---|---|---|---|
| 51 | int-render-roundtrip | 설계도 → 화면 → 다시 설계도로 바꿨을 때 처음과 똑같은지 확인함 | 여러 태그와 속성이 섞인 View로 DOM을 만든 뒤, 그 DOM을 다시 VNode로 바꿈 | 처음 View와 내용이 같음 |

주의: 51행은 **VNode→DOM→VNode**입니다. 로컬 T34~T37은 **DOM→VNode→DOM**입니다. 예전 M1 문서에서 '팀 목록' 출처로 적은 빈 요소·한글 mixed·엔티티 왕복이 이번 현 Lark 51행의 원문 개별 행으로 존재한다고 주장하지 않습니다. 현행 범위를 확인한 결과와 과거 개인 설계의 출처 표현을 구별해야 합니다.

52~59행의 int-roundtrip-text, attr, children, replace, view-replace, sequence, int-preserve-identity, fuzz는 Diff와 Patch 통합 담당 범위입니다. 58행의 기존 Node === 유지 요구는 Patch 대상에 대한 요구이지 createDomFromVNode가 기존 Node를 재사용하라는 요구가 아닙니다.

### M9 key 확장: 기본 M1 필수와 구분

| 행 | ID | 입력(H) | 기대(I) |
|---|---|---|---|
| 93 | fromdom-key | <li data-key=\"a\">를 바꿈 | key가 'a'이고 props에도 'data-key': 'a'가 남아 있음 |
| 94 | fromdom-no-key | data-key가 없는 요소를 바꿈 | key가 null임 |
| 95 | todom-key-hidden | key는 'a'이고 props에는 data-key가 없는 VNode로 DOM을 만듦 | 요소에 key나 data-key 속성이 없음 |

93~95행 자체 F열은 기본 또는 엣지이지만 B열은 Phase 1 · key 확장, C열은 M9입니다. **key 확장을 선택한 경우의 규칙**과 **기본 M1의 필수**를 혼동하지 않습니다. 현 VNode 타입에는 key가 없으므로 이 보고서의 기본 후보는 이를 도입하지 않습니다. props의 data-key 보존은 기본 문자열 속성 보존으로 볼 수 있지만 별도 key 필드는 M9 계약입니다.

## 5. 로컬 기존 T1~T38 inventory와 재사용 경계

| 로컬 ID | 확인 대상 | 현 Lark 대응 | 코딩 세션 판단 |
|---|---|---|---|
| T1~T2 | 빈 div 객체, p 안 hello 문자열 | 2·3·7행 일부 | T2는 자식 Text이고 Lark 3행은 루트 Text. 동일 계약 아님 |
| T3~T6 | 주석 제외, 여러 깊이 주석, DOM outerHTML 불변, a/주석/b 분리 | 11·16행, 나머지 보완 | 이미 코드 있음, 팀 채택 여부 별도 |
| T7~T9 | 속성 하나·여럿·빈 hidden | 4·8행 | input disabled와 hidden은 동등한 빈 속성 변수지만 exact fixture 다름 |
| T10~T12 | 깊이, mixed 순서, 빈 자식 요소 | 5·6행, 빈 자식 보완 | 이미 코드 있음 |
| T13~T15 | 공백만 보존, 엔티티와 앞뒤 공백, 빈 Text 보존 | 9행과 충돌, 14행 일부 | 공백 정책 확정 전 자동 이식 금지 |
| T16~T21 | 비입력 요소 .value 제외, 초기·타이핑·덮어쓰기·지움·빈 input | 대응 reader 현재값 행 없음 | Lark 보완 후보이나 코드 신규 아님 |
| T22~T26 | 생성 요소·루트 Text·속성·빈 속성 | 17~19행, 빈 속성 보완 | 이미 코드 있음 |
| T27~T30 | 재귀, mixed 순서, 빈 요소, 공백 Text | 20행 및 보완 | 공백 정책 의존 분리 |
| T31~T33 | literal Text, 빈 Text, input.value 생성 | 21·22행, 빈 Text 보완 | 이미 코드 있음 |
| T34~T37 | DOM왕복 빈 요소·한글 mixed·특수문자·현재 input.value | 현 51행과 반대 방향 | 기존 코드 재사용 가능하지만 51행 자체 검증은 별도 필요 |
| T38(todo) | M2·M3 주석 섞인 노드 수정 | 이 조사 범위 밖 | 실행 테스트가 아님. 변환 기능 완료 증거로 계산 금지 |

현 로컬에 직접 대응 테스트가 안 보인 항목: Lark 루트 Text·루트 Comment 계약, pre 특례의 직접 사례, 정확히 깊이 500, 명시적 VNode 비변경, 새 Node 독립성, VNode→DOM→VNode 방향. absence는 두 파일을 읽은 범위에 한정하며 프로젝트 전체 다른 파일을 검색한 결론은 아닙니다.

## 6. 보완 후보: stable ID

상태 표기: **코드기존**은 테스트 중복생성 금지, **보강**은 현 assertion보다 강한 검사, **신규후보**는 이 두 테스트 파일에서 직접 대응을 못 본 경우입니다. 개인 규칙 기반 후보는 결정 의존을 반드시 유지합니다. 아래 범위의 '단위'는 두 함수 중 명시한 함수 하나만 호출해 수기로 적은 기대값과 비교합니다.

| ID | 상태·입력 → 기대 | 근거 | 실패 영향 | 범위 | 결정 의존 |
|---|---|---|---|---|---|
| CONV-N001 | 코드기존 T12: div 안 빈 span → span 객체와 children:[] 유지 | VNode 정의, Lark 2·7행에서 자식까지 파생 | 빈 자리 소실, 후속 child index 어긋남 | reader 단위 | 빈 자식을 버리지 않는 계약 |
| CONV-N002 | 코드기존 T4: 여러 깊이에 여러 주석 → 모두 제외, 주변 요소·글자 유지 | Lark 11행, M1 T4 | 안쪽 주석이 데이터로 섞이거나 자식 누락 | reader 단위 | 루트 Comment와 별개로 child 주석 제외는 Lark 명시 |
| CONV-N003 | 코드기존 T6: a<!--x-->b → ['a','b'], 합치지 않음 | proposed ADR0005:13, 개인 D7·B1 | 뒤의 노드 위치 비교가 틀림 | reader 단위 | 팀 Text 경계 정책 채택 필요 |
| CONV-N004 | 코드기존 T13: b(a), 공백 하나, i(b) → 공백 Text 보존 | proposed ADR0005:11, 개인 D5·T13 | a b가 ab가 됨 | reader 단위 | **Lark 9행과 직접 충돌**, 임의 채택 금지 |
| CONV-N005 | 코드기존 T15: append(Text(''),b(x)) → ['',b객체] | proposed ADR0005:14, 개인 B4 | 빈 Text와 다음 요소 index가 어긋남 | reader 단위 | trim 기반 공백 삭제가 빈 문자열도 버리는지 명시 필요 |
| CONV-N006 | 코드기존 T14: 엔티티 포함 HTML → 해석된 <, &, 앞뒤 공백 그대로 | Lark14, GLOSSARY 문자열, 개인 T14 | 이중 디코딩 또는 trim으로 데이터 손실 | reader 단위 | 앞뒤 공백 정책을 공백-only와 별도로 정하기 |
| CONV-N007 | 코드기존 T17: input value='a', 현재값 미변경 → props.value='a' | Lark22의 역방향은 단독 근거 아님, proposed ADR0005:23 | 초기 표시값 소실 | reader 단위 | 현재값을 props.value에 저장하는 팀 결정 |
| CONV-N008 | 코드기존 T18: value 속성 없는 input, .value='typed' → value:'typed' | proposed ADR0005:23, 개인 D15 | 사용자가 친 내용이 Diff 입력에 안 들어감 | reader 단위 | 동일 |
| CONV-N009 | 코드기존 T19: attribute='a', .value='typed' → typed가 우선 | proposed ADR0005:23, 개인 T19 | 속성 복사가 현재값을 덮어 씀 | reader 단위 | 동일 |
| CONV-N010 | 코드기존 T20: attribute='a', .value='' → value 키 존재 및 '' | proposed ADR0005:23, 개인 D16·B6 | 지운 값을 제거 Patch로 오해, 과거 값 잔류 가능 | reader 단위, M3 결과는 미검증 | 빈 value 생략 여부 팀 결정 |
| CONV-N011 | 코드기존 T21: untouched input → value:'' 명시 | proposed ADR0005:23·35, 개인 D16 | 같은 빈 화면의 표현이 둘이 됨 | reader 단위 | 동일. 원본 outerHTML 동일 왕복은 기대하면 안 됨 |
| CONV-N012 | 코드기존 T16: li·button의 기본 .value를 읽지 않음; 보강 시 명시 value 속성은 문자열로 보존 | proposed ADR0005:25, Lark4 | 존재하지 않은 value 속성 생성, 목록 번호 변경 | reader 단위 | input 대상 범위 확정. 명시 attribute 복사와 property 제외를 혼동 금지 |
| CONV-N013 | 보강 T5·Lark16: DOM·child 참조, 주석, Text.data, attributes, input.value를 읽기 전후 비교 → 모두 동일 | Lark16 비변경 책임, create 동사 | 읽기만 했는데 화면 또는 현재 입력값 변경 | reader 단위 | 정책과 무관하게 비변경. outerHTML만으로 .value·참조 변경 검출 불가 |
| CONV-N014 | 코드기존 T26: props hidden:'' → hasAttribute true, getAttribute=='' | Lark8의 생성방향 파생, GLOSSARY props | hidden 또는 disabled 등 존재 의미 소실 | creator 단위 | 별도 없음, input fixture이면 .value 검사와 분리 |
| CONV-N015 | 코드기존 T28·T29: mixed ['one',b,'three'] 및 빈 span → childNodes 순서와 종류 유지 | Lark20, 기본 children 정의 | 문장 순서 변경, 빈 자리 삭제 | creator 단위 | 별도 없음 |
| CONV-N016 | 코드기존 T30: [b,' ',i] → 가운데 Text(' ') 유지 | GLOSSARY Text 하나, 개인 T30 | 화면 띄어쓰기 소실 | creator 단위 | reader 공백 정책과 별개로 문자열 생성 계약 확인 |
| CONV-N017 | 코드기존 T32: children:[''] → childNodes.length=1, nodeType TEXT_NODE | GLOSSARY Text 하나, 개인 B4·T32 | 빈 자리 소실, index 어긋남 | creator 단위 | 빈 문자열도 한 Text로 보는 계약 팀 확인 |
| CONV-N018 | 코드기존 T31 보강: literal '  a &amp; <img ...>  ' → Text 하나, 데이터 동일, img 요소 없음 | GLOSSARY8, Lark21 | HTML 주입, 글자 소실, 엔티티 이중 해석 | creator 단위 | 기존 문자열 정의로 지지. 스크립트 실행 테스트를 굳이 만들 필요 없음 |
| CONV-N019 | 신규후보·Lark23 코드화: nested VNode와 props·children snapshot → 생성 후 깊은 값 동일 | Lark23, create 동사 | 재사용 VNode·History 기준값 오염 | creator 단위 | 없음. 기대 snapshot을 SUT로 계산 금지 |
| CONV-N020 | 신규후보: 같은 VNode로 두 번 생성 → root와 각 하위 Node는 !==, 한 결과 수정해도 다른 결과·VNode 불변 | CONVENTION create=새로 만들어 반환 | DOM 공유로 다른 render 결과가 이동·오염 | creator 단위 | 새 결과 책임에 근거. Patch identity 유지와 구분 |
| CONV-N021 | 신규후보·보류: 루트 Text('hello') → 'hello'; 루트 Comment → null | 현 Lark3·12 | 목록대로 작성한 테스트가 타입검사부터 실패 | reader 단위 | **Node 입력 및 VNode 또는 null 반환으로 넓힐지 결정 먼저**. as unknown 캐스팅으로 덮지 않기 |
| CONV-N022 | 기존Lark 검증 이식 후보: pre의 들여쓰기·줄바꿈 원문 유지, 깊이500 트리의 depth 확인 | Lark10·15 | pre 표시 손실 또는 깊은 재귀 실패 | reader 단위 | pre 예외와 일반 공백 정책 정합성. 깊이500은 현 행의 구체치이지 무제한 보장 아님 |

### 왕복 후보

| ID | 상태·입력 → 기대 | 근거 | 실패 영향 | 범위 | 결정 의존 |
|---|---|---|---|---|---|
| ROUND-N001 | 신규방향·Lark51 코드화: 태그·문자열 속성·mixed children을 가진 **정규형 요소 VNode** → DOM → 처음과 깊은 값 동일 | Lark51 G:H:I 원문, README INTEG | 두 함수의 표현 규칙이 안 맞음 | 두 함수만, VNode→DOM→VNode | input을 넣으면 value:'' 정규형 여부, whitespace 정규형 여부 명시 |
| ROUND-N002 | 코드기존 T34: div 안 빈 span DOM → 왕복 후 isEqualNode true | 개인 D18·T34, 기본 children | History 복원 시 빈 자리 소실 | 두 함수, DOM→VNode→DOM | 대응 단위 CONV-N001 및 creator 빈 요소 검증과 짝 |
| ROUND-N003 | 코드기존 T35·T36: 한글 mixed, 앞뒤 공백·엔티티 DOM → 구조와 글자 동일 | 개인 T35·T36, Lark6·14 | 문장·문자 데이터가 변함 | 두 함수, DOM 방향, isEqualNode | 공백-only 포함 여부를 명시하고 N004 결정과 연결 |
| ROUND-N004 | 코드기존 T37 보강: input의 attribute='a', 현재 .value='typed' → 왕복 결과 .value='typed'; 지운 ''도 별도 | proposed ADR0005:23·35, 개인 T37 | 복원 입력칸이 과거 초기값 또는 빈 값으로 바뀜 | 두 함수, **.value 직접 비교** | input 대상범위·빈값정책 팀 결정. isEqualNode만 사용 금지 |
| ROUND-N005 | 신규후보: input 미변경 빈값을 두 번 왕복 → 합의한 props.value 정규형에서 안정됨 | 개인 D16·ADR0005:35 | 왕복할 때마다 표현이 바뀌어 가짜 Diff 발생 | 두 함수, 정규형 확인 | value:'' 명시 채택 시만. 첫 원본 DOM과 attribute 동일성 요구 금지 |
| ROUND-N006 | 보류후보: 주석 포함 DOM → 출력에는 주석 없이 두 Text 경계 유지, 원본 주석은 그대로 | Lark11, 개인 B1·B8 | 정규화 또는 원본보존이 깨짐 | 두 함수 합성의 **의도적 정보손실**, 동등왕복 아님 | 정책 채택 필요. 기존 개인 D18은 주석 DOM을 동등왕복에 쓰지 않음. 이름도 equality 왕복과 분리 |

모든 왕복에 테스트를 추가하라는 뜻은 아닙니다. 먼저 기존 단위 기대값으로 동일 변수를 확인하고, 대표 합성 사례만 남깁니다. 예: 두 함수가 class를 서로 같은 잘못된 값으로 바꾸거나, reader가 Text 둘을 합치고 creator도 그 합침을 유지하면 특정 화면 왕복만으로 표준 VNode 위반을 못 볼 수 있습니다. VNode→DOM→VNode 역시 양쪽이 같은 잘못된 인코딩을 쓰면 통과할 수 있습니다.

## 7. 결정 필요 목록

| 결정 | 충돌·공백의 정확한 출처 | 권고와 이유 | 영향 후보 |
|---|---|---|---|
| D-CONV-1 일반 공백-only Text 삭제 또는 보존 | Lark D9/H9/I9 '공백만 있는 문자열은 어느 children에도 들어 있지 않음' 대 ADR0005:11·개인 D5/T13·로컬 T13의 보존 | **보존을 선호**: inline 사이 띄어쓰기와 노드 위치를 잃지 않음. 하지만 현행 팀 결정을 바꿨다고 처리하지 않음. 들여쓰기와 화면의 공백을 구별하는 정책이면 CSS white-space와 pre 경계도 추가 결정 필요 | N004·N005·N006·N016·N022, ROUND3 |
| D-CONV-2 reader 루트 입력 및 null | Lark3 루트 Text→문자열, Lark12 루트 Comment→null 대 src/vnode.ts20 Element→VNode 및 개인 B2 최상위 객체 | 코딩 전에 한 계약으로 정하기. **Element-only 유지 시 Lark는 child Text와 child Comment 사례로 고쳐야 하며**, 이 변경은 승인 후 별도 작업. Node 지원을 고르면 타입·모든 호출자와 null 처리를 함께 변경 | N021, ROUND1 루트문자열 |
| D-CONV-3 현재 input .value와 빈 value 정규형 | Lark22는 creator 현재값만 명시. reader 현재값·항상 빈값은 proposed ADR0005:23, 개인 D14~D16·T17~T21 | 현재 .value를 저장하는 쪽 선호: 사용자 입력을 얻는 목적과 맞음. 초기 attribute와 current property는 별개임을 계약에 쓰기 | N007~N012, ROUND4~5 |
| D-CONV-4 입력칸 대상범위 | proposed ADR0005:23·38은 input 중 checkbox/radio 제외, textarea/select 등 제외. Lark22는 단순 input | 기본 테스트는 text input으로 한정하고 나머지 지원을 필수로 넓히지 않기. type=number 등 sanitization, file처럼 값 할당 제한이 있는 타입까지 무조건 '입력칸 모두'라 주장하지 않기 | 현재값 테스트 전체 |
| D-CONV-5 Text 경계와 빈 Text | 개인 D7·D13·B1·B4, proposed ADR0005:13~14; 현 Lark는 이 경계 구체 기대 없음 | 한 Text→한 문자열을 선호: Glossary와 이후 child 위치 대응에 유리. DOM.normalize로 합치기 또는 빈 문자열 필터 금지 여부를 팀 문서에서 확정 | N003·N005·N017, ROUND6 |
| D-CONV-6 왕복 방향과 동등성 | 현 Lark51은 VNode→DOM→VNode; 개인 D2·T34~37은 DOM→VNode→DOM; ADR35~36은 input·주석 equality 예외 | 두 방향을 별도 이름으로 유지. 지원 범위의 정규형에만 정확한 equality 요구. current .value는 직접 비교 | ROUND 전체 |
| D-CONV-7 M9 key 채택 여부 | README L15:N15, React Tests B93:C95 및 H:I | 기본 type·문자열props·children과 분리. M9를 선택할 때만 key↔data-key 불대칭의 왕복 예외를 따로 설계 | 현재 기본 후보에서는 제외 |

### 비교 수단의 한계

- isEqualNode는 노드 종류, 태그와 attributes, children 등 구조 비교에 쓰지만 input의 현재 .value를 비교하지 않습니다. 같은 value attribute를 가진 input 둘의 현재값이 달라도 구조상 같을 수 있습니다. 입력칸에는 반드시 .value assertion이 필요합니다.
- outerHTML은 현재 .value, JS Node 참조, 빈 Text를 충분히 보여주지 못합니다. reader 불변의 보강은 값과 원래 참조를 직접 확인합니다.
- textContent만 비교하면 mixed child의 태그·순서·Text 경계 손실을 놓칩니다. childNodes 개수, 각 nodeType과 값도 봅니다.
- DOM 파서 fixture가 이미 엔티티를 해석합니다. reader 입력 'a &lt; b'의 기대 'a < b'와 creator 입력 literal '&lt;'의 기대 '&lt;' Text는 반대 규칙이 아니라 입력 단계가 다른 것입니다.
- 생성된 새 input에서는 setAttribute('value',x)만으로 .value가 보일 수 있습니다. T33 또는 Lark22 통과가 M3에서 dirty input 값을 갱신하는 구현까지 증명하지는 않습니다.

## 8. 코딩 세션 handoff

1. 현재 브랜치와 src/vnode.ts·vnode.test.ts·CONVENTION·GLOSSARY diff부터 읽습니다. 이번 조사 중 동시 변경이 관찰되었습니다. 남의 작업을 덮어쓰지 않습니다.
2. 위 결정 D-CONV-1~6을 팀 결정 근거와 함께 정합니다. proposed ADR0005와 취소 PR #18의 개인 정의를 승인 근거로 대신하지 않습니다. 이 단계에서 Lark 또는 테스트를 임의 수정하지 않습니다.
3. 현 Lark 22개 단위와 51행을 기준 inventory로 보존합니다. 이미 로컬에 있는 T1~T37을 재작성하지 말고 후보 ID와 매핑합니다. Lark가 빠진 내용만 후보로 표시합니다.
4. 테스트 기대값은 직접 씁니다. 단위 테스트에서 반대 변환 함수를 oracle로 삼지 않습니다. 왕복은 단위 테스트와 짝지으며 Patch·Diff·History·hooks를 호출하지 않습니다.
5. 지원 대상 HTML, 공백 정책, input 정규형, 루트 계약을 fixture에 명시한 뒤 새 assertion이 실제로 해당 오류를 잡는지 확인합니다. 이 보고서 자체에는 실행 결과가 없습니다.

필수 확장으로 넣지 않는 것: 임의 null·undefined·유효하지 않은 태그와 속성 입력의 런타임 규칙, SVG와 namespace, template content, 제한 없는 대형 입력과 시간 예산, 이벤트 함수 props와 hooks, checked와 selected 복원. Lark15의 깊이500은 이미 있는 구체 테스트 정의라 inventory에는 유지합니다.

## 9. 읽은 범위·모르는 점·부모용 요약

- 읽은 파일: 요청한 M1-test-grilling.md 전체, vnode.test.draft.ts 본문, CONVENTION.md 전체, GLOSSARY.md 전체, src/vnode.ts 전체, src/vnode.test.ts 전체, ADR0005 전체. 초안과 현재 테스트는 import 이후 동일했습니다.
- 읽은 웹: 새 Lark 조사 탭 두 개에서 README 지정 셀과 React Tests 2~23·51·93~95행 원문, roundtrip 검색 8개 위치, 58행의 경계 참고. 두 조사 탭은 작업 종료 때 닫았습니다. 사용자 기존 탭은 닫거나 수정하지 않았습니다.
- 모르는 점: 현재 main과의 차이, PR #18 취소 화면과 #20 현 승인·병합 상태, proposed ADR의 후속 승인, 팀의 공백·루트·입력칸 정책 최종 결정, 테스트 실행 결과. claude-mem 조회는 PowerShell 도구가 WSL cwd 준비에서 실패하여 결과를 받지 못했습니다. 이 실패는 소스 접근 실패가 아니며 파일은 REPL fs로 읽었습니다.
- 결정: 이번 조사에서는 팀 동작을 새로 결정하지 않았습니다. 보존 선호와 결정 필요를 구별했고 source·tests·Lark 수정 및 실행을 하지 않았습니다.
- 부모용 요약: 현 Lark 변환 단위22건과 순수왕복1건을 확보했습니다. **가장 큰 충돌은 공백-only 삭제 대 보존, 루트 Text·Comment 지원 대 Element-only 시그니처**입니다. **Lark51 방향은 VNode→DOM→VNode**이며 로컬 T34~37과 반대입니다. 현재값 input 다섯 상태 등 대부분 보완안은 로컬 T에 이미 있으므로 코드 신규로 오인하지 마세요. creator 입력 VNode 비변경·새 Node 독립성과 Lark51 방향은 직접 테스트가 비어 있는 보완 지점입니다. M9 key는 기본 M1과 분리했습니다.


## 10. 부모 요청 추가: U-INPUT 공개 협력 함수

### 책임과 현재 협력 관계

isTextInput(element: Element): element is HTMLInputElement는 입력 요소 중 현재 .value를 화면 상태로 다루는 대상을 분류합니다. reader와 Patch가 같은 입력칸 분류를 사용하게 하는 공개 협력 함수입니다.

2026-11-09T03:59:42.539Z에 src/patch.ts 원문을 추가로 읽었습니다. 2행에서 isTextInput을 vnode에서 import하고 applyPropsToNode가 name === "value" && isTextInput(node)일 때 node.value에 씁니다. 따라서 export를 '테스트만을 위한 공개'라고 추정하면 안 됩니다. 이 조사에서는 Patch 구현의 정확성을 검증하지 않고 생산 코드의 사용 사실만 확인했습니다.

### U-INPUT 검증성질과 후보

| ID | 입력 → 기대 | 근거 | 실패 영향 | 범위 | 기존과 중복 및 결정 의존 |
|---|---|---|---|---|---|
| U-INPUT-N001 | input type=text 및 기본 input → true | src/vnode.ts의 공개 type guard, proposed ADR0005:23 | reader에서 타이핑 값을 놓치거나 Patch에서 attribute로 잘못 씀 | isTextInput 직접 단위, Boolean assertion | reader T17~21은 간접검증. text 대표값 하나와 기본값만 사용, 모든 inputtype 열거 금지 |
| U-INPUT-N002 | input type=checkbox 또는 radio → false | proposed ADR0005:23·38, 현 분류 조건 | .checked가 상태인 컨트롤에 .value 규칙을 잘못 적용 | 직접 단위 | 해당 컨트롤의 상태 복원을 구현하라는 뜻 아님. 두 제외 경계를 한 parameterized 사례로 묶을 수 있음 |
| U-INPUT-N003 | li 또는 button → false | proposed ADR0005:25, 개인 D14·T16 | 비입력 요소 .value를 현재 입력 상태로 취급해 잘못된 props 생성 | 직접 단위 | T16 간접검증과 구분. 두 대표 fixture 이상 무한 열거 불필요 |

**추가 대상 권고:** 부모의 Phase1 전체 대상 목록에는 U-INPUT을 독립 책임으로 올리되, 변환 테스트 전체를 다시 만들지 않고 위 분류 경계만 직접 검사합니다. 기존 T16~T21과 Patch의 입력값 반영 검사는 협력 검증으로 그대로 둡니다. 별도 invalid 입력, textarea·select의 범용 타입 분류, 모든 input subtype 지원 보장은 이번 추가의 범위가 아닙니다. ADR0005가 proposed인 지위는 그대로 유지합니다.

### 파일 관찰시각과 mtime

| 파일 | 2026-11-09T03:59:42.539Z에 관찰한 mtime(UTC) |
|---|---|
| src/vnode.ts | 2026-11-09T03:53:28.727Z |
| src/vnode.test.ts | 2026-11-08T19:43:13.626Z |
| src/patch.ts | 2026-11-09T03:54:38.109Z |
| CONVENTION.md | 2026-11-09T03:55:13.322Z |
| GLOSSARY.md | 2026-11-09T03:55:13.317Z |
| docs/adr/0005-dom-and-vnode-conversion-rules.md | 2026-11-07T13:23:37.127Z |

이는 **해당 관찰시점의 상태**이며 이 문서 작성 후에도 작업 트리는 바뀔 수 있습니다. 코딩 세션은 최신 파일을 다시 확인해야 합니다. 소스 mtime 변화나 export 자체로 승인·병합을 추론하지 않았습니다.
