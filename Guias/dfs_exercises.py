# Ejercicio 1 #
timer: int = 0
def dfs_times(adj: list[list[int]], start: int):
    global timer
    visited: list[bool] = [False for _ in range(len(adj))]
    parent: list[int] = [None for _ in range(len(adj))]
    tin: list[int] = [None for _ in range(len(adj))]
    tout: list[int] = [None for _ in range(len(adj))]

    timer = 0
    parent[start] = -1

    def DFS(s):
        global timer
        nonlocal visited, parent, tin, tout
        visited[s] = True
        timer += 1
        tin[s] = timer

        for vecino in adj[s]:
            if not visited[vecino]:
                parent[vecino] = s
                DFS(vecino)
        
        timer += 1
        tout[s] = timer

    DFS(start)

    return tin, tout, parent

def connected_components(adj: list[list[int]]):
    comps: list[list[int]] = []
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    componente: list[int]

    def DFS(s):
        nonlocal visited, componente
        visited[s] = True
        componente.append(s)

        for vecino in adj[s]:
            if not visited[vecino]:
                DFS(vecino)

    for v in range(n):
        if not visited[v]:
            componente = []
            DFS(v)
            comps.append(componente)
    
    return comps

def find_undirected_cycle(adj: list[list[int]]):
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    parent: list[int] = [None for _ in range(n)]
    has_cycle: bool = False
    cycle: list[int] = []

    def DFS(u):
        nonlocal visited, parent, has_cycle
        visited[u] = True

        for vecino in adj[u]:
            if has_cycle:
                break
            if not visited[vecino]:
                parent[vecino] = u
                DFS(vecino)
            elif parent[u] != vecino:
                has_cycle = True
                armar_ciclo(u, vecino)
                break
                

    def armar_ciclo(u, v):
        nonlocal cycle
        cycle = [u]
        w = u
        while w != v:
            w = parent[w]
            cycle.append(w)

    for v in range(n):
        if has_cycle:
            return cycle
        if not visited[v]:
            parent[v] = -1
            DFS(v)

    return []

def classify_edges_directed(adj: list[list[int]]):
    global timer
    timer = 0
    n = len(adj)
    visited: list[bool] = [False for _ in range(n)]
    tin: list[int] = [None for _ in range(n)]
    tout: list[int] = [None for _ in range(n)]
    tree: list[(int, int)] = []
    forward: list[(int, int)] = []
    back: list[(int, int)] = []
    cross: list[(int, int)] = []
    tree_edges = set()
    
    def ancestro(u, v):
        return tin[u] <= tin[v] and tout[v] <= tout[u] and u != v

    def DFS(u):
        global timer
        nonlocal visited, tin, tout, tree, forward, back, cross, tree_edges
        timer += 1
        tin[u] = timer
        visited[u] = True

        for vecino in adj[u]:
            if not visited[vecino]:
                tree.append((u,vecino))
                tree_edges.add((u,vecino))
                DFS(vecino)

        timer += 1
        tout[u] = timer

    for v in range(n):
        if not visited[v]:
            DFS(v)

    for u in range(n):
        for v in adj[u]:
            if (u, v) in tree_edges:
                continue
            if u == v:
                back.append((u, v))
            elif not ancestro(u, v) and not ancestro(v, u):
                cross.append((u, v))
            elif ancestro(v, u):
                back.append((u, v))
            elif ancestro(u, v) and (u, v) not in tree_edges:
                forward.append((u, v))
    
    return tree, back, forward, cross

def bipartite_or_odd_cycle(adj: list[list[int]]):
    n = len(adj)
    color: list[int] = [None for _ in range(n)]
    es_bipartito: bool = True
    parent: list[int] = [None for _ in range(n)]
    cycle: list[int] = []
    visited: list[bool] = [False for _ in range(n)]

    def armar_ciclo(u, v):
        nonlocal cycle
        cycle = [u]
        w = u
        while w != v:
            w = parent[w]
            cycle.append(w)

    def DFS(u):
        nonlocal color, es_bipartito, parent, visited
        visited[u] = True

        for vecino in adj[u]:
            if not es_bipartito:
                break
            if not visited[vecino]:
                visited[vecino] = True
                parent[vecino] = u
                color[vecino] = int(not color[u])
                DFS(vecino)
            if color[vecino] == color[u]:
                es_bipartito = False
                armar_ciclo(u, vecino)

    for v in range(n):
        if not visited[v]:
            parent[v] = -1
            color[v] = 0
            DFS(v)

    if es_bipartito:
        return es_bipartito, color
    return es_bipartito, cycle

def bridges(adj: list[list[int]]):
    n = len(adj)
    timer = 0
    parent: list[int] = [None for _ in range(n)]
    tin: list[int] = [None for _ in range(n)]
    low: list[int] = [None for _ in range(n)]
    visited: list[bool] = [False for _ in range(n)]
    puentes: list[(int, int)] = []

    def DFS(u):
        nonlocal timer, parent, tin, low, visited, puentes
        timer += 1
        tin[u] = low[u] = timer

        for vecino in adj[u]:
            if vecino == parent[u]:
                continue
            if not visited[vecino]:
                visited[vecino] = True
                parent[vecino] = u
                DFS(vecino)
                low[u] = min(low[u], low[vecino])
                if low[vecino] > tin[u]:
                    puentes.append((u, vecino))
            elif parent[u] != vecino:
                low[u] = min(low[u], tin[vecino])

    for v in range(n):
        if not visited[v]:
            parent[v] = -1
            visited[v] = True
            DFS(v)

    return puentes

def articulation_points(adj: list[list[int]]): # Falta regla de la raiz: Raiz con dos o mas hijos = articulacion
    n = len(adj)
    timer = 0
    parent: list[int] = [None for _ in range(n)]
    tin: list[int] = [None for _ in range(n)]
    low: list[int] = [None for _ in range(n)]
    visited: list[bool] = [False for _ in range(n)]
    articulation: list[int] = []

    def DFS(u):
        nonlocal timer, parent, tin, low, visited, articulation
        visited[u] = True
        timer += 1
        tin[u] = low[u] = timer

        for vecino in adj[u]:
            if vecino == parent[u]:
                continue
            if not visited[vecino]:
                parent[vecino] = u
                DFS(vecino)
                low[u] = min(low[u], low[vecino])
                if low[vecino] >= tin[u]:
                    articulation.append(u)
            else:
                low[u] = min(low[u], tin[vecino])

    for v in range(n):
        if not visited[v]:
            parent[v] = -1
            DFS(v)

    return articulation

def topo_or_cycle(adj: list[list[int]]):
    n = len(adj)
    color: list[int] = [0 for _ in range(n)]
    parent: list[int] = [None for _ in range(n)]
    has_cycle: bool = False
    cycle: list[int] = []
    order: list[int] = []

    def build_cycle(u, v):
        nonlocal cycle
        cycle.append(u)
        w = u
        while w != v:
            w = parent[w]
            cycle.append(w)
        cycle.reverse()

    def DFS(u):
        nonlocal color, parent, has_cycle, order
        color[u] += 1

        for vecino in adj[u]:
            if has_cycle:
                break
            if color[vecino] == 2:
                continue
            if color[vecino] == 1:  # Back-edge
                has_cycle = True
                parent[vecino] = u
                build_cycle(u, vecino)
            if color[vecino] == 0:
                parent[vecino] = u
                DFS(vecino)
        color[u] += 1
        order.append(u)

    for v in range(n):
        if has_cycle:
            return False, cycle
        if color[v] == 0:
            parent[v] = -1
            DFS(v)
    order.reverse()
    
    return True, order