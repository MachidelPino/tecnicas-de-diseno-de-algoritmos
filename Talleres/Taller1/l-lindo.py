import sys

def solve_seg(s, c):
    if len(s) == 1:
        return 0 if s[0] == c else 1
    m = len(s) // 2
    left, right = s[:m], s[m:]
    mal_left  = sum(ch != c for ch in left)
    mal_right = sum(ch != c for ch in right)
    return min(mal_left  + solve_seg(right, chr(ord(c)+1)),
               mal_right + solve_seg(left,  chr(ord(c)+1)))

t = int(sys.stdin.readline())
for _ in range(t):
    n = int(sys.stdin.readline())
    s = sys.stdin.readline().strip()
    print(solve_seg(s, 'a'))
