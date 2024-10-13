from copy import deepcopy
from collections import deque


class Knight:
    def __init__(self, x, y, h, w, k):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.k = k
        self.damage = 0
        self.points = [[i, j] for i in range(x, x + h) for j in range(y, y + w)]

    def move(self, d):
        self.x, self.y = self.x + dx[d], self.y + dy[d]
        for i in range(len(self.points)):
            self.points[i][0] = self.points[i][0] + dx[d]
            self.points[i][1] = self.points[i][1] + dy[d]

    def count_trap(self, board):
        cnt = 0
        for x, y in self.points:
            if board[x][y] == 1:
                cnt += 1
        return cnt


L, N, Q = map(int, input().split())
board = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
knight_list = []
ans = 0

for _ in range(L):
    board.append(list(map(int, input().split())))

for _ in range(N):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    knight_list.append(Knight(r, c, h, w, k))


def out_of_range(x, y):
    return x < 0 or x >= L or y < 0 or y >= L


def include_blocked(points):
    for x, y in points:
        if out_of_range(x, y) or board[x][y] == 2:
            return True
    return False


for _ in range(Q):
    i, d = map(int, input().split())
    i -= 1
    if knight_list[i].k <= 0:
        continue
    copy_knight_list = [row[:] for row in knight_list]
    knight = copy_knight_list[i]
    knight.move(d)
    is_blocked = False
    if include_blocked(knight.points):
        continue
    queue = deque([knight])
    moved_knight_list = {knight}
    while queue:
        if is_blocked:
            break
        cur_knight = queue.popleft()
        for x, y in cur_knight.points:
            for another_knight in copy_knight_list:
                if another_knight.k <= 0:
                    continue
                if cur_knight == another_knight:
                    continue
                if [x, y] in another_knight.points:
                    queue.append(another_knight)
                    another_knight.move(d)
                    moved_knight_list.add(another_knight)
                    if include_blocked(another_knight.points):
                        is_blocked = True
                        break

            if is_blocked:
                break
    if not is_blocked:
        for knight in moved_knight_list:
            if copy_knight_list[i] == knight:
                continue
            damage = knight.count_trap(board)
            knight.k -= damage
            knight.damage += damage
        knight_list = [row[:] for row in copy_knight_list]

for knight in knight_list:
    if knight.k > 0:
        ans += knight.damage
print(ans)

# 4 3 4
# 0 0 1 0
# 0 0 1 0
# 1 1 0 1
# 0 0 1 0
# 1 2 2 1 5
# 2 1 2 1 1
# 3 2 1 2 3
# 1 2
# 1 2
# 3 3
# 3 0