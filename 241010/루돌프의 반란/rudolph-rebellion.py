class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_dir = -1

    def set_move_dir(self, move_dir):
        self.move_dir = move_dir

    def move(self, cnt):
        self.x = self.x + cnt * dx[self.move_dir]
        self.y = self.y + cnt * dy[self.move_dir]


class Santa(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score = 0
        self.sturn = 0

    def set_sturn(self, sturn):
        self.sturn = sturn

    def add_score(self, score):
        self.score += score


class Rudolf(Player):
    def __init__(self, x, y):
        super().__init__(x, y)


def get_valid_santa_num(santa_list):
    cnt = 0
    for i in range(1, P + 1):
        if not out_of_range(santa_list[i].x, santa_list[i].y):
            cnt += 1
    return cnt


def get_rudolf_dir(rudolf, santa_list):
    cand = []  # 거리, sx, sy
    for santa in santa_list:
        if out_of_range(santa.x, santa.y):
            continue
        dist = (rudolf.x - santa.x) ** 2 + (rudolf.y - santa.y) ** 2
        cand.append([dist, santa.x, santa.y])
    cand.sort(key=lambda x: (x[0], -x[1], -x[2]))
    _, sx, sy = cand[0]
    move_dir = -1
    min_dist = -1
    for i in range(8):
        nx, ny = rudolf.x + dx[i], rudolf.y + dy[i]
        dist = (nx - sx) ** 2 + (ny - sy) ** 2
        if move_dir == -1:
            min_dist = dist
            move_dir = i
        elif min_dist > dist:
            min_dist = dist
            move_dir = i
    return move_dir


def check_another_santa_here(x, y, cur_santa, santa_list):
    for santa in santa_list:
        if not out_of_range(x, y) and santa != cur_santa and (santa.x, santa.y) == (x, y):
            return True
    return False


def get_another_santa_here(x, y, cur_santa, santa_list):
    for santa in santa_list:
        if santa != cur_santa and (santa.x, santa.y) == (x, y):
            return santa
    return None


def out_of_range(x, y):
    return x < 0 or x >= N or y < 0 or y >= N


def get_santa_dir(santa, rudolf, santa_list):
    cur_dist = (santa.x - rudolf.x) ** 2 + (santa.y - rudolf.y) ** 2
    cand = []  # dist, dir
    for i in range(4):
        d = i * 2  # 상우하좌
        nx, ny = santa.x + dx[d], santa.y + dy[d]
        if out_of_range(nx, ny) or check_another_santa_here(nx, ny, santa, santa_list):
            continue
        dist = (nx - rudolf.x) ** 2 + (ny - rudolf.y) ** 2
        cand.append([dist, d])
    cand.sort(key=lambda x: (x[0], x[1]))
    if len(cand) > 0:
        final_dist, final_dir = cand[0]
        if final_dist >= cur_dist:
            return -1
        else:
            return final_dir
    else:
        return -1


N, M, P, C, D = map(int, input().split())
rx, ry = map(int, input().split())
rx -= 1
ry -= 1
rudolf = Rudolf(rx, ry)
santa_list = [Santa(-1, -1) for _ in range(P + 1)]
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

for _ in range(P):
    pn, sx, sy = map(int, input().split())
    sx -= 1
    sy -= 1
    santa_list[pn] = Santa(sx, sy)


for turn in range(1, M + 1):
    valid_santa_num = get_valid_santa_num(santa_list)
    if valid_santa_num == 0:
        break
    move_dir = get_rudolf_dir(rudolf, santa_list)
    rudolf.set_move_dir(move_dir)
    rudolf.move(1)
    if check_another_santa_here(rudolf.x, rudolf.y, rudolf, santa_list):
        santa = get_another_santa_here(rudolf.x, rudolf.y, rudolf, santa_list)
        santa.set_sturn(turn + 1)
        santa.add_score(C)
        santa.set_move_dir(rudolf.move_dir)
        santa.move(C)
        while check_another_santa_here(santa.x, santa.y, santa, santa_list):
            new_santa = get_another_santa_here(santa.x, santa.y, santa, santa_list)
            new_santa.set_move_dir(santa.move_dir)
            new_santa.move(1)
            santa = new_santa
            if out_of_range(santa.x, santa.y):
                break

    for i in range(1, P + 1):
        santa = santa_list[i]
        if santa.sturn >= turn or out_of_range(santa.x, santa.y):
            continue
        move_dir = get_santa_dir(santa, rudolf, santa_list)
        if move_dir == -1:
            continue
        santa.set_move_dir(move_dir)
        santa.move(1)

        if (santa.x, santa.y) == (rudolf.x, rudolf.y):
            santa.set_sturn(turn + 1)
            reverse_move_dir = (santa.move_dir + 4) % 8
            santa.add_score(D)
            santa.set_move_dir(reverse_move_dir)
            santa.move(D)

            while check_another_santa_here(santa.x, santa.y, santa, santa_list):
                new_santa = get_another_santa_here(santa.x, santa.y, santa, santa_list)
                new_santa.set_move_dir(santa.move_dir)
                new_santa.move(1)
                santa = new_santa
                if out_of_range(santa.x, santa.y):
                    break

    for i in range(1, P + 1):
        if not out_of_range(santa_list[i].x, santa_list[i].y):
            santa_list[i].add_score(1)
for i in range(1, P + 1):
    print(santa_list[i].score, end=" ")