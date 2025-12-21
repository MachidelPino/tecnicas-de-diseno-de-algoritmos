import sys
import heapq
from bisect import bisect_left

def read_ints():
    return list(map(int, sys.stdin.buffer.readline().split()))

def leer_input():
    n, m = read_ints()

    # Lista de adyacencia, (vecino, tiempo)
    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = read_ints()
        g[u].append((v, w))
        g[v].append((u, w))

    bloqueados = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        line = read_ints() 
        ki = line[0]
        if ki:
            bloqueados[i] = line[1:]  

    return n, m, g, bloqueados

def viaje_intergalactico():
    def next_time(t, bloqueados_de_u):
        arr = bloqueados_de_u
        pos = bisect_left(arr, t)
        
        while pos < len(arr) and arr[pos] == t:
            t += 1
            pos += 1
        return t


    n, _, g, bloqueados = leer_input()
    INF = 10**18
    dist = [INF] * (n + 1)
    hp = []
    dist[1] = 0
    heapq.heappush(hp, (0, 1))

    while hp:
        d, u = heapq.heappop(hp)
        if d != dist[u]:
            continue

        
        t0 = next_time(dist[u], bloqueados[u])

        for v, w in g[u]:
            nd = t0 + w           
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(hp, (nd, v))


    print(-1 if dist[n] >= INF else dist[n])   

if __name__ == "__main__":
    viaje_intergalactico()
