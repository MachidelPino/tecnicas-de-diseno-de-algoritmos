import sys

def solve():
    _entrada=sys.stdin.readline
    n=int(_entrada().strip())
    s=_entrada().strip()
    dp=[[0]*n for _ in range(n)]
    for i in range(n):
        dp[i][i]=1
    for l in range(n-2,-1,-1):
        for r in range(l+1,n):
            v=1+dp[l+1][r]
            if s[l]==s[l+1]:
                if dp[l+1][r]<v:
                    v=dp[l+1][r]
            i=l+2
            while i<=r:
                if s[i]==s[l]:
                    t=dp[l+1][i-1]+dp[i][r]
                    if t<v:
                        v=t
                i+=1
            dp[l][r]=v
    print(dp[0][n-1])

if __name__=="__main__":
    solve()
