from collections import deque

N, M, P, C, D = map(int, input().split())
rx, ry = map(int, input().split())
santa = [[] for _ in range(31)]
santa_score = [0 for _ in range(31)]
stun = [0 for _ in range(31)]
board = [[-1 for _ in range(N + 1)] for __ in range(N + 1)]
dx = [-1, 0, 1, 0, -1, 1, 1, -1]
dy = [0, 1, 0, -1, 1, 1, -1, -1]

board[rx][ry] = 0

for i in range(P):
    si, sx, sy = map(int, input().split())
    santa[si].extend([sx, sy])
    board[sx][sy] = si


def move_rudolf(turn, rnx, rny):
    global rx, ry, board, santa
    # 충돌
    if board[rnx][rny] >= 1:

        si = board[rnx][rny]

        stun[si] = turn + 1
        santa_score[si] += C
        sdx, sdy = rnx - rx, rny - ry
        snx, sny = rnx, rny

        # 연쇄 이동 고려?
        for i in range(C):
            snx, sny = snx + sdx, sny + sdy
        if snx < 1 or snx > N or sny < 1 or sny > N:
            santa[si] = [-1, -1]
        else:

            queue = deque([])
            # 충돌 후 위치에 다른 산타 존재
            if board[snx][sny] >= 1:
                # 일단 밀어냄
                queue.append(board[snx][sny])

                board[snx][sny] = si
                santa[si] = [snx, sny]

                while queue:
                    cur_idx = queue.popleft()
                    ssnx, ssny = santa[cur_idx][0] + sdx, santa[cur_idx][1] + sdy
                    if ssnx < 1 or ssnx > N or ssny < 1 or ssny > N:
                        santa[cur_idx] = [-1, -1]
                        continue
                    if board[ssnx][ssny] >= 1:
                        queue.append(board[ssnx][ssny])
                    board[ssnx][ssny] = cur_idx
                    santa[cur_idx] = [ssnx, ssny]
            else:
                board[snx][sny] = si
                santa[si] = snx, sny

    board[rx][ry] = -1
    board[rnx][rny] = 0
    rx, ry = rnx, rny


def move_santa(turn, si, snx, sny):
    global santa, board

    if santa[si] != [snx, sny]:
        # 루돌프와 충돌하는 경우
        if board[snx][sny] == 0:
            stun[si] = turn + 1
            santa_score[si] += D
            sdx, sdy = -(snx - santa[si][0]), -(sny - santa[si][1])
            ssnx, ssny = snx, sny
            for i in range(D):
                ssnx, ssny = ssnx + sdx, ssny + sdy
            if ssnx < 1 or ssnx > N or ssny < 1 or ssny > N:
                santa[si] = [-1, -1]
            else:
                queue = deque([])
                # 충돌 위치에 다른 산타가 존재
                if board[ssnx][ssny] >= 1:
                    queue.append(board[ssnx][ssny])
                    board[ssnx][ssny] = si
                    santa[si] = [ssnx, ssny]

                    while queue:
                        cur_idx = queue.popleft()
                        sssnx, sssny = santa[cur_idx][0] + sdx, santa[cur_idx][1] + sdy
                        if sssnx < 1 or sssnx > N or sssny < 1 or sssny > N:
                            santa[cur_idx] = [-1, -1]
                            continue

                        if board[sssnx][sssny] >= 1:
                            queue.append(board[sssnx][sssny])

                        board[sssnx][sssny] = cur_idx
                        santa[cur_idx] = [sssnx, sssny]

                else:
                    board[santa[si][0]][santa[si][1]] = -1
                    board[ssnx][ssny] = si
                    santa[si] = [ssnx, ssny]
        else:
            board[santa[si][0]][santa[si][1]] = -1
            board[snx][sny] = si
            santa[si] = [snx, sny]


def find_nearest_rudolf(si):
    tx, ty = rx, ry

    sx, sy = santa[si]

    sd = (rx - sx) ** 2 + (ry - sy) ** 2
    cand = [[sd, sx, sy]]

    for i in range(4):
        nx, ny = sx + dx[i], sy + dy[i]
        if nx < 1 or nx > N or ny < 1 or ny > N or board[nx][ny] >= 1:
            continue
        d = (rx - nx) ** 2 + (ry - ny) ** 2
        cand.append([d, nx, ny, i])
    cand.sort(key=lambda x: (x[0], i))

    return si, cand[0][1], cand[0][2]


def find_nearest_santa():
    # 루돌프로부터 산타까지 거리 측정
    cand = []
    for i in range(1, P + 1):
        if santa[i] != [-1, -1]:
            d = (rx - santa[i][0]) ** 2 + (ry - santa[i][1]) ** 2
            cand.append([d, santa[i][0], santa[i][1], i])
    cand.sort(key=lambda x: (x[0], -x[1], -x[2]))
    tx, ty = cand[0][1], cand[0][2]

    cand2 = []
    for i in range(8):
        nx, ny = rx + dx[i], ry + dy[i]
        if nx < 1 or nx > N or ny < 1 or ny > N:
            continue
        d = (tx - nx) ** 2 + (ty - ny) ** 2
        cand2.append([d, nx, ny])
    cand2.sort(key=lambda x: (x[0]))

    return cand2[0][1], cand2[0][2]


for i in range(1, M + 1):

    move_rudolf(i, *find_nearest_santa())

    for j in range(1, P + 1):
        if stun[j] < i and santa[j] != [-1, -1]:
            move_santa(i, *find_nearest_rudolf(j))

    cnt = 0

    for j in range(1, P + 1):
        if santa[j] != [-1, -1]:
            santa_score[j] += 1
        else:
            cnt += 1
    if cnt == P:
        break
print(" ".join(map(str, santa_score[1:P + 1])))
# print(santa[1:P+1])
# print(" ".join(map(str, santa_score[1:P + 1])))