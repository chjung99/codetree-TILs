from collections import deque

n = int(input())
board = []
total_art_score = 0

dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]

for _ in range(n):
    board.append(list(map(int, input().split())))


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(cx, cy, visit):
    queue = deque([[cx, cy]])
    visit[cx][cy] = 1
    group_locations = [[cx, cy]]
    group_number = board[cx][cy]
    group_cnt = 1

    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if board[cx][cy] == board[nx][ny]:
                visit[nx][ny] = 1
                queue.append([nx, ny])
                group_locations.append([nx, ny])
                group_cnt += 1
    return [group_cnt, group_number, group_locations]


def get_groups(board):
    groups = []
    visit = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            if not visit[i][j]:
                groups.append(bfs(i, j, visit))
    return groups


def get_adj_cnt(a, b, groups, board):
    cnt = 0
    for x, y in groups[a][2]:
        for d in range(4):
            nx, ny = x + dx[d], y + dy[d]
            if out_of_range(nx, ny):
                continue
            if [nx, ny] in groups[b][2]:
                cnt += 1
            # if board[nx][ny] == groups[b][1]:
            #     cnt += 1
    return cnt

def calc_harmony_score(a, b, groups, board):
    adj_cnt = get_adj_cnt(a, b, groups, board)
    return (groups[a][0] + groups[b][0]) * groups[a][1] * groups[b][1] * adj_cnt


def calc_art_score(board, groups):
    total_art_score = 0
    size_of_groups = len(groups)
    for i in range(size_of_groups):
        art_score = 0
        for j in range(i + 1, size_of_groups):
            harmony_score = calc_harmony_score(i, j, groups, board)
            art_score += harmony_score
        total_art_score += art_score
    return total_art_score


def rotate_square(px, py, square_size):
    new_board = [board[i][:] for i in range(n)]
    for i in range(square_size):
        for j in range(square_size):
            src_x, src_y = px + i, py + j
            dest_x, dest_y = px + j, py + (square_size-1-i)
            new_board[dest_x][dest_y] = board[src_x][src_y]
    for i in range(n):
        for j in range(n):
            board[i][j] = new_board[i][j]

def rotate_cross(cx, cy, board):
    new_board = [board[i][:] for i in range(n)]
    for d in range(4):
        nx, ny, nd = cx, cy, (d-1)%4
        for r in range(1, n+1):
            nx, ny = cx + dx[d] * r, cy + dy[d] * r
            dest_x, dest_y = cx + dx[nd] * r, cy+dy[nd]*r
            if out_of_range(nx, ny):
                break
            new_board[dest_x][dest_y] = board[nx][ny]
    for i in range(n):
        for j in range(n):
            board[i][j] = new_board[i][j]


def rotate_board(board):
    rotate_cross(n // 2, n // 2, board)
    rotate_square(0, 0, n // 2)
    rotate_square(n // 2 + 1, 0, n // 2)
    rotate_square(0, n // 2 + 1, n // 2)
    rotate_square(n // 2 + 1, n // 2 + 1, n // 2)


for _ in range(4):
    groups = get_groups(board)
    total_art_score += calc_art_score(board, groups)
    rotate_board(board)
print(total_art_score)