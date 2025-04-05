from collections import deque


def out_of_range(x, y):
    return x < 0 or x >= N or y < 0 or y >= N


def bfs(x, y, visit):
    dist = [[-1 for _ in range(N)] for __ in range(N)]
    visit[x][y] = 1
    dist[x][y] = 0
    queue = deque([[x, y]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if road[nx][ny] == 0:
                dist[nx][ny] = dist[cx][cy] + 1
                visit[nx][ny] = 1
                queue.append([nx, ny])
    return dist[ex][ey]


def check(sx, sy, ex, ey):
    visit = [[0 for _ in range(N)] for __ in range(N)]
    bfs(sx, sy, visit)
    return visit[ex][ey]


def move_medusa():

    cand = []
    for i in range(4):
        nx, ny = sx + dx[i], sy + dy[i]

        if not out_of_range(nx, ny) and road[nx][ny]==0:
            visit = [[0 for _ in range(N)]for __ in range(N)]
            nd = bfs(nx, ny, visit)
            cand.append([nd, i, nx, ny])
    cand.sort(key=lambda x: (x[0], x[1]))
    return cand[0][2:]


def catch_warriors(sx, sy, warriors):
    tmp = deque([])
    while warriors:
        x, y = warriors.popleft()
        if (x, y) != (sx, sy):
            tmp.append([x, y])
    while tmp:
        warriors.append(tmp.popleft())


def get_light_area(sx, sy, sd):
    light_area = [[0 for _ in range(N)]for __ in range(N)]
    nx, ny = sx + dx[sd], sy + dy[sd]
    cnt = 0
    if sd == 0:
        while not out_of_range(nx, ny):
            cnt += 1
            light_area[nx][ny] = 1
            for d in [2, 3]:
                for i in range(1, cnt+1):
                    nnx, nny = nx + i * dx[d], ny + i * dy[d]
                    if not out_of_range(nnx, nny):
                        light_area[nnx][nny] = 1
            nx, ny = nx + dx[sd], ny + dy[sd]

    if sd == 1:
        while not out_of_range(nx, ny):
            cnt += 1
            light_area[nx][ny] = 1
            for d in [2, 3]:
                for i in range(1, cnt + 1):
                    nnx, nny = nx + i * dx[d], ny + i * dy[d]
                    if not out_of_range(nnx, nny):
                        light_area[nnx][nny] = 1
            nx, ny = nx + dx[sd], ny + dy[sd]
    if sd == 2:
        while not out_of_range(nx, ny):
            cnt += 1
            light_area[nx][ny] = 1
            for d in [0, 1]:
                for i in range(1, cnt + 1):
                    nnx, nny = nx + i * dx[d], ny + i * dy[d]
                    if not out_of_range(nnx, nny):
                        light_area[nnx][nny] = 1
            nx, ny = nx + dx[sd], ny + dy[sd]
    if sd == 3:
        while not out_of_range(nx, ny):
            cnt += 1
            light_area[nx][ny] = 1
            for d in [0, 1]:
                for i in range(1, cnt + 1):
                    nnx, nny = nx + i * dx[d], ny + i * dy[d]
                    if not out_of_range(nnx, nny):
                        light_area[nnx][nny] = 1
            nx, ny = nx + dx[sd], ny + dy[sd]
    return light_area


def get_shadow_area(sx, sy, sd, warriors, light_area):
    shadow_area = [[0 for _ in range(N)]for __ in range(N)]
    for idx in range(len(warriors)):
        wx, wy = warriors[idx]
        if not light_area[wx][wy]:
            continue

        ddx = wx - sx
        ddy = wy - sy
        dirs = []
        if sd == 0 or sd == 1:

            if (ddy > 0):
                dirs = [3]
            if (ddy < 0):
                dirs = [2]
        else:
            if (ddx > 0):
                dirs = [1]
            if (ddx < 0):
                dirs = [0]

        nx, ny = wx + dx[sd], wy + dy[sd]
        cnt = 0
        while not out_of_range(nx, ny):
            cnt += 1
            shadow_area[nx][ny] = 1
            for d in dirs:

                for i in range(1, cnt+1):
                    nnx, nny = nx + i * dx[d], ny + i * dy[d]
                    # if not out_of_range(nnx, nny) and (abs(nx-sx)+abs(ny-sy))<(abs(nnx-sx)+abs(nny-sy)):
                    if not out_of_range(nnx, nny):
                            shadow_area[nnx][nny] = 1

            nx, ny = nx + dx[sd], ny + dy[sd]
    return shadow_area



def get_visible_warrior_cnt(light_area, shadow_area, warriors):
    cnt = 0
    for idx in range(len(warriors)):
        x, y = warriors[idx]
        if light_area[x][y] and not shadow_area[x][y]:
            cnt += 1
    return cnt


def find_dir(sx, sy, warriors):
    cand = []
    for i in range(4):
        light_area = get_light_area(sx, sy, i)
        shadow_area = get_shadow_area(sx, sy, i, warriors, light_area)
        warrior_cnt = get_visible_warrior_cnt(light_area, shadow_area, warriors)

        cand.append([warrior_cnt, i])
    cand.sort(key=lambda x:(-x[0],x[1]))
    return cand[0]


def move_warriors(sx, sy, warriors):
    total_dist = 0
    cnt = 0
    tmp = deque([])
    while warriors:
        x, y = warriors.popleft()
        if not light_area[x][y] or shadow_area[x][y]:
            cur_dist = abs(x-sx)+abs(y-sy)
            cand = []
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if out_of_range(nx, ny): continue
                if not light_area[nx][ny] or shadow_area[nx][ny]:
                    cand.append([abs(nx-sx)+abs(ny-sy), i])
            if len(cand) == 0:
                tmp.append([x, y])
                continue
            
            cand.sort(key=lambda q:(q[0],q[1]))
            
            nxt_dist, nd = cand[0]
            if nxt_dist<cur_dist:
                total_dist += 1
                nx, ny = x + dx[nd], y + dy[nd]
                if (nx, ny) == (sx, sy):
                    cnt += 1
                else:
                    x, y = nx, ny
                    cur_dist = abs(x - sx) + abs(y - sy)
                    cand = []
                    for i in range(4):
                        nx, ny = x + dx[i], y + dy[i]
                        if out_of_range(nx, ny): continue
                        if not light_area[nx][ny] or shadow_area[nx][ny]:
                            cand.append([abs(nx - sx) + abs(ny - sy), i])
                    if len(cand) == 0:
                        tmp.append([x, y])
                        continue
                    cand.sort(key=lambda q: (q[0], q[1]))
                    nxt_dist, nd = cand[0]
                    if nxt_dist < cur_dist:
                        total_dist += 1
                        nx, ny = x + dx[nd], y + dy[nd]
                        if (nx, ny) == (sx, sy):
                            cnt += 1
                        else:
                            tmp.append([nx, ny])
                    else:
                        tmp.append([x, y])
            else:
                tmp.append([x, y])
        else:
            tmp.append([x, y])

    while tmp:
        warriors.append(tmp.popleft())
    return total_dist, cnt

N, M = map(int, input().split())
sx, sy, ex, ey = map(int, input().split())
warriors = deque([])
light_area = [[0 for _ in range(N)] for __ in range(N)]
shadow_area = [[0 for _ in range(N)] for __ in range(N)]

road = []
tmp = list(map(int, input().split()))
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

for i in range(0, 2 * M, 2):
    warriors.append(tmp[i:i + 2])

for _ in range(N):
    road.append(list(map(int, input().split())))

if not check(sx, sy, ex, ey):
    print("-1")
else:
    while True:
        sx, sy = move_medusa()
        if (sx, sy) == (ex, ey):
            break
        catch_warriors(sx, sy, warriors)
        b, sd = find_dir(sx, sy, warriors)
        light_area = get_light_area(sx, sy, sd)
        shadow_area = get_shadow_area(sx, sy, sd, warriors, light_area)
        a, c = move_warriors(sx, sy, warriors)
        print(f"{a} {b} {c}")
    print("0")
