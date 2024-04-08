from collections import deque

n, m, k, c = map(int, input().split())
board = []
jechojes = deque([])
removed_tree = 0
dx = [0, 1, 0, -1, 1, 1, -1, -1]
dy = [1, 0, -1, 0, 1, -1, 1, -1]

for _ in range(n):
    board.append(list(map(int, input().split())))


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def grow_trees(board):
    for i in range(n):
        for j in range(n):
            if board[i][j] <= 0:
                continue
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if out_of_range(nx, ny):
                    continue
                if board[nx][ny] > 0:
                    board[i][j] += 1


def reproduce_trees(board):
    tmp = deque([])
    new_board = [board[i][:] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if board[i][j] <= 0:
                continue
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if out_of_range(nx, ny):
                    continue
                if board[nx][ny] == 0:
                    tmp.append([nx, ny])
            cnt = len(tmp)
            while tmp:
                nx, ny = tmp.popleft()
                new_board[nx][ny] += board[i][j] // cnt
    for i in range(n):
        for j in range(n):
            board[i][j] = new_board[i][j]



def find_location(board):
    cand = []
    cnt = board[0][0]
    tmp = [[0, 0]]
    for i in range(n):
        for j in range(n):
            if board[i][j] >= 0:
                cnt = board[i][j]
            elif board[i][j] == -2:
                cnt = 0
            else:
                continue
            tmp = [[i, j]]
            for d in range(4, 8, 1):
                nx, ny = i, j
                for r in range(k):
                    nx, ny = nx + dx[d], ny + dy[d]
                    if out_of_range(nx, ny):
                        continue
                    if board[nx][ny] == -1:
                        break
                    if board[nx][ny] > 0:
                        cnt += board[nx][ny]
                        tmp.append([nx, ny])
                    if board[nx][ny] == 0:
                        cnt += board[nx][ny]
                        tmp.append([nx, ny])
                        break
            cand.append([cnt, tmp])
    try:
        # for x, y in cand:
        #     print(y)
        #     print(y[0], y[1])
        #     print("+++++++++++++")
        cand.sort(key=lambda x: (-x[0], x[1][0][0], x[1][0][1]))
    except:
        import pdb;pdb.set_trace()
    return cand[0]


def spread_jechoje(locations, year, c, board, jechojes):
    for x, y in locations:
        board[x][y] = -2
        jechojes.append([x, y, year + c])


def clear_expired(board, jechojes, year):
    new_jechojes = deque([])
    while jechojes:
        x, y, expired = jechojes.popleft()
        if expired == year:
            continue
        new_jechojes.append([x, y, expired])

    while new_jechojes:
        x, y, expired = new_jechojes.popleft()
        jechojes.append([x, y, expired])


for year in range(m):
    grow_trees(board)
    reproduce_trees(board)
    cnt, locations = find_location(board)
    removed_tree += cnt
    spread_jechoje(locations, year, c, board, jechojes)
    clear_expired(board, jechojes, year)

print(removed_tree)