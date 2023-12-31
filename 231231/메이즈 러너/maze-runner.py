N, M, K = map(int, input().split())
blocks = []
gamers = []
answer = 0

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

for _ in range(N):
    blocks.append(list(map(int, input().split())))
for _ in range(M):
    gx, gy = map(int, input().split())
    gamers.append([gx - 1, gy - 1])  # 좌표,이동거리

ex, ey = map(int, input().split())
escape = [ex - 1, ey - 1]


def move():
    global gamers, answer
    new_gamers = []
    for cx, cy in gamers:
        cur_dist = abs(escape[0] - cx) + abs(escape[1] - cy)
        flag = True
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or blocks[nx][ny] != 0:
                continue
            nxt_dist = abs(escape[0] - nx) + abs(escape[1] - ny)
            if cur_dist > nxt_dist:
                flag = False
                answer += 1
                if nxt_dist != 0:

                    new_gamers.append([nx, ny])
                break
        if flag:
            new_gamers.append([cx, cy])
    gamers = new_gamers


def rotate():
    global escape, blocks, gamers
    # tmp = [[abs(escape[0] - gx) + abs(escape[1] - gy), gx, gy] for gx, gy, gd in gamers]
    # tmp.sort(key=lambda x:(x[0], x[1], x[2]))
    # px, py = tmp[0][1:]
    cand = []  # width, x_min, y_min
    for k in range(1, N):
        for i in range(N):
            for j in range(N):
                if i + k >= N or j + k >= N:
                    continue
                if i <= escape[0] <= i + k and j <= escape[1] <= j + k:
                    for gx, gy in gamers:
                        if i <= gx <= i + k and j <= gy <= j + k:
                            cand.extend([i, j, i + k, j + k])
                            break
                    if len(cand) != 0:
                        break
            if len(cand) != 0:
                break
        if len(cand) != 0:
            break

    for i in range(N):
        for j in range(N):
            if cand[0] <= i <= cand[2] and cand[1] <= j <= cand[3] and blocks[i][j]:
                blocks[i][j] -= 1
    # for i in range(cand[0], cand[2]+1):
    #     for j in range(cand[1], cand[3]+1):
    #         if blocks[i][j]:
    #             blocks[i][j] -= 1

    tmp = [[0 for _ in range(N)] for __ in range(N)]
    tmp2 = [[0 for _ in range(N)] for __ in range(N)]
    tmp3 = [[0 for _ in range(N)] for __ in range(N)]
    for i in range(N):
        for j in range(N):
            if cand[0] <= i <= cand[2] and cand[1] <= j <= cand[3]:
                tmp[i][j] = blocks[cand[2]-cand[0]+1-1-(j-cand[0]-cand[1])][i +(cand[1]-cand[0])]
            else:
                tmp[i][j] = blocks[i][j]
    blocks = tmp

    tmp2[escape[0]][escape[1]] = 1
    for gx, gy in gamers:
        tmp2[gx][gy] = 2

    for i in range(N):
        for j in range(N):
            if cand[0] <= i <= cand[2] and cand[1] <= j <= cand[3]:
                tmp3[i][j] = tmp2[cand[2]-cand[0]+1-1-(j-cand[0]-cand[1])][i +(cand[1]-cand[0])]
            else:
                tmp3[i][j] = tmp2[i][j]
    # for t in blocks:
    #     print(t)
    # print("====")
    # for t in tmp3:
    #     print(t)
    new_gamers = []
    new_escape = []
    for i in range(N):
        for j in range(N):
            if tmp3[i][j] == 1:
                new_escape.extend([i, j])
            elif tmp3[i][j] == 2:
                new_gamers.append([i, j])
    # print("====")
    gamers = new_gamers
    escape = new_escape


while K > 0:
    move()
    if len(gamers) == 0:
        break
    rotate()
    K -= 1
    # print(f"answer={answer}")

print(answer)
print(escape[0]+1, escape[1]+1)