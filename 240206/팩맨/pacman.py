from collections import deque
from copy import deepcopy

m, t = map(int, input().split())
px, py = map(int, input().split())

monsters = [[[0 for _ in range(8)] for __ in range(5)] for ___ in range(5)]
dead_monsters = [[0 for __ in range(5)] for ___ in range(5)]
ttl_monsters = deque([])
eggs = [[[0 for _ in range(8)] for __ in range(5)] for ___ in range(5)]
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

for _ in range(m):
    x, y, d = map(int, input().split())
    monsters[x][y][d - 1] += 1


def get_alive_monsters():
    cnt = 0
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(8):
                cnt += monsters[i][j][k]
    return cnt


def make_eggs():
    global eggs
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(8):
                eggs[i][j][k] = monsters[i][j][k]


def wake_eggs():
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(8):
                monsters[i][j][k] += eggs[i][j][k]


def is_out_board(nx, ny):
    return nx < 1 or nx > 4 or ny < 1 or ny > 4


def is_packman(nx, ny):
    return px == nx and py == ny


def is_dead_monster(nx, ny):
    return dead_monsters[nx][ny] > 0


def find_next_step(cx, cy, cd):
    nx, ny, nd = cx + dx[cd], cy + dy[cd], cd
    cnt = 7
    while cnt:
        if not is_out_board(nx, ny) and not is_packman(nx, ny) and not is_dead_monster(nx, ny):
            return nx, ny, nd
        nd = (nd + 1) % 8
        nx, ny, nd = cx + dx[nd], cy + dy[nd], nd
        cnt -= 1
    return cx, cy, cd


def move_monsters():
    global monsters
    tmp_monsters = deepcopy(monsters)
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(8):
                cnt = monsters[i][j][k]
                if cnt > 0:
                    nx, ny, nd = find_next_step(i, j, k)
                    tmp_monsters[i][j][k] -= cnt
                    tmp_monsters[nx][ny][nd] += cnt
    monsters = tmp_monsters


def find_next_path(cx, cy):
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
                    cnt += sum(monsters[nx][ny])
                    eat.append([nx, ny])

                nx, ny = nx + dx[j_dir], ny + dy[j_dir]

                if is_out_board(nx, ny):
                    continue
                else:
                    if [nx, ny] not in eat:
                        cnt += sum(monsters[nx][ny])
                        eat.append([nx, ny])

                nx, ny = nx + dx[k_dir], ny + dy[k_dir]

                if is_out_board(nx, ny):
                    continue
                else:
                    if [nx, ny] not in eat:
                        cnt += sum(monsters[nx][ny])
                result.append([cnt, str(i) + str(j) + str(k)])

    result.sort(key=lambda x: (-x[0], x[1]))
    return result[0][-1]


def move_and_eat(next_path, cur_turn):
    global px, py
    for str_dir in next_path:
        cur_dir = (int(str_dir) - 1) * 2

        px, py = px + dx[cur_dir], py + dy[cur_dir]
        # 몬스터 잡기
        num_of_deads = sum(monsters[px][py])
        dead_monsters[px][py] += num_of_deads
        ttl_monsters.append([cur_turn + 2, px, py, num_of_deads])
        for k in range(8):
            monsters[px][py][k] = 0


def move_packman(cur_turn):
    next_path = find_next_path(px, py)
    # print(px, py, next_path)
    move_and_eat(next_path, cur_turn)


def clear_dead_monsters(cur_turn):
    head = ttl_monsters.popleft()
    while head[0] == cur_turn:
        cx, cy, num_of_deads = head[1:]
        dead_monsters[cx][cy] -= num_of_deads
        head = ttl_monsters.popleft()
    if head[0] != cur_turn:
        ttl_monsters.appendleft(head)


for turn in range(1, t + 1):
    make_eggs()
    # for i in range(1, 5):
    #     for j in range(1, 5):
    #         print(sum(monsters[i][j]), end=" ")
    #     print()
    move_monsters()
    # print("===move===")
    # for i in range(1, 5):
    #     for j in range(1, 5):
    #         print(sum(monsters[i][j]), end=" ")
    #     print()
    # print()
    move_packman(turn)
    clear_dead_monsters(turn)
    wake_eggs()

print(get_alive_monsters())
'''
5 5
4 2
1 1 6
3 1 6
2 2 7
1 2 5
2 3 6

'''