from collections import deque


class Monster:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num


n, m = map(int, input().split())
board = []
attack = []
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
answer = 0

monster_loc = []
visit = [[0 for _ in range(n)] for __ in range(n)]
monster_queue = deque([])
for _ in range(n):
    board.append(list(map(int, input().split())))
for _ in range(m):
    d, p = map(int, input().split())
    attack.append([d, p])

sx, sy = 0, 0
s_dir = 0
while True:
    if (sx, sy) == (n // 2, n // 2):
        break
    monster_loc.append([sx, sy])
    visit[sx][sy] = 1
    nx, ny = sx + dx[s_dir], sy + dy[s_dir]
    if nx < 0 or nx >= n or ny < 0 or ny >= n or visit[nx][ny]:
        s_dir = (s_dir + 1) % 4
        nx, ny = sx + dx[s_dir], sy + dy[s_dir]
    sx, sy = nx, ny

monster_loc.reverse()
for x, y in monster_loc:
    if board[x][y] == 0:
        break
    else:
        monster_queue.append(Monster(x, y, board[x][y]))


def get_attack_positions(cx, cy, d, p):
    attack_pos = []

    for i in range(1, p + 1):
        nx, ny = cx + dx[d] * i, cy + dy[d] * i
        attack_pos.append([nx, ny])
    return attack_pos


def attack_monsters(attack_pos, monster_queue):
    global answer
    flag = True
    tmp_queue = deque([])
    new_monster_queue = deque([])

    while monster_queue:
        cm = monster_queue.popleft()
        if [cm.x, cm.y] not in attack_pos:
            new_monster_queue.append(cm)
        else:
            answer += cm.num
    while flag:
        while new_monster_queue:
            cm = new_monster_queue.popleft()
            if not tmp_queue:
                tmp_queue.append(cm)
            else:
                if tmp_queue[-1].num == cm.num:
                    tmp_queue.append(cm)
                else:
                    if len(tmp_queue) < 4:
                        monster_queue += tmp_queue
                    else:
                        answer += tmp_queue[-1].num * len(tmp_queue)
                    tmp_queue.clear()
                    tmp_queue.append(cm)
        if tmp_queue:
            if len(tmp_queue) < 4:
                monster_queue += tmp_queue
            else:
                answer += tmp_queue[-1].num * len(tmp_queue)
            tmp_queue.clear()

        flag2 = 0
        for cm in monster_queue:
            if not tmp_queue:
                tmp_queue.append(cm)
            else:
                if tmp_queue[-1].num == cm.num:
                    tmp_queue.append(cm)
                else:
                    if len(tmp_queue) >= 4:
                        flag2 = 1
                        break
                    tmp_queue.clear()
                    tmp_queue.append(cm)
        if tmp_queue:
            if len(tmp_queue) >= 4:
                flag2 = 1
            tmp_queue.clear()
        if flag2 == 0:
            flag = False
        else:
            while monster_queue:
                new_monster_queue.append(monster_queue.popleft())

    for i, cm in enumerate(monster_queue):
        cm.x, cm.y = monster_loc[i][0], monster_loc[i][1]


def set_monsters(monster_queue):
    tmp_queue = deque([])
    new_monster_queue = deque([])
    while monster_queue:
        cm = monster_queue.popleft()
        if not tmp_queue:
            tmp_queue.append(cm)
        else:
            if tmp_queue[-1].num == cm.num:
                tmp_queue.append(cm)
            else:
                new_monster_queue.append(Monster(-1, -1, len(tmp_queue)))
                new_monster_queue.append(Monster(-1, -1, tmp_queue[-1].num))
                tmp_queue.clear()
                tmp_queue.append(cm)

    if tmp_queue:
        new_monster_queue.append(Monster(-1, -1, len(tmp_queue)))
        new_monster_queue.append(Monster(-1, -1, tmp_queue[-1].num))
        tmp_queue.clear()

    cnt = 0
    while new_monster_queue:
        cm = new_monster_queue.popleft()
        if cnt >= len(monster_loc):
            break
        cm.x, cm.y = monster_loc[cnt][0], monster_loc[cnt][1]
        monster_queue.append(cm)
        cnt += 1


for i in range(m):
    attack_pos = get_attack_positions(n // 2, n // 2, attack[i][0], attack[i][1])
    attack_monsters(attack_pos, monster_queue)
    set_monsters(monster_queue)

print(answer)