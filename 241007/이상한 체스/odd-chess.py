from collections import deque


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >=m


def enque_locations(cx, cy, cd, queue, board):
    # cd 방향으로 직진했을 때 갈 수 있는 모든 위치 담는다, cx,cy 제외하고
    tmp_q = deque([[cx, cy]])
    while tmp_q:
        cx, cy = tmp_q.popleft()
        nx, ny = cx + dx[cd], cy + dy[cd]
        if out_of_range(nx, ny) or board[nx][ny] == 6:
            continue
        queue.append([nx, ny])
        tmp_q.append([nx, ny])


def set_visit_locations(queue, visit):
    for x, y in queue:
        visit[x][y] += 1

def unset_visit_locations(queue, visit):
    for x, y in queue:
        visit[x][y] -= 1


def count_unreachable_cells(visit):
    cnt = 0
    for i in range(n):
        for j in range(m):
            if visit[i][j] == 0:
                cnt += 1
    return cnt


def dfs(idx, max_depth, visit, my_horse_list, board):
    global ans
    if idx == max_depth:
        cnt = count_unreachable_cells(visit)
        
        ans = min(ans, cnt)

        return

    cx, cy = my_horse_list[idx]
    horse_dir_list = horse_dir_rule[board[cx][cy]]
    for i in range(4):
        queue = [[cx, cy]]
        for cd in horse_dir_list:
            turned_dir = (cd+i) % 4
            enque_locations(cx, cy, turned_dir, queue, board)
        set_visit_locations(queue, visit)
        dfs(idx+1, max_depth, visit, my_horse_list, board)
        unset_visit_locations(queue, visit)



n, m = map(int, input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

horse_dir_rule = [[], [0], [1, 3], [0, 1], [0, 1, 3], [0, 1, 2, 3]]
visit = [[0 for _ in range(m)]for __ in range(n)]
my_horse_list = []
board = []
ans = n * m

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(m):
        if 1 <= row[j] <= 5:
            my_horse_list.append([i, j])
        if row[j] == 6:
            visit[i][j] = -1
            ans -= 1
    board.append(row)

max_depth = len(my_horse_list)

if max_depth == 0:
    print(ans)
else:
    cx, cy = my_horse_list[0]
    horse_dir_list = horse_dir_rule[board[cx][cy]]
    for i in range(4):
        queue = [[cx, cy]]
        for cd in horse_dir_list:
            turned_dir = (cd+i) % 4
            enque_locations(cx, cy, turned_dir, queue, board)
        set_visit_locations(queue, visit)
        dfs(1, max_depth, visit, my_horse_list, board)
        unset_visit_locations(queue, visit)
    print(ans)