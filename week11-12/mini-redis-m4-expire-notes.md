---
scope: 오라버니의 M4 `expire` 사전 공부 노트 (개인용, 임시)
status: 임시 — grill 2단계 전에 오라버니 혼자 보는 자료
written: 2026-11-14
---

# M4 `expire` decision points

> [!WARNING]
> 이 파일에는 Redis의 답이 들어 있어요. 팀 규칙(`CONVENTION.md` § 마일스톤)은 Redis의 답을 grill 2단계 끝에 공개하므로, 이 파일을 `mini-redis/` 레포로 옮기지 않아요. grill AI도 레포 문서를 읽기 때문이에요.

- **Requirement:** L9 — "보관 기간이 만료된 값을 요청받았을 때, 이를 어떻게 처리할지 방안을 마련합니다."
- **Expected choice** 칸은 M2와 M3(PR #15)의 결정을 보고 에이전트가 추측한 값이에요. 팀이 합의한 내용이 아니에요.
- 각 문제 아래의 `Notes`는 오라버니와 이야기하면서 채워요.

## Summary

| # | Problem | General options | Expected choice | Redis |
|---|---|---|---|---|
| 1 | client가 TTL을 보내는 방법 | 헤더, body JSON, 별도 경로, query string | `PUT` 헤더 | 명령 인자(`EX` 등), `EXPIRE` |
| 2 | 저장하는 값의 형태 | 상대 TTL, 절대 만료 시각 | 절대 만료 시각 | 절대 unix ms |
| 3 | 시계 | wall clock, monotonic | monotonic | wall clock(ms), 명령 중 고정 |
| 4 | 만료된 key 조회 응답 | 없는 key와 같게, `410`, 새 오류 이유 | `404 key_not_found` | 없는 key와 같음 |
| 5 | 지우는 시점 | lazy, active, 둘 다 | 둘 다 | 둘 다 |
| 6 | active 청소 방식 | 전수 스캔, min-heap, 정렬 list, timing wheel, 샘플링 | min-heap | TTL 테이블을 커서로 조금씩 훑기 (6.0 전: 무작위 샘플링) |
| 7 | 청소와 M3 지연 목표 | 개수 상한, 시간 예산, 해제 쪼개기, 해제 스레드 | 상한, 스레드 없음 | 시간 예산, lazyfree 스레드 |
| 8 | 만료 시각을 두는 곳 | entry 필드, 별도 테이블 | entry 필드와 heap | 별도 dict `expires` |
| 9 | 덮어쓰기, 조회의 영향 | TTL 지우기, 유지, 조회 시 연장 | 덮어쓰면 새로 정함 | `SET`이 지움, `GET` 무영향 |
| 10 | 경계, 단위, 잘못된 값 | 초 또는 ms, 경계 판정, 0과 음수 | 초 단위 양의 정수 | ms, 0 이하면 즉시 삭제 |
| 11 | TTL 조회와 해제 API | 없음, 조회만, 조회와 해제 | 없음 | `TTL`, `PTTL`, `PERSIST` |

## 1. TTL in the request

- **General options:** 헤더(`X-TTL` 같은 이름), body를 JSON으로 감싸기, 별도 경로(`PUT /keys/<key>/ttl` 같은), query string.
- **Expected choice:** `PUT` 요청의 헤더.
- **Redis:** 명령 인자 `SET k v EX 10`(초), `PX`(ms), `EXAT`(절대 초), `PXAT`(절대 ms). 이미 있는 key에는 별도 명령 `EXPIRE`, `PEXPIRE`, `EXPIREAT`, `PEXPIREAT`을 써요.
- **Our constraints:** M2는 인코딩하지 않은 `?`를 `400 bad_key_encoding`으로 거절해요. 그래서 query string은 M2 결정을 바꿔야 해요. M2는 body를 value 바이트 그대로 받으므로, JSON으로 감싸는 방법도 M2 결정을 뒤집어요.

Notes:

- (2026-11-14, 오라버니 이해 확인) JSON을 쓰지 않는 이유는 ADR `http-methods-and-raw-body`에 이미 있어요. "헤더와 body로 충분하다"는 그 이유가 TTL을 헤더에 두는 선택과도 맞아요.
- 헤더 줄의 형식은 HTTP가 정하고, 헤더 이름의 의미는 우리가 정해서 `README.md`의 API 절에 적어요. 서버는 `mg_http_get_header`로 값을 꺼내 api 층에 인자로 넘겨요. M2의 `api_reject_headers`와 같은 길이에요.
- 헤더는 선택 사항으로 두는 쪽이 자연스러워요. 헤더가 없으면 만료 없이 저장해요.
- Redis의 `SET k v EX 60`과 우리의 "`PUT` body + 헤더"는 자리만 다르고, value와 TTL을 요청 하나로 보낸다는 생각은 같아요.
- query string은 보류했어요.

## 2. Relative TTL or absolute deadline

- **General options:** 받은 상대 TTL을 그대로 저장하기, 받는 순간에 절대 만료 시각으로 바꿔 저장하기.
- **Expected choice:** 절대 만료 시각.
- **Redis:** 절대 unix 시각을 ms로 저장해요. 복제와 AOF로 전파할 때도 `PEXPIREAT` 절대 시각으로 바꿔서 보내요.

Notes:

- (2026-11-14) 저장은 절대 만료 시각으로 하는 것을 이해했어요. 입력을 상대 시각으로 받을지 절대 시각으로 받을지는 결정하지 못하고 넘어갔어요.
- 상대 시각 입력의 오차는 전송 지연이에요. 보통 ms 단위이고, 항상 조금 늦게 만료돼요.
- 절대 시각 입력의 오차는 client 시계와 서버 시계의 차이예요. 시간대와는 상관이 없어요(Unix 시각은 UTC 기준). 관리된 서버끼리는 작지만 보장되지 않고, 방향도 정해져 있지 않아요.
- 남은 하위 질문: 상대 시각의 기준을 헤더 도착 시각으로 할지, handler 실행 시각으로 할지. 16 MiB를 느리게 올리면 두 시각이 몇 초 벌어져요.

## 3. Clock

- **General options:** wall clock(`CLOCK_REALTIME`), monotonic clock(`CLOCK_MONOTONIC`).
- **Expected choice:** monotonic clock. M6 `persist`를 하게 되면 다시 검토해요.
- **Redis:** wall clock을 ms로 써요. 명령 하나가 실행되는 동안에는 시각을 한 번만 읽어서 고정해요.
- **Trade-off:** wall clock은 재시작 후에도 의미가 있지만, 시계를 조정하면 값이 튀어요. monotonic clock은 튀지 않지만, 재시작하면 기준점이 사라져요.

Notes:

## 4. Response for an expired key

- **General options:** 없는 key와 같은 응답, `410 Gone`, 상태 코드는 `404`로 두고 새 오류 이유로 구분.
- **Expected choice:** `404 key_not_found`, 없는 key와 같은 응답.
- **Redis:** 없는 key와 구분하지 않아요(nil).

Notes:

- (2026-11-14, 오라버니: "너무 당연한 얘기") `404 key_not_found`로 없는 key와 같게 답하는 쪽으로 기울었어요. 구분하려면 청소 후에도 지운 key를 기억해야 하고, 그러지 않으면 청소 시점에 따라 답이 바뀌어요.

## 5. When to delete

- **General options:** lazy만(조회할 때 검사), active만(주기 청소), 둘 다.
- **Expected choice:** 둘 다.
- **Redis:** 둘 다 써요. 모든 key 조회 경로에서 lazy 검사를 하고, 주기 청소를 함께 돌려요.
- **Trade-off:** lazy만 쓰면 다시 조회되지 않는 key가 메모리에 영원히 남아요. active만 쓰면 청소 주기 사이에 만료된 값을 돌려줄 수 있어요.

Notes:

- (2026-11-14, 오라버니: "반쯤 당연") 둘 다 쓰는 쪽으로 기울었어요. lazy는 정확성(만료된 값을 돌려주지 않기)을, active는 메모리 회수를 맡아요.
- 당연하지 않은 절반은 6번(어떻게 찾나)과 7번(한 번에 얼마나 하나)으로 넘어가요.
- lazy만 쓰는 시스템은 메모리가 차면 오래된 항목을 밀어내는(eviction) 장치가 있어요. 우리 store에는 그 장치가 없어요.

## 6. Active sweep method

- **General options:** 전수 스캔, min-heap(libevent, Go 타이머), 정렬 list(Pintos alarm clock의 sleep list와 같은 방식), timing wheel(Linux 커널 타이머, Netty), 무작위 샘플링.
- **Expected choice:** 만료 시각 순 min-heap에서 앞부터 꺼내기.
- **Redis:** TTL이 있는 key만 모은 테이블을 커서로 조금씩 훑어요(한 번에 약 20개). 만료 비율이 10%를 넘으면 한 번 더 훑어요. Redis 6.0 전에는 그 테이블에서 무작위로 20개를 샘플링했고, Redis 문서는 아직 그 방식으로 설명해요. (2026-11-14 정정: 처음에는 무작위 샘플링이라고만 적었어요.)

Notes:

## 7. Sweep cost and the M3 latency target

- **General options:** 한 번에 처리할 개수 상한, 시간 예산, 큰 value 해제 쪼개기, 해제 전용 스레드.
- **Expected choice:** 한 번에 처리할 개수나 시간에 상한을 두고, 스레드는 늘리지 않아요.
- **Redis:** 시간 예산을 둬요(slow cycle은 CPU 25%, fast cycle은 1 ms). `lazyfree-lazy-expire` 옵션을 켜면 백그라운드 스레드가 큰 값을 해제해요.
- **Our constraints:** PR #15의 ADR `single-thread-event-loop`는 큰 메모리 해제도 다른 스레드에 맡기지 않는다고 정했어요. 목표는 방해 요청이 있어도 작은 GET의 p99가 10 ms 이하예요. 16 MiB value 여러 개가 한꺼번에 만료되거나 삭제 때문에 rehash가 일어나면 이 목표를 넘을 수 있어요. 해제 스레드를 쓰려면 새 ADR로 그 ADR을 대체해야 해요.

Notes:

- (2026-11-14, 오라버니 이해 확인) active 청소는 스케줄링 문제예요. 언제 돌릴지(루프의 타이머)와 한 번에 얼마나 돌릴지(상한)를 정해야 해요.
- 우리 서버는 협력형 스케줄링이에요. 스레드 하나가 handler를 끝까지 실행하고, 중간에 멈춰 주는 존재가 없어요. 그래서 청소가 스스로 일을 나눠 루프에 돌려줘야 해요.
- 7번의 상한은 "이 작업이 스레드를 얼마나 붙잡을지"의 상한이에요. 오라버니가 떠올린 모양은 time slice예요. 정해진 만큼 일하면 자리를 넘기고 대기열 뒤로 가서, 다음 차례에 이어서 해요.
- 협력형에서 이어서 하려면 작업이 어디까지 했는지(커서)를 스스로 저장해야 해요. 청소는 "어디까지 봤는지"를 남기고 멈췄다가 다음 타이머에서 이어 가요.
- M3의 16 MiB body 상한은 이것과 달라요. 큰 일을 거절하는 입구 상한이고, 나눠서 이어 하지 않아요. p99 10 ms는 장치가 아니라 목표예요. slice 크기를 정할 때 기준이 돼요.
- 정할 것 세 가지: 언제 깨울지, 한 번에 얼마나 할지, 멈춘 자리를 어떻게 기억할지.
- 언제 깨울지 (오라버니 대략 이해): 루프는 늦어도 `POLL_INTERVAL_MS`(100 ms)마다 깨어나요. 방법은 A(poll이 돌아올 때마다 우리가 시간 검사), B(`mg_timer_add`), C(요청마다 조금씩)예요. M3 issue 03의 쉬는 시간 검사와 같은 장치를 쓸지 정해야 해요. Redis는 `serverCron`(기본 1초에 10번)과 `beforeSleep`을 함께 써요.
- 얼마나 할지: 개수 상한은 단순하고 테스트하기 쉽지만 key마다 비용이 달라 시간을 보장하지 못해요. 시간 예산은 시간을 보장하지만 테스트하려면 시계를 바꿔 끼워야 해요. 삭제가 일으키는 rehash는 한 번에 모든 entry를 옮기므로 청소의 예산으로 자를 수 없어요.
- 멈춘 자리: 6번의 구조가 정해요. min-heap은 항상 맨 위만 보면 되므로 커서가 필요 없어요. 해시 테이블을 훑으면 커서가 필요하고, rehash가 일어나면 bucket 배치가 바뀌어 커서가 어긋날 수 있어요. 무작위 샘플링은 기억할 자리가 없어요.
- Pintos 대응: sleep list(깨어날 시각 순 정렬) ↔ 6번, timer interrupt ↔ 루프 타이머, time slice ↔ 시간 예산. 차이: Pintos는 선점형이에요.

## 8. Where the deadline lives

- **General options:** `struct entry`의 필드(모든 entry가 8바이트 늘어나요), TTL이 있는 key만 담는 별도 테이블.
- **Expected choice:** `struct entry`의 필드와 청소용 heap. store는 현재 시각을 인자로 받아요.
- **Redis:** 별도 dict `expires`에 둬요. TTL이 없는 key는 비용을 내지 않아요.
- **Our constraints:** store가 시각을 직접 읽으면 테스트가 `sleep`에 기대서 느려지고 결과가 흔들려요. 시각을 인자로 넘기면 공개 함수만 불러서 경계를 정확히 검사할 수 있어요. ADR `get-lends-value-until-next-change`도 확인해야 해요. active 청소가 "다음 변경"에 해당하므로, 조회한 뒤 응답을 다 보내기 전에 청소가 끼어들 수 있는지 봐야 해요.

Notes:

## 9. Overwrite and read effects on TTL

- **General options:** 덮어쓰면 TTL을 지우기, 덮어써도 TTL을 유지하기, 조회하면 TTL을 연장하기(sliding expiration).
- **Expected choice:** 덮어쓰면 entry가 통째로 바뀌므로 TTL도 그 요청이 새로 정해요. 조회는 TTL을 바꾸지 않아요.
- **Redis:** `SET`은 TTL을 지우고, `KEEPTTL`을 붙이면 유지해요. `GET`은 TTL을 건드리지 않아요. TTL을 바꾸며 읽으려면 `GETEX`를 써요.

Notes:

## 10. Boundaries, units, invalid values

- **General options:** 초 단위 또는 ms 단위, 만료 시각과 같은 순간을 만료로 볼지, 0과 음수 처리, 아주 큰 값의 오버플로.
- **Expected choice:** 초 단위 양의 정수만 받고, 그 밖의 값은 `400`과 새 오류 이유로 거절해요. 만료 시각과 같은 순간부터 만료로 봐요.
- **Redis:** 내부 단위는 ms이고, 문서에 오차가 0~1 ms라고 적혀 있어요. 0 이하의 TTL을 주면 key를 바로 지워요.

Notes:

## 11. TTL query and removal API

- **General options:** 만들지 않기, 남은 TTL 조회만, 조회와 해제.
- **Expected choice:** 만들지 않아요. L9 범위 밖이에요.
- **Redis:** `TTL`, `PTTL`로 조회해요(`-2`는 key 없음, `-1`은 만료 없음). `PERSIST`로 TTL을 해제해요.

Notes:

## Links to later milestones

- M5 `cache`는 무효화에 TTL을 쓸 가능성이 높아요.
- M6 `persist`는 3번에서 monotonic clock을 고르면 재시작 후 만료 시각을 복원할 수 없어요.
