def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= m


def dfs(depth, sum_of_blocks, blocks, visit, board):
    global ans
    if depth == 4:
        ans = max(ans, sum_of_blocks)
        return
    for cx, cy in blocks:
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            visit[nx][ny] = 1
            blocks.append([nx, ny])
            dfs(depth + 1, sum_of_blocks + board[nx][ny], blocks, visit, board)
            blocks.pop(-1)
            visit[nx][ny] = 0


n, m = map(int, input().split())
board = []
visit = [[0 for _ in range(m)] for __ in range(n)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

ans = 0
for _ in range(n):
    board.append(list(map(int, input().split())))

for i in range(n):
    for j in range(m):
        visit[i][j] = 1
        dfs(1, board[i][j], [[i, j]], visit, board)
        visit[i][j] = 0

print(ans)
# 4 5
# 0 0 0 1 0
# 1 0 0 1 1
# 1 100 0 0 1
# 1 0 0 0 0