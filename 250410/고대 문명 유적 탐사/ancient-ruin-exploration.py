from collections import deque

K, M = map(int, input().split())
ori_board = [list(map(int, input().split())) for _ in range(5)]
fresh_q = deque(list(map(int, input().split())))

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

def turn_90(x, y, board):
    new_board = [board[i][:] for i in range(5)]
    for i in range(3):
        for j in range(3):
            new_board[x - 1 + j][y - 1 + 2 - i] = board[x - 1 + i][y - 1 + j]
    for i in range(5):
        for j in range(5):
            board[i][j] = new_board[i][j]
    return new_board

def turn_180(x, y, board):
    board = turn_90(x, y, board)
    board = turn_90(x, y, board)
    return board

def turn_270(x, y, board):
    board = turn_90(x, y, board)
    board = turn_90(x, y, board)
    board = turn_90(x, y, board)
    return board


def turn_board(x, y, d, board):
    if d == 90:
        return turn_90(x, y, board)
    elif d == 180:
        return turn_180(x, y, board)
    elif d == 270:
        return turn_270(x, y, board)
    return -1


def out_of_range(x, y):
    return x < 0 or x >= 5 or y < 0 or y >= 5


def bfs(x, y, visit, board):
    visit[x][y] = 1
    locations = [[x, y]]
    queue = deque([[x, y]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if board[nx][ny] == board[cx][cy]:
                visit[nx][ny] = 1
                queue.append([nx, ny])
                locations.append([nx, ny])
    return locations


def find_locations(board):
    locations = []
    visit = [[0] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if not visit[i][j]:
                tmp = bfs(i, j, visit, board)
                if len(tmp) >= 3:
                    locations.extend(tmp)
    return locations


for t in range(K):
    value = 0
    # 1. 탐사 진행
    cand = []
    for x in range(1, 3 + 1):
        for y in range(1, 3 + 1):
            for d in range(1, 3 + 1):
                new_board = [ori_board[i][:] for i in range(5)]
                new_board = turn_board(x, y, 90 * d, new_board)
                locations = find_locations(new_board)
                cand.append([locations, 90 * d, y, x])

    cand.sort(key=lambda x: (-len(x[0]), x[1], x[2], x[3]))
    flocations, fd, fy, fx = cand[0]

    # 진짜 배열 회전
    ori_board = turn_board(fx, fy, fd, ori_board)
    # 2. 유물 회득
    while True:
        # 2-2. 유물 연쇄 획득
        locations = find_locations(ori_board)
        value += len(locations)

        if len(locations) == 0:
            break
        # 우선순위에 맞게 정렬 [(x,y)..] 열, 행
        locations.sort(key=lambda x: (x[1], -x[0]))
        # 2-1. 유물이 사라지면 조각 탄생
        for x, y in locations:
            ori_board[x][y] = fresh_q.popleft()

    if value == 0:
        break
    else:
        print(value, end=" ")
