# Phase 1 테스트 사례 재고와 보완 후보

관찰일: 2026-11-09. 실행 결과가 아니라 코드 생성 입력이다. 상위 정의와 최신 결정 상태는 phase1-test-design.md를 따른다. Lark 기존 표현(CREATE 포함)은 출처 보존용이며 현재 로컬안에 맞춰 조용히 바꾸지 않았다. 후보 ID는 추적 단위이지 신규 실행 테스트 개수가 아니다. 같은 ID 안의 조건은 필요한 만큼 매개변수화할 수 있고, 이미 코드가 있는 부분은 재사용한다.

## 읽는 순서

1. 대상 정의와 결정표를 읽는다. 2. 아래 기존 사례를 빠짐없이 매핑한다. 3. 보완 후보의 기존 코드 대응을 확인한다. 4. 미정 의존만 blocked로 분리한다.

## 기존 사례 전체 색인

| 시트 행 | ID | 레벨 | 분류 | 상세 소유 |
|---|---|---|---|---|
| 2 | fromdom-elem | 단위 | 기본·엣지 | 변환 |
| 3 | fromdom-text | 단위 | 기본·엣지 | 변환 |
| 4 | fromdom-attrs | 단위 | 기본·엣지 | 변환 |
| 5 | fromdom-nested | 단위 | 기본·엣지 | 변환 |
| 6 | fromdom-mixed-children | 단위 | 기본·엣지 | 변환 |
| 7 | fromdom-empty | 단위 | 기본·엣지 | 변환 |
| 8 | fromdom-bool-attr | 단위 | 기본·엣지 | 변환 |
| 9 | fromdom-skip-whitespace | 단위 | 기본·엣지 | 변환 |
| 10 | fromdom-keep-pre-space | 단위 | 기본·엣지 | 변환 |
| 11 | fromdom-skip-comment | 단위 | 기본·엣지 | 변환 |
| 12 | fromdom-comment-node | 단위 | 기본·엣지 | 변환 |
| 13 | fromdom-tag-lowercase | 단위 | 기본·엣지 | 변환 |
| 14 | fromdom-special-chars | 단위 | 기본·엣지 | 변환 |
| 15 | fromdom-deep | 단위 | 기본·엣지 | 변환 |
| 16 | fromdom-no-mutate | 단위 | 기본·엣지 | 변환 |
| 17 | todom-elem | 단위 | 기본·엣지 | 변환 |
| 18 | todom-text | 단위 | 기본·엣지 | 변환 |
| 19 | todom-attrs | 단위 | 기본·엣지 | 변환 |
| 20 | todom-nested | 단위 | 기본·엣지 | 변환 |
| 21 | todom-text-escape | 단위 | 기본·엣지 | 변환 |
| 22 | todom-value-prop | 단위 | 기본·엣지 | 변환 |
| 23 | todom-no-mutate | 단위 | 기본·엣지 | 변환 |
| 24 | diff-same | 단위 | 기본·엣지 | Diff·Patch |
| 25 | diff-text | 단위 | 기본·엣지 | Diff·Patch |
| 26 | diff-tag | 단위 | 기본·엣지 | Diff·Patch |
| 27 | diff-text-to-elem | 단위 | 기본·엣지 | Diff·Patch |
| 28 | diff-attr-change | 단위 | 기본·엣지 | Diff·Patch |
| 29 | diff-attr-add | 단위 | 기본·엣지 | Diff·Patch |
| 30 | diff-attr-remove | 단위 | 기본·엣지 | Diff·Patch |
| 31 | diff-child-add | 단위 | 기본·엣지 | Diff·Patch |
| 32 | diff-child-remove | 단위 | 기본·엣지 | Diff·Patch |
| 33 | diff-child-insert-middle | 단위 | 기본·엣지 | Diff·Patch |
| 34 | diff-deep | 단위 | 기본·엣지 | Diff·Patch |
| 35 | diff-multi | 단위 | 기본·엣지 | Diff·Patch |
| 36 | diff-remove-all | 단위 | 기본·엣지 | Diff·Patch |
| 37 | diff-from-empty | 단위 | 기본·엣지 | Diff·Patch |
| 38 | diff-no-mutate | 단위 | 기본·엣지 | Diff·Patch |
| 39 | diff-invalid-arg | 단위 | 기본·엣지 | Diff·Patch |
| 40 | patch-text | 단위 | 기본·엣지 | Diff·Patch |
| 41 | patch-replace | 단위 | 기본·엣지 | Diff·Patch |
| 42 | patch-props-set | 단위 | 기본·엣지 | Diff·Patch |
| 43 | patch-props-remove | 단위 | 기본·엣지 | Diff·Patch |
| 44 | patch-create | 단위 | 기본·엣지 | Diff·Patch |
| 45 | patch-remove | 단위 | 기본·엣지 | Diff·Patch |
| 46 | patch-view-replace | 단위 | 기본·엣지 | Diff·Patch |
| 47 | patch-empty | 단위 | 기본·엣지 | Diff·Patch |
| 48 | patch-value-prop | 단위 | 기본·엣지 | Diff·Patch |
| 49 | patch-invalid-path | 단위 | 기본·엣지 | Diff·Patch |
| 50 | patch-mutation-count | 단위 | 기본·엣지 | Diff·Patch |
| 51 | int-render-roundtrip | 통합 | 기본·엣지 | 변환 |
| 52 | int-roundtrip-text | 통합 | 기본·엣지 | Diff·Patch |
| 53 | int-roundtrip-attr | 통합 | 기본·엣지 | Diff·Patch |
| 54 | int-roundtrip-children | 통합 | 기본·엣지 | Diff·Patch |
| 55 | int-roundtrip-replace | 통합 | 기본·엣지 | Diff·Patch |
| 56 | int-roundtrip-view-replace | 통합 | 기본·엣지 | Diff·Patch |
| 57 | int-roundtrip-sequence | 통합 | 기본·엣지 | Diff·Patch |
| 58 | int-preserve-identity | 통합 | 기본·엣지 | Diff·Patch |
| 59 | int-roundtrip-fuzz | 통합 | 기본·엣지 | Diff·Patch |
| 60 | hist-empty | 단위 | 엣지 | History |
| 61 | hist-push-one | 단위 | 기본 | History |
| 62 | hist-back | 단위 | 기본 | History |
| 63 | hist-forward | 단위 | 기본 | History |
| 64 | hist-back-at-start | 단위 | 엣지 | History |
| 65 | hist-forward-at-end | 단위 | 엣지 | History |
| 66 | hist-push-truncates | 단위 | 기본 | History |
| 67 | hist-isolation-input | 단위 | 엣지 | History |
| 68 | hist-isolation-output | 단위 | 엣지 | History |
| 69 | hist-max-size | 단위 | 선택 | History |
| 70 | verify-layout | 기능 | 기본 | 페이지 |
| 71 | verify-load | 기능 | 기본 | 페이지 |
| 72 | verify-load-buttons | 기능 | 기본 | 페이지 |
| 73 | verify-edit-no-apply | 기능 | 기본 | 페이지 |
| 74 | verify-patch-apply | 기능 | 기본 | 페이지 |
| 75 | verify-patch-partial | 기능 | 기본 | 페이지 |
| 76 | verify-patch-history | 기능 | 기본 | 페이지 |
| 77 | verify-attr-edit | 기능 | 기본 | 페이지 |
| 78 | verify-delete-node | 기능 | 기본 | 페이지 |
| 79 | verify-many-tags | 기능 | 기본 | 페이지 |
| 80 | verify-patch-nochange | 기능 | 엣지 | 페이지 |
| 81 | verify-back | 기능 | 기본 | 페이지 |
| 82 | verify-forward | 기능 | 기본 | 페이지 |
| 83 | verify-back-to-start | 기능 | 엣지 | 페이지 |
| 84 | verify-back-then-patch | 기능 | 엣지 | 페이지 |
| 85 | verify-empty-input | 기능 | 엣지 | 페이지 |
| 86 | verify-multi-top | 기능 | 엣지 | 페이지 |
| 87 | verify-invalid-html | 기능 | 엣지 | 페이지 |
| 88 | verify-no-script-exec | 기능 | 엣지 | 페이지 |
| 89 | verify-rapid-click | 기능 | 엣지 | 페이지 |
| 90 | verify-back-partial | 기능 | 선택 | 페이지 |
| 91 | verify-patch-log | 기능 | 선택 | 페이지 |
| 92 | verify-highlight | 기능 | 선택 | 페이지 |

# A. DOM과 VNode 변환 및 왕복

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

# B. Diff와 Patch 및 연결

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
- 입력: old는 <div><section id="left"><p>a</p><p>b</p><p>c</p></section><aside>s</aside></div>, new는 <div><section id="left" class="active"><p>A<b>new</b></p><p>b</p></section><aside>s</aside></div>에 대응하는 수기 VNode다. 마지막 p(c) 삭제, section class 추가, 첫 p의 Text 변경과 b 자식 추가를 섞는다. 사전상태는 두 View와 입력 snapshot이며 실제 DOM refs는 이 단위 테스트에 필요 없다. 동작: diff.
- 기대: 단위에서는 직접 작성한 기대 Patch의 종류·경로·payload와 비교하고 aside 등 변경 밖을 가리키는 지시가 없음을 확인한다. 최종 DOM과 refs는 DP-N04에서 검사한다. 현재 로컬안대로 앞 Patch 적용 후 path와 비교→INSERT정순→REMOVE역순의 계약을 반영한다. 왜:35는 글자+속성만,32는 삭제만. 범위:UNIT D5,DP-N04와 짝. 결정 의존:D-01,D-02.

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
- 입력:TEXT/PROPS 1개 batch와 INSERT 1개 batch를 각각 분리. 사전상태:첫 적용 후 DOM. 동작:동일 목록 재적용.
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
- 입력: DIFF-N05에 고정한 old/new 대표쌍. 사전상태: old root div, section(경로[0]), 첫 p([0,0]), 둘째 p([0,1]), aside([1])의 실제 refs와 삭제할 셋째 p([0,2])를 저장한다. 동작: diff→patch→readback.
- 기대: 내용은 new와 일치하고 old root·section·첫 p·둘째 p·aside는 같은 위치의 new 노드와 ===다. 셋째 p만 부모에서 제거되고 첫 p 안의 b는 새 노드다. 중간 삭제처럼 내용상 같은 항목이 다른 index로 이동한 경우에 old 항목 identity 유지를 강제하지 않는다. 왜:32·35·54가개별성공해도batch경로실패가능. 범위:INTEG D5/P2. 결정 의존:Patch내부읽지않음,기본index와key최적화를혼동하지않음.

### DP-N05 comment·whitespace·빈Text mapping 연결
- 입력:DOM API로만든emptyText,공백Text,주석,일반Text,span이있는실제DOM과span글자만다른new View. 사전상태:각실제ref와DOM구조기록. 동작:read→diff→patch→read.
- 기대:의도span만바뀌고주변Text·Element참조유지;주석제외VNode기준위치가정확. 왜:readback내용만보면주석누락과동일내용노드교체를놓침. 범위:INTEG P3. 결정 의존:D-04,D-08;주석보존그자체는별도정책. DOM전체isEqualNode를주석제거왕복oracle로쓰지않음.

### DP-N06 연속갱신과 fuzz 관찰 보강
- 입력:기존57 A→B→C→A에한번의빈text/value및구조변경대표를넣고,기존59고정seed생성기는유효Phase1범위로제한. 사전상태:단계별기대View와변경밖refs. 동작:매단계새read/diff/patch,실패seed출력.
- 기대:각단계내용·.value·생존refs를독립관찰. 왜:최종A만맞는상쇄실패와isEqualNode의property맹점방지. 범위:INTEG기존57/59보강,새500×모든edge곱금지. 결정 의존:D-04,D-05;같은batch재적용은이후보아님.

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

## 부모 통합 보완: DIFF-N08 호출 간 독립성

- 상태: 추가 후보. 현재 소스에 이미 있는지 코드 생성 전 검색한다.
- 입력과 사전상태: 서로 다른 B와 C를 갖는 A/B/C View를 직접 작성한다. A와 첫 반환 목록을 기록한다.
- 동작: diffViews(A,B), 이어 diffViews(A,C)를 호출한다.
- 기대: 두 번째 결과는 A→C의 차이만 나타내고 첫 반환 목록과 A/B/C는 다음 호출로 바뀌지 않는다. 구체 Patch 표현은 DEC-05의 채택 계약에 맞춘다.
- 이유: 내용 불변만으로 공용 결과 배열의 누적·재사용을 잡지 못한다.
- 범위: U-DIFF 단위. 같은 입력의 무한 반복이나 시간 성능 요구가 아니다.


# C. StateHistory와 복원 연결

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

### HR-N01 · 초기 상태 저장과 첫 변경의 연결
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
- 기대: 실제 변경 없는 A는 새 이력을 만들지 않음. 빈 입력·다중 root 거절은 현재 View, 저장된 내용 전체, 이동 가능 상태, 실제 영역과 기존 redo 재방문을 모두 보존한다. 정상 무변경 Patch를 과거 위치에서 누르는 경우의 redo 보존만 D7(상위 DEC-09)에서 결정한다.
- 필요성: 행80,85,86은 이미 no-op과 거절 시 이력 보존을 요구한다. 버튼 메시지는 이 테스트 소유가 아니며 이력 측면만 검증한다.
- 범위: INTEG. 결정의존: D7은 정상 무변경 Patch의 비교 의미와 과거 위치 redo에만 적용한다. 거절 입력의 이력 전체 보존은 기존 verify-empty-input·verify-multi-top의 기대를 구체화한 assertion이며 미정으로 두지 않는다. 내부 snapshots를 공개하지 않고 공개 이동 결과로 보존을 관찰한다.

### HR-N06 · 미저장 편집 중 이동
- 입력: 저장 A→B→C에서 B 복원 후 테스트 영역만 X로 편집.
- 사전상태: 실제 B, 이력현재 B, 테스트 영역 X.
- 동작: 뒤로 또는 앞으로 이동.
- 기대: D8 전 미정. 대안① X를 버리고 대상 A/C를 두 영역에 복원. 대안② 이동 전에 명시적으로 X를 저장. 대안③ 이동을 거절하고 X를 유지. 부모 LMS 전달의 ‘이동하면 두 영역 변경’과 가장 단순하게 맞는 것은①이지만 확정하지 않음.
- 필요성: 행73은 Patch 전 실제 DOM 불변만 다루며 편집 후 이동의 계약은 다루지 않는다.
- 범위: INTEG. 결정의존: D8. 담당4의 실제 사용자 흐름 테스트에 같은 결정 전달 필요.

# D. 검증 페이지와 전체 흐름

## 5. 기존 page case inventory: 원문 보존
열: 행, ID(D), 분류(F), 필요성(G), 시나리오(H), 기대(I). 전체 FUNC, Phase1 M4 영역.

### 행 70: verify-layout [기본]
- 필요성: 검증 페이지에 필요한 영역 2개와 버튼 3개가 모두 있는지 확인함
- 시나리오: 페이지를 연다
- 기대: 실제 영역, 테스트 영역과 Patch, 뒤로가기, 앞으로가기 버튼이 모두 화면에 있음

### 행 71: verify-load [기본]
- 필요성: 처음 열었을 때 두 영역이 같은 내용을 보여 주는지 확인함
- 시나리오: 페이지를 연 직후 두 영역을 비교함
- 기대: 테스트 영역의 HTML을 View로 바꾼 결과와 실제 영역을 View로 바꾼 결과가 같음

### 행 72: verify-load-buttons [기본]
- 필요성: 처음에는 기록이 하나뿐이라 뒤로/앞으로 버튼이 꺼져 있는지 확인함
- 시나리오: 페이지를 연 직후 버튼 상태를 확인함
- 기대: 기록이 하나뿐이라 뒤로가기와 앞으로가기가 모두 비활성화되어 있음

### 행 73: verify-edit-no-apply [기본]
- 필요성: Patch를 누르기 전에는 실제 영역이 바뀌지 않는지 확인함
- 시나리오: 테스트 영역만 고치고 Patch는 누르지 않음
- 기대: 실제 영역은 전혀 바뀌지 않음

### 행 74: verify-patch-apply [기본]
- 필요성: 글자를 고치고 Patch를 누르면 실제 영역에 반영되는지 확인함
- 시나리오: 테스트 영역에서 글자 하나를 고치고 Patch를 누름
- 기대: 실제 영역에 고친 글자가 보임

### 행 75: verify-patch-partial [기본]
- 필요성: 한 곳만 고치면 실제 영역에서도 그 한 곳만 바뀌는지 확인함
- 시나리오: 여러 요소 중 한 곳의 글자만 고치고 Patch를 누름
- 기대: MutationObserver 기록이 고친 곳에만 있고, 나머지 요소는 같은 요소로 남아 있음

### 행 76: verify-patch-history [기본]
- 필요성: Patch를 누른 뒤 뒤로가기를 쓸 수 있게 되는지 확인함
- 시나리오: 글자를 고치고 Patch를 누름
- 기대: 뒤로가기 버튼이 활성화되고 앞으로가기는 비활성 상태임

### 행 77: verify-attr-edit [기본]
- 필요성: class와 style을 바꾸면 그 요소에만 적용되는지 확인함
- 시나리오: 테스트 영역에서 요소의 class를 바꾸고 style을 추가한 뒤 Patch를 누름
- 기대: 실제 영역의 그 요소에만 새 class와 style이 적용됨

### 행 78: verify-delete-node [기본]
- 필요성: 요소를 지우면 실제 영역에서도 그것만 사라지는지 확인함
- 시나리오: 테스트 영역에서 요소 하나를 지우고 Patch를 누름
- 기대: 실제 영역에서도 그 요소만 사라짐

### 행 79: verify-many-tags [기본]
- 필요성: 표, 목록, 입력창, 링크, 이미지 같은 여러 태그도 제대로 반영되는지 확인함
- 시나리오: 테스트 영역에 table, ul/li, input, a, img, 여러 단계로 겹친 div를 추가하고 Patch를 누름
- 기대: 추가한 모든 요소가 같은 구조와 속성으로 실제 영역에 나타남

### 행 80: verify-patch-nochange [엣지]
- 필요성: 아무것도 안 바꾸고 Patch를 누르면 아무 일도 없고 기록도 쌓이지 않는지 확인함
- 시나리오: 아무것도 고치지 않고 Patch를 누름
- 기대: 실제 영역의 DOM 변경이 0건이고 뒤로가기 버튼도 계속 비활성임

### 행 81: verify-back [기본]
- 필요성: 뒤로가기를 누르면 두 영역이 함께 이전 상태로 돌아가는지 확인함
- 시나리오: 서로 다른 내용으로 Patch를 두 번 한 뒤 뒤로가기를 누름
- 기대: 실제 영역과 테스트 영역이 모두 첫 번째 Patch 직후 상태로 돌아감

### 행 82: verify-forward [기본]
- 필요성: 앞으로가기를 누르면 두 영역이 함께 다음 상태로 돌아오는지 확인함
- 시나리오: 뒤로가기를 누른 뒤 앞으로가기를 누름
- 기대: 두 영역이 모두 두 번째 Patch 직후 상태로 돌아오고, 앞으로가기는 다시 비활성화됨

### 행 83: verify-back-to-start [엣지]
- 필요성: 뒤로가기를 끝까지 누르면 처음 상태가 되고 버튼이 꺼지는지 확인함
- 시나리오: Patch를 여러 번 한 뒤 뒤로가기를 더 이상 갈 수 없을 때까지 누름
- 기대: 두 영역이 페이지를 처음 연 상태가 되고 뒤로가기 버튼이 비활성화됨

### 행 84: verify-back-then-patch [엣지]
- 필요성: 뒤로 간 뒤 새로 고치면 앞쪽 기록이 사라지는지 확인함
- 시나리오: 뒤로가기를 한 뒤 새로운 내용으로 Patch를 누름
- 기대: 새 내용이 반영되고, 이전의 앞쪽 기록은 사라져 앞으로가기가 비활성임

### 행 85: verify-empty-input [엣지]
- 필요성: 내용을 다 지우고 Patch를 누르면 반영하지 않고 안내를 보여 주는지 확인함
- 시나리오: 테스트 영역을 모두 지우고 Patch를 누름
- 기대: 실제 영역과 history는 그대로이고, 최상위 노드가 하나 필요하다는 안내가 #message에 표시됨

### 행 86: verify-multi-top [엣지]
- 필요성: 맨 위 요소를 두 개 넣으면 반영하지 않고 안내를 보여 주는지 확인함
- 시나리오: 테스트 영역에 <p>a</p><p>b</p>처럼 최상위 요소를 두 개 입력하고 Patch를 누름
- 기대: 실제 영역과 history는 그대로이고, 최상위 노드가 하나 필요하다는 안내가 #message에 표시됨

### 행 87: verify-invalid-html [엣지]
- 필요성: 닫는 태그를 빠뜨려도 브라우저가 고친 모양대로 오류 없이 반영되는지 확인함
- 시나리오: <div><p>abc</div>처럼 닫히지 않은 태그가 있는 HTML을 입력하고 Patch를 누름
- 기대: 오류 없이, 브라우저가 자동으로 고친 구조(<div><p>abc</p></div>)대로 반영됨

### 행 88: verify-no-script-exec [엣지]
- 필요성: 입력에 위험한 스크립트가 들어 있어도 실행되지 않는지 확인함
- 시나리오: <script>와 <img src=\"x\" onerror=\"...\">가 들어 있는 HTML을 입력하고 Patch를 누름
- 기대: 어떤 스크립트도 실행되지 않고, 실제 영역에 script 요소와 onerror 속성이 없음

### 행 89: verify-rapid-click [엣지]
- 필요성: 버튼을 마구 눌러도 오류 없이 두 영역이 같은 상태로 끝나는지 확인함
- 시나리오: Patch, 뒤로가기, 앞으로가기를 빠르게 연달아 누름
- 기대: 콘솔 오류가 없고, 마지막에 두 영역을 View로 바꾼 결과가 서로 같음

### 행 90: verify-back-partial [선택]
- 필요성: 뒤로가기도 바뀐 부분만 고치는지 확인함
- 시나리오: 한 곳만 다른 두 기록 사이에서 뒤로가기를 누름
- 기대: 실제 영역에서도 다른 부분만 바뀌고 나머지 요소는 같은 요소로 남아 있음

### 행 91: verify-patch-log [선택]
- 필요성: 이번 Patch에서 어떤 지시가 적용됐는지 화면에 목록으로 보여 주는지 확인함
- 시나리오: Patch 버튼을 누름
- 기대: 이번에 적용된 Patch 목록(종류와 path)이 화면의 로그 영역에 표시됨

### 행 92: verify-highlight [선택]
- 필요성: 바뀐 요소가 잠깐 강조되어 눈으로 확인할 수 있는지 확인함
- 시나리오: Patch 버튼을 누름
- 기대: 실제 영역에서 바뀐 요소가 잠시 강조 표시되어 어디가 바뀌었는지 눈으로 볼 수 있음

## 7. 추가 후보 stable ID: 기존과 다른 이유·범위·결정 의존

### PAGE-N01 초기 복사 객체 독립성
- 추가후보. A를 초기표시한 후 actual/test 대응node가 !==, test 내부 수정해도 actual 불변, actual을 직접 바꾸는 보조격리검사에서는 test 불변. 실제 사용자흐름의 핵심은 test→actual 격리.
- 기존71은 두 변환결과 내용동등만,73은 미적용만 검사하므로 노드비공유 관찰을 더함. private VNode 접근을 위한 export 추가 금지.
- 결정의존: 편집영역이 DOM 자체인지 HTML 문자열컨트롤인지에 따라 직접대응node 검사를 조정.

### PAGE-N02 no-op 이후 실제 변경·이력 검증 강화
- 기존80 확장이지 no-op 신규누락이라고 부르지 않음. A에서 no-op 여러번→B 커밋→뒤로 1번 A→앞으로 B. 실제영역 mutation0·기존node===·불필요 이력step 없음.
- 필요성: 초기버튼만 false라는 결과는 이후 숨은 중복기록을 놓칠 수 있음. History 공개size가 없다면 사용자이동 횟수로 확인.
- 결정의존: no-op 시 앞쪽이력 유지 여부는 아래 FLOW-N04 별도.

### PAGE-N03 실제 typing·IME 완료값
- 추가후보. text input에 브라우저 키입력, 한글 IME 수동확인 또는 실제 조합지원 자동화로 완성값 입력 후 Patch와 뒤·앞. DOM값·화면값·저장값 기대를 직접 적음.
- 필요성: jsdom 값대입 테스트가 놓치는 실제편집·composition 경로.
- 범위: 완성된 값 반영은 Phase1 변환·page 협력. 조합중 Patch·focus/caret 보존은 계약확정후만 필수. textarea·select·checkbox까지 계약없이 확대하지 않음.

### PAGE-N04 브라우저 표시와 HTML 정규화
- 기존79/87 강화. table의 tbody 자동삽입, class/style 실제시각적용·input property 등 지원되는 항목을 명시적 fixture로 점검.
- 필요성: 문자열HTML동등과 브라우저 최종 DOM구조·사용자표시 구분.
- 결정의존: test영역 편집파서 계약, whitespace·root 범위, 보안정제 계약. screenshot은 보조증거이며 img 실제파일 가용성은 별도.

### FLOW-N01 혼합구조 전체흐름
- 추가후보. A=안바뀌는 header와 중첩 list. B=텍스트·속성변경+자식추가+삭제+태그교체를 같은커밋에 섞음. C=같은부위를 재수정. A→B→C→뒤B→앞C. 매단계 양영역을 수기로 적은 내용·순서·속성과 비교하고, Patch 전후 header node===.
- 필요성: 기존74·77·78·79 각각 단발성은 연속 index이동·stale currentView·혼합연산 연결결함을 놓칠 수 있음. Diff/Patch 단위 다중연산 oracle와 중복하지 않고 버튼연결·현재DOM재읽기·history저장까지 확인.
- 결정의존: 지원HTML 범위와 Patch 공개 API. key없는 positional 계약으로만 수행, M9 key 이동identity는 별도.

### FLOW-N02 반복갱신 후 과거스냅샷 독립성
- 추가후보. A→B 저장, C로 편집만 하고 뒤로 A·앞으로 B. B가 C로 오염되지 않음. 이어 B→D 커밋후 B 복귀하면 B 원문 유지.
- 필요성: history unit 원본참조복제검사67/68과 달리 실제페이지 편집DOM·현재VNode·History 연결에서 alias 누출을 검사.
- 결정의존: 미저장편집 후 이동이 편집을 버리는지, 확인후 이동하는지는 본 흐름의 첫 절반을 실행하기 전에 정책결정. 저장후 이동 절반은 바로 검사가능.

### FLOW-N03 분기절단 후 재생
- 기존84 확장. A→B→C→뒤B→D Patch→앞으로 경계→뒤B→뒤A→앞B→앞D. 두 영역과 버튼상태, C 불가 확인.
- 필요성: 단순 앞으로 disabled만으로 History 실자료·currentView·다음Diff 기준의 일관성을 보장하지 못함.
- 결정의존: 기존84가 기준. 새 분기규칙을 발명하지 않음.

### FLOW-N04 되돌린 위치 no-op
- 결정필요 추가후보. A→B→C→뒤B→무수정Patch. 실제영역은 mutation0, B 유지. 이후 앞으로 C가 남는가가 미정.
- 필요성: 기존80은 최초상태 no-op만,84는 '새로운 내용'의 Patch만이라 둘의 교차조건 없음.
- 권고: 의미있는 변경이 없으면 history도 분기도 유지. 기존 no-op 정신에 맞지만 확정계약 아님.

### FLOW-N05 빠른클릭 재현가능한 순서
- 기존89 강화. '마구' 대신 B Patch→뒤→앞→뒤→D Patch→앞의 조작열과 결과 D를 고정. 저장commit 횟수와 예상버튼 포함.
- 필요성: 두 영역이 서로 같아도 둘 다 틀린상태인 결함을 잡음. 동등성만 oracle로 쓰지 않음.
- 결정의존: 처리중 비활성·debounce·async 처리계약이 생기면 허용된 이벤트 처리순서 정의. 현재 동기구현을 가정한 성능시간제한 임의추가 금지.

# E. 결정 ID 대응

상위 DEC 번호는 phase1-test-design.md에 있다. 상세 후보의 과거 담당별 ID는 다음과 같이 해석한다.

- 변환 D-CONV-1→DEC-01, 2→DEC-02, 3·4→DEC-03, 5→DEC-04. D-CONV-6은 두 왕복 방향과 oracle를 분리하는 방법이고 새 정책 결정이 아니다. D-CONV-7은 선택 M9다.
- Diff·Patch D-01·02→DEC-05, D-03→DEC-05·13, D-04→DEC-01·04, D-05→DEC-03·13, D-06→DEC-13, D-07→DEC-05(로컬 noRollback 구체안), D-08→DEC-04(교체 밖 주석과 노드 범위).
- History D1·D2→DEC-06, D3→DEC-08, D4→DEC-07, D5→초기 이력1개는 기존·구체 초기화 API는DEC-06·11, D6→복원 결과는 기존·부분 복원은 선택90, D7→DEC-09, D8→DEC-10, D9→선택hist-max-size.
- 페이지의 미저장 편집→DEC-10, 과거 위치 no-op→DEC-09, 편집·selector→DEC-11, 안전 입력→DEC-12, IME·runner→DEC-14.


# F. Phase 1 key 확장: 기본 범위와 분리

선택한 M9 확장 안에서 적용할 기존 규칙 8개다. rows98~99 h-key와 h-no-key는 부모가 Phase 2 · key 확장으로 직접 확인해 제외했다. 현재 로컬 Patch 다섯 종류에는 MOVE가 없으므로 선택 채택 전 기본 tests에 끼워 넣지 않는다.

| 행 | ID | 기존 시나리오와 기대 요약 |
|---|---|---|
|93|fromdom-key|data-key=a → key=a, props의 data-key도 보존|
|94|fromdom-no-key|data-key 없음 → key=null|
|95|todom-key-hidden|key=a이나 props에 data-key 없음 → DOM에 key·data-key 속성 없음|
|96|diff-key-change|같은 li의 key a→b → 해당 위치 REPLACE 하나|
|97|diff-key-added|key null→a → 해당 위치 REPLACE 하나|
|100|diff-keyed-reorder|a,b,c→c,a,b → MOVE만, REPLACE·CREATE·REMOVE 없음|
|101|diff-keyed-insert|a,c 사이 b 삽입 → b 생성만, a·c Patch 없음|
|102|patch-move|ul의 c를 맨 앞으로 MOVE → c,a,b, 세 요소 모두 이전과 ===|

93~97은 확장 안의 기본·엣지 규칙이며,100~102는 선택으로 표시된 이동 최적화다. M9 자체를 기본 M1~M4에 자동 포함하지 않는다. key와 data-key의 비대칭 때문에 왕복 정규형과 경로·순서 계약을 다시 확인한다.
