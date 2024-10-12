from copy import deepcopy
from collections import deque


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dist = 0
        self.is_arrived = 0

    def move_to(self, nx, ny):
        self.x = nx
        self.y = ny

    def add_dist(self, d):
        self.dist += d


def out_of_range(x, y):
    return x < 0 or x >= N or y < 0 or y >= N


def find_exit(board):
    ex, ey = -1, -1
    for i in range(N):
        for j in range(N):
            if board[i][j] == -1:
                return i, j


def move_players(on_board_players, board):
    new_players = deque([])
    while on_board_players:
        player = on_board_players.popleft()
        ex, ey = find_exit(board)
        cur_dist = abs(player.x - ex) + abs(player.y - ey)
        cand = []
        for i in range(4):
            nx, ny = player.x + dx[i], player.y + dy[i]
            next_dist = abs(nx - ex) + abs(ny - ey)
            if out_of_range(nx, ny) or cur_dist <= next_dist or 1 <= board[nx][ny] <= 9:
                continue
            cand.append([next_dist, nx, ny, i])
        cand.sort(key=lambda x: (x[0],x[3]))
        if len(cand) >= 1:
            nx, ny = cand[0][1], cand[0][2]
            player.move_to(nx, ny)
            player.add_dist(1)
            if (player.x, player.y) != (ex, ey):
                new_players.append(player)
            else:
                player.is_arrived = True
        else:  # 이동할 곳이 없으면 그냥 제자리에있는 거 넣음
            new_players.append(player)
    while new_players:
        on_board_players.append(new_players.popleft())


def invalid_square(x, y, size):
    return out_of_range(x + size - 1, y + size - 1)


def square_include_player_and_exit(x, y, size, on_board_players, board):
    is_exit = False
    is_player = False
    for i in range(x, x + size):
        for j in range(y, y + size):
            if 1 <= board[i][j] <= 9:
                continue
            elif board[i][j] == -1:
                is_exit = True
                continue
            for player in on_board_players:
                if (player.x, player.y) == (i, j):
                    is_player = True
                    break
    return is_exit and is_player


def find_min_square(on_board_players, board):
    cand = []
    for i in range(N):
        for j in range(N):
            for size in range(2, N + 1):
                if invalid_square(i, j, size):
                    continue
                if square_include_player_and_exit(i, j, size, on_board_players, board):
                    cand.append([size, i, j])
    cand.sort(key=lambda x: (x[0], x[1], x[2]))
    if len(cand) > 0:
        return cand[0][1], cand[0][2], cand[0][0]


def find_block_in_square(left_x, left_y, size):
    blocks = []
    for i in range(left_x, left_x + size):
        for j in range(left_y, left_y + size):
            if 1 <= board[i][j] <= 9:
                blocks.append([i, j])
    return blocks


def down_block_power(blocks, board):
    for x, y in blocks:
        board[x][y] -= 1


def rotate_square(left_x, left_y, size, board):
    new_board = deepcopy(board)
    for i in range(size):
        for j in range(size):
            new_board[left_x + j][left_y + size - 1 - i] = board[left_x + i][left_y + j]
    return new_board


def rotate_player(left_x, left_y, size, on_board_players, board):
    new_players = deepcopy(on_board_players)
    for i in range(size):
        for j in range(size):
            for idx in range(len(on_board_players)):
                player = on_board_players[idx]
                if (left_x+i, left_y+j) == (player.x, player.y):
                    new_players[idx].move_to(left_x + j, left_y + size - 1 - i)
    for idx in range(len(new_players)):
        on_board_players[idx].x = new_players[idx].x
        on_board_players[idx].y = new_players[idx].y

N, M, K = map(int, input().split())
board = []
player_list = []
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
for _ in range(N):
    board.append(list(map(int, input().split())))

for _ in range(M):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    player_list.append(Player(x, y))

ex, ey = map(int, input().split())
ex -= 1
ey -= 1
board[ex][ey] = -1

on_board_players = deque(player_list)

for _ in range(K):
    # print(f"{_+1}초:")
    # for b in board:
    #     print(b)

    move_players(on_board_players, board)
    # print("참가자 이동")
    # for b in on_board_players:
    #     print(b.x, b.y, b.is_arrived)
    # print("참가자 이동 횟수")
    # for player in player_list:
    #     print(player.dist, end=" ")
    # print("")
    if len(on_board_players) == 0:
        break
    left_x, left_y, size = find_min_square(on_board_players, board)
    blocks = find_block_in_square(left_x, left_y, size)
    rotate_player(left_x, left_y, size, on_board_players, board)

    down_block_power(blocks, board)
    board = rotate_square(left_x, left_y, size, board)
    # print("보드 회전")
    #
    # for b in board:
    #     print(b)
    # print("참가자 회전")
    # for b in on_board_players:
    #     print(b.x, b.y, b.is_arrived)
    # print("====")


ans = 0
for player in player_list:
    ans += player.dist

print(ans)
ex, ey = find_exit(board)
print(ex+1, ey+1)

# 5 3 100
# 0 0 0 0 1
# 9 2 2 0 0
# 0 1 0 1 0
# 0 0 0 1 0
# 0 0 0 0 0
# 1 3
# 3 1
# 3 5
# 3 3