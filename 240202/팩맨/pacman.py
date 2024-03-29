from collections import deque




class Monster:
    def __init__(self, x, y, d, alive, ttl):
        self.location = [x, y]
        self.direction = d
        self.alive = alive
        self.ttl = ttl

    def rotate45(self):
        self.direction = (self.direction + 1) % 8

    def move(self, next_step):
        # board에서도 변경
        for mon in board[self.location[0]][self.location[1]][:]:
            if mon == self:
                board[self.location[0]][self.location[1]].remove(mon)

        self.location = next_step

        # board에서도 변경
        board[self.location[0]][self.location[1]].append(self)

    def find_next_step(self):
        can_move = False
        nx, ny = self.location[0] + dx[self.direction], self.location[1] + dy[self.direction]
        if is_out_board(nx, ny) or is_dead_monster(nx, ny) or is_packman(nx, ny):
            self.rotate45()
            for _ in range(7):
                nx, ny = self.location[0] + dx[self.direction], self.location[1] + dy[self.direction]
                if not is_out_board(nx, ny) and not is_dead_monster(nx, ny) and not is_packman(nx, ny):
                    can_move = True
                    break
                self.rotate45()
        else:
            can_move = True
        if not can_move:
            return self.location
        else:
            return [nx, ny]


def is_out_board(nx, ny):
    return nx < 1 or nx > 4 or ny < 1 or ny > 4


def is_dead_monster(nx, ny):
    for mon in board[nx][ny]:
        if not mon.alive:
            return True
    return False

def is_packman(nx, ny):
    return nx == px and ny == py

def make_monster_eggs():
    global eggs

    for mon in monsters:
        if mon.alive:
            egg = Monster(mon.location[0], mon.location[1], mon.direction, False, -1)
            eggs.append(egg)


def move_monsters():
    global monsters

    for mon in monsters:
        if mon.alive:
            next_step = mon.find_next_step()
            mon.move(next_step)


def find_best_path(cx, cy):
    result = []  # [몬스터수, "123"]
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                cnt = 0
                visit = []
                i_dir = (i - 1) * 2
                j_dir = (j - 1) * 2
                k_dir = (k - 1) * 2

                nx, ny = cx + dx[i_dir], cy + dy[i_dir]
                visit.append([nx, ny])
                if is_out_board(nx, ny):
                    continue
                else:
                    for mon in board[nx][ny]:
                        if mon.alive:
                            cnt += 1

                nx, ny = nx + dx[j_dir], ny + dy[j_dir]

                if is_out_board(nx, ny) or [nx, ny] in visit:
                    continue
                else:
                    visit.append([nx, ny])
                    for mon in board[nx][ny]:
                        if mon.alive:
                            cnt += 1

                nx, ny = nx + dx[k_dir], ny + dy[k_dir]

                if is_out_board(nx, ny) or [nx, ny] in visit:
                    continue
                else:
                    for mon in board[nx][ny]:
                        if mon.alive:
                            cnt += 1
                result.append([cnt, str(i) + str(j) + str(k)])

    result.sort(key=lambda x: (-x[0], x[1]))
    return result[0][-1]


def move_and_eat(path, cur_turn):  # path = "123"
    global px, py, monsters, board
    for str_dir in path:
        cur_dir = (int(str_dir) - 1) * 2

        px, py = px + dx[cur_dir], py + dy[cur_dir]
        # 몬스터 잡기
        # monsters에서 적용
        for mon in monsters:
            if mon.alive:
                if mon.location == [px, py]:
                    mon.alive = False
                    mon.ttl = turn + 2
        # board에서 적용
        for mon in board[px][py]:
            if mon.alive:
                mon.alive = False
                mon.ttl = turn + 2



def move_packman(x, y, turn):
    path = find_best_path(x, y)
    move_and_eat(path, turn)


def clear_dead_monsters(cur_turn):
    for mon in monsters[:]:
        if not mon.alive and mon.ttl == cur_turn:
            # board에서 제거
            board[mon.location[0]][mon.location[1]].remove(mon)

            monsters.remove(mon)


def wake_monster_eggs():
    global eggs, monsters

    while eggs:
        egg = eggs.popleft()
        monster = Monster(egg.location[0], egg.location[1], egg.direction, True, -1)
        board[egg.location[0]][egg.location[1]].append(monster)
        monsters.append(monster)


def get_alive_monsters():
    global monsters
    cnt = 0
    for mon in monsters:
        if mon.alive:
            cnt += 1
    return cnt


m, t = map(int, input().split())
px, py = map(int, input().split())  # 1,1 ~ 4,4
monsters = []
eggs = deque([])
board = [[[] for _ in range(5)] for __ in range(5)]  # 1,1 ~ 4.4
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

for _ in range(m):
    mx, my, md = map(int, input().split())
    monster = Monster(mx, my, md - 1, True, -1)
    board[mx][my].append(monster)
    monsters.append(monster)

for turn in range(t):
    make_monster_eggs()
    move_monsters()

    move_packman(px, py, turn)
    clear_dead_monsters(turn)
    wake_monster_eggs()

print(get_alive_monsters())


'''
4 1
3 1
1 3 5
2 2 7
3 4 6
4 2 2

4 2
3 1
1 3 5
2 2 7
3 4 6
4 2 2

'''