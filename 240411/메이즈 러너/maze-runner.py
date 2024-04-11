from collections import deque


def every_player_exit(player_board):
    for i in range(N):
        for j in range(N):
            if len(player_board[i][j]) != 0:
                return False
    return True


def get_dist(x, y, nx, ny):
    return abs(x - nx) + abs((y - ny))


def out_of_range(nx, ny):
    return nx < 0 or nx >= N or ny < 0 or ny >= N


def move_player(new_player_board, player_board, x, y, nx, ny):
    while (player_board[x][y]):
        new_player_board[nx][ny].append(player_board[x][y].popleft())


def move_every_player(player_board, board, exit):
    global total_move

    new_player_board = [[deque([]) for _ in range(N)] for __ in range(N)]
    for i in range(N):
        for j in range(N):
            if len(player_board[i][j]) == 0:
                continue
            cand = []
            cur_dist = get_dist(i, j, exit[0], exit[1])
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if out_of_range(nx, ny) or board[nx][ny] >= 1:
                    continue
                next_dist = get_dist(nx, ny, exit[0], exit[1])
                if next_dist >= cur_dist:
                    continue
                cand.append([next_dist, d, nx, ny])
            if len(cand) == 0:
                move_player(new_player_board, player_board, i, j, i, j)
            else:
                total_move += 1
                cand.sort(key=lambda x: (x[0], x[1]))
                next_dist, next_dir, nx, ny = cand[0]
                if [nx, ny] != exit:
                    move_player(new_player_board, player_board, i, j, nx, ny)
                else:
                    player_board[i][j].clear()
    for i in range(N):
        for j in range(N):
            while (new_player_board[i][j]):
                player_board[i][j].append(new_player_board[i][j].popleft())


def available_square(cx, cy, size, player_board, board, exit):
    in_player = False
    in_exit = False
    for i in range(size):
        for j in range(size):
            if [cx + i, cy + j] == exit:
                in_exit = True
            elif len(player_board[cx + i][cy + j]) > 0:
                in_player = True
    return in_player and in_exit


def rotate_square(fx, fy, fd, player_board, board, exit):
    new_board = [[0 for _ in range(N)] for __ in range(N)]
    new_player_board = [[deque([]) for _ in range(N)] for __ in range(N)]

    for i in range(fd):
        for j in range(fd):
            src_x, src_y = fx+i, fy+j
            dest_x, dest_y = fx+j, fy+fd-i-1
            # if board[src_x][src_y] == 0 or len(player_board[src_x][src_y]) ==0:
            #     continue
            if board[src_x][src_y] == -1:
                exit[0], exit[1] = dest_x, dest_y
            new_board[dest_x][dest_y] = board[src_x][src_y]
            if board[src_x][src_y] > 0:
                new_board[dest_x][dest_y] -= 1
            move_player(new_player_board, player_board, src_x, src_y, dest_x, dest_y)


    for i in range(fd):
        for j in range(fd):
            board[fx+i][fy+j] = new_board[fx+i][fy+j]
            move_player(player_board, new_player_board, fx+i, fy+j, fx+i, fy+j)
def rotate_board(player_board, board, exit):
    cand = []
    for i in range(N):
        for j in range(N):
            for d in range(1, N + 1):
                fx, fy = i + d - 1, j + d - 1
                if out_of_range(fx, fy):
                    continue
                if not available_square(i, j, d, player_board, board, exit):
                    continue
                cand.append([i, j, d])
    cand.sort(key=lambda x: (x[2], x[1], x[0]))
    try:
        fx, fy, fd = cand[0]
        rotate_square(fx, fy, fd, player_board, board, exit)
    except:
        import pdb;pdb.set_trace()


N, M, K = map(int, input().split())
board = []
player_board = [[deque([]) for _ in range(N)] for __ in range(N)]
total_move = 0
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

for _ in range(N):
    board.append(list(map(int, input().split())))

for i in range(M):
    x, y = map(int, input().split())
    x, y = x - 1, y - 1
    player_board[x][y].append(i)

ex, ey = map(int, input().split())
ex, ey = ex - 1, ey - 1
board[ex][ey] = -1
exit = [ex, ey]

for _ in range(K):
    
    move_every_player(player_board, board, exit)
    if every_player_exit(player_board):
        break
    rotate_board(player_board, board, exit)
print(total_move)
print(exit[0]+1, exit[1]+1)