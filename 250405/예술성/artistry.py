from collections import deque


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(x, y, group_cnt):
    global visit, groups, group_board
    visit[x][y] = 1
    queue = deque([[x, y]])
    cur_group = [[x, y]]
    while queue:
        cx, cy = queue.popleft()
        group_board[cx][cy] = group_cnt
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if ori_board[nx][ny] == ori_board[cx][cy]:
                visit[nx][ny] = 1
                queue.append([nx, ny])
                cur_group.append([nx, ny])
    groups.append(cur_group)


def get_adj(a, b, groups):
    cnt = 0
    # adj_visit = [[0 for _ in range(n)]for __ in range(n)]
    group_num_b = group_board[groups[b][0][0]][groups[b][0][1]]

    for x, y in groups[a]:
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            # if out_of_range(nx, ny) or adj_visit[nx][ny]:
            if out_of_range(nx, ny):
                continue
            if group_board[nx][ny] == group_num_b:
                # adj_visit[nx][ny] = 1
                cnt += 1

    return cnt


def get_score(groups):
    score = 0
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            adj = get_adj(i, j, groups)
            x = (len(groups[i]) + len(groups[j])) \
                * (ori_board[groups[i][0][0]][groups[i][0][1]]) \
                * (ori_board[groups[j][0][0]][groups[j][0][1]]) \
                * adj
            score += x
    return score


def rotate_cross_anti_clockwise(ori_board):
    new_board = [row[:] for row in ori_board]
    cx, cy = n//2, n//2
    for i in range(4):
        for k in range(1, n//2+1):
            ax, ay = cx + k * dx[i], cy + k * dy[i]
            bx, by = cx + k * dx[(i-1)%4], cy + k * dy[(i-1)%4]
            new_board[bx][by] = ori_board[ax][ay]

    return new_board

def rotate_sqaure_clockwise(cx, cy, size, ori_board):
    new_board = [row[:] for row in ori_board]
    for i in range(size):
        for j in range(size):
            new_board[cx+j][cy+size-1-i] = ori_board[cx+i][cy+j]
    return new_board

def rotate_board(ori_board):
    ori_board = rotate_cross_anti_clockwise(ori_board)

    ori_board = rotate_sqaure_clockwise(0, 0, n // 2, ori_board)
    ori_board = rotate_sqaure_clockwise(0, n // 2 + 1, n // 2, ori_board)
    ori_board = rotate_sqaure_clockwise(n // 2 + 1, 0, n // 2, ori_board)
    ori_board = rotate_sqaure_clockwise(n // 2 + 1, n // 2 + 1, n // 2, ori_board)

    return ori_board


n = int(input())
ori_board = []

score = 0
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

for _ in range(n):
    ori_board.append(list(map(int, input().split())))

group_board = [[0 for _ in range(n)] for __ in range(n)]
visit = [[0 for _ in range(n)] for __ in range(n)]
group_cnt = 0
groups = []

for i in range(n):
    for j in range(n):
        if not visit[i][j]:
            bfs(i, j, group_cnt)
            group_cnt += 1

score = get_score(groups)

for _ in range(3):
    ori_board = rotate_board(ori_board)

    group_board = [[0 for _ in range(n)] for __ in range(n)]
    visit = [[0 for _ in range(n)] for __ in range(n)]
    group_cnt = 0
    groups = []

    for i in range(n):
        for j in range(n):
            if not visit[i][j]:
                bfs(i, j, group_cnt)
                group_cnt += 1
    score += get_score(groups)

print(score)
