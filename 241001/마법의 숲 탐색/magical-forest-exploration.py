from collections import deque

def can_move_to_south(cx, cy, board):
    # 이동방향에 board가 1이 아니면 됨 + 좌우 범위 C
    dd_x, dd_y = cx + 2, cy
    dl_x, dl_y = cx + 1, cy - 1
    dr_x, dr_y = cx + 1, cy + 1

    if (dd_x <= R+2 and dl_x <= R+2 and dr_x <= R+2) and \
        (1 <= dd_y <= C and 1 <= dl_y <= C and 1 <= dr_y <= C):
        return board[dd_x][dd_y] == 0 and board[dl_x][dl_y] == 0 and \
            board[dr_x][dr_y] == 0

    return False


def can_move_to_west_south(cx, cy, board):
    ll_x, ll_y = cx, cy - 2
    lu_x, lu_y = cx - 1, cy - 1
    ld_x, ld_y = cx + 1, cy - 1
    if (ll_x <= R+2 and lu_x <= R+2 and ld_x <= R+2) and \
            (1 <= ll_y <= C and 1 <= lu_y <= C and 1 <= ld_y <= C):
        return board[ll_x][ll_y] == 0 and board[lu_x][lu_y] == 0 and \
            board[ld_x][ld_y] == 0 and can_move_to_south(cx, cy - 1, board)
    return False


def can_move_to_east_south(cx, cy, board):
    rr_x, rr_y = cx, cy + 2
    ru_x, ru_y = cx - 1, cy + 1
    rd_x, rd_y = cx + 1, cy + 1
    if (rr_x <= R+2 and ru_x <= R+2 and rd_x <= R+2) and \
            (1 <= rr_y <= C and 1 <= ru_y <= C and 1 <= rd_y <= C):
        return board[rr_x][rr_y] == 0 and board[ru_x][ru_y] == 0 and \
            board[rd_x][rd_y] == 0 and can_move_to_south(cx, cy + 1, board)
    return False


def out_of_forest(x, y):
    return x < 3 or x > R + 2 or y < 1 or y > C


class Golem:
    def __init__(self, cx, cy, cd):
        self.cx = cx
        self.cy = cy
        self.cd = cd

    def move_south(self):
        self.cx += 1

    def move_east(self):
        self.cy += 1

    def move_west(self):
        self.cy -= 1

    def rotate_clockwise(self):
        self.cd = (self.cd + 1) % 4

    def rotate_anti_clockwise(self):
        self.cd = (self.cd - 1) % 4

    def add_on_board(self, board, door, num):
        board[self.cx][self.cy] = num
        for i in range(4):
            nx, ny = self.cx + dx[i], self.cy + dy[i]
            board[nx][ny] = num
            if i == self.cd:
                door[nx][ny] = 1

    def remove_on_board(self, board, door):
        board[self.cx][self.cy] = 0
        for i in range(4):
            nx, ny = self.cx + dx[i], self.cy + dy[i]
            board[nx][ny] = 0
            if i == self.cd:
                door[nx][ny] = 0

    def is_body_out_of_forest(self):
        body = [[self.cx, self.cy]]
        for i in range(4):
            nx, ny = self.cx + dx[i], self.cy + dy[i]
            body.append([nx, ny])
        for bx, by in body:
            if out_of_forest(bx, by):
                return True
        return False


R, C, K = map(int, input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# x = [3, R+2] = [1, R]
# 0, 1, 2는 준비 칸 3부터 첫번째 행 -> 답은 -2해주기
# 이동하기 위한 범위 -> 0 <= x <= R+2
# 보드 위에 있기 위한 범위 -> 3 <= x <= R+2
board = [[0 for _ in range(C+1)] for __ in range(R + 3)]
door = [[0 for _ in range(C+1)] for __ in range(R + 3)]

golems = []
golems_on_board = []
ans = 0

for _ in range(K):
    ci, di = map(int, input().split())
    golems.append(Golem(1, ci, di))


def bfs(cx, cy, board, door):
    fx = cx - 2
    visit = [[0 for _ in range(C+1)] for __ in range(R + 3)]
    queue = deque([[cx, cy]])
    visit[cx][cy] = 1
    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_forest(nx, ny) or visit[nx][ny] or board[nx][ny]==0:
                continue
            if board[cx][cy] == board[nx][ny] or door[cx][cy]:
                visit[nx][ny] = 1
                fx = max(fx, nx-2)
                queue.append([nx, ny])
    return fx



for i in range(K):
    while True:
        if can_move_to_south(golems[i].cx, golems[i].cy, board):
            golems[i].move_south()
        elif can_move_to_west_south(golems[i].cx, golems[i].cy, board):
            golems[i].move_west()
            golems[i].rotate_anti_clockwise()
            golems[i].move_south()
        elif can_move_to_east_south(golems[i].cx, golems[i].cy, board):
            golems[i].move_east()
            golems[i].rotate_clockwise()
            golems[i].move_south()
        else:
            break
    if golems[i].is_body_out_of_forest():
        for g in golems_on_board:
            g.remove_on_board(board, door)
        golems_on_board.clear()
    else:
        golems_on_board.append(golems[i])
        golems[i].add_on_board(board, door, i+1)

        ans += bfs(golems[i].cx, golems[i].cy, board, door)

print(ans)