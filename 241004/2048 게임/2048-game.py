from collections import deque

def move_line(queue):
    out = deque([])
    t = len(queue)
    while queue:
        if len(queue) >= 2 and queue[0] == queue[1]:
            out.append(queue[0] + queue[1])
            queue.popleft()
            queue.popleft()
        else:
            out.append(queue.popleft())
    while len(out) != t:
        out.append(0)
    return out


def move_board(move_dir, board):
    new_board = [[0 for _ in range(n)]for __ in range(n)]
    if move_dir == 0: # 북
        for i in range(n):
            queue = deque([])
            for j in range(n):
                if board[j][i]:
                    queue.append(board[j][i])
            out = move_line(queue)
            for j in range(n):
                if len(out):
                    new_board[j][i] = out.popleft()
    elif move_dir == 2: # 남
        for i in range(n):
            queue = deque([])
            for j in range(n-1, -1, -1):
                if board[j][i]:
                    queue.append(board[j][i])
            out = move_line(queue)
            for j in range(n-1, -1, -1):
                if len(out):
                    new_board[j][i] = out.popleft()
    elif move_dir == 1: # 동
        for i in range(n):
            queue = deque([])
            for j in range(n-1, -1, -1):
                if board[i][j]:
                    queue.append(board[i][j])
            out = move_line(queue)
            for j in range(n-1, -1, -1):
                if len(out):
                    new_board[i][j] = out.popleft()
    else: # 서
        for i in range(n):
            queue = deque([])
            for j in range(n):
                if board[i][j]:
                    queue.append(board[i][j])
            out = move_line(queue)
            for j in range(n):
                if len(out):
                    new_board[i][j] = out.popleft()
    return new_board


def find_max(board):
    max_v = -1
    for i in range(n):
        for j in range(n):
            max_v = max(max_v, board[i][j])
    return max_v


def dfs(move_dir, depth, board):
    global ans
    if depth > 5:
        ans = max(ans, find_max(board))
        return
    new_board = move_board(move_dir, board)
    for i in range(4):
        dfs(i, depth+1, new_board)
n  = int(input())
board = []
ans = 0
for _ in range(n):
    board.append(list(map(int, input().split())))

for i in range(4):
    dfs(i, 0, board)
print(ans)