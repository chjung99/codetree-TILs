from collections import deque


def choice_attacker(board, tower_history):
    # 공격력이 1이상인 타워 중 공격력이 가장 약한 타워를 선정합니다
    cand = []  # [공격력, 공격턴, 행, 열]
    # 정렬 기준 x[0], -x[1], -(x[2]+x[3]), -x[3] (공격력 -, 공격턴 +, 행+열 +, 열 +)
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0:
                continue

            cand.append([board[i][j], tower_history[i][j], i, j])

    cand.sort(key=lambda x: (x[0], -x[1], -(x[2] + x[3]), -x[3]))
    return cand[0][2], cand[0][3]


def increase_tower_ability(x, y, board, score):
    board[x][y] += score


def decrease_tower_ability(x, y, board, score):
    board[x][y] -= score


def choice_target(ax, ay, board, tower_history):
    # 공격력이 1이상인 타워 중 공격력이 가장 강한 타워를 선정합니다
    cand = []  # [공격력, 공격턴, 행, 열]
    # 정렬 기준 -x[0], x[1], x[2]+x[3], x[3] (공격력 +, 공격턴 -, 행+열 -, 열 -)
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0 or [i, j] == [ax, ay]:
                continue
            cand.append([board[i][j], tower_history[i][j], i, j])
    cand.sort(key=lambda x: (-x[0], x[1], x[2] + x[3], x[3]))
    return cand[0][2], cand[0][3]


def bfs(sx, sy, board, dist):
    dist[sx][sy] = 0
    queue = deque([[sx, sy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = (cx + dx[i]) % N, (cy + dy[i]) % M
            if board[nx][ny] <= 0:
                continue
            if dist[nx][ny] == -1:
                dist[nx][ny] = dist[cx][cy] + 1
                queue.append([nx, ny])
            else:
                dist[nx][ny] = min(dist[nx][ny], dist[cx][cy] + 1)


def find_shortest_path(sx, sy, ex, ey, dist_start, dist_end, board, shortest_path):
    shortest_path.append([sx, sy])
    queue = deque([[sx, sy]])
    visit = [[0 for _ in range(M)] for __ in range(N)]
    visit[sx][sy] = 1
    while queue:
        cx, cy = queue.popleft()
        if [cx, cy] == [ex, ey]:
            break
        for i in range(4):
            nx, ny = (cx + dx[i]) % N, (cy + dy[i]) % M
            if dist_start[nx][ny] == -1 or dist_end[nx][ny] == -1 or visit[nx][ny]:
                continue
            if dist_start[nx][ny] == dist_start[cx][cy] + 1 and \
                    dist_end[nx][ny] + 1 == dist_end[cx][cy]:
                visit[nx][ny] = 1
                queue.append([nx, ny])
                shortest_path.append([nx, ny])
                break


def do_laser_attack(ax, ay, tx, ty, board, shortest_path, score, half_score, attack_and_targets):
    for x, y in shortest_path:
        attack_and_targets.append([x, y])
        if [x, y] == [ax, ay]:
            continue
        elif [x, y] == [tx, ty]:
            decrease_tower_ability(x, y, board, score)
            # board[x][y] -= score
        else:
            decrease_tower_ability(x, y, board, half_score)
            # board[x][y] -= half_score


def available_laser_attack(ax, ay, tx, ty, board, attack_and_targets):
    dist_start = [[-1 for _ in range(M)] for __ in range(N)]
    dist_end = [[-1 for _ in range(M)] for __ in range(N)]
    shortest_path = deque([])
    score = board[ax][ay]
    half_score = score // 2

    bfs(ax, ay, board, dist_start)
    bfs(tx, ty, board, dist_end)

    if dist_start[tx][ty] == -1:
        return False
    find_shortest_path(ax, ay, tx, ty, dist_start, dist_end, board, shortest_path)
    do_laser_attack(ax, ay, tx, ty, board, shortest_path, score, half_score, attack_and_targets)

    return True


def do_potan_attack(ax, ay, tx, ty, board, attack_and_targets):
    score = board[ax][ay]
    half_score = score // 2

    # 공격자 추가
    attack_and_targets.append([ax, ay])
    # 공격 대상 추가
    attack_and_targets.append([tx, ty])
    decrease_tower_ability(tx, ty, board, score)
    # 주변 대상 추가, 단 공격자 중복 시 제거
    for i in range(8):
        nx, ny = (tx + dx[i]) % N, (ty + dy[i]) % M
        if [nx, ny] == [ax, ay]:
            continue
        elif board[nx][ny] <= 0:
            continue
        else:
            attack_and_targets.append([nx, ny])
            decrease_tower_ability(nx, ny, board, half_score)


def attack_target(ax, ay, tx, ty, board, attack_and_targets):
    if not available_laser_attack(ax, ay, tx, ty, board, attack_and_targets):
        do_potan_attack(ax, ay, tx, ty, board, attack_and_targets)


def repair_towers(board, attack_and_targets):
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0 or [i, j] in attack_and_targets:
                continue
            board[i][j] += 1


def count_unbroken_tower(board):
    cnt = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0:
                cnt += 1
    return cnt


def strogest_tower(board):
    max_value = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] > max_value:
                max_value = board[i][j]
    return max_value


N, M, K = map(int, input().split())
board = []  # NxM임을 주의하자
tower_history = [[0 for _ in range(M)] for __ in range(N)]
dx = [0, 1, 0, -1, 1, 1, -1, -1]
dy = [1, 0, -1, 0, 1, -1, 1, -1]

for _ in range(N):
    board.append(list(map(int, input().split())))

for turn in range(1, K + 1):
    attack_and_targets = []

    ax, ay = choice_attacker(board, tower_history)

    tx, ty = choice_target(ax, ay, board, tower_history)

    increase_tower_ability(ax, ay, board, N + M)

    attack_target(ax, ay, tx, ty, board, attack_and_targets)

    tower_history[ax][ay] = turn

    repair_towers(board, attack_and_targets)

    if count_unbroken_tower(board) == 1:
        break

print(strogest_tower(board))
"""
3 3 3
0 1 0
0 2 0
0 3 0
"""