"""visited를 통째로 없앤 BFS. 무한 루프에 빠지는 것을 보여줍니다.

실행:
    python3 bfs_no_visited.py

visited가 없으면 사이클(A-B-E-D-A)을 따라 같은 노드를 계속 다시 발견합니다.
q에서 하나 꺼낼 때마다 이웃을 여러 개 넣으므로 q는 줄어들 틈 없이 계속 커집니다.
`while q:`는 q가 비어야 끝나는데 영영 비지 않으므로, 진짜로 실행하면
메모리가 바닥날 때까지 돌아갑니다. 그래서 아래에서는 12바퀴로 강제 종료합니다.
"""
from collections import deque

from graph import graph

LIMIT = 12

q = deque(['A'])
order = []

for turn in range(1, LIMIT + 1):
    v = q.popleft()
    order.append(v)
    for w in graph[v]:
        q.append(w)            # visited 검사가 없으므로 무조건 다시 넣습니다
    print(f"{turn:2}바퀴  처리={v}  q크기={len(q):2}  q={list(q)}")

print(f"\n처리 순서: {' '.join(order)}")
print(f"{LIMIT}바퀴를 돌았는데도 q에 {len(q)}개가 남아 있습니다. 계속 커지는 중입니다.")
print("A가 여러 번 처리된 것을 보세요. bfs_trace.py에서는 딱 한 번씩만 처리됩니다.")
