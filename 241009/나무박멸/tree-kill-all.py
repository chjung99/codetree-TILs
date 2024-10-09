from copy import deepcopy


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def grow_trees(board):
    new_board = deepcopy(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] <= 0:
                continue
            cnt = 0
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if out_of_range(nx, ny) or board[nx][ny] < 1:
                    continue
                cnt += 1
            new_board[i][j] = board[i][j] + cnt
    return new_board


def spread_trees(board, jecho_board):
    new_board = deepcopy(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] <= 0:
                continue
            valid_locations = []
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if out_of_range(nx, ny) or board[nx][ny] != 0 or jecho_board[nx][ny] >= year:
                    continue
                valid_locations.append([nx, ny])
            if len(valid_locations) >= 1:
                cnt = board[i][j] // len(valid_locations)
                for x, y in valid_locations:
                    new_board[x][y] += cnt
    return new_board


def find_jecho_locations(cx, cy, k, board):
    locs = [[cx, cy]]
    adx = [-1, -1, 1, 1]
    ady = [-1, 1, -1, 1]
    if board[cx][cy] >= 1:
        for ad in range(4):
            for i in range(1, k+1):
                nx, ny = cx + i * adx[ad], cy + i * ady[ad]
                if out_of_range(nx, ny) or board[nx][ny] == -1:
                    break
                locs.append([nx, ny])
                if board[nx][ny] <= 0:
                    break
    return locs


def get_jecho_info(k, board):
    jecho_cand_list = []
    for i in range(n):
        for j in range(n):
            locs = find_jecho_locations(i, j, k, board)
            cnt = 0
            for x, y in locs:
                if board[x][y] >= 1:
                    cnt += board[x][y]
            jecho_cand_list.append([cnt, i, j])
    jecho_cand_list.sort(key=lambda x:(-x[0], x[1], x[2]))
    return jecho_cand_list[0]


def jecho_trees(x, y, k, updated_year, board, jecho_board):
    locs = find_jecho_locations(x, y, k, board)
    for x, y in locs:
        if board[x][y] >= 1:
            board[x][y] = 0
        jecho_board[x][y] = updated_year


n, m, k, c = map(int, input().split())
board = []
for _ in range(n):
    board.append(list(map(int, input().split())))
jecho_board = [[0 for _ in range(n)] for __ in range(n)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
ans = 0

for year in range(1, m + 1):
    board = grow_trees(board)
    board = spread_trees(board, jecho_board)
    cnt, x, y = get_jecho_info(k, board)
    jecho_trees(x, y, k, year + c, board, jecho_board)
    ans += cnt
print(ans)
# 5 3 2 1
# 0 0 0 0 0
# 0 30 23 0 0
# 0 0 -1 0 0
# 0 0 17 46 77
# 0 0 0 12 0