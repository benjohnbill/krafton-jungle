# 팀 환경 참고본 (6주차 이후)

2026-09-10 작성. 팀 배정과 6주차 과제 내용이 공지되기 **전에** 미리 써 둔 것이다.
확정 사양이 아니라, 팀이 환경 이야기를 꺼낼 때 내놓을 초안 또는 대조표다.

## 근거가 있는 것과 추정인 것

| 내용 | 근거 |
|---|---|
| 원본 Dockerfile 구조 | `krafton-jungle/data_structures_docker` 실물 |
| uid 1000 일치 문제 | 2026-09-10 실측. 컨테이너가 bind mount 에 쓴 파일이 호스트에서 `benjohnbill` 소유로 남는 것을 확인 |
| `/dev/kvm` 존재 | 실측. `crw-rw---- root:kvm`, 호스트 사용자는 kvm 그룹 **미포함** |
| `/mnt/c` 성능 저하 | 실측. 파일 300개 쓰기·읽기가 1,492ms 대 5,216ms (3.5배) |
| gcc 15 의 C23 기본값 | 실측. implicit declaration 이 경고가 아니라 **에러** |
| `gcc-multilib` 필요 | **추정**. CS:APP malloc lab 이 통상 `-m32` 를 쓴다는 일반적 사실에 근거 |
| `qemu-system-x86` | **추정**. pintos-kaist 요구 패키지는 해당 주차에 저장소 문서로 확인할 것 |
| 22.04 선택 | **판단**. pintos-kaist 가 18.04~20.04 시절 코드라는 점에서 고른 타협점 |

## 팀 Dockerfile을 검토할 때 볼 세 지점

1. **베이스 이미지에 버전이 박혀 있는가.** `ubuntu:latest` 면 팀원마다 다른
   환경을 받는다. 컨테이너를 쓰는 이유 자체가 무너진다.
2. **`USER` 가 root 가 아니고 uid 가 1000 인가.** root 로 돌면 컨테이너가 만든
   오브젝트 파일이 호스트에서 root 소유로 찍혀, 호스트에서 지우려면 sudo 가
   필요해진다. 팀원 uid 가 제각각이면 `ARG USER_UID` 로 받는다.
3. **핀토스 주차라면 `--device=/dev/kvm` 이 있는가.** 없으면 QEMU 가 순수
   에뮬레이션으로 떨어져 `make check` 한 바퀴가 몇 배 느려진다. 컨테이너 유저가
   `kvm` 그룹에 있어야 한다는 조건이 따라온다.

## 실행

```bash
# 빌드 (팀원마다 각자 한 번)
docker build -t jungle-team .

# 일반 주차
docker run -it --rm -v "$PWD":/work -w /work jungle-team bash

# 핀토스 주차
docker run -it --rm -v "$PWD":/work -w /work --device=/dev/kvm jungle-team bash
```

소스는 반드시 WSL 파일시스템(`~/dev/...`)에 둔다. `/mnt/c` 아래면 위 표의
3.5배 차이가 빌드마다 붙는다.

## Zed 사용자의 작업 배치

Zed 는 Dev Containers 를 지원하지 않는다. VS Code 처럼 에디터를 컨테이너 안으로
옮기는 대신, 이렇게 나눈다.

```
Windows Zed ──remote──> WSL 호스트          편집, git
                          └─ 컨테이너 터미널  빌드, 실행, gdb
```

bind mount 라 양쪽이 같은 파일을 본다. Zed 에서 저장하면 컨테이너에 즉시 반영된다.

## 6주차에 다시 켜기

5주차까지는 데몬을 내려 두는 것을 전제로 한다 (`dockerd` + `containerd` 상주
328MB). 다시 쓸 때:

```bash
sudo systemctl enable --now docker.service
```

또는 `docker.socket` 만 켜 두면 `docker` 명령을 칠 때 데몬이 자동으로 뜬다.
