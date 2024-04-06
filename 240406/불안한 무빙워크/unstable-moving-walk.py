from collections import deque

n, k = map(int, input().split())
safety = list(map(int, input().split()))
cnt = 0
moving_walk = deque([[False, safety[i]] for i in range(len(safety))])


def count_zero(moving_walk):
    cnt_zero = 0
    for person, safe in moving_walk:
        if safe == 0:
            cnt_zero += 1
    return cnt_zero


while True:
    if count_zero(moving_walk) >= k:
        break
    moving_walk.rotate(1)
    for i in range(n-2, -1, -1):
        if moving_walk[i][0]:
            if not moving_walk[i+1][0] and moving_walk[i+1][i] > 0:
                moving_walk[i][0] = False
                moving_walk[i+1][0] = True
                moving_walk[i+1][1] -= 1
    if moving_walk[n-1][0]:
        moving_walk[n-1][0] = False
    if not moving_walk[0][0] and moving_walk[0][1] > 0:
        moving_walk[0][0] = True
        moving_walk[0][1] -= 1
    cnt += 1
print(cnt)