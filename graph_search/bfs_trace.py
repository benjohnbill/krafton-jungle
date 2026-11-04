"""BFS를 한 바퀴씩 추적하면서 visited와 q의 상태를 전부 출력합니다.

실행:
    python3 bfs_trace.py          # 'A'에서 출발
    python3 bfs_trace.py G        # 'G'에서 출발

보아야 할 것 두 가지:
  1. visited의 크기는 한 번도 줄지 않습니다.  (계단처럼 올라가기만 함)
  2. q의 크기는 늘었다 줄었다 하다가 0으로 끝납니다.  (산 모양)
"""
import sys
from collections import deque

from graph import graph


def show(tag, visited, q):
    print(f"    {tag:<20} visited={sorted(visited)}  (크기 {len(visited)})")
    print(f"    {'':<20} q      ={list(q)}  (크기 {len(q)})")


def bfs(start):
    # visited: 이미 발견한 노드. 한 번 들어가면 절대 안 나옵니다.  -> 중복 방지 담당
    # q:       아직 처리하지 않은 노드. 처리하면 빠집니다.          -> 순서 결정 담당
    visited = {start}
    q = deque([start])
    order = []

    print(f"[시작] start = {start!r}")
    show("초기 상태", visited, q)

    turn = 0
    while q:                       # 바깥 루프: 노드 하나를 '처리'하는 단위
        turn += 1
        v = q.popleft()            # 가장 먼저 들어온 것을 꺼냄 (FIFO)
        order.append(v)

        print(f"\n=== 바깥 while {turn}번째 바퀴 ===")
        print(f"    q.popleft() -> v = {v!r}   (q가 하나 줄어듭니다)")
        show("popleft 직후", visited, q)
        print(f"    이웃 목록 graph[{v!r}] = {graph[v]}")

        for w in graph[v]:         # 안쪽 루프: v의 이웃을 하나씩 살펴봄
            if w not in visited:   # w는 이 for문이 매 바퀴 새로 대입하는 변수입니다
                visited.add(w)     # 도장 찍기   — 두 번 다시 안 건드림
                q.append(w)        # 할 일 등록 — 나중에 처리할 것
                print(f"      w={w!r} -> 처음 봄. visited에 추가 + q에 추가")
            else:
                print(f"      w={w!r} -> 이미 visited에 있음. 아무것도 안 함")

        show("이웃 처리 후", visited, q)

    print("\n[끝] q가 비어서 while 종료.")
    print(f"     처리 순서   = {' '.join(order)}")
    print(f"     visited 최종 = {sorted(visited)}  (크기 {len(visited)})")
    print(f"     q      최종 = {list(q)}  (크기 {len(q)})")
    return order


if __name__ == '__main__':
    start = sys.argv[1] if len(sys.argv) > 1 else 'A'
    if start not in graph:
        sys.exit(f"'{start}'는 그래프에 없는 노드입니다. 가능한 값: {sorted(graph)}")
    bfs(start)
