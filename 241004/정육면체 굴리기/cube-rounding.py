from collections import deque



def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= m


def move_dice(nx, ny, move_dir, dice_horizon, dice_vertical, board):
    if move_dir == 1 or move_dir == 2:
        if move_dir == 1:
            dice_horizon.rotate(1)
        else:
            dice_horizon.rotate(-1)
        dice_vertical[0] = dice_horizon[0]
        dice_vertical[2] = dice_horizon[2]
    else:
        if move_dir == 3:
            dice_vertical.rotate(-1)
        else:
            dice_vertical.rotate(1)
        dice_horizon[0] = dice_vertical[0]
        dice_horizon[2] = dice_vertical[2]

    if board[nx][ny] == 0:
        board[nx][ny] = dice_horizon[2]
    else:
        dice_horizon[2] = dice_vertical[2] = board[nx][ny]
        board[nx][ny] = 0

n, m, x, y, k = map(int, input().split())
board = []
for _ in range(n):
    board.append(list(map(int, input().split())))
move_list = list(map(int, input().split()))
dice_horizon = deque([0, 0, 0, 0])
dice_vertical = deque([0, 0, 0, 0])

dx = [0, 0, 0, -1, 1]
dy = [0, 1, -1, 0, 0]

cx, cy = x, y


for move_dir in move_list:
    nx, ny = cx + dx[move_dir], cy + dy[move_dir]
    if not out_of_range(nx, ny):
        move_dice(nx, ny, move_dir, dice_horizon, dice_vertical, board)
        cx, cy = nx, ny
        print(dice_horizon[0])