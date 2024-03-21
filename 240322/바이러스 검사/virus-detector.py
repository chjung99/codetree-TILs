n = int(input())
s = list(map(int, input().split()))
x, y = map(int, input().split())
ans = 0
for i in range(n):
    if s[i]-x > 0:
        if (s[i]-x) % y == 0:
            ans += 1+(s[i]-x)//y
        else:
            ans += 2 + (s[i]-x)//y
    else:
        ans+=1
print(ans)