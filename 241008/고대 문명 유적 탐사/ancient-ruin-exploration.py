# 턴, 숫자 개수임 M은 열번호아니다!!
from collections import deque
from copy import deepcopy
from typing import final


def rotate_square_clockwise_90(left_x, left_y, board):
    new_board = deepcopy(board)
    for i in range(R):
        for j in range(R):
            new_board[left_x + j][left_y + R-1-i] = board[left_x + i][left_y + j]
    return new_board


def rotate_square_clockwise_degree(left_x, left_y, deg, board):
    new_board = deepcopy(board)
    for i in range(deg // 90):
        new_board = rotate_square_clockwise_90(left_x, left_y, new_board)
    return new_board

def out_of_range(x, y):
    return x < 0 or x >= N or y < 0 or y >= N


def bfs(cx, cy, board, visit):
    group = [[cx, cy]]
    visit[cx][cy] = 1
    queue = deque([[cx, cy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if board[nx][ny] == board[cx][cy]:
                visit[nx][ny] = 1
                queue.append([nx, ny])
                group.append([nx, ny])
    return group

def calc_init_value(board):
    init_value = 0
    visit = [[0 for _ in range(N)]for __ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visit[i][j]:
                cnt = len(bfs(i, j, board, visit))
                if cnt >= 3:
                    init_value += cnt
    return init_value



def get_rotate_cand_list(board):
    cand_list = []
    # [1차획득 가치, 회전각도, left_y, left_x]
    for x in range(R):
        for y in range(R):
            for d in [90, 180, 270]:
                new_board = rotate_square_clockwise_degree(x, y, d, board)
                init_value = calc_init_value(new_board)
                cand_list.append([init_value, d, y, x])
    return cand_list

def add_treasure(board, treasure_list):
    visit = [[0 for _ in range(N)] for __ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visit[i][j]:
                group = bfs(i, j, board, visit)
                if len(group) >= 3:
                    treasure_list.extend(group)

def replace_number_on_board(treasure_list, number_queue, board):
    for x, y in treasure_list:
        board[x][y] = number_queue.popleft()


K, M = map(int, input().split())
board = []
N = 5
R = 3
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(N):
    board.append(list(map(int, input().split())))

number_queue = deque(list(map(int, input().split())))

for _ in range(K):
    final_value = 0
    # [1차획득 가치, 회전각도, y, x]
    rotate_cand_list = get_rotate_cand_list(board)
    rotate_cand_list.sort(key=lambda x:(-x[0], x[1], x[2], x[3]))
    init_value, deg, left_y, left_x = rotate_cand_list[0]

    if init_value == 0:
        break

    board = rotate_square_clockwise_degree(left_x, left_y, deg, board)
    treasure_list = [] # x,y

    while True:
        add_treasure(board, treasure_list)
        final_value += len(treasure_list)
        if len(treasure_list) == 0:
            break
        treasure_list.sort(key=lambda x:(x[1], -x[0]))
        replace_number_on_board(treasure_list, number_queue, board)
        treasure_list.clear()
    print(final_value, end=" ")