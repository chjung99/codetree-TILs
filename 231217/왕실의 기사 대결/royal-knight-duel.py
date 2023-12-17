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

    vis = [[0 for _ in range(L)] for __ in range(L)]
    group = [[0 for _ in range(L)] for __ in range(L)]
    new_board = [[-1 for _ in range(L)] for __ in range(L)]

    # new_board = 기사 영역
    for idx, knight in enumerate(knights):
        if knight[-2] == 0:
            continue
        nx, ny, h, w = knight[:-2]
        for j in range(h):
            for k in range(w):
                new_board[nx + j][ny + k] = idx

    # 명령 받은 기사와 붙어 있는 그룹 확인
    kx, ky, kh, kw = knights[i - 1][:4]
    queue = deque([])

    for j in range(kh):
        for k in range(kw):
            queue.append((kx + j, ky + k, i-1))
            vis[kx + j][ky + k] = 1
            group[kx + j][ky + k] = 1
    # for b in new_board:
    #     print(b)

    while queue:
        cx, cy, c_idx = queue.pop()
        nx, ny = cx + dx[d], cy + dy[d]
        if nx >= L or nx < 0 or ny >= L or ny < 0 or vis[nx][ny]:
            continue
        n_idx = new_board[nx][ny]
        # print(nx,ny,n_idx)
        if n_idx != -1:
            # print("!")
            nkx, nky, nkh, nkw = knights[n_idx][:4]

            for j in range(nkh):
                for k in range(nkw):
                    queue.append((nkx + j, nky + k, n_idx))
                    vis[nkx + j][nky + k] = 1
                    group[nkx+j][nky+k] = 1

    #
    # for g in group:
    #     print(g)

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
    # print(is_block)
    if not is_block:
        for j in range(len(knights)):
            if group[knights[j][0]][knights[j][1]] and knights[j][-2]:
                knights[j][0] += dx[d]
                knights[j][1] += dy[d]

                if (kx + dx[d], ky + dy[d]) != (knights[j][0], knights[j][1]):
                    for k in range(knights[j][2]):
                        for l in range(knights[j][3]):
                            if knights[j][-2] > 0 and boards[knights[j][0] + k][knights[j][1] + l] == 1:
                                knights[j][-2] -= 1
                                knights[j][-1] += 1
    # for knight in knights:
    #     print(knights)
    # print("====")
ans = 0
for knight in knights:
    if knight[-2]:
        ans += knight[-1]
print(ans)