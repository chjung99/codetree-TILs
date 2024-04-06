from collections import deque
from math import floor

n, m, k = map(int, input().split())
offices = []
aircons = []
temp = [[0 for _ in range(n)] for __ in range(n)]
blocks = []
cur_time = 0
dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]

for i in range(n):
    board_line = list(map(int, input().split()))
    for j in range(n):
        if board_line[j] == 1:
            offices.append([i, j])
        elif board_line[j] > 1:
            aircons.append([i, j, board_line[j]])
for _ in range(m):
    x, y, s = map(int, input().split())
    blocks.append([x - 1, y - 1, s])


def check(offices, temp, k):
    for ox, oy in offices:
        if temp[ox][oy] < k:
            return False
    return True


def is_blocked(cx, cy, nd, blocks):
    if nd == 0:
        return [cx, cy, 1] in blocks
    elif nd == 1:
        return [cx, cy, 0] in blocks
    elif nd == 2:
        return [cx, cy + 1, 1] in blocks
    else:
        return [cx + 1, cy, 0] in blocks


def find_nexts(cx, cy, cd, visit, blocks):
    next_loc = []
    nd = cd - 2
    nx, ny = cx + dx[nd], cy + dy[nd]
    if 0 <= nx < n and 0 <= ny < n and not visit[nx][ny] and not is_blocked(cx, cy, nd, blocks):
        next_loc.append([nx, ny])

    nd = (cd - 2 + 1) % 4
    nx, ny = cx + dx[nd], cy + dy[nd]
    if 0 <= nx < n and 0 <= ny < n and not visit[nx][ny] and not is_blocked(cx, cy, nd, blocks):
        nd = cd - 2
        nx, ny = nx + dx[nd], ny + dy[nd]
        if 0 <= nx < n and 0 <= ny < n and not visit[nx][ny] and not is_blocked(cx, cy, nd, blocks):
            next_loc.append([nx, ny])

    nd = (cd - 2 + 3) % 4
    nx, ny = cx + dx[nd], cy + dy[nd]
    if 0 <= nx < n and 0 <= ny < n and not visit[nx][ny] and not is_blocked(cx, cy, nd, blocks):
        nd = cd - 2
        nx, ny = nx + dx[nd], ny + dy[nd]
        if 0 <= nx < n and 0 <= ny < n and not visit[nx][ny] and not is_blocked(cx, cy, nd, blocks):
            next_loc.append([nx, ny])

    return next_loc


def bfs(cx, cy, cd, blocks, temp):
    visit = [[0 for _ in range(n)] for __ in range(n)]
    queue = deque([[cx, cy, 5]])
    visit[cx][cy] = 1
    temp[cx][cy] += 5

    while queue:
        cx, cy, cz = queue.popleft()
        if cz >= 1:
            nexts = find_nexts(cx, cy, cd, visit, blocks)
            for nx, ny in nexts:
                visit[nx][ny] = 1
                queue.append([nx, ny, cz - 1])
                temp[nx][ny] += cz - 1


def run_aircon(aircons, blocks, temp):
    for ax, ay, ad in aircons:
        nx, ny = ax + dx[ad - 2], ay + dy[ad - 2]
        bfs(nx, ny, ad, blocks, temp)


def bfs2(cx, cy, temp, blocks):
    visit = [[0 for _ in range(n)] for __ in range(n)]
    visit[cx][cy] = 1
    queue = deque([[cx, cy]])
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n or visit[nx][ny]:
                continue
            if not is_blocked(cx, cy, i, blocks):
                visit[nx][ny] = 1
                queue.append([nx, ny])
                diff = abs(temp[cx][cy] - temp[nx][ny])
                if diff >= 4:
                    diff = int(floor(diff / 4))
                    if temp[cx][cy] > temp[nx][ny]:
                        temp[cx][cy] -= diff
                        temp[nx][ny] += diff
                    else:
                        temp[cx][cy] += diff
                        temp[nx][ny] -= diff


def mix_air(temp, blocks):
    # bfs2(0, 0, temp, blocks)
    temp2 = [[0 for _ in range(n)] for __ in range(n)]

    for i in range(n):
        for j in range(n):
            temp2[i][j] = temp[i][j]
    for i in range(n):
        for j in range(n):
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if nx < 0 or nx >= n or ny < 0 or ny >= n or is_blocked(i,j,d,blocks):
                    continue
                if temp[nx][ny] >= temp[i][j]:
                    continue
                diff = (temp[i][j] - temp[nx][ny]) //4
                temp2[i][j] -= diff
                temp2[nx][ny] += diff

    for i in range(n):
        for j in range(n):
            temp[i][j] = temp2[i][j]


def drop_edges(temp):
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or i == n - 1 or j == n - 1:
                if temp[i][j] > 0:
                    temp[i][j] -= 1


while True:
    if check(offices, temp, k):
        break
    if cur_time > 100:
        cur_time = -1
        break
    run_aircon(aircons, blocks, temp)
    mix_air(temp, blocks)
    drop_edges(temp)
    cur_time += 1
    # for i in range(n):
    #     for j in range(n):
    #         print(temp[i][j], end=" ")
    #     print("")
    # print("")
print(cur_time)