from collections import deque


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(x, y):
    team_num = 0
    team = deque([[x, y]])
    queue = deque([[x, y]])
    visit[x][y] = 1
    if 0 < board[x][y] < 4:
        team_num += 1

    while queue:
        cx, cy = queue.popleft()

        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if board[nx][ny] != 0 and board[nx][ny] <= board[cx][cy] + 1:
                visit[nx][ny] = 1
                queue.append([nx, ny])
                team.append([nx, ny])
                if 0 < board[nx][ny] < 4:
                    team_num += 1
    return [team, team_num]


def move_teams():
    global team_list
    for team, team_num in team_list:
        team.rotate(1)


def get_line(round):
    if 0 <= round <= n-1:
        return [round, 0, 0]
    elif n <= round <= 2*n-1:
        return [n-1, round-n,1]
    elif 2*n <= round <= 3*n-1:
        return [n-1-(round-2*n), n-1, 2]
    else:
        return [0, n-1-(round-3*n), 3]




def find_person(x, y, d, team_list):
    nx, ny = x, y
    while True:
        for team_idx, (team, team_num) in enumerate(team_list):
            for i in range(team_num):
                if team[i] == [nx, ny]:
                    return team_idx, i+1
        if out_of_range(nx, ny):
            break
        nx, ny = nx + dx[d], ny + dy[d]
    return -1, -1


def change_dir(team_idx):
    global team_list
    team, team_num = team_list[team_idx]

    new_team = deque([])
    for i in range(team_num):
        new_team.appendleft(team.popleft())
    while team:
        new_team.append(team.pop())
    team_list[team_idx] = [new_team, team_num]

def throw_ball(round, team_list):
    x, y, d = get_line(round)
    team_idx, k = find_person(x,y,d,team_list)
    if (team_idx, k) != (-1, -1):
        change_dir(team_idx)
        return k**2
    return 0


n, m, k = map(int, input().split())
board = []
team_list = []
dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]

visit = [[0 for _ in range(n)] for __ in range(n)]
for _ in range(n):
    board.append(list(map(int, input().split())))
score = 0

for i in range(n):
    for j in range(n):
        if not visit[i][j] and board[i][j] == 1:
            team_list.append(bfs(i, j))


for i in range(k):
    move_teams()
    score += throw_ball(i % (4*n), team_list)

print(score)