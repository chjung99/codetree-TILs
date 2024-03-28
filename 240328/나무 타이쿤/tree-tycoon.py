from collections import deque


class Nutrient:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, move_dir, move_cnt):
        nx = self.x
        ny = self.y
        for _ in range(move_cnt):
            nx = nx + dx[move_dir]
            if nx >= n:
                nx = nx % n
            if nx < 0:
                nx += n
            ny = ny + dy[move_dir]
            if ny >= n:
                ny = ny % n
            if ny < 0:
                ny += n
        self.x = nx
        self.y = ny

    def put(self):
        visit[self.x][self.y] = 1
        board[self.x][self.y] += 1

    def grow_more(self):
        cnt = 0
        for i in range(1, 5):
            nx = self.x + dx[i * 2]
            ny = self.y + dy[i * 2]
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            if board[nx][ny] >= 1:
                cnt += 1
        board[self.x][self.y] += cnt

def move_nutrients(move_dir, move_cnt):
    global visit, board, nutrients
    for nut in nutrients:
        nut.move(move_dir, move_cnt)
        nut.put()
    while nutrients:
        nut = nutrients.popleft()
        nut.grow_more()


def cut_and_put_nutrients():
    global nutrients, board
    for i in range(n):
        for j in range(n):
            if not visit[i][j] and board[i][j] >= 2:
                board[i][j] -= 2
                new_nut = Nutrient(i, j)
                nutrients.append(new_nut)


def calc_total_heigh():
    cnt = 0
    for i in range(n):
        for j in range(n):
            cnt += board[i][j]
    return cnt


n, m = map(int, input().split())
visit = [[0 for _ in range(n)] for __ in range(n)]
dx = [0, 0, -1, -1, -1, 0, 1, 1, 1]
dy = [0, 1, 1, 0, -1, -1, -1, 0, 1]
board = []
move = deque([])
nutrients = deque([Nutrient(n-2, 0), Nutrient(n-1, 0), Nutrient(n-2, 1), Nutrient(n-1, 1)])
for _ in range(n):
    board.append(list(map(int, input().split())))
for _ in range(m):
    d, p = map(int, input().split())
    move.append([d, p])

for _ in range(m):
    visit = [[0 for _ in range(n)] for __ in range(n)]
    move_dir, move_cnt = move.popleft()
    move_nutrients(move_dir, move_cnt)
    cut_and_put_nutrients()

answer = calc_total_heigh()
print(answer)