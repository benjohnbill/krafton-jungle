# 요청 흐름 (소켓과 TCP) Resources

## Knowledge

- Book: _Computer Systems: A Programmer's Perspective_ (CSAPP), 3rd ed., 11.4 The Sockets Interface
  코스 지정 교재. Use for: socket, bind, listen, accept, connect의 순서와 역할. 각 lesson의 주 자료.
- [tcp(7) — Linux manual page](https://man7.org/linux/man-pages/man7/tcp.7.html)
  Linux TCP의 동작과 상태. Use for: TIME_WAIT, RST, 재전송, 소켓 옵션.
- [listen(2)](https://man7.org/linux/man-pages/man2/listen.2.html) · [accept(2)](https://man7.org/linux/man-pages/man2/accept.2.html)
  backlog와 accept 대기열의 정의. Use for: L1의 "accept 없이 handshake가 끝나는가".
- [socket(7)](https://man7.org/linux/man-pages/man7/socket.7.html)
  소켓 수준 옵션과 버퍼. Use for: L2의 수신 버퍼, SO_RCVBUF.
- [ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html)
  Recv-Q와 Send-Q의 뜻이 LISTEN 소켓과 연결 소켓에서 다르다. Use for: 모든 관찰 명령의 출력 읽기.
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
  소켓 API를 C 예제로 설명. Use for: T2 따라치기 전 코드 모양 확인.

## Wisdom (Communities)

- 크래프톤 정글 week13 팀. Use for: mini-webserver 결정을 서로 설명하고 검증.

## Gaps

- 커널 안에서 패킷이 소켓까지 가는 경로(포트로 소켓 찾기)를 짧게 다룬 1차 자료. L2 전에 찾는다.
