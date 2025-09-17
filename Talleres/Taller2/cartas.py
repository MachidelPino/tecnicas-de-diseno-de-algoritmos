import sys
from collections import Counter

def main():
    _entrada = sys.stdin.readline
    _, k = map(int, _entrada().split())
    cards = list(map(int, _entrada().split()))
    favs = list(map(int, _entrada().split()))
    h = [0] + list(map(int, _entrada().split()))

    cnt_cards = Counter(cards)
    cnt_favs = Counter(favs)

    ans = 0
    for v, a in cnt_favs.items():
        b = cnt_cards.get(v, 0)
        if b == 0:
            continue
        m = min(b, a * k)
        dp = [-10**18] * (m + 1)
        dp[0] = 0
        for i in range(1, a + 1):
            upper = min(i * k, m)
            prev_upper = min((i - 1) * k, m)
            ndp = dp[:]  # hasta upper será lo único relevante
            lim_t = min(k, upper)
            for t in range(1, lim_t + 1):
                val_add = h[t]
                start = t
                end = min(upper, prev_upper + t)
                for u in range(start, end + 1):
                    x = dp[u - t] + val_add
                    if x > ndp[u]:
                        ndp[u] = x
            dp = ndp
        ans += dp[m]
    print(ans)

if __name__ == "__main__":
    main()