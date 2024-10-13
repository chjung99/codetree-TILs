from collections import deque


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(cx, cy, visit, board):
    order = deque([board[cx][cy]])
    location = deque([[cx, cy]])
    visit[cx][cy] = 1
    queue = deque([[cx, cy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or board[nx][ny] == 0 or visit[nx][ny]:
                continue
            visit[nx][ny] = 1
            order.append(board[nx][ny])
            location.append([nx, ny])
            queue.append([nx, ny])
            break
    return order, location


def get_rotate_dir(head, order):
    if order[head - 1] == 2:
        return 1
    else:
        return -1


def move_team(team_order_list):
    for i in range(m):
        head = team_order_list[i].index(1)
        rotate_dir = get_rotate_dir(head, team_order_list[i])
        team_order_list[i].rotate(rotate_dir)


def find_team_person_num(nx, ny, team_location_list, team_order_list):
    team_num = -1
    person_num = -1
    for i in range(m):
        for j in range(len(team_location_list[i])):
            x, y = team_location_list[i][j]
            if (x, y) == (nx, ny) and team_order_list[i][j] != 4:
                head = team_order_list[i].index(1)
                rotate_dir = get_rotate_dir(head, team_order_list[i])
                team_num = i
                person_num = 1
                cur_idx = j
                while team_order_list[i][cur_idx] != 1:
                    cur_idx = (cur_idx + rotate_dir) % len(team_location_list[i])
                    person_num += 1

                return team_num, person_num
    return team_num, person_num

def change_head_tail(team_num, team_order_list):
    head = team_order_list[team_num].index(1)
    tail = team_order_list[team_num].index(3)
    team_order_list[team_num][head] = 3
    team_order_list[team_num][tail] = 1


def throw_ball(cur_round, team_order_list, team_location_list):
    cur_round = cur_round % (4 * n)
    if 0 <= cur_round <= n - 1:
        d = 1
        cx, cy = cur_round, 0

    elif n <= cur_round <= 2 * n - 1:
        d = 0
        cx, cy = n - 1, cur_round - n

    elif 2 * n <= cur_round <= 3 * n - 1:
        d = 3
        cx, cy = n - 1 - (cur_round - 2 * n), n - 1

    else:
        d = 2
        cx, cy = 0, n - (cur_round - 3 * n + 1)

    for i in range(n):
        nx, ny = cx + i * dx[d], cy + i * dy[d]

        team_num, person_num = find_team_person_num(nx, ny, team_location_list, team_order_list)
        if team_num != -1:
            change_head_tail(team_num, team_order_list)
            return person_num ** 2
    return 0

n, m, k = map(int, input().split())
board = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(n):
    board.append(list(map(int, input().split())))

team_order_list = []
team_location_list = []

visit = [[0 for _ in range(n)] for __ in range(n)]

for i in range(n):
    for j in range(n):
        if not visit[i][j] and board[i][j]:
            order, location = bfs(i, j, visit, board)
            team_order_list.append(order)
            team_location_list.append(location)
score = 0

for i in range(k):
    move_team(team_order_list)
    score += throw_ball(i, team_order_list, team_location_list)
print(score)