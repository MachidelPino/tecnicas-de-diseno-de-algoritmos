import sys
sys.setrecursionlimit(1 << 20)

from functools import lru_cache

@lru_cache(maxsize=None)
def length(n: int) -> int:
    if n <= 1:
        return 1
    return 2 * length(n // 2) + 1

def count_ones(n: int, seg_l: int, seg_r: int, l: int, r: int) -> int:
    if r < seg_l or seg_r < l:
        return 0
    if seg_l == seg_r:
        return 1 if n == 1 else 0
    left_len = length(n // 2)
    mid = seg_l + left_len
    ans = 0
    ans += count_ones(n // 2, seg_l, mid - 1, l, r)
    if l <= mid <= r:
        ans += n % 2
    ans += count_ones(n // 2, mid + 1, seg_r, l, r)
    return ans

n, l, r = map(int, sys.stdin.readline().split())
print(count_ones(n, 1, length(n), l, r))
