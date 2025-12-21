from typing import List
import heapq

class DSU:
    def __init__(self, n: int):
        self.parent: List[int] = list(range(n))
        self.size: List[int] = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        # Path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True
    
    def same(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)
    
    def comp_size(self, a: int) -> int:
        return self.size[self.find(a)]


def kruskal_mst(n: int, edges: list[tuple[int, int, int]]):
    mst_weight: int = 0
    mst_edges: list[tuple[int, int, int]] = []
    uf: DSU = DSU(n)
    edges_sorted = sorted(edges, key= lambda x: (x[2], x[0], x[1]))

    for u, v, w in edges_sorted:
        if uf.find(u) != uf.find(v):
            mst_edges.append((u,v,w))
            mst_weight += w
            uf.union(u,v)

    return mst_weight, mst_edges


def prim_mst(n: int, adj: list[list[tuple[int, int]]]):
    INF = 10**18
    root = 0
    mst_weight: int = 0
    parent: list[int] = [None for _ in range(n)]
    key: list[int] = [INF for _ in range(n)]
    inMST: list[bool] = [False for _ in range(n)]
    key[root] = 0
    parent[root] = -1

    pq = [(0, root)]
    taken = 0
    
    while pq and taken < n:
        k, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        mst_weight += k
        taken += 1

        for v, w in adj[u]:
            if not inMST[v] and w < key[v]:
                key[v] = w
                parent[v] = u
                heapq.heappush(pq, (w, v))
        
    return mst_weight, parent
                
