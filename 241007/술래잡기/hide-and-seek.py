from collections import deque

class Person:
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d
    def move(self, nx, ny):
        self.x = nx
        self.y = ny
    def turn(self, nd):
        self.d = nd
class Runner(Person):
    def __init__(self, x, y, d):
        super().__init__(x, y, d)

class Host(Person):
    def __init__(self, x, y, d):
        super().__init__(x, y, d)
        self.tar_point = (0, 0)
        self.turn_points = get_turn_points(x, y, d)

def get_turn_points(cx, cy, cd):
    points = []
    move_charge = 1
    turn_cnt = 0
    charge = 1
    while (cx, cy) != (0, 0):
        if move_charge:
            nx, ny = cx + dx[cd], cy + dy[cd]
            move_charge -= 1
            cx, cy = nx, ny
        else:
            points.append((cx, cy))
            cd = (cd + 1) % 4
            turn_cnt += 1
            if turn_cnt == 2:
                turn_cnt = 0
                charge += 1
            move_charge = charge
    return points

def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def get_dist(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def move_runners(runners, host):
    for runner in runners:
        dist = get_dist(runner.x, runner.y, host.x, host.y)
        if dist > 3:
            continue
        nx, ny = runner.x + dx[runner.d], runner.y + dy[runner.d]
        if out_of_range(nx, ny):
            runner.turn((runner.d + 2) % 4)
            nx, ny = runner.x + dx[runner.d], runner.y + dy[runner.d]
            if host.x != nx or host.y != ny:
                runner.move(nx, ny)
        elif host.x != nx or host.y != ny:
            runner.move(nx, ny)

def move_host(host):
    nx, ny = host.x + dx[host.d], host.y + dy[host.d]
    if host.tar_point== (nx, ny):
        if host.tar_point == (0, 0):
            host.d = 2
            host.tar_point = (n//2, n//2)
        else:
            host.d = 0
            host.tar_point = (0, 0)
    if (nx, ny) in host.turn_points:
        if host.tar_point == (0, 0): # 시작 -> 도착 = 시계방향
            nd = (host.d + 1) % 4
        else:
            nd = (host.d - 1) % 4
        host.turn(nd)
    host.move(nx, ny)


def get_find_bound(x, y, d, board):
    ret = []
    for i in range(3):
        nx, ny = x + i * dx[d], y + i * dy[d]
        if out_of_range(nx, ny) or board[nx][ny]:
            continue
        ret.append([nx, ny])
    return ret

def catch_runners(host, runners, board):
    cnt = 0
    find_bound = get_find_bound(host.x, host.y, host.d, board)
    for runner in runners.copy():
        if [runner.x, runner.y] in find_bound:
            cnt += 1
            runners.remove(runner)
    return cnt


n, m, h, k = map(int, input().split())
runners = deque([])
board = [[0 for _ in range(n)]for __ in range(n)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
for _ in range(m):
    x, y, t = map(int, input().split())
    runners.append(Runner(x-1, y-1, t))

for _ in range(h):
    x, y = map(int, input().split())
    board[x-1][y-1] = 1

host = Host(n//2, n//2, 0)
score = 0

for t in range(1, k+1):
    move_runners(runners, host)
    move_host(host)
    cnt = catch_runners(host, runners, board)
    score += t * cnt
print(score)