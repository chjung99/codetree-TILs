class Gun:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.power = power


class Player:
    def __init__(self, x, y, d, s):
        self.x = x
        self.y = y
        self.d = d
        self.s = s
        self.point = 0
        self.gun = None

    def put_gun(self):
        self.gun = None

    def get_gun(self, gun_list):
        max_power = -1
        max_gun = None
        for gun in gun_list:
            if (gun.x, gun.y) != (self.x, self.y):
                continue
            if max_gun is None:
                max_gun = gun
                max_power = gun.power
            if gun.power > max_power:
                max_power = gun.power
                max_gun = gun
        self.gun = max_gun

    def move_to(self, nx, ny):
        self.x, self.y = nx, ny
        if self.gun:
            self.gun.x = nx
            self.gun.y = ny

    def rotate_dir(self):
        self.d = (self.d + 1) % 4

    def add_point(self, diff):
        self.point += diff


def find_player_next_step(player):
    nx, ny = player.x + dx[player.d], player.y + dy[player.d]
    if out_of_range(nx, ny):
        player.rotate_dir()
        player.rotate_dir()
        nx, ny = player.x + dx[player.d], player.y + dy[player.d]
    return nx, ny


def find_lose_player_next_step(player):
    nx, ny = player.x + dx[player.d], player.y + dy[player.d]
    if out_of_range(nx, ny):
        player.rotate_dir()
        nx, ny = player.x + dx[player.d], player.y + dy[player.d]
    return nx, ny


def check_another_player_here(nx, ny, player, player_list):
    for another_player in player_list:
        if another_player == player:
            continue
        if (another_player.x, another_player.y) == (nx, ny):
            return True
    return False


def get_another_player_here(nx, ny, player, player_list):
    for another_player in player_list:
        if another_player == player:
            continue
        if (another_player.x, another_player.y) == (nx, ny):
            return another_player


def fight_players(player, another_player):
    player_score = player.s
    if player.gun:
        player_score += player.gun.power
    another_player_score = another_player.s
    if another_player.gun:
        another_player_score += another_player.gun.power
    raw_diff = player_score - another_player_score
    if raw_diff > 0:
        return player, another_player, abs(raw_diff)
    elif raw_diff < 0:
        return another_player, player, abs(raw_diff)
    else:
        if player.s > another_player.s:
            return player, another_player, abs(raw_diff)
        else:
            return another_player, player, abs(raw_diff)


def out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= n


n, m, k = map(int, input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
gun_list = []
player_list = []
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if row[j] > 0:
            gun_list.append(Gun(i, j, row[j]))

for i in range(m):
    x, y, d, s = map(int, input().split())
    x -= 1
    y -= 1
    player_list.append(Player(x, y, d, s))

for _ in range(k):
    for player in player_list:
        nx, ny = find_player_next_step(player)
        player.move_to(nx, ny)
        if check_another_player_here(nx, ny, player, player_list):
            another_player = get_another_player_here(nx, ny, player, player_list)
            win_player, lose_player, diff = fight_players(player, another_player)
            win_player.add_point(diff)
            lose_player.put_gun()
            nx, ny = find_lose_player_next_step(lose_player)
            while out_of_range(nx, ny) or check_another_player_here(nx, ny, lose_player, player_list):
                lose_player.rotate_dir()
                nx, ny = find_lose_player_next_step(lose_player)
            lose_player.move_to(nx, ny)
            lose_player.get_gun(gun_list)

            win_player.put_gun()
            win_player.get_gun(gun_list)
        else:
            player.put_gun()
            player.get_gun(gun_list)
for player in player_list:
    print(player.point, end=" ")