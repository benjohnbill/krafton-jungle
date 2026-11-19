# 01-dns — 이름이 IP로 바뀌기

## 실행할 명령

```bash
ip -br addr
getent hosts example.com
getent ahosts example.com
dig example.com 2>&1 | bat -l log
dig AAAA example.com +short
dig A example.com +short
dig +short google.com
dig google.com | grep SERVER
ping -c 3 example.com 2>&1 | bat -l log
bat /etc/hosts
bat /etc/resolv.conf
```

`ip -br addr`은 내 컴퓨터의 번호, 나머지는 상대 서버의 번호를 본다.

## 볼 것

- `dig`의 `ANSWER SECTION`: 이름 하나에 IP가 몇 개 붙어 있나. `google.com`은 실행할 때마다 순서가 바뀌나.
- `dig` 맨 아래 `SERVER:` 줄: 누구에게 물어봤나. `/etc/resolv.conf`의 `nameserver`와 같은가.
- `ping` 첫 줄: 이름이 어떤 IP로 바뀌었나. `time=` 값은 무엇을 잰 것인가.
- `getent`는 C 함수 `getaddrinfo()`와 같은 경로로 이름을 찾는다. 서버 코드가 쓰는 방식이 이쪽이다.

## 혼자 하는 변경 과제

`/etc/hosts`에 한 줄을 더한다.

```bash
echo '127.0.0.1 jungle.local' | sudo tee -a /etc/hosts
```

실행 전에 예측한다: `getent hosts jungle.local`과 `dig jungle.local`이 각각 무엇을 돌려줄까. 그다음 실행하고, 둘이 다르면 왜 다른지 설명한다.

끝나면 그 줄을 지운다(WSL은 재시작할 때 `/etc/hosts`를 다시 만들 수도 있다).

## 내 문장

- 
