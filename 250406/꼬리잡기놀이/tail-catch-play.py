# 변수 선언 및 입력:

n, m, k = tuple(map(int, input().split()))
board = [[0] * (n + 1)]
for _ in range(n):
    board.append([0] + list(map(int, input().split())))

# 각 팀별 레일 위치를 관리합니다.
v = [[] for _ in range(m + 1)]
# 각 팀별 tail 위치를 관리합니다.
tail = [0] * (m + 1)
visited = [
    [False] * (n + 1)
    for _ in range(n + 1)
]

# 격자 내 레일에 각 팀 번호를 적어줍니다.
board_idx = [
    [0] * (n + 1)
    for _ in range(n + 1)
]

ans = 0

dxs = [-1,  0, 1, 0]
dys = [ 0, -1, 0, 1]


def is_out_range(x, y):
    return not (1 <= x and x <= n and 1 <= y and y <= n)


# 초기 레일을 만들기 위해 dfs를 이용합니다.
def dfs(x, y, idx):
    visited[x][y] = True
    board_idx[x][y] = idx
    for dx, dy in zip(dxs, dys):
        nx, ny = x + dx, y + dy
        if is_out_range(nx, ny): 
            continue

        # 이미 지나간 경로거나 경로가 아니면 넘어갑니다.
        if board[nx][ny] == 0: 
            continue
        if visited[nx][ny]: 
            continue

        # 가장 처음 탐색할 때 2가 있는 방향으로 dfs를 진행합니다.
        if len(v[idx]) == 1 and board[nx][ny] != 2: 
            continue

        v[idx].append((nx, ny))
        if board[nx][ny] == 3:
            tail[idx] = len(v[idx])
        dfs(nx, ny, idx)


# 초기 작업을 합니다.
def init():
    cnt = 1

    # 레일을 벡터에 저장합니다. 머리사람을 우선 앞에 넣어줍니다.
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if board[i][j] == 1: 
                v[cnt].append((i, j))
                cnt += 1

    # dfs를 통해 레일을 벡터에 순서대로 넣어줍니다.
    for i in range(1, m + 1):
        x, y = v[i][0]
        dfs(x, y, i)


# 각 팀을 이동시키는 함수입니다.
def move_all():
    for i in range(1, m + 1):
        # 각 팀에 대해 레일을 한 칸씩 뒤로 이동시킵니다.
        tmp = v[i][-1]
        for j in range(len(v[i]) - 1, 0, -1):
            v[i][j] = v[i][j - 1]
        v[i][0] = tmp

    for i in range(1, m + 1):
        # 벡터에 저장한 정보를 바탕으로 보드의 표기 역시 바꿔줍니다.
        for j, (x, y) in enumerate(v[i]):
            if j == 0:
                board[x][y] = 1
            elif j < tail[i] - 1:
                board[x][y] = 2
            elif j == tail[i] - 1:
                board[x][y] = 3
            else:
                board[x][y] = 4


# (x, y) 지점에 공이 닿았을 때의 점수를 계산합니다.
def get_point(x, y):
    global ans
    idx = board_idx[x][y]
    cnt = v[idx].index((x, y))
    ans += (cnt + 1) * (cnt + 1)


# turn 번째 라운드의 공을 던집니다.
# 공을 던졌을 때 이를 받은 팀의 번호를 반환합니다.
def throw_ball(turn):
    t = (turn - 1) % (4 * n) + 1

    if t <= n:
        # 1 ~ n 라운드의 경우 왼쪽에서 오른쪽 방향으로 공을 던집니다.
        for i in range(1, n + 1):
            if 1 <= board[t][i] and board[t][i] <= 3:
                # 사람이 있는 첫 번째 지점을 찾습니다.
                # 찾게 되면 점수를 체크한 뒤 찾은 사람의 팀 번호를 저장합니다.
                get_point(t, i)
                return board_idx[t][i]
    elif t <= 2 * n:
        # n+1 ~ 2n 라운드의 경우 아래에서 윗쪽 방향으로 공을 던집니다.
        t -= n
        for i in range(1, n + 1):
            if 1 <= board[n + 1 - i][t] and board[n + 1 - i][t] <= 3:
                # 사람이 있는 첫 번째 지점을 찾습니다.
                # 찾게 되면 점수를 체크한 뒤 찾은 사람의 팀 번호를 저장합니다.
                get_point(n + 1 - i, t)
                return board_idx[n + 1 - i][t]
    elif t <= 3 * n:
        # 2n+1 ~ 3n 라운드의 경우 오른쪽에서 왼쪽 방향으로 공을 던집니다.
        t -= (2 * n)
        for i in range(1, n + 1):
            if 1 <= board[n + 1 - t][n + 1 - i] and board[n + 1 - t][n + 1 - i] <= 3:
                # 사람이 있는 첫 번째 지점을 찾습니다.
                # 찾게 되면 점수를 체크한 뒤 찾은 사람의 팀 번호를 저장합니다.
                get_point(n + 1 - t, n + 1 - i)
                return board_idx[n + 1 - t][n + 1 - i]
    else:
        # 3n+1 ~ 4n 라운드의 경우 위에서 아랫쪽 방향으로 공을 던집니다.
        t -= (3 * n)
        for i in range(1, n + 1):
            if 1 <= board[i][n + 1 - t] and board[i][n + 1 - t] <= 3:
                # 사람이 있는 첫 번째 지점을 찾습니다.
                # 찾게 되면 점수를 체크한 뒤 찾은 사람의 팀 번호를 저장합니다.
                get_point(i, n + 1 - t)
                return board_idx[i][n + 1 - t]

    # 공이 그대로 지나간다면 0을 반환합니다.
    return 0


# 공을 획득한 팀을 순서를 바꿉니다.
def reverse(got_ball_idx):
    # 아무도 공을 받지 못했으면 넘어갑니다.
    if got_ball_idx == 0: 
        return

    idx = got_ball_idx

    new_v = []

    # 순서를 맞춰 new_v에 레일을 넣어줍니다.
    for j in range(tail[idx] - 1, -1, -1):
        new_v.append(v[idx][j])

    for j in range(len(v[idx]) - 1, tail[idx] - 1, -1):
        new_v.append(v[idx][j])

    v[idx] = new_v[:]

    # 벡터에 저장한 정보를 바탕으로 보드의 표기 역시 바꿔줍니다.
    for j, (x, y) in enumerate(v[idx]):
        if j == 0:
            board[x][y] = 1
        elif j < tail[idx] - 1:
            board[x][y] = 2
        elif j == tail[idx] - 1:
            board[x][y] = 3
        else:
            board[x][y] = 4


# 입력을 받고 구현을 위한 기본적인 처리를 합니다.
init()
for i in range(1, k + 1):
# 각 팀을 머리사람을 따라 한칸씩 이동시킵니다.
    move_all()

    # i번째 라운드의 공을 던집니다. 공을 받은 사람을 찾아 점수를 추가합니다.
    got_ball_idx = throw_ball(i)

    # 공을 획득한 팀의 방향을 바꿉니다.
    reverse(got_ball_idx)

print(ans)
