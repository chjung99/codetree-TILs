from collections import deque


class Player:
    def __init__(self, x, y, num, team_idx):
        self.location = [x, y]
        self.num = num
        self.team = team_idx


def find_team_members(sx, sy, team_idx):
    head_player = Player(sx, sy, 1, team_idx)
    team = [head_player]
    visit = [[0 for _ in range(n)] for __ in range(n)]
    queue = deque([[sx, sy]])
    visit[sx][sy] = 1
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            if not visit[nx][ny] and player_board[cx][cy] <= player_board[nx][ny] <= 3:
                visit[nx][ny] = 1
                new_player = Player(nx, ny, player_board[nx][ny], team_idx)
                queue.append([nx, ny])
                team.append(new_player)
    return team


def find_next_step(x, y):
    nx, ny = x, y
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if nx < 0 or nx >= n or ny < 0 or ny >= n:
            continue
        if player_board[nx][ny] == 4:
            return [nx, ny]
    return [nx, ny]


def move_players(team):
    head = team[0]
    next_step = find_next_step(*head.location)

    pre_step = head.location

    player_board[next_step[0]][next_step[1]] = head.num
    player_board[pre_step[0]][pre_step[1]] = 4

    head.location = next_step

    for i in range(1, len(team)):
        next_step = pre_step
        pre_step = team[i].location

        player_board[next_step[0]][next_step[1]] = team[i].num
        player_board[pre_step[0]][pre_step[1]] = 4

        team[i].location = next_step


def shoot_ball(ball_dir, ball_cnt):
    global score
    row = 0
    col = 0

    if ball_dir == 0:
        row = ball_cnt
        col = 0
        for i in range(n):
            if 1 <= player_board[row][i] <= 3:
                # score += player_board[row][i] ** 2
                team_number, idx = get_team_number_and_idx([row, i])
                score += idx ** 2
                return [row, i, team_number]

    elif ball_dir == 1:
        row = n - 1
        col = ball_cnt
        for i in range(row, -1, -1):
            if 1 <= player_board[i][col] <= 3:
                # score += player_board[i][col] ** 2
                team_number, idx = get_team_number_and_idx([i, col])
                score += idx ** 2
                return [i, col, team_number]

    elif ball_dir == 2:
        row = n - 1 - ball_cnt
        col = n - 1
        for i in range(col, -1, -1):
            if 1 <= player_board[row][i] <= 3:
                team_number, idx = get_team_number_and_idx([row, i])
                score += idx ** 2
                # score += player_board[row][i] ** 2
                return [row, i, team_number]

    else:
        row = 0
        col = n - 1 - ball_cnt
        for i in range(n):
            if 1 <= player_board[i][col] <= 3:
                team_number, idx = get_team_number_and_idx([i, col])
                score += idx ** 2
                # score += player_board[i][col] ** 2
                return [i, col, team_number]
    return [-1, -1, -1]


def get_team_number_and_idx(location):
    for i in range(len(teams)):
        for j in range(len(teams[i])):
            if teams[i][j].location == location:
                return i, j+1
    return -1, -1


def change_direction(team_number):
    global teams
    head_location = teams[team_number][0].location
    tail_location = teams[team_number][-1].location

    teams[team_number].reverse()

    player_board[head_location[0]][head_location[1]] = 3
    player_board[tail_location[0]][tail_location[1]] = 1


dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]
n, m, k = map(int, input().split())
line_board = []
player_board = []
head_players = []
teams = []
ball_dir = 0
ball_cnt = 0
score = 0
cnt = 0
for i in range(n):
    tmp = list(map(int, input().split()))
    if 1 in tmp:
        head_players.append([i, tmp.index(1), cnt])
        cnt += 1
    filtered_tmp = []
    for t in tmp:
        if 1 <= t <= 3:
            filtered_tmp.append(4)
        else:
            filtered_tmp.append(t)
    line_board.append(filtered_tmp)
    player_board.append(tmp)

for hx, hy, hidx in head_players:
    teams.append(find_team_members(hx, hy, hidx))

for i in range(k):
    r = i % (4 * n)
    if 0 <= r < n:
        ball_dir = 0
    elif n <= r < 2 * n:
        ball_dir = 1
    elif 2 * n <= r < 3 * n:
        ball_dir = 2
    else:
        ball_dir = 3

    for j in range(len(teams)):
        move_players(teams[j])

    hit_result = shoot_ball(ball_dir, ball_cnt)
    if hit_result != [-1, -1, -1]:
        hit_team_number = hit_result[-1]
        # print(hit_result[:2])
        change_direction(hit_team_number)

    ball_cnt = (ball_cnt + 1) % n

print(score)
'''
7 2 2
3 2 1 0 0 0 0
4 0 4 0 2 1 4
4 4 4 0 2 0 4
0 0 0 0 3 0 4
0 0 4 4 4 0 4
0 0 4 0 0 0 4
0 0 4 4 4 4 4


'''