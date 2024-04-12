from collections import deque


def every_person_arrived(people):
    cnt = 0
    for i in range(1, m + 1):
        if people[i][-1] == 1:
            cnt += 1
    return cnt == m


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


def bfs(cx, cy, ex, ey, board, dist):
    queue = deque([[cx, cy]])
    dist[cx][cy] = 0
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            # if out_of_range(nx, ny) or board[nx][ny] == -1 or \
            #         dist[nx][ny] != -1:
            #     continue
            if out_of_range(nx, ny) or dist[nx][ny] != -1:
                continue
            # 도착 지점이 아니라면 지나갈 수 있는 칸 이어야 함
            if [nx, ny] != [ex, ey] and board[nx][ny] == -1:
                continue
            dist[nx][ny] = dist[cx][cy] + 1
            queue.append([nx, ny])


def find_next_step(px, py, sx, sy, board):
    dist_start = [[-1 for _ in range(n)] for __ in range(n)]
    dist_end = [[-1 for _ in range(n)] for __ in range(n)]
    bfs(px, py, sx, sy, board, dist_start)
    bfs(sx, sy, px, py, board, dist_end)
    nx, ny = -1, -1
    for i in range(4):
        nx, ny = px + dx[i], py + dy[i]
        if out_of_range(nx, ny):
            continue
        if dist_start[nx][ny] == dist_start[px][py] + 1 and \
                dist_end[nx][ny] + 1 == dist_end[px][py]:
            break
    return nx, ny


def move_person(p_num, people, nx, ny):
    # 다음 위치로 움직임
    people[p_num][0], people[p_num][1] = nx, ny


def move_inboard_person(people, store, board, blocked):
    for i in range(1, m + 1):
        px, py, is_arrived = people[i]
        # 격자 밖에 있거나 도착한 사람이라면 움직임 패스
        if [px, py] == [-1, -1] or is_arrived:
            continue

        sx, sy = store[i]
        nx, ny = find_next_step(px, py, sx, sy, board)
        move_person(i, people, nx, ny)
        # 도착 위치가 (편의점) 인 경우
        if people[i][:2] == [sx, sy]:
            # 도착 완료 처리
            people[i][-1] = 1
            # 못지나가게 처리하기 위한 block배열에 추가해둠(당장은 처리안함)
            blocked.append([sx, sy])

def find_nearest_base(sx, sy, board):
    cand = []
    dist = [[-1 for _ in range(n)] for __ in range(n)]
    bfs(sx, sy, sx, sy, board, dist)
    for i in range(n):
        for j in range(n):
            # 지나갈 수 없는 칸 이거나 베이스캠프가 아니면 패스
            if dist[i][j] == -1 or board[i][j] != 1:
                continue
            cand.append([dist[i][j], i, j])
    cand.sort(key=lambda x: (x[0], x[1], x[2]))
    return cand[0][1:3]


def set_person_in_base(people, store, board, t, blocked):
    if t <= m:
        sx, sy = store[t]
        bx, by = find_nearest_base(sx, sy, board)

        move_person(t, people, bx, by)

        # 도착 위치가 (3과정에서 베이스캠프) 인 경우
        blocked.append([bx, by])


n, m = map(int, input().split())
board = []
cur_time = 1
store = [[-1, -1]]  # x,y 1~ m
people = [[-1, -1, 0]]  # x, y, is_arrived 1~m
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
for _ in range(n):
    board.append(list(map(int, input().split())))
for _ in range(m):
    people.append([-1, -1, 0])
    x, y = map(int, input().split())
    store.append([x - 1, y - 1])


def block_board(blocked):
    # 도착한 편의점들을 못들어가게 -1 처리
    while blocked:
        bx, by = blocked.popleft()
        board[bx][by] = -1


while True:
    blocked = deque([])
    move_inboard_person(people, store, board, blocked)
    block_board(blocked)
    set_person_in_base(people, store, board, cur_time, blocked)
    block_board(blocked)
    if every_person_arrived(people):
        break
    cur_time += 1
print(cur_time)