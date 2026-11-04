"""각 노드가 '언제 발견되어 q에 들어갔고', '언제 pop되어 for문을 돌았는지' 기록합니다.

핵심: 모든 노드가 발견 시각과 처리 시각을 하나씩 가집니다.
      visited에 일찍 들어갔다고 해서 처리 차례를 건너뛰는 노드는 없습니다.
"""
from collections import deque


start = 'A'
visited = {start}
q = deque([start])
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'F'],
    'D': ['A', 'E'],
    'E': ['B', 'D', 'F', 'G'],
    'F': ['C', 'E'],
    'G': ['E'],
}

found_at = {start: '시작'}   # 언제 q에 들어갔는가
done_at = {}                 # 언제 pop되어 for문을 돌았는가
turn = 0

while q:
    turn += 1
    v = q.popleft()
    done_at[v] = turn
    for w in graph[v]:
        if w not in visited:
            visited.add(w)
            q.append(w)
            found_at[w] = f"{turn}바퀴({v}가 발견)"

print(f"{'노드':<5} {'q에 들어간 시점':<22} {'pop되어 for문 돈 시점'}")
print("-" * 60)
for node in sorted(graph):
    print(f"{node:<6} {found_at[node]:<24} {done_at[node]}바퀴")

print()
print(f"노드 개수      = {len(graph)}")
print(f"for문 돈 노드  = {len(done_at)}   <- 빠진 노드가 없습니다")
print(f"G를 발견한 것은 {found_at['G']}, G 자신이 for문을 돈 것은 {done_at['G']}바퀴")
