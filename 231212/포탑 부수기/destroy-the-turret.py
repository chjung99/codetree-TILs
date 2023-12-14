from collections import deque

N, M, K = map(int, input().split())
A = []
T = [[0 for i in range(M)] for j in range(N)]

dx = [0, 1, 0, -1, 1, 1, -1, -1]
dy = [1, 0, -1, 0, 1, -1, -1, 1]

for i in range(N):
    A.append(list(map(int, input().split())))

for i in range(K):

    attackers = []
    is_rel = [[0 for _ in range(M)] for __ in range(N)]
    cnt = 0
    for j in range(N):
        for k in range(M):
            if A[j][k] != 0:
                cnt += 1
                attackers.append([A[j][k], T[j][k], j + k, k, j])
    if cnt == 1:
        break
    vis = [[0 for _ in range(M)] for __ in range(N)]
    dist = [[0 for _ in range(M)] for __ in range(N)]

    # 1. 공격자 선정
    attacker = sorted(attackers, key=lambda x: (x[0], -x[1], -x[2], -x[3]))[0]

    ax = attacker[-1]
    ay = attacker[-2]
    A[ax][ay] += (N + M)
    T[ax][ay] = i+1
    is_rel[ax][ay] = 1
    # 2. 공격자의 공격

    # 2.1 target 선정
    target = sorted(attackers, key=lambda x: (-x[0], x[1], x[2], x[3]))[0]
    tx = target[-1]
    ty = target[-2]

    is_rel[tx][ty] = 1

    # 2.2 레이저 공격 시도
    # 최단 경로 있는 지 확인 dfs
    queue = deque([(ax, ay)])
    vis[ax][ay] = 1
    while queue:
        cx, cy = queue.popleft()

        for j in range(4):
            nx, ny = cx + dx[j], cy + dy[j]
            if nx < 0:
                nx = nx + N
            if nx >= N:
                nx = nx % N
            if ny < 0:
                ny = ny + M
            if ny >= M:
                ny = ny % M
            if vis[nx][ny] == 0 and A[nx][ny] > 0:
                dist[nx][ny] = dist[cx][cy] + 1
                queue.append((nx, ny))
                vis[nx][ny] = 1

    # 최단 경로 존재하면 경로 하나로 선택

    if vis[tx][ty] == 1:

        vis2 = [[0 for _ in range(M)] for __ in range(N)]
        cur = (ax, ay)
        dest = (tx, ty)

        queue2 = [cur]
        while cur != dest:

            flag = False
            for j in range(4):
                nx, ny = cur[0] + dx[j], cur[1] + dy[j]

                if nx < 0:
                    nx = nx + N
                if nx >= N:
                    nx = nx % N
                if ny < 0:
                    ny = ny + M
                if ny >= M:
                    ny = ny % M
                if vis2[nx][ny] == 0 and dist[nx][ny] == dist[cur[0]][cur[1]] + 1 and A[nx][ny] > 0:

                    queue2.append((nx, ny))
                    vis2[nx][ny] = 1
                    flag = True
                    break
            if not flag:
                queue2.pop()
            if len(queue2) > 0:
                cur = queue2[-1]
            else:
                break

        for k in queue2:
            if (k[0], k[1]) == (ax, ay):
                continue
            if k == dest:
                A[k[0]][k[1]] -= A[ax][ay]
            else:
                is_rel[k[0]][k[1]] = 1
                A[k[0]][k[1]] -= A[ax][ay] // 2
            if A[k[0]][k[1]] < 0:
                A[k[0]][k[1]] = 0

    else:
        # 2.3 포탄 공격 시도

        for j in range(8):
            nx, ny = tx + dx[j], ty + dy[j]

            if nx < 0:
                nx = nx + N
            if nx >= N:
                nx = nx % N
            if ny < 0:
                ny = ny + M
            if ny >= M:
                ny = ny % M
            if A[nx][ny] > 0 and (nx, ny) != (ax, ay):

                is_rel[nx][ny] = 1
                A[nx][ny] -= A[ax][ay] // 2
                if A[nx][ny] < 0:
                    A[nx][ny] = 0
        A[tx][ty] -= A[ax][ay]
        if A[tx][ty] < 0:
            A[tx][ty] = 0
    # 3. 포탑 부서짐
    for j in range(N):
        for k in range(M):
            if A[j][k] < 0:
                A[j][k] = 0
            if not is_rel[j][k] and A[j][k] > 0:
                A[j][k] += 1

# K 번의 턴 종료 후 가장 강한 포탄의 공격력
answer = 0
for i in range(N):
    answer = max(answer, max(A[i]))
print(answer)
