def count_fail_santa(santa_state):
    return santa_state.count(-1)


def get_dist(x, y, nx, ny):
    return (nx - x) ** 2 + (ny - y) ** 2


def get_nearest_santa(rx, ry, board, santas, santa_state):
    cand = []
    for i in range(1, P + 1):
        if santa_state[i] == -1: continue
        dist = get_dist(rx, ry, santas[i][0], santas[i][1])
        cand.append([dist, santas[i][0], santas[i][1], i])
    cand.sort(key=lambda x: (x[0], -x[1], -x[2]))
    return cand[0]


def out_of_range(nx, ny):
    return nx < 0 or nx >= N or ny < 0 or ny >= N


def get_move_dir_rudolf(rx, ry, sx, sy, dist):
    final_dir = -1
    min_dist = dist
    for i in range(8):
        nx, ny = rx + dx[i], ry + dy[i]
        if out_of_range(nx, ny):
            continue
        next_dist = get_dist(nx, ny, sx, sy)
        if min_dist >= next_dist:
            min_dist = next_dist
            final_dir = i
    return final_dir


def put_santa(sx, sy, snx, sny, santa_num, santas, board):
    board[snx][sny] = santa_num
    # 문제 1
    if board[sx][sy] == santa_num:
        board[sx][sy] = 0
    santas[santa_num][0], santas[santa_num][1] = snx, sny


def collision_by_rudolf(rx, ry, sx, sy, santa_num, move_dir, board, santas, santa_state, santa_score, turn):
    santa_score[santa_num] += C
    snx, sny = sx + C * dx[move_dir], sy + C * dy[move_dir]
    santa_state[santa_num] = turn + 1
    if out_of_range(snx, sny):
        if board[sx][sy] == santa_num:
            board[sx][sy] = 0
        santas[santa_num][0], santas[santa_num][1] = -1, -1
        santa_state[santa_num] = -1
    elif board[snx][sny] == 0:
        put_santa(sx, sy, snx, sny, santa_num, santas, board)
    else:
        while True:
            if out_of_range(snx, sny):
                santas[santa_num][0], santas[santa_num][1] = -1, -1
                santa_state[santa_num] = -1
                break
            if board[snx][sny] == 0:
                put_santa(sx, sy, snx, sny, santa_num, santas, board)
                break
            next_santa_num = board[snx][sny]
            put_santa(sx, sy, snx, sny, santa_num, santas, board)
            santa_num = next_santa_num
            sx, sy = snx, sny
            snx, sny = sx + dx[move_dir], sy + dy[move_dir]



def move_rudolf(rudolf, move_dir, board, santas, santa_state, santa_score, turn):
    rx, ry = rudolf
    rnx, rny = rx + dx[move_dir], ry + dy[move_dir]

    santa_num = board[rnx][rny]
    board[rnx][rny] = board[rx][ry]

    board[rx][ry] = 0
    rudolf[0], rudolf[1] = rnx, rny

    if santa_num >= 1:
        sx, sy = rnx, rny

        collision_by_rudolf(rx, ry, sx, sy, santa_num, move_dir, board, santas, santa_state, santa_score, turn)




def command_rudolf(rudolf, board, santas, santa_state, santa_score, turn):
    rx, ry = rudolf
    dist, sx, sy, santa_num = get_nearest_santa(rx, ry, board, santas, santa_state)
    move_dir = get_move_dir_rudolf(rx, ry, sx, sy, dist)
    move_rudolf(rudolf, move_dir, board, santas, santa_state, santa_score, turn)


def available_santa(i, santa_state, turn):
    if santa_state[i] == -1:
        return False
    return santa_state[i] == 0 or santa_state[i] < turn


def get_move_dir_santa(sx, sy, rx, ry, dist, board):
    final_dir = -1
    min_dist = dist
    for i in range(3, -1, -1):
        nx, ny = sx + dx[i], sy + dy[i]
        if out_of_range(nx, ny) or board[nx][ny] > 0:
            continue
        next_dist = get_dist(nx, ny, rx, ry)
        if next_dist == dist:
            continue
        if min_dist >= next_dist:
            final_dir = i
            min_dist = next_dist
    return final_dir


def collision_by_santa(rudolf, sx, sy, move_dir, santas, santa_state, santa_score, turn):
    rx, ry = rudolf
    santa_num = board[sx][sy]
    santa_score[santa_num] += D
    snx, sny = rx - D * dx[move_dir], ry - D * dy[move_dir]
    santa_state[santa_num] = turn + 1
    if out_of_range(snx, sny):
        board[sx][sy] = 0
        santas[santa_num][0], santas[santa_num][1] = -1, -1
        santa_state[santa_num] = -1
    elif board[snx][sny] == santa_num:
        pass
    elif board[snx][sny] == 0:
        put_santa(sx, sy, snx, sny, santa_num, santas, board)
        santa_state[santa_num] = turn + 1
    else:
        while True:
            if out_of_range(snx, sny):
                break
            if board[snx][sny] == 0:
                put_santa(sx, sy, snx, sny, santa_num, santas, board)
                break
            next_santa_num = board[snx][sny]
            if [sx, sy] != [snx, sny]:
                put_santa(sx, sy, snx, sny, santa_num, santas, board)
            santa_num = next_santa_num
            sx, sy = snx, sny
            snx, sny = sx - dx[move_dir], sy - dy[move_dir]

def move_santa(rudolf, sx, sy, move_dir, santas, santa_state, santa_score, turn):
    santa_num = board[sx][sy]
    snx, sny = sx + dx[move_dir], sy + dy[move_dir]
    if board[snx][sny] == 0:
        board[snx][sny] = board[sx][sy]
        board[sx][sy] = 0
        santas[santa_num][0], santas[santa_num][1] = snx, sny
    else:
        collision_by_santa(rudolf, sx, sy, move_dir, santas, santa_state, santa_score, turn)


def command_santa(i, rudolf, santas, board, santa_state, santa_score, turn):
    sx, sy = santas[i]
    rx, ry = rudolf
    dist = get_dist(sx, sy, rx, ry)
    move_dir = get_move_dir_santa(sx, sy, rx, ry, dist, board)
    if move_dir != -1:
        move_santa(rudolf, sx, sy, move_dir, santas, santa_state, santa_score, turn)


N, M, P, C, D = map(int, input().split())
board = [[0 for _ in range(N)] for __ in range(N)]

rx, ry = map(int, input().split())
rx -= 1
ry -= 1
rudolf = [rx, ry]
board[rx][ry] = -1  # 루돌프 -1 빈공간 0 산타 1~P
santa_score = [0 for _ in range(P + 1)]
santa_state = [0 for _ in range(P + 1)]  # -1 탈락 / 0 정상 / 1 기절
santas = [[-1, -1] for _ in range(P + 1)]

dx = [-1, 0, 1, 0, 1, 1, -1, -1]
dy = [0, 1, 0, -1, 1, -1, 1, -1]

for _ in range(P):
    pn, sx, sy = map(int, input().split())
    sx -= 1
    sy -= 1
    santas[pn] = [sx, sy]
    board[sx][sy] = pn

for turn in range(M):
    if count_fail_santa(santa_state) == P:
        break
    command_rudolf(rudolf, board, santas, santa_state, santa_score, turn)
    for i in range(1, P + 1):
        if available_santa(i, santa_state, turn):
            command_santa(i, rudolf, santas, board, santa_state, santa_score, turn)
    for i in range(1, P + 1):
        if santa_state[i] != -1:
            santa_score[i] += 1
for i in range(1, P + 1):
    print(santa_score[i], end=" ")