from collections import deque

BOARD_SIZE = 5
ROTATE_SIZE = 3
dx = [1, 0, -1, 0]
dy = [0, 1, 0 ,-1]
K, M = map(int, input().split())
board = []

for _ in range(BOARD_SIZE):
    board.append(list(map(int,input().split())))
ready_blocks = list(map(int, input().split()))
ready_blocks = deque(ready_blocks)


def out_of_range(y, x):
    return y < 0 or y >= BOARD_SIZE or x < 0 or x >= BOARD_SIZE


def find_rotate_location(board):
    degrees = [90, 180, 270]
    cand = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if out_of_range(y+ROTATE_SIZE-1, x+ROTATE_SIZE-1):
                continue
            for d in range(3):
                rotated_board = [board[i][:] for i in range(BOARD_SIZE)]
                rotate_board(x, y, degrees[d], rotated_board)
                score_blocks, score = get_score_blocks(rotated_board)
                cand.append([score, degrees[d], x, y, score_blocks])
    cand.sort(key=lambda x:(-x[0], x[1], x[2], x[3]))
    return cand[0]


def rotate_part_90(tx, ty, new_board, src_board):
    for ry in range(ROTATE_SIZE):
        for rx in range(ROTATE_SIZE):
            new_board[ty + rx][tx + (2-ry)] = src_board[ty+ry][tx+rx]


def copy_part(tx, ty, board, new_board):
    for ry in range(ROTATE_SIZE):
        for rx in range(ROTATE_SIZE):
            board[ty + ry][tx + rx] = new_board[ty + ry][tx + rx]


def rotate_board(tx, ty, degree, board):
    new_board = [[-1 for _ in range(BOARD_SIZE)] for __ in range(BOARD_SIZE)]
    if degree == 90:
        src_board = board
        rotate_part_90(tx, ty, new_board, src_board)

        copy_part(tx, ty, board, new_board)
    elif degree == 180:
        src_board = board
        rotate_part_90(tx, ty, new_board, src_board)

        new_board2 = [[-1 for _ in range(BOARD_SIZE)] for __ in range(BOARD_SIZE)]
        src_board = new_board
        rotate_part_90(tx, ty, new_board2, src_board)

        copy_part(tx, ty, board, new_board2)
    elif degree == 270:
        src_board = board
        rotate_part_90(tx, ty, new_board, src_board)

        new_board2 = [[-1 for _ in range(BOARD_SIZE)] for __ in range(BOARD_SIZE)]
        src_board = new_board
        rotate_part_90(tx, ty, new_board2, src_board)

        new_board3 = [[-1 for _ in range(BOARD_SIZE)] for __ in range(BOARD_SIZE)]
        src_board = new_board2
        rotate_part_90(tx, ty, new_board3, src_board)

        copy_part(tx, ty, board, new_board3)

def bfs(cy, cx, visit, board):
    visit[cy][cx] = 1
    tmp_q = deque([[cy, cx]])
    queue = deque([[cy, cx]])
    while queue:
        cy, cx = queue.popleft()
        for i in range(4):
            ny, nx = cy + dy[i], cx + dx[i]
            if out_of_range(ny, nx) or visit[ny][nx]:
                continue
            if board[ny][nx] == board[cy][cx]:
                visit[ny][nx] = 1
                tmp_q.append([ny, nx])
                queue.append([ny, nx])
    return [len(tmp_q), tmp_q]

def get_score_blocks(board):
    score = 0
    score_blocks = []
    visit = [[0 for _ in range(BOARD_SIZE)]for __ in range(BOARD_SIZE)]
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if not visit[y][x]:
                group = bfs(y, x, visit, board)
                if group[0] >= 3:
                    score += group[0]
                    while group[1]:
                        gy, gx = group[1].popleft()
                        score_blocks.append([gy, gx])
    score_blocks.sort(key=lambda x:(x[1], -x[0]))
    score_blocks = deque(score_blocks)
    return score_blocks, score

def replace_board(score_blocks, ready_blocks, board):
    while score_blocks:
        dest_y, dest_x = score_blocks.popleft()
        src = ready_blocks.popleft()
        board[dest_y][dest_x] = src


for _ in range(K):
    turn_score = 0
    score, degree, tx, ty, score_blocks = find_rotate_location(board)
    if score == 0:
        break
    rotate_board(tx, ty, degree, board)
    score_blocks, score = get_score_blocks(board)
    while score != 0:
        turn_score += score
        replace_board(score_blocks, ready_blocks, board)
        score_blocks, score = get_score_blocks(board)
    print(turn_score, end=" ")