from collections import deque

L, N, Q = map(int, input().split())

boards = []  # (0,0)
knights = []
orders = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(L):
    boards.append(list(map(int, input().split())))
for i in range(N):
    tmp = list(map(int, input().split()))
    tmp.append(0)
    tmp[0] -= 1
    tmp[1] -= 1
    knights.append(tmp)
for i in range(Q):
    orders.append(list(map(int, input().split())))

for order in orders:
    i, d = order
    if knights[i - 1][-2] == 0:  # 사라진 기사
        continue

    group = [[0 for _ in range(L)] for __ in range(L)]
    new_board = [[0 for _ in range(L)] for __ in range(L)]

    # new_board = 기사 영역
    for knight in knights:
        if knight[-2] == 0:
            continue
        nx, ny, h, w = knight[:-2]
        for j in range(h):
            for k in range(w):
                new_board[nx + j][ny + k] = 1
    # 명령 받은 기사와 붙어 있는 그룹 확인
    kx, ky = knights[i - 1][:2]
    queue = deque([(kx, ky)])
    group[kx][ky] = 1

    while queue:
        cx, cy = queue.pop()
        for j in range(4):
            nx, ny = cx + dx[j], cy + dy[j]
            if nx >= L or nx < 0 or ny >= L or ny < 0:
                continue
            if group[nx][ny] == 0 and new_board[nx][ny]:
                group[nx][ny] = 1
                queue.append((nx, ny))

    # 벽이 있는 지 확인
    is_block = False
    for j in range(L):
        for k in range(L):
            if group[j][k]:
                nx, ny = j + dx[d], k + dy[d]
                if nx >= L or nx < 0 or ny >= L or ny < 0 or boards[nx][ny] == 2:
                    is_block = True
                    break
        if is_block:
            break

    # 벽이 없으면 그룹 이동 & 데미지 계산
    if not is_block:
        for j in range(len(knights)):
            if group[knights[j][0]][knights[j][1]] and knights[j][-2]:
                knights[j][0] += dx[d]
                knights[j][1] += dy[d]

                if (kx+dx[d], ky+dy[d]) != (knights[j][0], knights[j][1]):
                    for k in range(knights[j][2]):
                        for l in range(knights[j][3]):
                            if knights[j][-2] > 0 and boards[knights[j][0] + k][knights[j][1] + l] == 1:
                                knights[j][-2] -= 1
                                knights[j][-1] += 1
ans = 0
for knight in knights:
    if knight[-2]:
        ans+=knight[-1]
print(ans)