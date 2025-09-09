import sys

x, y = map(int, sys.stdin.readline().split())

seq = [y]
while y > x:
    if y % 2 == 0:
        y //= 2
    elif y % 10 == 1:
        y = (y - 1) // 10
    else:
        break
    seq.append(y)

if y == x:
    print("YES")
    print(len(seq))
    print(*reversed(seq))
else:
    print("NO")
