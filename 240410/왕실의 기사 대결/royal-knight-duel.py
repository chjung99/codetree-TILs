from collections import deque


def out_of_range(nx, ny):
    return nx < 0 or nx >= L or ny < 0 or ny >= L


def get_cluster(i, d, knights, knight_board):
    visit = [[0 for _ in range(L)] for __ in range(L)]
    cx, cy, ck = knights[i][0], knights[i][1], i
    visit[cx][cy] = 1
    cluster = [[cx, cy, ck]]
    cluster_knights = {i}
    queue = deque([[cx, cy, ck]])

    while queue:
        cx, cy, ck = queue.popleft()
        for r in range(4):
            nx, ny = cx + dx[r], cy + dy[r]
            if out_of_range(nx, ny) or visit[nx][ny] or knight_board[nx][ny] <= 0: continue
            if knight_board[nx][ny] == knight_board[cx][cy] or d == r:
                nk = knight_board[nx][ny]
                queue.append([nx, ny, nk])
                visit[nx][ny] = 1
                cluster_knights.add(nk)
                cluster.append([nx, ny, nk])
    return cluster_knights, cluster


def blocked(cluster, knight_board, d):
    for cx, cy, ck in cluster:
        nx, ny = cx + dx[d], cy + dy[d]
        if out_of_range(nx, ny) or knight_board[nx][ny] == -1:
            return True
    return False


def clear_knight(k_num, knights, new_board):
    cx, cy, ch, cw = knights[k_num][:4]
    for i in range(ch):
        for j in range(cw):
            new_board[cx + i][cy + j] = 0


def command_knight(i, d, knight_board, trap_board, knights):
    cluster_knights, cluster = get_cluster(i, d, knights, knight_board)
    if blocked(cluster, knight_board, d): return
    new_board = [[0 for _ in range(L)] for __ in range(L)]
    # 벽 복사
    for p in range(L):
        for q in range(L):
            if knight_board[p][q] == -1:
                new_board[p][q] = -1

    # knights 기준점 업데이트
    for k_num in cluster_knights:
        knights[k_num][0] += dx[d]
        knights[k_num][1] += dy[d]
        # if knights[k_num][4] < 0:
        #     clear_knight(k_num, knights, knight_board)

    # 업데이트된 knights 보드 세팅
    for k_num in range(1, N + 1):
        if knights[k_num][-2] <= 0: continue
        px, py, ph, pw, pk, pd = knights[k_num]
        # 보드 세팅과 동시에 함정 개수 세기
        cnt = 0
        for p in range(ph):
            for q in range(pw):
                new_board[px + p][py + q] = k_num
                if trap_board[px + p][py + q] == 1:
                    cnt += 1
        # 명령을 받은 기사는 데미지를 입지 않음
        if k_num == i or k_num not in cluster_knights: continue
        # 나머지 기사는 데미지를 입음, 체력이 0이하인 경우 보드에서 제거
        knights[k_num][4] -= cnt  # 체력 감소
        knights[k_num][5] += cnt  # 누적 데미지 증가
        if knights[k_num][4] <= 0:
            clear_knight(k_num, knights, new_board)

    # 보드 업데이트
    for p in range(L):
        for q in range(L):
            knight_board[p][q] = new_board[p][q]


def alive_knights_damage(knights):
    answer = 0
    for i in range(1, N + 1):
        k, d = knights[i][-2:]
        if k > 0:
            answer += d
    return answer


dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
L, N, Q = map(int, input().split())
knight_board = [[0 for _ in range(L)] for __ in range(L)]  # 벽 -1, 빈공간 0, 나머지 기사들
trap_board = []  # 1 트랩 0 빈공간 2 벽
knights = [[]]  # 1 ~ N,[r,c,h,w,k,damage]

for i in range(L):
    tmp = list(map(int, input().split()))
    for j in range(L):
        if tmp[j] == 2:
            knight_board[i][j] = -1
    trap_board.append(tmp)

for knight_num in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knights.append([r - 1, c - 1, h, w, k, 0])
    for i in range(h):
        for j in range(w):
            knight_board[i + r - 1][j + c - 1] = knight_num

for _ in range(Q):
    i, d = map(int, input().split())
    if knights[i][-2] > 0:
        command_knight(i, d, knight_board, trap_board, knights)

print(alive_knights_damage(knights))