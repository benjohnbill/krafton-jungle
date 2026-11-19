# Mission: 요청 하나가 지나는 네 칸 — 클라 앱, 클라 커널, 서버 커널, 서버 앱

## Why
week13 mini-webserver의 각 결정(소켓, 동시성 모델, proxy)을 내 말로 설명해야 한다. 그러려면 요청 하나가 클라이언트 앱 → 클라이언트 커널 → 서버 커널 → 서버 앱을 어떻게 지나고, 응답이 어떻게 돌아오는지 알아야 한다. lesson은 lab 트랙의 C 코드를 치기 전에, 그 코드가 보여 줄 것을 예측하게 한다.

## Success looks like
- 각 구간에서 일하는 것이 앱인지 커널인지 말한다. socket, bind, listen, accept, connect, read, write, close가 네 칸의 어디에 있는지 말한다.
- 소켓이 fd라서 read, write, close를 쓴다는 것을 `/proc/<pid>/fd`로 보이며 설명한다.
- 커널이 주소 네 개로 소켓을 찾고, 수신 버퍼에 쌓고, read가 꺼낸다는 것을 `ss`의 Recv-Q로 보인다.
- 트랙을 시작하기 전에 예측을 남기고, 트랙이 끝난 뒤 예측과 실제를 probe README에 비교한다.

## Constraints
- 한국어 본문. syscall 이름, TCP 상태 이름, 명령은 영어 원문.
- lesson마다 4칸 그림(`assets/flow-lanes.js`), 빈 4칸 복습, 퀴즈와 예측, 답안 복사 버튼(`assets/quiz.js`).
- lesson은 4개. 각 lesson은 그 lesson이 예측하는 트랙 바로 앞: L1 연결 준비와 fd, L2 포트로 소켓 찾기와 수신 버퍼 (T2 앞), L3 close와 실패 (T3 앞), L4 두 커널과 가운데 앱 (T6 앞).
- T1 노트(`../pages/`)의 출력을 근거로 다시 쓴다. 새 관찰은 커널 안(tcpdump, ss의 대기열과 버퍼)만.
- 서버는 loopback으로 시작하고, 이때 두 커널 칸이 같은 커널 하나임을 밝힌다. 관찰 명령(sudo 포함)은 그가 직접 실행하고 출력을 붙인다.

## Out of scope
- IP 라우팅, NIC, 드라이버, Ethernet, ARP. 커널 사이의 선으로만 그린다.
- 코드 문법과 syscall 호출법. 따라치기의 몫이다.
- epoll lesson. T4가 끝난 뒤 다시 정한다.
