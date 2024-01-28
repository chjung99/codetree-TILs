class Player:
    def __init__(self, x: int, y: int, direction: int, is_runner: bool, runner_type: int):
        self.location = [x, y]
        self.direction = direction
        self.is_runner = is_runner
        self.runner_type = runner_type
        self.tagger_step = 1
        self.tagger_long_step = 0
        self.tagger_move_type = 0
        self.tagger_score = 0

    def calculate_distance_from_tagger(self):
        d = abs(self.location[0] - tagger.location[0]) + abs(self.location[1] - tagger.location[1])
        return d

    def find_next_step(self):
        nx = self.location[0] + dx[self.direction]
        ny = self.location[1] + dy[self.direction]
        return [nx, ny]

    def is_with_tagger(self):
        return self.location == tagger.location

    def get_reverse_direction(self):
        return (self.direction + 2) % 4

    def move(self, next_location):
        self.location = next_location

    def turn(self, next_direction):
        self.direction = next_direction

    def find_runners(self, turn):
        cand_locations = []
        for i in range(3):
            nx, ny = self.location[0] + dx[self.direction] * i, self.location[1] + dy[self.direction] * i
            cand_locations.append([nx, ny])
        for fx, fy in cand_locations:
            if board[fx][fy]:
                continue
            for runner in runners:
                if runner.location == [fx, fy]:
                    self.tagger_score += 1*turn
                    runners.remove(runner)


    def checkpoint_reached(self):
        return self.location == [1, 1] or self.location == [center, center]

    def move_and_turn_tagger(self):

        nx, ny = self.location[0] + dx[self.direction], self.location[1] + dy[self.direction]
        self.location = [nx, ny]
        self.tagger_step -= 1

        if self.checkpoint_reached():
            if self.location == [1, 1]:
                self.tagger_move_type = 1
                self.tagger_step = (self.tagger_long_step // 2)
            elif self.location == [center, center]:
                self.tagger_move_type = 0
                self.tagger_step = 1
                self.tagger_long_step = 0
            self.turn(self.get_reverse_direction())

        elif self.tagger_step == 0:

            next_dir = self.direction
            if self.tagger_move_type == 0:
                next_dir = (next_dir + 1) % 4
                self.tagger_long_step += 1
            else:
                next_dir = (next_dir - 1) % 4
                self.tagger_long_step -= 1
            self.turn(next_dir)
            self.tagger_step = (self.tagger_long_step // 2) + 1


n, m, h, k = map(int, input().split())
board = [[0 for _ in range(n + 1)] for __ in range(n + 1)]  # 1,1 ~ n,n
center = (n + 1) // 2
tagger = Player(center, center, 0, False, -1)
runners = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(m):
    x, y, d = map(int, input().split())  # d = runner_type
    direction = 1 if d == 1 else 2
    ptmp = Player(x, y, direction, True, d)
    runners.append(ptmp)
for i in range(h):
    x, y = map(int, input().split())
    board[x][y] = 1

for i in range(k):
    for j in range(len(runners)):
        if runners[j].calculate_distance_from_tagger() <= 3:
            next_step = runners[j].find_next_step()
            if 1 <= next_step[0] <= n and 1 <= next_step[1] <= n:
                if next_step != tagger.location:
                    runners[j].move(next_step)
            else:
                runners[j].direction = runners[j].get_reverse_direction()
                next_step = runners[j].find_next_step()
                if next_step != tagger.location:
                    runners[j].move(next_step)
    tagger.move_and_turn_tagger()
    tagger.find_runners(i+1)

print(tagger.tagger_score)