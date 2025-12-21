import sys
from collections import deque

def maquina_misterios():
    data = sys.stdin.buffer.read().split()
    n, m = map(int, data[:2])

    
    if m <= n:
        print(n - m)
        return

    LIMIT = 2 * m + 2  
    dist = [-1] * (LIMIT + 1)
    q = deque([n])
    dist[n] = 0

    while q:
        u = q.popleft()
        if u == m:
            print(dist[u])
            return

        
        if u > 1 and dist[u - 1] == -1:
            dist[u - 1] = dist[u] + 1
            q.append(u - 1)

        
        v = u * 2
        if v <= LIMIT and dist[v] == -1:
            dist[v] = dist[u] + 1
            q.append(v)

if __name__ == "__main__":
    maquina_misterios()
