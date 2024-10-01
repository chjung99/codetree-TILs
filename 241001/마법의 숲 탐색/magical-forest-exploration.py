from collections import deque
from xmlrpc.client import FastParser

R, C, K = map(int ,input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def out_of_range(x, y):
    return x < 0 or x > R or y < 1 or y > C

def can_move_to(locations, board):
    for nx, ny in locations:
        if out_of_range(nx, ny) or board[nx][ny]:
            return False
    return True

class Golam:
    def __init__(self, x, y, d):
        self.cx = x
        self.cy = y
        self.cd = d
    def rotate_exit_clockwise(self):
        self.cd = (self.cd + 1) % 4
    def rotate_exit_reverse_clockwise(self):
        self.cd = (self.cd - 1) % 4
    def move_south(self):
        self.cx = self.cx + 1
    def move_east(self):
        self.cy = self.cy + 1
    def move_west(self):
        self.cy = self.cy - 1
    def out_ch(self):
        return self.cx, self.cy
    def record_on_board(self, board, num):
        board[self.cx][self.cy] = num
        for i in range(4):
            nx, ny = self.cx + dx[i], self.cy + dy[i]
            board[nx][ny] = num
        door[self.cx+dx[self.cd]][self.cy+dy[self.cd]] = 1
    def pop_on_board(self, board):
        board[self.cx][self.cy] = 0
        for i in range(4):
            nx, ny = self.cx + dx[i], self.cy + dy[i]
            board[nx][ny] = 0
        door[self.cx + dx[self.cd]][self.cy + dy[self.cd]] = 0
    def is_possible_move_south(self, board):
        # 범위를 벗어나거나, 골렘이 있는 경우 이동 불가
        next_locations = []
        for i in range(4):
            if i == 0:
                continue
            nx, ny = self.cx + 1 + dx[i], self.cy + dy[i]
            next_locations.append([nx, ny])
        return can_move_to(next_locations, board)

    def is_possible_move_east_south(self, board):
        # 범위를 벗어나거나, 골렘이 있는 경우 이동 불가
        next_east_locations = []
        for i in range(4):
            if self.cx == 0 and i == 0:
                continue
            if i == 3:
                continue
            nx, ny = self.cx + dx[i], self.cy + 1 + dy[i]
            next_east_locations.append([nx, ny])

        next_south_locations = []
        for i in range(4):
            if i == 0:
                continue
            nx, ny = self.cx + 1 + dx[i], self.cy + 1 + dy[i]
            next_south_locations.append([nx, ny])

        return can_move_to(next_east_locations, board) and \
            can_move_to(next_south_locations, board)

    def is_possible_move_west_south(self, board):
        next_west_locations = []
        for i in range(4):
            if self.cx == 0 and i == 0:
                continue
            if i == 1:
                continue
            nx, ny = self.cx + dx[i], self.cy - 1 + dy[i]
            next_west_locations.append([nx, ny])

        next_south_locations = []
        for i in range(4):
            if i == 0:
                continue
            nx, ny = self.cx + 1 + dx[i], self.cy - 1 + dy[i]
            next_south_locations.append([nx, ny])

        return can_move_to(next_west_locations, board) and \
            can_move_to(next_south_locations, board)

    def is_out_of_board(self):
        if self.cx < 1 or self.cx > R or self.cy < 1 or self.cy > C:
            return True

        for i in range(4):
            nx, ny = self.cx + dx[i], self.cy + dy[i]
            if nx < 1 or nx > R or ny < 1 or ny > C:
                return True
        return False
golams = []
board = [[0 for _ in range(C+1)]for __ in range(R+1)]
door = [[0 for _ in range(C+1)]for __ in range(R+1)]
ans = 0
cur_golams = []
for _ in range(K):
    ci, di = map(int,input().split())
    golams.append(Golam(0, ci, di))


def bfs(cx, cy, cn, board):
    visit = [[0 for _ in range(C+1)]for __ in range(R+1)]
    visit[cx][cy] = 1
    queue = deque([[cx, cy, cn]])
    fx, fy = cx, cy
    while queue:
        cx, cy, cn = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            nn = board[nx][ny]
            if door[cx][cy] == 0:
                if cn == nn:
                    visit[nx][ny] = 1
                    queue.append([nx, ny, nn])
                    if fx < nx:
                        fx, fy = nx, ny
            else:
                if nn != 0:
                    visit[nx][ny] = 1
                    queue.append([nx, ny, nn])
                    if fx < nx:
                        fx, fy = nx, ny

    return fx, fy


for i in range(K):
    while True:
        if golams[i].is_possible_move_south(board):
            golams[i].move_south()
        elif golams[i].is_possible_move_west_south(board):
            golams[i].move_west()
            golams[i].rotate_exit_reverse_clockwise()
            golams[i].move_south()
        elif golams[i].is_possible_move_east_south(board):
            golams[i].move_east()
            golams[i].rotate_exit_clockwise()
            golams[i].move_south()
        else:
            break

    if golams[i].is_out_of_board():
        for g in cur_golams:
            g.pop_on_board(board)
        cur_golams.clear()
        continue
    else:
        golams[i].record_on_board(board, i+1)
        cur_golams.append(golams[i])
        cx, cy = golams[i].out_ch()
        cn = board[cx][cy]
        fx, fy = bfs(cx, cy, cn, board)
        ans += fx
        # for x in range(1, R+1):
        #     for y in range(1, C+1):
        #         if door[x][y]:
        #             print("*", end=" ")
        #         else:
        #             print(board[x][y], end=" ")
        #     print("")
        # print("-----")
        # print(fx, fy)
print(ans)