from collections import deque


def find_same_numbers(cx, cy):
    cnt = 1
    visit = [[0 for _ in range(n)] for __ in range(n)]
    visit[cx][cy] = 1
    queue = deque([[cx, cy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n or visit[nx][ny]:
                continue
            if board[nx][ny] == board[cx][cy]:
                cnt += 1
                visit[nx][ny] = 1
                queue.append([nx, ny])
    return cnt


class Dice:
    def __init__(self, x, y, d, bottom_num):
        self.x = x
        self.y = y
        self.direction = d
        self.bottom_num = bottom_num
        self.score = 0

    def move(self):
        nx, ny = self.x + dx[self.direction], self.y + dy[self.direction]

        if nx < 0 or nx >= n or ny < 0 or ny >= n:
            self.direction = (self.direction + 2) % 4
            nx, ny = self.x + dx[self.direction], self.y + dy[self.direction]

        self.change_bottom_num()
        self.x, self.y = nx, ny

    def calculate_score(self):
        cnt = find_same_numbers(self.x, self.y)
        self.score += board[self.x][self.y] * cnt

    def compare_with_board(self):
        if self.bottom_num > board[self.x][self.y]:
            self.direction = (self.direction + 1) % 4
        elif self.bottom_num < board[self.x][self.y]:
            if self.direction == 0:
                self.direction = 3
            else:
                self.direction -= 1

    def change_bottom_num(self):
        self.bottom_num = dice_move[self.bottom_num][self.direction]


n, m = map(int, input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
board = []  # 0,0 ~ n-1, n-1
for _ in range(n):
    board.append(list(map(int, input().split())))
dice = Dice(0, 0, 1, 6)
dice_move = [[], [5, 3, 2 ,4], [6, 3, 1, 4], [5, 1, 2, 6], [5, 1, 2, 6], [6, 3, 1, 4], [5, 3, 2, 4]]

for _ in range(m):
    dice.move()
    dice.calculate_score()
    dice.compare_with_board()

print(dice.score)
'''
4 3
1 2 4 4
4 2 2 2
5 2 6 6
5 3 3 1
'''