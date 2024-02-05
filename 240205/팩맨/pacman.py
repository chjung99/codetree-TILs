from collections import deque


def rotate45(self):
    self.direction = (self.direction + 1) % 8


def move(mon, next_step):
    x, y, d, alive, ttl = mon
    board[x][y] -= 1
    x, y = next_step

    board[x][y] += 1


def find_next_step(x, y, d):
    can_move = False
    nx, ny = x + dx[d], y + dy[d]
    if is_out_board(nx, ny) or is_dead_monster(nx, ny) or is_packman(nx, ny):
        d = (d + 1) % 8
        for _ in range(7):
            nx, ny = x + dx[d], y + dy[d]
            if not is_out_board(nx, ny) and not is_dead_monster(nx, ny) and not is_packman(nx, ny):
                can_move = True
                break
            d = (d + 1) % 8
    else:
        can_move = True
    if not can_move:
        return [x, y, d]
    else:
        return [nx, ny, d]


def is_out_board(nx, ny):
    return nx < 1 or nx > 4 or ny < 1 or ny > 4


def is_dead_monster(nx, ny):
    return ghost_board[nx][ny] > 0


def is_packman(nx, ny):
    return nx == px and ny == py


def make_monster_eggs():
    for x, y, d, alive, ttl in monsters:
        if alive:
            egg = [x, y, d, False, -1]
            eggs.append(egg)


def move_monsters():
    for i, (x, y, d, alive, ttl) in enumerate(monsters):
        if alive:
            nx, ny, nd = find_next_step(x, y, d)
            board[x][y] -= 1

            board[nx][ny] += 1
            monsters[i][0] = nx
            monsters[i][1] = ny
            monsters[i][2] = nd


def find_best_path(cx, cy):
    result = []  # [몬스터수, "123"]
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                cnt = 0

                i_dir = (i - 1) * 2
                j_dir = (j - 1) * 2
                k_dir = (k - 1) * 2

                nx, ny = cx + dx[i_dir], cy + dy[i_dir]
                eat = []
                if is_out_board(nx, ny):
                    continue
                else:
                    cnt += board[nx][ny]
                    eat.append([nx, ny])

                nx, ny = nx + dx[j_dir], ny + dy[j_dir]

                if is_out_board(nx, ny):
                    continue
                else:
                    if [nx, ny] not in eat:
                        cnt += board[nx][ny]
                        eat.append([nx, ny])

                nx, ny = nx + dx[k_dir], ny + dy[k_dir]

                if is_out_board(nx, ny):
                    continue
                else:
                    if [nx, ny] not in eat:
                        cnt += board[nx][ny]
                result.append([cnt, str(i) + str(j) + str(k)])

    result.sort(key=lambda x: (-x[0], x[1]))
    return result[0][-1]


def move_and_eat(path, cur_turn):  # path = "123"
    global px, py
    for str_dir in path:
        cur_dir = (int(str_dir) - 1) * 2

        px, py = px + dx[cur_dir], py + dy[cur_dir]

        for i, (x, y, d, alive, ttl) in enumerate(monsters):
            if alive:
                if [x, y] == [px, py]:
                    monsters[i][3] = False
                    monsters[i][4] = turn + 2
                    board[px][py] -= 1
                    ghost_board[px][py] += 1


def move_packman(x, y, turn):
    path = find_best_path(x, y)
    move_and_eat(path, turn)


def clear_dead_monsters(cur_turn):
    global monsters
    new_monsters = deque([])
    while monsters:
        mon = monsters.popleft()
        x, y, d, alive, ttl = mon
        if not alive and ttl == cur_turn:
            ghost_board[x][y] -= 1
            continue
        new_monsters.append(mon)
    monsters = new_monsters


def wake_monster_eggs():
    while eggs:
        egg = eggs.popleft()
        monster = [egg[0], egg[1], egg[2], True, -1]
        board[egg[0]][egg[1]] += 1
        monsters.append(monster)


def get_alive_monsters():
    cnt = 0
    for i in range(1, 5):
        for j in range(1, 5):
            cnt += board[i][j]
    return cnt


m, t = map(int, input().split())
px, py = map(int, input().split())  # 1,1 ~ 4,4
monsters = deque([])
eggs = deque([])
board = [[0 for _ in range(5)] for __ in range(5)]  # 1,1 ~ 4.4
ghost_board = [[0 for _ in range(5)] for __ in range(5)]  # 1,1 ~ 4.4
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

for _ in range(m):
    mx, my, md = map(int, input().split())
    monster = [mx, my, md - 1, True, -1]
    board[mx][my] += 1
    monsters.append(monster)

for turn in range(t):  # 25
    make_monster_eggs()  # 100 0000
    move_monsters()  # 7 * 100 0000 * 100 0000

    move_packman(px, py, turn)  # 1 * 100 0000 + 3 * 100 0000
    clear_dead_monsters(turn)  # 100 0000
    wake_monster_eggs()  # 100 0000
    # for mon in monsters:
    #     print(mon, end=" ")
    # print()

print(get_alive_monsters())