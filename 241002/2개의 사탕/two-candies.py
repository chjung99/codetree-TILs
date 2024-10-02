N, M = map(int, input().split())
board = []
rx, ry, bx, by = -1, -1, -1, -1

ans = -1
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def euque(arr, move_dir):
    if move_dir == 0:
        arr.sort(key=lambda x: x[0])
    elif move_dir == 1:
        arr.sort(key=lambda x: -x[1])
    elif move_dir == 2:
        arr.sort(key=lambda x: -x[0])
    else:
        arr.sort(key=lambda x: x[1])
    return arr


def out_of_range(x, y):
    return x < 0 or x >= N or y < 0 or y >= M


def can_move_to(x, y, rx, ry, bx, by, board):
    if board[x][y] == 'O':
        return True
    if out_of_range(x, y) or [x, y] in [[rx, ry], [bx, by]]:
        return False
    if board[x][y] == '.':
        return True
    return False


def slip_to_dir(x, y, move_dir, rx, ry, bx, by, board):
    cx, cy = x, y
    nx, ny = cx + dx[move_dir], cy + dy[move_dir]

    while board[cx][cy] != 'O' and can_move_to(nx, ny, rx, ry, bx, by, board):
        cx, cy = nx, ny
        nx, ny = cx + dx[move_dir], cy + dy[move_dir]

    return cx, cy


def dfs(rx, ry, bx, by, depth, prev_dir, board):
    global ans
    if depth > 10:
        return

    if board[rx][ry] == 'O' and board[bx][by] == 'O':
        return
    elif board[bx][by] == 'O':
        return
    elif board[rx][ry] == 'O':
        if ans == -1:
            ans = depth
        else:
            ans = min(ans, depth)

    for nxt_dir in range(4):
        if prev_dir != -1 and (prev_dir + 2) % 4 == nxt_dir:
            continue
        pq = euque([[rx, ry, 'R'], [bx, by, 'B']], nxt_dir)
        nrx, nry, nbx, nby = rx, ry, bx, by
        for x, y, color in pq:
            if color == 'R':
                nrx, nry = slip_to_dir(x, y, nxt_dir, nrx, nry, nbx, nby, board)
            else:
                nbx, nby = slip_to_dir(x, y, nxt_dir, nrx, nry, nbx, nby, board)

        dfs(nrx, nry, nbx, nby, depth + 1, nxt_dir, board)


for i in range(N):
    row_tmp = input()
    red_idx = row_tmp.find('R')
    blue_idx = row_tmp.find('B')

    if red_idx != -1:
        row_tmp = row_tmp.replace('R', '.')
        rx, ry = i, red_idx
    if blue_idx != -1:
        row_tmp = row_tmp.replace('B', '.')
        bx, by = i, blue_idx

    board.append(list(row_tmp))

dfs(rx, ry, bx, by, 0, -1, board)

print(ans)