from collections import deque


def bfs(cx, cy, cd, board):
    global ans
    visit = [[0 for _ in range(m)] for __ in range(n)]
    queue = deque([[cx, cy, cd]])
    visit[cx][cy] = 1
    while queue:
        cx, cy, cd = queue.popleft()
        flag = False
        for _ in range(4):
            nd = (cd-1) % 4
            nx, ny = cx + dx[nd], cy + dy[nd]
            if visit[nx][ny] or board[nx][ny]:
                cd = nd
                continue
            visit[nx][ny] = 1
            ans += 1
            queue.append([nx, ny, nd])
            flag = True
            break
        if not flag:
            nd = (cd+2) % 4
            nx, ny = cx + dx[nd], cy + dy[nd]
            if board[nx][ny]:
                return
            queue.append([nx, ny, cd])


n, m = map(int, input().split())
x, y, d = map(int, input().split())
board = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
for _ in range(n):
    board.append(list(map(int, input().split())))
ans = 1

bfs(x, y, d, board)
print(ans)
# 5 5
# 3 2 0
# 1 1 1 1 1
# 1 0 1 0 1
# 1 0 1 0 1
# 1 0 0 0 1
# 1 1 1 1 1