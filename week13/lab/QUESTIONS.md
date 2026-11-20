# Questions

체험하면서 생긴 질문. 한 줄에 하나, 앞에 probe 번호. 풀리면 체크한다. 팀 프로토타입을 만들 때 이 목록에서 질문을 고른다.

- [x] 03: 디스크도 안 쓰는데 소켓에 `read`와 `write`를 쓰는 이유 (소켓도 fd) → flow lesson 0001
- [ ] 03: 커널이 들어온 패킷을 어느 소켓에 줄지 고르는 방법 (주소 네 개) → flow 결정 5번
- [ ] 03: IPv6에서 공유기 방화벽이 들어오는 연결을 막는 방식 → 범위 밖
- [ ] 03: request smuggling (너그러운 파싱의 한계) → T6 
- [ ] 06: 서버 쪽이 클라이언트보다 연결을 먼저 끊으면 어떻게 되는가 (서버 쪽 TIME-WAIT, 재시작 시 `bind: Address already in use`) → T3
- [ ] 06: reverse proxy가 backend 여럿에 나눠 줄 때, backend 대기열이 차면 proxy의 `connect`가 2분쯤 멈춘다. connect timeout을 두고 다른 backend로 옮길까 → T6
