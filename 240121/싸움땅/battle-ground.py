class Player:
    def __init__(self, idx, x, y, d, s):
        self.num = idx
        self.location = [x, y]
        self.dir = d
        self.ability = s
        self.gun = 0
        self.score = 0
    def get_reverse_dir(self):
        return (self.dir + 2) % 2

    def find_next_step(self):
        nx = self.location[0] + dx[self.dir]
        ny = self.location[1] + dy[self.dir]
        if nx < 1 or nx > n or ny < 1 or ny > n:
            self.dir = self.get_reverse_dir()
            nx = self.location[0] + dx[self.dir]
            ny = self.location[1] + dy[self.dir]
        return [nx, ny]

    def lose_player_find_next_step(self):
        self.dir = self.get_reverse_dir()
        nx = self.location[0] + dx[self.dir]
        ny = self.location[1] + dy[self.dir]
        next_step = [nx, ny]
        if nx < 1 or nx > n or ny < 1 or ny > n or isinstance(self.find_player(next_step, players), Player):
            for i in range(4):
                self.dir = (self.dir + 1) % 4
                nx = self.location[0] + dx[self.dir]
                ny = self.location[1] + dy[self.dir]
                next_step = [nx, ny]
                if nx < 1 or nx > n or ny < 1 or ny > n or isinstance(self.find_player(next_step, players), Player):
                    continue
                else:
                    break
        return next_step


    def move(self, next_step):
        self.location = next_step
    def get_gun(self):
        idx = -1
        max_value = self.gun
        try:
            for i, g in enumerate(board[self.location[0]][self.location[1]]):
                if g > max_value:
                    max_value = g
                    idx = i
            if idx != -1:
                board[self.location[0]][self.location[1]].pop(idx)
                self.gun = max_value
        except:
            import pdb;pdb.set_trace()



    def find_player(self, loc, players):
        for p in players:
            if p.num == self.num:
                continue
            if p.location == loc:
                return p
        return False
    def put_gun(self):
        board[self.location[0]][self.location[1]].extend([self.gun])
        self.gun = 0



def fight(player1, player2):
    power1 = player1.ability + player1.gun
    power2 = player2.ability + player2.gun

    diff = power1 - power2

    if diff > 0:
        win_player = player1
        lose_player = player2

    elif diff < 0:
        win_player = player2
        lose_player = player1

    else:
        if player1.ability > player2.ability:
            win_player = player1
            lose_player = player2
        else:
            win_player = player2
            lose_player = player1

    win_player.score += abs(diff)
    lose_player.put_gun()

    win_player.get_gun()

    lose_next_step = lose_player.lose_player_find_next_step()
    lose_player.move(lose_next_step)
    lose_player.get_gun()

n, m, k = map(int, input().split())
board = [[[] for _ in range(n + 1)] for __ in range(n + 1)]

players = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(1, n + 1):
    tmp = list(map(int, input().split()))
    for j in range(1, n + 1):
        board[i][j].append(tmp[j - 1])
for i in range(m):
    x, y, d, s = map(int, input().split())
    players.append(Player(i, x, y, d, s))

for i in range(k):
    for j in range(m):
        next_step = players[j].find_next_step()

        players[j].move(next_step)

        another_player = players[j].find_player(next_step, players)

        if isinstance(another_player, Player):
            fight(another_player, players[j])
        else:
            players[j].get_gun()

for p in players:
    print(p.score, end=" ")
class Player:
    def __init__(self, idx, x, y, d, s):
        self.num = idx
        self.location = [x, y]
        self.dir = d
        self.ability = s
        self.gun = 0
        self.score = 0
    def get_reverse_dir(self):
        return (self.dir + 2) % 4

    def find_next_step(self):
        nx = self.location[0] + dx[self.dir]
        ny = self.location[1] + dy[self.dir]
        if nx < 1 or nx > n or ny < 1 or ny > n:

            self.dir = self.get_reverse_dir()

            nx = self.location[0] + dx[self.dir]
            ny = self.location[1] + dy[self.dir]

        return [nx, ny]

    def lose_player_find_next_step(self):
        nx = self.location[0] + dx[self.dir]
        ny = self.location[1] + dy[self.dir]
        next_step = [nx, ny]
        if nx < 1 or nx > n or ny < 1 or ny > n or isinstance(self.find_player(next_step, players), Player):
            for i in range(4):
                self.dir = (self.dir + 1) % 4
                nx = self.location[0] + dx[self.dir]
                ny = self.location[1] + dy[self.dir]
                next_step = [nx, ny]
                if nx < 1 or nx > n or ny < 1 or ny > n or isinstance(self.find_player(next_step, players), Player):
                    continue
                else:
                    break
        return next_step


    def move(self, next_step):
        self.location = next_step
    def get_gun(self):
        idx = -1
        max_value = self.gun

        for i, g in enumerate(board[self.location[0]][self.location[1]]):
            if g > max_value:
                max_value = g
                idx = i
        if idx != -1:
            board[self.location[0]][self.location[1]].pop(idx)
            self.put_gun()
            # board[self.location[0]][self.location[1]].append(self.gun)
            self.gun = max_value




    def find_player(self, loc, players):
        for p in players:
            if p.num == self.num:
                continue
            if p.location == loc:
                return p
        return False
    def put_gun(self):
        if self.gun != 0:
            board[self.location[0]][self.location[1]].append(self.gun)
            self.gun = 0



def fight(player1, player2):
    power1 = player1.ability + player1.gun
    power2 = player2.ability + player2.gun

    diff = power1 - power2

    if diff > 0:
        win_player = player1
        lose_player = player2

    elif diff < 0:
        win_player = player2
        lose_player = player1

    else:
        if player1.ability > player2.ability:
            win_player = player1
            lose_player = player2
        else:
            win_player = player2
            lose_player = player1

    win_player.score += abs(diff)

    lose_player.put_gun()

    win_player.get_gun()

    lose_next_step = lose_player.lose_player_find_next_step()
    lose_player.move(lose_next_step)
    lose_player.get_gun()

n, m, k = map(int, input().split())
board = [[[] for _ in range(n + 1)] for __ in range(n + 1)]

players = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(1, n + 1):
    tmp = list(map(int, input().split()))
    for j in range(1, n + 1):
        if tmp[j-1] != 0:
            board[i][j].append(tmp[j - 1])
for i in range(m):
    x, y, d, s = map(int, input().split())
    players.append(Player(i, x, y, d, s))

for i in range(k):
    for j in range(m):
        next_step = players[j].find_next_step()
        # print(f"player = {j}, next = {next_step}")
        players[j].move(next_step)

        another_player = players[j].find_player(next_step, players)

        if isinstance(another_player, Player):
            fight(another_player, players[j])
        else:
            players[j].get_gun()
    # for k in players:
    #     print(k.num, k.location, k.gun)
    # print("=====")
    # for r in board:
    #     print(r[1:])


for p in players:
    print(p.score, end=" ")