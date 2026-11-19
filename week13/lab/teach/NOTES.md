# Notes

- 질문은 하나씩. 그가 쓴 문장을 먼저 맞다·틀리다로 판정하고, 틀린 한 곳만 고친다 (week11-12 NOTES에서 가져옴).
- 관찰 명령은 그가 직접 실행하고 출력을 붙인다. 에이전트는 sudo를 실행하지 않는다 (PLAN.html).
- 그는 CSAPP 11장을 읽지 않는다. 주 자료는 man page와 커널 소스를 우선한다.
- 레슨은 답안 복사 블록을 받으면 `learning-records/`에 기록하고, 예측은 다음 probe README의 볼 것에 넣는다 (`../CLAUDE.md`).
- 레슨은 T1 노트를 `../../pages/`로 링크한다. `publish/build.py`는 `../`가 남으면 멈추므로, 사이트에 올릴 때 이 링크를 사이트 주소로 바꾸는 규칙을 build.py에 더해야 한다.
- 2026-11-20 확인: OpenBSD netcat, backlog 2에 연결 3개가 accept 대기열에 들어감 (Recv-Q 3, Send-Q 2).
