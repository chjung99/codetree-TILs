from collections import deque

global score, tx, ty, td, clockwise

n, m, h, k = map(int, input().split())
runners = deque()
score = 0
board = [[0 for _ in range(n)] for __ in range(n)]
visit = [[0 for _ in range(n)] for __ in range(n)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
for _ in range(m):
    x, y, d = map(int, input().split())
    runners.append([x - 1, y - 1, d])

for _ in range(h):
    x, y = map(int, input().split())
    board[x - 1][y - 1] = 1  # 나무

tx, ty, td = n // 2, n // 2, 0
visit[tx][ty] = 1
clockwise = 1


def move_runners(runners, board):
    for idx in range(len(runners)):
        cx, cy, cd = runners[idx]
        if abs(cx - tx) + abs(cy - ty) > 3:
            continue
        nx, ny = cx + dx[cd], cy + dy[cd]
        if not out_of_bound(nx, ny):
            if (tx, ty) != (nx, ny):
                runners[idx] = [nx, ny, cd]
        else:
            cd = (cd + 2) % 4
            nnx, nny = cx + dx[cd], cy + dy[cd]
            if (tx, ty) != (nnx, nny):
                runners[idx] = [nnx, nny, cd]


def out_of_bound(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def move_tagger():
    global tx, ty, td, clockwise, visit
    if clockwise:
        nx, ny, nd = tx + dx[td], ty + dy[td], (td + 1) % 4
        nnx, nny = nx + dx[nd], ny + dy[nd]
        visit[nx][ny] = 1
        tx, ty = nx, ny
        if not visit[nnx][nny]:
            td = nd

        if (tx, ty) == (0, 0):
            td = 2
            clockwise = 0
            visit = [[0 for _ in range(n)] for __ in range(n)]
            visit[tx][ty] = 1

    else:
        nx, ny, nd = tx + dx[td], ty + dy[td], (td - 1) % 4
        nnx, nny = nx + dx[td], ny + dy[td]
        visit[nx][ny] = 1
        tx, ty = nx, ny
        if out_of_bound(nnx, nny) or visit[nnx][nny]:
            td = nd

        if (tx, ty) == (n // 2, n // 2):
            td = 0
            clockwise = 1
            visit = [[0 for _ in range(n)] for __ in range(n)]
            visit[tx][ty] = 1


def catch_runners(runners, board):
    cnt = 0
    tmp = deque()

    area = []
    for i in range(3):
        cx, cy = tx + i * dx[td], ty + i * dy[td]
        if not out_of_bound(cx, cy) and board[cx][cy]:
            continue
        area.append([cx, cy])

    while runners:
        cx, cy, cd = runners.popleft()
        if [cx, cy] in area:
            cnt += 1
        else:
            tmp.append([cx, cy, cd])
    while tmp:
        runners.append(tmp.popleft())
    return cnt


for t in range(1, k + 1):
    move_runners(runners, board)
    move_tagger()
    score += t * catch_runners(runners, board)

print(score)
