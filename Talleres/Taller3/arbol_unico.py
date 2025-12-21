import sys
from collections import deque
from array import array
sys.setrecursionlimit(1 << 25)

def read_ints():
    return list(map(int, sys.stdin.buffer.readline().split()))


class DSU:
    def __init__(self, n):
        self.p = array('i', range(n+1))
        self.r = array('i', [0]*(n+1))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True

def solve():
    n, m = read_ints()
    edges = []
    for idx in range(m):
        u, v, w = read_ints()
        edges.append((w, u, v, idx))

    
    edges.sort()  
    dsu = DSU(n)
    in_tree = bytearray(m)  
    T = [[] for _ in range(n+1)]

    taken = 0
    for w, u, v, idx in edges:
        if dsu.union(u, v):
            in_tree[idx] = 1
            T[u].append((v, w))
            T[v].append((u, w))
            taken += 1
            if taken == n-1:
                break

   
    LOG = n.bit_length()
    up = [array('i', [0]) * (n+1) for _ in range(LOG)]
    mx = [array('i', [0]) * (n+1) for _ in range(LOG)]
    depth = array('i', [0]) * (n+1)

    
    q = deque([1])
    depth[1] = 0
    up[0][1] = 1
    mx[0][1] = 0
    seen = bytearray(n+1)
    seen[1] = 1
    while q:
        u = q.popleft()
        for v, w in T[u]:
            if not seen[v]:
                seen[v] = 1
                depth[v] = depth[u] + 1
                up[0][v] = u
                mx[0][v] = w
                q.append(v)

    for k in range(1, LOG):
        upk_1 = up[k-1]
        mxk_1 = mx[k-1]
        upk = up[k]
        mxk = mx[k]
        for v in range(1, n+1):
            p = upk_1[v]
            upk[v] = upk_1[p]
            
            m1 = mxk_1[v]
            m2 = mxk_1[p]
            mxk[v] = m1 if m1 >= m2 else m2

    def max_on_path(a, b):
        if a == b: return 0
        res = 0
        if depth[a] < depth[b]:
            a, b = b, a
       
        diff = depth[a] - depth[b]
        k = 0
        while diff:
            if diff & 1:
                if mx[k][a] > res: res = mx[k][a]
                a = up[k][a]
            diff >>= 1
            k += 1
        if a == b:
            return res
        for k in range(LOG-1, -1, -1):
            if up[k][a] != up[k][b]:
                if mx[k][a] > res: res = mx[k][a]
                if mx[k][b] > res: res = mx[k][b]
                a = up[k][a]
                b = up[k][b]
       
        if mx[0][a] > res: res = mx[0][a]
        if mx[0][b] > res: res = mx[0][b]
        return res

    
    ans = 0
    for w, u, v, idx in edges:
        if not in_tree[idx]:
            if w == max_on_path(u, v):
                ans += 1
    print(ans)

if __name__ == "__main__":
    solve()

