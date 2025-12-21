import heapq
from collections import defaultdict

def build_path(parent, s, t):
    path = []
    x = t
    while x != parent[s]:
        path.append(x)
        x = parent[x]
    path.reverse()
    return path


def shortest_avoiding_efficient_edges(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> tuple[list[int], float] | None:
    def dijkstra(n: int, adj: list[list[tuple[int,int]]], s: int):
        dist: list[int] = [None for _ in range(n)]
        parent: list[int] = [-1 for _ in range(n)]
        hp = []
        heapq.heapify(hp)
        heapq.heappush(hp, (0, s))
        dist[s] = 0

        while hp:
            d, u = heapq.heappop(hp)
            if d > dist[u]:
                continue
            
            for v, w in adj[u]:
                if dist[v] is None or dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(hp, (dist[v], v))

        return dist, parent

    adjs: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    adjt: list[list[tuple[int, int]]] = [[] for _ in range(n)]

    for arista in edges:
        u, v, w = arista
        adjs[u].append((v, w))
        adjt[v].append((u, w))
    
    dist_s = dijkstra(n, adjs, s)[0]
    dist_t = dijkstra(n, adjt, t)[0]

    for u, v, w in edges:
        if dist_s[u] + w + dist_t[v] == dist_s[t]:
            adjs[u].remove((v, w))

    costos, parent = dijkstra(n, adjs, s)
    costo = costos[t]

    if costo is not None:
        path = build_path(parent, s, t)
        return path, costo
    else:
        return None
    
def max_edge_under_path_budget(n, edges: list[tuple[int, int, float]], s, t, C) -> tuple[int, int, float] | None:
    def dijkstra(n: int, adj: list[list[tuple[int,int]]], s: int):
        dist: list[int] = [None for _ in range(n)]
        parent: list[int] = [-1 for _ in range(n)]
        hp = []
        heapq.heapify(hp)
        heapq.heappush(hp, (0, s))
        dist[s] = 0

        while hp:
            d, u = heapq.heappop(hp)
            if d > dist[u]:
                continue
            
            for v, w in adj[u]:
                if dist[v] is None or dist[u] + w > dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(hp, (dist[v], v))

        return dist, parent

    adjs: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    adjt: list[list[tuple[int, float]]] = [[] for _ in range(n)]

    for arista in edges:
        u, v, w = arista
        adjs[u].append((v, w))
        adjt[v].append((u, w))
    
    dist_s = dijkstra(n, adjs, s)[0]
    dist_t = dijkstra(n, adjt, t)[0]

    best = (-1, -1, -1)
    for arista in edges:
        u, v, w = arista
        if dist_s[u] + w + dist_t[v] <= C and best[2] <= w:
            best = arista

    return best if best[1] != -1 else None

def min_path_with_at_most_one_negative(n: int, edges: list[tuple[int, int, float]], s: int, t: int) -> float | None:
    def dijkstra(n: int, adj: list[list[tuple[int, float]]], s: int):
        dist: list[int] = [INF for _ in range(n)]
        hp = []
        heapq.heapify(hp)
        dist[s] = 0
        heapq.heappush(hp, (0, s))

        while hp:
            d, u = heapq.heappop(hp)
            if d != dist[u]:
                continue

            for v, w in adj[u]:
                if w < 0:
                    continue
                elif dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(hp, (dist[v], v))
        
        return dist
    INF = 10**18
    adjs: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    adjt: list[list[tuple[int, float]]] = [[] for _ in range(n)]

    for arista in edges:
        u, v, w = arista
        adjs[u].append((v, w))
        adjt[v].append((u, w))

    dist_s = dijkstra(n, adjs, s)
    dist_t = dijkstra(n, adjt, t)

    for u, v, w in edges:
        if w >= 0:
            continue
        elif dist_s[u] + w + dist_t[v] < dist_s[t]:
            dist_s[t] = dist_s[u] + w + dist_t[v]

    return dist_s[t] if dist_s[t] != INF else None

def improving_edges_joint(n: int, edges: list[tuple[int, int, float]], s: int, t: int, candidates: list[tuple[int, int, float]]) -> list[tuple[int, int, float]]:
    def dijkstra(n, adj, s):
        dist: list[float] = [float("inf") for _ in range(n)]
        hp = []
        heapq.heapify(hp)
        dist[s] = 0
        heapq.heappush(hp, (0, s))

        while hp:
            d, u = heapq.heappop(hp)
            if d != dist[u]:
                continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(hp, (dist[v], v))
        
        return dist
    
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    adjs_c: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    adjt_c: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    res = []

    for u, v, w in edges:
        adj[u].append((v, w))

    for u, v, w in edges + candidates:
        adjs_c[u].append((v, w))
        adjt_c[v].append((u, w))

    base = dijkstra(n, adj, s)[t]
    dist_sc = dijkstra(n, adjs_c, s)
    dist_tc = dijkstra(n, adjt_c, t)

    if base > dist_sc[t]:
        for arista in candidates:
            u, v, w = arista
            if dist_sc[u] + w + dist_tc[v] == dist_sc[t]:
                res.append(arista)

    return res
    
def critical_edges(n: int, edges: list[tuple[int, int, float]], s: int, t: int) -> list[tuple[int, int, float]]:
    def dijkstra(n: int, adj: list[list[int, float]], s: int):
        dist: list[float] = [float("inf") for _ in range(n)]
        hp = []
        heapq.heapify(hp)
        heapq.heappush(hp, (0, s))
        dist[s] = 0

        while hp:
            d, u = heapq.heappop(hp)
            if d != dist[u]:
                continue
            
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(hp, (dist[v], v))
            
        return dist
    
    adjs: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    adjt: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    spg: list[list[tuple[int, float]]] = [[] for _ in range(n)]

    for u, v, w in edges:
        adjs[u].append((v, w))
        adjt[v].append((u, w))

    dist_s = dijkstra(n, adjs, s)
    if dist_s[t] == float("inf"):
        return []
    dist_t = dijkstra(n, adjt, t)
    used_edges = []

    for u, v, w in edges:
        if dist_s[u] + w + dist_t[v] == dist_s[t]:
            spg[u].append((v, w))
            used_edges.append((u, v, w))
    
    order = sorted(range(n), key=lambda x: (dist_s[x], x))

    waysS = [0]*n
    waysS[s] = 1
    for u in order:
        if waysS[u] == 0:
            continue
        for v, _ in spg[u]:
            waysS[v] += waysS[u]

    waysT = [0]*n
    waysT[t] = 1
    for u in reversed(order):
        for v, _ in spg[u]:
            waysT[u] += waysT[v]
    
    crit = []
    for u, v, w in used_edges:
        if waysS[u] * waysT[v] == waysS[t]:
            crit.append((u, v, w))
    
    return crit
    
def min_multiplicative_path(n: int, edges: list[tuple[int, int, float]], s: int, t: int) -> float | None:
    # Pesos mayores a 1
    INF = float("inf")
    def dijkstra_mult(n: int, adj: list[list[tuple[int, float]]], s: int):
        dist: list[float] = [INF for _ in range(n)]
        hp = []
        heapq.heapify(hp)
        dist[s] = 1
        heapq.heappush(hp, (dist[s], s))

        while hp:
            d, u = heapq.heappop(hp)
            if d != dist[u]:
                continue
            for v, w in adj[u]:
                if dist[u] * w < dist[v]:
                    dist[v] = dist[u] * w
                    heapq.heappush(hp, (dist[v], v))
        
        return dist

    adj_s: list[list[tuple[int, float]]] = [[] for _ in range(n)]

    for u, v, w in edges:
        adj_s[u].append((v, w))
    
    res = dijkstra_mult(n, adj_s, s)[t]
    return res if res != float("inf") else None

def has_profit_cycle(cabins_cost: list[float], travel_cost: list[tuple[int, int, float]]) -> bool:
    def bellman_ford(n: int, edges: list[tuple[int, int, float]], s: int) -> list[tuple[int, int, float]] | None:
        EPS = 1e-12
        dist: list[float] = [float("inf") for _ in range(n+1)]
        dist[s] = 0

        for _ in range(n):
            changed = False
            for u, v, w in edges:
                if dist[u] + w < dist[v] - EPS:
                    dist[v] = dist[u] + w
                    changed = True
            if not changed:
                break
        
        for u, v, w in edges:
            if dist[u] + w < dist[v] - EPS:
                return None
        
        return dist

    n = len(cabins_cost)

    edges: list[tuple[int, int, float]] = []
    for u, v, w in travel_cost:
        wprime = cabins_cost[v] + w
        edges.append((u, v, wprime))

    s = n
    for u in range(n):
        edges.append((s, u, 0.0))

    res = bellman_ford(n, edges, s)

    return res == None

def count_paths_dag(n: int, edges: list[tuple[int, int]]) -> int:
    def topological_sort(n: int, adj: list[list[int]]):
        def DFS(u: int):
            visited[u] = True
            
            for v in adj[u]:
                if not visited[v]:
                    DFS(v)
            order.append(u)

        visited: list[bool] = [False for _ in range(n)]
        order: list[int] = []

        for u in range(n):
            if not visited[u]:
                DFS(u)
        order.reverse()

        return order

    if not edges:
        return 0
    
    adj: list[list[int]] = [[] for _ in range(n)]

    for u, v in edges:
        adj[u].append(v)
    
    orden_topologico: list[int] = topological_sort(n, adj)
    dp = [0 for _ in range(n)]

    for u in reversed(orden_topologico):
        for v in adj[u]:
            dp[u] += 1 + dp[v]

    return sum(dp)

def solve_srd(n: int, inequalities: list[tuple[int, int, float]]) -> tuple[str, list[float]] | tuple[str, list[tuple[int, int, float]]]:
    def build_negative_cycle(parent, u, v):  # Acomodar, pide devolver el ciclo tal q: list[tuple[int, int, float]], es decir lista de aristas (u,v,w)
        x = u
        cycle = []
        while x != v:
            cycle.append(x)
            x = parent[x]
        cycle.append(v)
        cycle.reverse()
        return cycle
    
    dist: list[float] = [float("inf") for _ in range(n+1)]
    parent: list[int] = [-1 for _ in range(n+1)]
    dist[n] = 0
    v0 = n
    ghost = []
    for i in range(n):
        ghost.append((v0, i, 0.0))
    
    edges = inequalities + ghost

    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break
    
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return "UNSAT", inequalities
    
    return "SAT", dist[:n]

def assign_queues_linear(
        M: int, 
        fights: list[tuple[int, int, float, bool]], 
        friends: list[tuple[int, int, float]]
        ) -> tuple[str, list[int]] | tuple[str, list[tuple[int, int, float]]]:
    max_id = -1
    for i, j, _, _ in fights:
        max_id = max(max_id, i, j)
    for i, j, _ in friends:
        max_id = max(max_id, i, j)
    
    if max_id < 0:
        return "SAT", []
    
    n_people = max_id + 1

    c = n_people
    n_nodes = n_people + 1

    ineq: list[tuple[int, int, float]] = []

    # Rango
    for i in range(n_people):
        ineq.append((c, i, float(M)))
        ineq.append((i, c, -1.0))

    # Peleas
    for i, j, K, left_is_i in fights:
        w = float(K)
        if left_is_i:
            ineq.append((j, i, -w))
        else:
            ineq.append((i, j, -w))

    # Amistades
    for k, m, L in friends:
        w = float(L)
        ineq.append((m, k, w))
        ineq.append((k, m, w))
    
    status, data = solve_srd(n_nodes, ineq)

    if status == "UNSAT":
        return status, data
    
    dist = data
    base = dist[c]

    assigment: list[int] = []
    for i in range(n_people):
        x = dist[i] - base
        x_int = int(round(x))
        assigment.append(x_int)
    
    return "SAT", assigment

def is_geodesic(n: int, edges: list[tuple[int, int, float]], D: list[tuple[int, int]]) -> bool:  # En los test te pasa un set() con vertices, te deberia pasar un set() de pares (u,v)
    cubierto: list[bool] = [False for _ in range(n)]
    def floyd_warshall(n: int, edges: list[tuple[int, int, float]]):
        dist: list[list[int]] = [[float("inf") for _ in range(n)] for _ in range(n)]

        for i in range(n): 
                dist[i][i] = 0
        
        for u, v, w in edges:
            dist[u][v] = w
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        for i in range(n):
            if dist[i][i] < 0:
                return False
        print(dist)
        return dist
    
    distancias = floyd_warshall(n, edges)
    if distancias == False:
        return False
    
    for i in D:
        for j in D:
            for k in range(n):
                if distancias[i][k] + distancias[k][j] == distancias[i][j]:
                    cubierto[k] = True

    for i in range(len(cubierto)):
        if not cubierto[i]:
            return False
    
    return True
