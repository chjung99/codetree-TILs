from collections import deque


class Person:
    def __init__(self, tx, ty):
        self.x = -1
        self.y = -1
        self.tx = tx
        self.ty = ty

    def move_to(self, nx, ny):
        self.x = nx
        self.y = ny


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(cx, cy, dist, board):
    visit = [[0 for _ in range(n)] for __ in range(n)]
    dist[cx][cy] = 0
    visit[cx][cy] = 1
    queue = deque([[cx, cy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny] or board[nx][ny] == -1:
                continue
            visit[nx][ny] = 1
            dist[nx][ny] = dist[cx][cy] + 1
            queue.append([nx, ny])


def find_person_move_dir(person, board):
    dist = [[-1 for _ in range(n)] for __ in range(n)]
    bfs(person.tx, person.ty, dist, board)
    cand = []
    for i in range(4):
        nx, ny = person.x + dx[i], person.y + dy[i]
        if out_of_range(nx, ny) or board[nx][ny] == -1 or dist[nx][ny] == -1:
            continue
        cand.append([dist[nx][ny], i])
    cand.sort(key=lambda x: (x[0], x[1]))
    if len(cand) > 0:
        return cand[0][1]
    return -1

def check_person_arrived(person):
    return (person.tx, person.ty) == (person.x, person.y)


def move_on_board_people(on_board_person_queue, board):
    new_queue = deque([])
    for i in range(len(on_board_person_queue)):
        person = on_board_person_queue[i]
        move_dir = find_person_move_dir(person, board)
        nx, ny = person.x + dx[move_dir], person.y + dy[move_dir]
        person.move_to(nx, ny)
    while on_board_person_queue:
        person = on_board_person_queue.popleft()
        if check_person_arrived(person):
            board[person.x][person.y] = -1
        else:
            new_queue.append(person)
    while new_queue:
        on_board_person_queue.append(new_queue.popleft())


def find_start_base_camp(person, base_list, board):
    dist = [[-1 for _ in range(n)] for __ in range(n)]
    bfs(person.tx, person.ty, dist, board)
    cand = []
    for bx, by in base_list:
        if board[bx][by] == -1:
            continue
        cand.append([dist[bx][by], bx, by])
    cand.sort(key=lambda x: (x[0], x[1], x[2]))
    if len(cand) > 0:
        return cand[0][1], cand[0][2]
    return -1, -1

def get_num_of_arrived(person_list):
    cnt = 0
    for i in range(1, m + 1):
        person = person_list[i]
        if check_person_arrived(person):
            cnt += 1
    return cnt


n, m = map(int, input().split())
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
board = []
base_list = []
person_list = [None]
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if row[j] == 1:
            base_list.append([i, j])
    board.append(row)

for _ in range(m):
    tx, ty = map(int, input().split())
    tx -= 1
    ty -= 1
    person_list.append(Person(tx, ty))

on_board_person_queue = deque([])
time = 0

while True:
    time += 1

    move_on_board_people(on_board_person_queue, board)

    if time <= m:
        person = person_list[time]
        bx, by = find_start_base_camp(person, base_list, board)
        person.move_to(bx, by)
        board[bx][by] = -1
        on_board_person_queue.append(person)

    num_of_arrived = get_num_of_arrived(person_list)
    if num_of_arrived == m:
        print(time)
        break