# 크래프톤 정글 팀 환경 참고본 (6주차 이후)
#
# 출처: krafton-jungle/data_structures_docker 의 .devcontainer/Dockerfile 을
#       기반으로, 팀 공용으로 쓸 때 문제가 되는 지점 세 곳을 고쳤다.
#       원본과 다른 부분에는 [변경] 주석을 달아 두었다.
#
# 사용:
#   docker build -t jungle-team .
#   docker run -it --rm \
#     -v "$PWD":/work -w /work \
#     --device=/dev/kvm \          # 핀토스 주차에만 필요
#     jungle-team bash

FROM ubuntu:22.04
# [변경] 원본은 ubuntu:latest 였다. latest 는 시점마다 다른 배포판을 가리켜서
#        팀원끼리 같은 Dockerfile로 다른 환경을 얻게 된다. 버전을 못 박는다.
#        22.04 를 고른 이유: pintos-kaist 가 18.04~20.04 시절에 만들어졌고,
#        22.04(gcc 11)가 그 코드와 현행 패키지 사이의 타협점이다.

ENV TZ=Asia/Seoul LANG=ko_KR.UTF-8 LANGUAGE=ko_KR.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    locales tzdata \
    build-essential gcc make cmake \
    gcc-multilib \
    gdb valgrind \
    python3 python3-pip \
    git vim curl wget \
    sudo telnet net-tools iproute2 \
 && locale-gen ko_KR.UTF-8 && update-locale LANG=ko_KR.UTF-8 \
 && rm -rf /var/lib/apt/lists/*
# [변경] gcc-multilib 추가. 6주차 malloc lab(CS:APP)의 Makefile 은 통상
#        CFLAGS 에 -m32 를 쓴다. 이게 없으면 32비트 빌드가 실패한다.
#        팀 과제가 64비트로만 돈다면 빼도 된다.
# [변경] --no-install-recommends 와 apt 캐시 삭제 추가. 이미지가 수백 MB 줄고,
#        팀원마다 받는 용량이 준다.

# --- 핀토스 주차(7~10주)에만 필요. 그 전에는 주석 처리해 두면 이미지가 가볍다.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     qemu-system-x86 \
#  && rm -rf /var/lib/apt/lists/*
# pintos-kaist 가 실제로 요구하는 패키지 목록은 해당 주차에 저장소 문서를
# 직접 확인할 것. 여기 적힌 것은 최소 추정치다.

# [변경] uid/gid 를 1000 으로 명시하고 kvm 그룹에 넣는다.
#        이유 1: 호스트(WSL) 사용자도 uid 1000 이라, 컨테이너가 bind mount 에
#                만든 파일이 호스트에서 본인 소유로 남는다. 어긋나면 root 소유
#                파일이 생겨 호스트에서 sudo 없이 지우지 못한다.
#        이유 2: --device=/dev/kvm 을 넘겨도 컨테이너 유저가 kvm 그룹에 없으면
#                QEMU 가 가속을 못 쓰고 순수 에뮬레이션으로 떨어진다.
#        (팀원 중 uid 가 1000 이 아닌 사람이 있으면 build-arg 로 받도록 바꾼다.)
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd -g ${USER_GID} jungle \
 && useradd -m -u ${USER_UID} -g ${USER_GID} -s /bin/bash jungle \
 && usermod -aG sudo jungle \
 && groupadd -f -g 991 kvm && usermod -aG kvm jungle \
 && echo 'jungle ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/jungle

USER jungle
WORKDIR /work
# [변경] 원본은 WORKDIR /home/jungle 이었다. bind mount 지점을 작업 디렉터리로
#        삼아야 컨테이너에 들어가자마자 소스가 보인다.
