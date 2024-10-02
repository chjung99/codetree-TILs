def out_of_range(x, y):
    return x < 0 or x >= N or y < 0 or y >= M


def can_move(cx, cy, move_dir, board, key):
    # 다음 위치가 빈칸 or 출구 인 경우만 이동가능
    # 단, R 또는 B 가 있는 경우는 이동 불가
    rx, ry, bx, by = key
    nx, ny = cx + dx[move_dir], cy + dy[move_dir]

    if not out_of_range(nx, ny):
        # 출구면 무조건 이동
        if board[nx][ny] == 'O':
            return True
        elif board[nx][ny] == '.':
            return [nx, ny] not in [[rx, ry], [bx, by]]
    return False


def slip_to_dir(x, y, move_dir, board, key):
    while can_move(x, y, move_dir, board, key):
        x, y = x + dx[move_dir], y + dy[move_dir]
    return x, y


def enque(arr, move_dir):
    if move_dir == 0:
        # 북쪽이면 x가 작은거 먼저
        arr.sort(key=lambda x:x[0])

    elif move_dir == 1:
        # 동쪽이면 y가 큰거 먼저
        arr.sort(key=lambda x:(-x[1]))

    elif move_dir == 2:
        # 남쪽이면 x가 큰거 먼저
        arr.sort(key=lambda x:(-x[0]))

    else:
        # 서쪽이면 y가 작은거 먼저
        arr.sort(key=lambda x:x[1])
    return arr



def dfs(key, depth, board):
    global ans
    rx, ry, bx, by = key
    if board[rx][ry] == 'O' and board[bx][by] == 'O':
        return
    elif board[rx][ry] == 'O':
        if ans == -1:
            ans = depth
        else:
            ans = min(ans, depth)
        return
    elif board[bx][by] == 'O':
        return
    if depth >= 10:
        return

    for i in range(4):
        rx, ry, bx, by = key
        arr = [[rx, ry, 'R'], [bx, by ,'B']]
        queue = enque(arr, i)
        new_key = key
        for cx, cy, color in queue:
            if color == 'R':
                rx, ry = slip_to_dir(cx, cy, i, board, new_key)
                new_key = (rx, ry, bx, by)
            else:
                bx, by = slip_to_dir(cx, cy, i, board, new_key)
                new_key = (rx, ry, bx, by)
        dfs(new_key, depth+1, board)


N, M = map(int, input().split())
board = []
# 북 동 남 서
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

rx, ry = -1, -1
bx, by = -1, -1
ans = -1

for i in range(N):
    row_tmp = input()

    if row_tmp.find('R') != -1:
        rx, ry = i, row_tmp.find('R')
        row_tmp = row_tmp.replace('R', '.')
    if row_tmp.find('B') != -1:
        bx, by = i, row_tmp.find('B')
        row_tmp = row_tmp.replace('B', '.')

    board.append(list(row_tmp))

start_key = (rx, ry, bx, by)

dfs(start_key, 0, board)




print(ans)