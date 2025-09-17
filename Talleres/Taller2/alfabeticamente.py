import sys

def main():
    _entrada = sys.stdin.readline
    n = int(_entrada().strip())
    c = list(map(int, _entrada().split()))
    s = [_entrada().strip() for _ in range(n)]
    r = [x[::-1] for x in s]

    INF = 10**19
    dp0 = [INF]*n
    dp1 = [INF]*n
    dp0[0] = 0
    dp1[0] = c[0]

    for i in range(1, n):
        a, ar = s[i], r[i]
        b, br = s[i-1], r[i-1]
        best0 = INF
        best1 = INF
        if a >= b and dp0[i-1] < INF:
            best0 = min(best0, dp0[i-1])
        if a >= br and dp1[i-1] < INF:
            best0 = min(best0, dp1[i-1])
        if ar >= b and dp0[i-1] < INF:
            best1 = min(best1, dp0[i-1] + c[i])
        if ar >= br and dp1[i-1] < INF:
            best1 = min(best1, dp1[i-1] + c[i])
        dp0[i] = best0
        dp1[i] = best1

    ans = min(dp0[-1], dp1[-1])
    print(-1 if ans >= INF else ans)

if __name__ == "__main__":
    main()
