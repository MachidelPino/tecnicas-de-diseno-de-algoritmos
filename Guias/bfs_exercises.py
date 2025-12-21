from collections import deque

def bfs_tree(adj: list[list[int]], s: int):
    n = len(adj)
    parent: list[int] = [None for _ in range(n)]
    q: deque[int] = deque()
    dist: list[int] = [-1 for _ in range(n)]
    visited: list[bool] = [False for _ in range(n)]
    parent[s] = -1
    dist[s] = 0
    visited[s] = True
    q.append(s)

    while q:
        u = q.pop()
        for vecino in adj[u]:
            if not visited[vecino]: 
                visited[vecino] = True
                dist[vecino] = dist[u] + 1
                parent[vecino] = u
                q.append(vecino)
    
    return dist, parent

def shortest_path(adj: list[list[int]], s: int, t: int):
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    parent: list[int] = [None for _ in range(n)]
    dist: list[int] = [-1 for _ in range(n)]
    q: deque = deque()
    path: list[int] = []
    visited[s] = True
    parent[s] = -1
    dist[s] = 0
    q.append(s)
    
    def rebuild_path():
        nonlocal path
        v = t
        while v != s:
            path.append(v)
            v = parent[v]
        path.append(s)
        path.reverse()

    while q:
        if visited[t]:
            break
        u = q.pop()
        for vecino in adj[u]:
            if not visited[vecino]:
                visited[vecino] = True
                parent[vecino] = u
                dist[vecino] = dist[u] + 1
                q.append(vecino)
                if vecino == t:
                    rebuild_path()
                    break
    return path

def bipartite_bfs(adj: list[list[int]]):
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    parent: list[int] = [None for _ in range(n)]
    dist: list[int] = [-1 for _ in range(n)]
    is_bipartite: bool = True
    color: list[int] = [None for _ in range(n)]
    q: deque = deque()
    cycle: list[int] = []

    def rebuild_cycle(v, u):
        nonlocal cycle
        path1: list[int] = []
        path2: list[int] = []
        if dist[v] > dist[u]:
            w = v
            z = u
        else:
            w = u
            z = v
        while dist[w] > dist[z]:
            path1.append(w)
            w = parent[w]
        while w != z:
            path1.append(w)
            path2.append(z)
            w = parent[w]
            z = parent[z]

        path1.append(w)
        path2.reverse()
        cycle = path1 + path2
        print(cycle)
        
        return cycle

    for v in range(n):
        if not is_bipartite:
            break
        if not visited[v]:
            visited[v] = True
            parent[v] = -1
            dist[v] = 0
            color[v] = 0
            q.append(v)
            while q:
                if not is_bipartite:
                    break
                u = q.pop()
                for vecino in adj[u]:
                    if not visited[vecino]:
                        visited[vecino] = True
                        parent[vecino] = u
                        dist[vecino] = dist[u] + 1
                        color[vecino] = int(not color[u])
                        q.append(vecino)
                    elif color[vecino] == color[u]:
                        is_bipartite = False
                        rebuild_cycle(vecino, u)
                        break
    
    return (True, color) if is_bipartite else (False, cycle)

def connected_components_bfs(adj: list[list[int]]):
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    comps: list[list[int]] = []
    ncomp: int = -1
    q: deque = deque()

    for v in range(n):
        if not visited[v]:
            ncomp += 1
            comps.append([])
            visited[v] = True
            comps[ncomp].append(v)
            q.append(v)
            while q:
                u = q.pop()
                for vecino in adj[u]:
                    if not visited[vecino]:
                        visited[vecino] = True
                        comps[ncomp].append(vecino)
                        q.append(vecino)
    
    return comps

def multisource_dist_directed(adj: list[list[int]], sources: list[int]):
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    dist: list[int] = [-1 for _ in range(n)]
    q: deque = deque()

    for s in sources:
        dist[s] = 0
        visited[s] = True
        q.append(s)
        while q:
            u = q.pop()
            for vecino in adj[u]:
                if not visited[vecino]:
                    visited[vecino] = True
                    dist[vecino] = dist[u] + 1
                    q.append(vecino)
                else:
                    dist[vecino] = min(dist[vecino], dist[u] + 1)
                    q.append(vecino)
    
    return dist

def grid_shortest_path(grid: list[list[int]], s: tuple[int, int], t: tuple[int, int]):
    m = len(grid)
    n = len(grid[0])
    visited: list[list[bool]] = [[False for _ in range(n)] for _ in range(m)]
    dist: list[list[int]] = [[-1 for _ in range(n)] for _ in range(m)]
    q: deque[tuple[int, int]] = deque()
    q.append(s)
    visited[s[0]][s[1]] = True
    dist[s[0]][s[1]] = 0
    movimientos: list[tuple[int, int]] = [(-1, 0),(1, 0),(0, -1),(0, 1)]

    while q:
        u1, u2 = q.pop()
        for v1, v2 in movimientos:
            n1 = u1 + v1
            n2 = u2 + v2
            if n1 in range(m) and n2 in range(n):
                if grid[n1][n2] == 1:
                    continue
                elif not visited[n1][n2]:
                    visited[n1][n2] = True
                    dist[n1][n2] = dist[u1][u2] + 1
                    q.append([n1, n2])

    return dist[t[0]][t[1]]

def grid_multisource_dist(grid: list[list[int]], sources: list[tuple[int, int]]):
    m = len(grid)
    n = len(grid[0])
    visited: list[list[bool]] = [[False for _ in range(n)] for _ in range(m)]
    dist: list[list[int]] = [[-1 for _ in range(n)] for _ in range(m)]
    q: deque[tuple[int, int]] = deque()
    movimientos: list[tuple[int, int]] = [(0,-1),(0,1),(1,0),(-1,0)]

    for v1, v2 in sources:
        q.clear()
        dist[v1][v2] = 0
        visited[v1][v2] = True
        q.append([v1, v2])
        while q:
            print(q)
            u1, u2 = q.pop()
            for m1, m2 in movimientos:
                n1 = u1 + m1
                n2 = u2 + m2
                if n1 in range(m) and n2 in range(n):
                    if grid[n1][n2] == 1:
                        continue
                    elif not visited[n1][n2]:
                        visited[n1][n2] = True
                        dist[n1][n2] = dist[u1][u2] + 1
                        q.append([n1, n2])
                    else:
                        if dist[n1][n2] == dist[u1][u2] + 1:
                            continue
                        else:
                            dist[n1][n2] = min(dist[n1][n2], dist[u1][u2] + 1)
                            q.append([n1,n2])
    
    return dist