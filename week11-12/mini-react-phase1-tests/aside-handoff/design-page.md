# mini-react Phase1 검증페이지 및 전체 workflow 인수조건

조사일: 2026-11-09. 읽기 전용. 시트는 개인 새 탭에서 이름상자 좌표 선택과 수식 textbox snapshot으로 읽었고 외부 셀·코드는 수정하지 않았어요. 로컬은 조사 중 다른 세션이 수정하고 있어, 아래 구현부재는 첫 소스 열거 시점 관찰이에요. 이후 부모가 patch.ts 추가를 확인했으므로 코딩 세션은 시작 시 파일목록을 다시 읽어야 해요.

## 1. 대상 책임
검증페이지는 실제 영역의 최초 HTML을 VNode로 복사한 테스트 영역을 제공하고, 사용자가 수정한 현재 테스트 DOM을 Patch로 실제 영역에 반영한 뒤 History 이동으로 두 영역을 동기화해요. 이 보고서는 버튼·현재 DOM 재읽기·데이터 경로·화면 결과의 결합을 검사하고, 변환·Diff·Patch·History 각 함수의 단위 oracle를 재정의하지 않아요.

## 2. 근거와 읽은 범위
- React Tests: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=ffbb46
- canonical page inventory: D/G/H/I70:92. 모든 행의 F 분류를 직접 읽었어요. B70과 B85는 Phase 1, C70과 C85는 M4, E70/E85/E88:92는 FUNC. 화면 시각확인에서도 M4 기능영역의 연속행이에요.
- README: https://wsgxty2zedqf.sg.larksuite.com/sheets/RINBsUvXIhdoE8tAECClFykZgWg?sheet=Ojre1q, B7/C5:C8/D5:D7/C13:C15 직접 읽음.
- History60:69는 D/H/I 보조확인만 했어요. 변환·Diff 부분통합52:59의 canonical inventory는 다른 담당 소유예요. 따라서 이 보고서만으로 전체 Phase1 모든 행의 누락을 단정하지 않아요.
- LMS https://jungle-lms.krafton.com/learning/1307 는 중복조사를 피하라는 부모 지시로 직접 열지 않았어요. 부모가 실제 원문 확인한 필수 흐름: 로드 시 실제 샘플 HTML→VNode→테스트영역 렌더, Patch 시 현재테스트DOM 다시읽기→이전VNode와Diff→변경부분만 실제영역반영→새VNode History저장, 뒤·앞으로 특정 저장VNode 이동 시 실제·테스트 두 영역 변경. 이 내용은 부모 확인 근거이며 본 담당의 직접열람 증거가 아니에요.
- render라는 별도 함수가 Phase1인지의 원문행은 본 담당이 읽지 못했어요. 최초 VNode→DOM 렌더 동작은 Phase1이고, FunctionComponent render와 hooks는 Phase2로 본 범위에서 제외해요. render API의 단계를 이름만으로 단정하지 말고 부모의 다른 담당 근거와 결합해야 해요. M9 optional key와 key 기반 reorder는 아래 필수그룹에 포함하지 않아요.

## 3. 로컬 규칙·계획·구현 관찰
프로젝트: \\wsl.localhost\Ubuntu-26.04\home\benjohnbill\dev\krafton-jungle\week11-12\mini-react
- CONVENTION.md: 공개함수의 동작을 테스트하고, 테스트만을 위한 export 금지. 기대값을 검사대상 함수로 계산하지 않음. 다른 공개함수 결과와 비교하는 통합 비교는 허용. Patch 형식 정해지기 전 내부 Patch 내용 읽지 않음. 공통테스트 구현 전 PR, 빈함수 테스트 skip. 파일은 기능당 src 한 파일, 페이지 경로 src/test-pages/verification-page.ts 계획.
- docs/adr/0004-one-file-per-feature-and-patch-format-later.md: proposed. createVNodeFromDom(element), createDomFromVNode(vnode), diffViews(currentView,newView), applyPatchesToDom(container,patches) 공개명 제시. 인자·반환은 Patch 형식 결정 때 변경 가능. History와 page API는 이 파일에서 정하지 않음.
- GLOSSARY.md: View는 최상위 VNode, container는 View를 넣는 DOM 요소.
- README.md: 마일스톤 범위는 첫 팀 회의에서 정함. npm test는 단위테스트 명령. package.json에 browser E2E 스크립트나 browser runner 의존성은 조사 시점에 없어요. vitest.config.ts environment=jsdom.
- 첫 조사 src 목록: vnode.ts, vnode.test.ts, setup.test.ts, main.ts. main.ts는 #app.textContent='mini-react'뿐이며 index.html은 #app과 main.ts script뿐. verification-page.ts와 실제·테스트 두 영역, Patch·뒤·앞 버튼 연결은 미구현이에요. 부모가 조사 도중 patch.ts·patch.test.ts·ADR0006 추가를 별도로 확인했으므로 첫 목록을 최신 전체 구현상태라고 재사용하면 안 돼요.
- 현재 직접 읽은 변환코드는 VNode=string 또는 type/props/children, createVNodeFromDom은 Element/Text를 처리하며 텍스트 input live value를 props.value에 읽어요. 이것은 typing·IME·브라우저 focus 성공의 증거가 아니에요.
- 부모 알림: 새 Patch안 TEXT/REPLACE/PROPS/INSERT/REMOVE, []=View, 앞 Patch 반영후 경로, comment 제외·whitespace 포함. Lark CREATE·공백 관련 기대와 충돌 가능. 본 담당은 새 파일을 직접 재검토하지 않았으므로 아래 페이지 설계는 Patch 내부형식에 의존하지 않아요.

## 4. README 레벨·필수성 원문
- C5: 단위 테스트
- D5: 함수나 클래스 하나가 주어진 입력에 맞는 결과를 내는지 확인함
- C6: 통합 테스트
- D6: 두 개 이상의 함수를 이어서 썼을 때 결과가 맞는지 확인함 (예: diffViews의 결과를 applyPatchesToDom에 넘김)
- C7: 기능 테스트
- D7: 실제 브라우저에서 페이지를 열고, 사용자처럼 입력하고 클릭했을 때 화면이 맞게 바뀌는지 확인함
- C13: 반드시 통과해야 하는 정상 동작
- C14: 빈 입력, 경계값, 잘못된 사용 같은 예외 상황. 반드시 통과해야 함
- C15: 요구사항에는 없지만 다른 팀과의 차별점이 되는 추가 구현. 구현하지 않았다면 테스트를 skip으로 둠

기본과 엣지는 반드시 통과, 선택만 미구현 skip이에요. LMS가 초기저장·no-op저장·버튼disable을 명시하지 않았어도 시트에는 해당 기대가 이미 있으므로 이를 '새롭게 미정인 요구'라고 지우면 안 돼요. 다른 계약과 충돌하면 기존 기대를 보존하고 충돌결정으로 올려야 해요.

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

## 6. 검증성질 그룹: 기능 책임에서 도출

### P-G1 최초표시·복사독립성
- 사전상태: 실제 영역에 알려진 샘플 View A. 페이지 새 로드.
- 사용자조작: 초기표시 확인, 테스트영역만 편집.
- 관찰결과: 영역2개·버튼3개 존재, 최초 내용 A, 테스트영역 편집은 실제영역 A를 바꾸지 않음. 두 영역의 대응 노드는 같은 객체가 아님.
- 협력함수: main 또는 verification-page 초기화, createVNodeFromDom, createDomFromVNode, History 초기저장·버튼상태. page initializer 이름·공개 API는 아직 몰라요.
- 성질: 최초 내용보존, 양방향 객체비공유, 미저장편집 비적용. 기존70~73과 겹치되 객체독립성은 추가 관찰.

### P-G2 Patch 커밋
- 사전상태: 저장된 A, 테스트영역은 사용자가 B로 편집.
- 사용자조작: Patch 클릭. 그후 C로 다시 편집하고 다시 Patch.
- 관찰결과: 실제영역 B→C, 현재 테스트DOM을 매번 읽음. 이전 B를 기준으로 C를 반영하며 stale A에서 계산한 결과가 남지 않음. 변경하지 않은 실제영역 sibling은 참조동일, 실제영역 DOM mutation은 변경부에 한정. 내용·순서·속성은 직접 적은 기대값으로 확인.
- 협력함수: DOM→VNode, diffViews, applyPatchesToDom, History push, 페이지 상태·버튼갱신.
- 성질: 현 DOM 입력충실성, 반복 커밋, 변경국소성, no-op 무변경, 내용과 이력의 커밋일치. 기존74~80.

### P-G3 저장상태 이동·branching
- 사전상태: A→B→C 각 커밋 완료.
- 사용자조작: 뒤로 B, 앞으로 C, 다시 뒤로 B, 새 D 커밋, 경계까지 이동.
- 관찰결과: 두 영역이 같은 저장상태, B→D 뒤 C로 앞으로 갈 수 없음. 초기·경계 disable은 기존72/76/80/82/83/84 기대를 따라 검사.
- 협력함수: History back/forward/current/canBack/canForward와 두 영역 렌더, Patch 처리. History API 명칭은 시트 기대이지 로컬 구현확정 아님.
- 성질: 이력재생 정확성·두 영역 동기화·분기절단·경계안전. 기존81~84. 뒤로가기 변경국소성은 선택90이며 필수75와 구분.

### P-G4 실제 사용자 입력·브라우저 고유상태
- 사전상태: 지원하는 text input 또는 편집컨트롤에 초기값 A.
- 사용자조작: 실제 키보드 입력으로 B, 한글 IME 조합완료 후 Patch, 다른 곳 수정 후 다시 Patch, History 이동.
- 관찰결과: 사용자에게 보이는 완성값과 현재 DOM value가 예상값, Patch가 live value를 읽고 최종값을 반영. 관찰로그에는 compositionstart/update/end 및 input 순서와 activeElement·selectionStart/End를 기록.
- 협력함수: 브라우저 편집, DOM→VNode의 live value, Patch, page event handler.
- 성질: 입력손실·중복커밋 방지. jsdom .value 대입은 실제 사용자 typing/IME 증거가 아니고, 합성 composition event도 OS IME 증거가 아님.
- 지원계약 없는 focus·caret 유지, 조합도중 Patch 정책, 테스트영역 편집방식(textarea/contenteditable/실제 DOM 컨트롤)은 결정필요. Patch 버튼 클릭은 정상적으로 focus를 버튼으로 옮길 수 있으므로 버튼을 클릭해도 input focus 그대로라고 임의 필수화 금지.

### P-G5 입력경계·선택시각화
- 사전상태: 정상커밋 존재.
- 사용자조작: 빈 입력·복수최상위·불완전HTML·위험HTML·빠른버튼, 선택구현이면 log/highlight.
- 관찰결과: 기존85~89를 그대로 oracle로 두되 빈입력 처리·#message와 sanitizer는 시트 명시 기대이며 LMS 원문에 있다고 오인하지 않음. 빠른클릭은 조작열·마지막 기대상태를 고정해야 재현 가능. 선택90~92는 구현선택.
- 협력함수: 편집파서·입력검사·안전한 렌더·페이지 핸들러. 실제API 없음.
- 성질: 오류시 커밋불변, 브라우저파싱계약, 실행안전성, 조작열 일관성. 기존 오류UX 밖 새로운 토스트·복구UI는 요구하지 않음.

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

## 8. 단위 oracle와 E2E oracle 구분
- 단위: createVNodeFromDom 특정입력→직접적은VNode, diffViews 및 Patch 반환·적용, StateHistory 복제·경계는 다른 담당.
- page 통합: 실제 export된 초기화 또는 실제 entry 실행으로 DOM fixture를 구성하고 버튼이벤트→모든실제협력함수→두영역·버튼 결과 검사. 함수 mock만으로 연결성 검증완료라고 하지 않음. app 초기화API가 없으므로 코딩세션이 공개 surface를 먼저 확인.
- 브라우저 FUNC: 실제페이지URL 로드·사용자편집·버튼클릭·두영역 결과·DOMidentity·관찰로그·필요시 screenshot. 현재 package에는 runner가 없어 runner채택 또는 수동재현절차 결정 필요. 개발도구추가는 런타임프레임워크금지와 별개.
- isEqualNode는 노드종류·attribute·자식구조 동등 보조검사일 뿐, live value·checked·focus·caret·eventlistener·history상태·nodeidentity를 보장하지 않음. 값/property·참조===·activeElement·selection·버튼·경로재생을 각 별도로 관찰.
- 변환결과끼리 비교하는 기존71·89는 보조불변식. 두변환이 같은 오류를 공유해도 통과할 수 있으므로 대표fixture의 구체text·순서·속성·livevalue를 직접적은 기대값으로 보강.
- MutationObserver 범위는 실제영역으로 제한하고 버튼disable·로그·highlight의 UI mutation을 별도 관찰. highlight가 실제영역 attribute를 바꾸면 mutation검사의 제외규칙을 명시해야 함. 정확한 내부 mutation개수는 불필요하게 고정하지 않음. no-op0·안바뀐subtree 참조유지 등 공개성질 우선.

## 9. 실제 누락·미정·읽지 못함 분리
- 실제 구현누락(첫관찰): verification-page.ts·영역2개·버튼3개·page기능테스트 및 browser runner. 코딩세션 시작시 재확인필수.
- 시트내 부재후보(읽은70:92 기준): 초기객체독립성, 다단계혼합전체flow, 실제typing/IME, 되돌린위치no-op 교차정책, 결정적빠른조작열. 다른단위·부분통합행에 유사기대가 있을 수 있으므로 '프로젝트전체에전혀없음' 단정하지 않음.
- 기존 명시됨: no-op80, 반복Patch사전조건81, branching84, 부분갱신75, 초기내용71, 미적용73, error #message85/86, 안전정제88. 이를 신규누락 목록에 넣지 않음.
- 결정필요: 실제편집UI·root추출/빈공백계약·no-op분기보존·미저장편집후History이동·조합중Patch·focus/caret 유지정책·browser테스트수단·동시로컬Patch안과시트기대충돌. focus보존이나새오류UX를 계약없이 필수화하지 않음.
- API모름: verification-page 초기화, selector/영역명, history 실제class/export, 오류/정제함수, 로그/highlight구현 API. 테스트편의만을 위한 export를 요구하지 않음.
- 읽지못함: LMS 본담당직접원문, render단계원문행, Phase2/M9 전체재고. 부모원문과다른담당보고로통합. 로그인차단은 이 담당에게 발생하지 않았고 Lark는 공개읽기가능했어요.

## 10. 별도코딩 세션 시작점
1. 최신 src와ADR0006·git상태를 읽어 동시변경을 보존. 시트기대와실제API 충돌을 부모결정표에 기록.
2. M4 기존 FUNC70~89를우선실행가능하게연결. 선택90~92와M9 key는별도skip.
3. PAGE-N01과 FLOW-N01·저장후FLOW-N02·FLOW-N03을대표통합으로추가. 단위case전량복제금지.
4. 브라우저실입력 PAGE-N03과시각표시 PAGE-N04를독립실행. IME증거와jsdom증거를구분.
5. 최종handoff에는 case ID→관찰증거→pass/fail/skip/blocked 및결정의존을보존. 이번조사는실행테스트나CI통과를주장하지않아요.
