from collections import deque

n, m = map(int, input().split())
board = []
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
score = 0

for _ in range(n):
    board.append(list(map(int, input().split())))


class BombGroup:
    def __init__(self, px, py, bombs, red_bomb_cnt, total_bomb_cnt):
        self.px = px
        self.py = py
        self.bombs = bombs
        self.red_bomb_cnt = red_bomb_cnt
        self.total_bomb_cnt = total_bomb_cnt


def bfs(cx, cy, visit):
    color = board[cx][cy]
    bombs = [[cx, cy]]
    visit[cx][cy] = 1
    red_bombs = []
    queue = deque([[cx, cy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            if not visit[nx][ny] and (board[nx][ny] == 0 or board[nx][ny] == color):
                visit[nx][ny] = 1
                queue.append([nx, ny])
                if board[nx][ny] == 0:
                    red_bombs.append([nx, ny])
                else:
                    bombs.append([nx, ny])
    total_bomb_cnt = len(bombs) + len(red_bombs)
    red_bomb_cnt = len(red_bombs)

    for rx, ry in red_bombs:
        visit[rx][ry] = 0

    if total_bomb_cnt >= 2:
        bombs.sort(key=lambda x: (-x[0], x[1]))
        return BombGroup(bombs[0][0], bombs[0][1], bombs + red_bombs, red_bomb_cnt, total_bomb_cnt)
    else:
        return None


def find_max_bomb_group():
    bomb_groups = []
    visit = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            if board[i][j] >= 1 and not visit[i][j]:
                bomb_group = bfs(i, j, visit)
                if bomb_group is not None:
                    bomb_groups.append(bomb_group)
    if len(bomb_groups) > 0:
        bomb_groups.sort(key=lambda x: (-x.total_bomb_cnt, x.red_bomb_cnt, -x.px, x.py))
        return bomb_groups[0]
    else:
        return None


def remove_bombs(board, selected_group):
    for bx, by in selected_group.bombs:
        board[bx][by] = -2


def find_next_loc(cx, cy):
    nx, ny = cx, cy
    while True:
        if nx + 1 >= n or board[nx + 1][ny] >= -1:
            break
        if board[nx + 1][ny] == -2:
            nx += 1
    return [nx, ny]


def move_bomb(cx, cy, nx, ny, board):
    board[nx][ny] = board[cx][cy]
    board[cx][cy] = -2


def fall_bombs(board):
    for cy in range(n):
        for cx in range(n - 1, -1, -1):
            if board[cx][cy] >= 0:
                nx, ny = find_next_loc(cx, cy)
                if [nx, ny] != [cx, cy]:
                    move_bomb(cx, cy, nx, ny, board)


def rotate_board(board):
    new_board = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            new_board[i][j] = board[j][n - 1 - i]
    for i in range(n):
        for j in range(n):
            board[i][j] = new_board[i][j]


while True:
    selected_group = find_max_bomb_group()
    if selected_group is None:
        break
    remove_bombs(board, selected_group)
    score += selected_group.total_bomb_cnt ** 2
    fall_bombs(board)
    rotate_board(board)
    fall_bombs(board)
print(score)