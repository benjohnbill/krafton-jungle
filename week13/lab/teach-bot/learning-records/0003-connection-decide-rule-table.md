# 그는 `connection_decide`를 따라쳤고, 규칙 표가 "행 하나를 더해 규칙을 늘리는 구조"라고 설명했다

2026-11-24, L1 따라치기. 파일은 `teach-bot/type/connection_verdict.c`이고, repo 테스트 `tests/test_connection_verdict.c`의 다섯 사례가 그의 파일로 통과했다.

Evidence:

- 처음에는 "규칙에 맞으면 verdict를 돌려준다"까지만 잡혔고, 함수 포인터와 표, 마지막 `return CONN_PASS`에서 막혔다 (user said "함수형 포인터라던가, 자료구조가 너무 복잡해서"). 표가 메모리에 두 행으로 놓인 그림을 보여 주고 "`i = 1`이면 어느 함수가 실행되나"를 물었다. 그는 스스로 정리했다: 두 match 함수로 검사하고, 맞으면 그 판결을 내보내고, 어느 행도 맞지 않으면 `CONN_PASS`다.
- 바로잡은 것: `if`에 들어가는 조건은 "값이 있다"가 아니라 `matches`가 `true`를 돌려준 경우다. 돌려주는 값은 "PASS가 아니라서"가 아니라 그 행의 `verdict` 칸이다.
- 바로잡은 것: 그는 이 파일이 IP와 JA4를 block list와 table에서 찾는다고 보았다. 실제 조회는 `event_loop.c`의 `connection_verdict_get`이 하고, 이 파일은 bool 신호를 Verdict로 바꾸기만 한다. 그는 `ja4_label`을 읽는 규칙이 아직 없다는 것을 스스로 짚었다.
- 확인 질문(표 대 `if`)에 대한 답: "앞으로 계층이 추가될 때마다 계속해서 추가할 수 있다." 방향은 맞다. agent가 범위를 좁혔다. 이 표는 Connection Verdict 한 단계의 규칙만 담는다. HTTP 단계의 규칙은 `verdict_decide`(L5, 같은 모양에 8행)에 들어간다. 행을 추가해도 반복문은 바뀌지 않는다.

Implications: 함수 포인터는 아직 낯설다. L5 `verdict_decide`에서 같은 모양을 다시 만나면 그림 없이 설명할 수 있는지 묻는다. 행 순서가 곧 우선순위라는 것은 4절 과제에서 이미 확인했으니 다시 묻지 않는다.
