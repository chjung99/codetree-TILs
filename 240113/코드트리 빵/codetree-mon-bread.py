from collections import deque
import heapq

n, m = map(int, input().split())
arr = []
tar = []
base_camp = []
cur_time = 0
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
arrive_cnt = 0
people = deque([])  # [cx, cy, tx, ty]
new_people = deque([])

for i in range(n):
    arr.append(list(map(int, input().split())))
for i in range(m):
    tx, ty = map(int, input().split())
    tar.append([tx - 1, ty - 1])


def find_base_camp(start):
    global arr
    dist = [[0 for i in range(n)] for j in range(n)]
    dist[start[0]][start[1]] = 1
    queue = deque([[start[0], start[1]]])
    cand = []
    while queue:
        cur = queue.popleft()
        for i in range(4):
            nx, ny = cur[0] + dx[i], cur[1] + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            if dist[nx][ny] == 0:
                dist[nx][ny] = dist[cur[0]][cur[1]] + 1
                queue.append([nx, ny])
                if arr[nx][ny] == 1:
                    cand.append([dist[nx][ny], nx, ny])
    cand.sort(key=lambda x: (x[0], x[1], x[2]))
    arr[cand[0][1]][cand[0][2]] = -1
    return cand[0][1:]


def move(nx, ny, tx, ty):
    global arrive_cnt, new_people
    if (nx, ny) == (tx, ty):
        arr[tx][ty] = -1
        arrive_cnt += 1
    else:
        new_people.append([nx, ny, tx, ty])


def find_shortest_path(person):
    dist = [[float("inf") for _ in range(n)] for __ in range(n)]
    prev = [[[] for _ in range(n)] for __ in range(n)]
    start = [person[0], person[1]]
    end = [person[2], person[3]]

    pq = []
    dist[start[0]][start[1]] = 0
    heapq.heappush(pq, [0, start[0], start[1]])

    while pq:
        cur_dist, cur_x, cur_y = heapq.heappop(pq)
        if cur_dist != dist[cur_x][cur_y]:
            continue
        for i in range(4):
            nx, ny = cur_x + dx[i], cur_y + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n or arr[nx][ny] == -1:
                continue
            if dist[nx][ny] > cur_dist + 1:
                dist[nx][ny] = cur_dist + 1
                heapq.heappush(pq,[dist[nx][ny], nx, ny])
                prev[nx][ny].extend([cur_x, cur_y])
    path = deque([])
    current = end
    while prev[current[0]][current[1]]:
        path.appendleft(current)
        current = prev[current[0]][current[1]]
    return path[0]


while arrive_cnt < m:
    if people:
        while people:
            cur_person = people.popleft()
            nx, ny = find_shortest_path(cur_person)
            move(nx, ny, cur_person[2], cur_person[3])
        while new_people:
            people.append(new_people.popleft())



    if cur_time < m:
        base_camp = find_base_camp(tar[cur_time])
        people.append([base_camp[0], base_camp[1], tar[cur_time][0], tar[cur_time][1]])
    cur_time += 1
    # arrive_cnt += 1


print(cur_time)