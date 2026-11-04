"""하노이 탑을 '상태 그래프' 위의 BFS로 풀어봅니다.

노드 = 게임의 한 상황.  state[i] = i번 원반이 올려진 기둥 번호 (원반 0이 가장 작음)
간선 = 규칙에 맞는 한 수.

BFS로 시작 상황에서 목표 상황까지의 최단 거리를 구하면,
그 값이 재귀 해법의 이동 횟수 2**n - 1과 정확히 같습니다.
"""
from collections import deque

N = 3
START = (0,) * N          # 전부 0번 기둥
GOAL = (2,) * N           # 전부 2번 기둥


def neighbors(state):
    """이 상황에서 한 수 만에 갈 수 있는 모든 상황."""
    top = {}                                   # top[기둥] = 그 기둥의 맨 위 원반
    for disk, peg in enumerate(state):         # 원반 0이 가장 작으므로 먼저 만난 것이 맨 위
        top.setdefault(peg, disk)

    result = []
    for peg, disk in top.items():              # 각 기둥의 맨 위 원반을
        for dest in range(3):                  # 다른 기둥으로 옮겨봄
            if dest == peg:
                continue
            if dest in top and top[dest] < disk:
                continue                       # 더 작은 원반 위에는 못 놓음
            moved = list(state)
            moved[disk] = dest
            result.append((tuple(moved), disk, peg, dest))
    return result


# ---- BFS. 구조는 bfs_trace.py와 완전히 같습니다 ----
dist = {START: 0}
parent = {START: None}
q = deque([START])

while q:
    v = q.popleft()
    for w, disk, src, dst in neighbors(v):
        if w not in dist:
            dist[w] = dist[v] + 1
            parent[w] = (v, disk, src, dst)
            q.append(w)

print(f"원반 {N}개")
print(f"도달 가능한 상황의 수 = {len(dist)}   (3**{N} = {3**N})")
print(f"목표까지 최단 거리     = {dist[GOAL]}   (2**{N} - 1 = {2**N - 1})")

# 거리별로 상황이 몇 개씩 있는지 = BFS의 '레이어'
layers = {}
for state, d in dist.items():
    layers[d] = layers.get(d, 0) + 1
print("\n거리별 상황 개수 (= BFS 레이어):")
for d in sorted(layers):
    print(f"  거리 {d:2}: {layers[d]:2}개  {'#' * layers[d]}")

# parent를 거꾸로 따라가며 실제 수순 복원
steps = []
cur = GOAL
while parent[cur] is not None:
    prev, disk, src, dst = parent[cur]
    steps.append(f"원반 {disk} : 기둥 {src} -> 기둥 {dst}")
    cur = prev
steps.reverse()

print("\nBFS가 찾아낸 최단 수순:")
for i, s in enumerate(steps, 1):
    print(f"  {i}. {s}")


# ---- 재귀 해법과 비교 ----
rec = []
def hanoi(n, src, dst, via):
    if n == 0:
        return
    hanoi(n - 1, src, via, dst)
    rec.append(f"원반 {n - 1} : 기둥 {src} -> 기둥 {dst}")
    hanoi(n - 1, via, dst, src)

hanoi(N, 0, 2, 1)
print(f"\n재귀 해법의 수순 개수 = {len(rec)}")
print(f"두 수순이 완전히 같은가? {steps == rec}")
