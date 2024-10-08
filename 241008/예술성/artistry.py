from collections import deque
from copy import deepcopy


def rotate_cross_anti_clockwise(board):
    new_board = deepcopy(board)
    for d in range(4):
        for r in range(1, n//2 + 1):
            if d == 0:
                x, y = -r, 0
                nx, ny = y, x
            elif d == 1:
                x, y = 0, r
                nx, ny = -y, x
            elif d == 2:
                x, y = r, 0
                nx, ny = y, x
            else:
                x, y = 0, -r
                nx, ny = -y, x
            nx += n//2
            ny += n//2
            cx = x + n//2
            cy = y + n//2
            new_board[nx][ny] = board[cx][cy]
    return new_board

def rotate_square_list(new_board):
    new_board = rotate_square_clockwise_90(0,0,n//2,new_board)
    new_board = rotate_square_clockwise_90(0,n//2+1,n//2,new_board)
    new_board = rotate_square_clockwise_90(n//2+1,0,n//2,new_board)
    new_board = rotate_square_clockwise_90(n//2+1,n//2+1,n//2,new_board)
    return new_board

def rotate_square_clockwise_90(start_x, start_y, r, board):
    new_board = deepcopy(board)
    for i in range(r):
        for j in range(r):
            new_board[start_x+j][start_y+r-1-i] = board[start_x+i][start_y+j]
    return new_board

def rotate_board(board):

    new_board = rotate_cross_anti_clockwise(board)
    new_board = rotate_square_list(new_board)
    for i in range(n):
        for j in range(n):
            board[i][j] = new_board[i][j]

def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(cx, cy, visit, board):
    queue = deque([[cx, cy]])
    visit[cx][cy] = 1
    group = [[cx, cy]]
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if board[nx][ny] == board[cx][cy]:
                queue.append([nx, ny])
                group.append([nx, ny])
                visit[nx][ny] = 1
    return group


def find_groups(board):
    tmp_groups = []
    visit = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            if not visit[i][j]:
                tmp_groups.append(bfs(i, j, visit, board))
    return tmp_groups


def set_group_board(groups, group_board):
    for i in range(len(groups)):
        for x, y in groups[i]:
            group_board[x][y] = i


def make_group_combination(groups):
    comb = []
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            comb.append([i, j])
    return comb


def count_common_side(a, b, groups, group_board):
    cnt = 0
    for x, y in groups[a]:
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if out_of_range(nx, ny):
                continue
            if group_board[nx][ny] == b:
                cnt += 1
    return cnt


def calc_harmony(group_comb_idx, groups, board, group_board):
    score = 0
    for a, b in group_comb_idx:
        common_side_cnt = count_common_side(a, b, groups, group_board)
        num_a = board[groups[a][0][0]][groups[a][0][1]]
        num_b = board[groups[b][0][0]][groups[b][0][1]]

        score += (len(groups[a]) + len(groups[b])) * num_a * num_b * common_side_cnt

    return score


n = int(input())
board = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
ans = 0

for i in range(n):
    board.append(list(map(int, input().split())))

for i in range(4):
    group_board = [[0 for _ in range(n)] for __ in range(n)]
    if i > 0:
        rotate_board(board)
    groups = find_groups(board)
    set_group_board(groups, group_board)
    group_comb_idx = make_group_combination(groups)
    turn_score = calc_harmony(group_comb_idx, groups, board, group_board)
    ans += turn_score

print(ans)