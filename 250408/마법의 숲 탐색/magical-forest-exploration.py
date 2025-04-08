from collections import deque


def out_of_range(x, y):
    return x < 0 or x >= R + 3 or y < 0 or y >= C


def check(r, c):
    if out_of_range(r, c) or board[r][c] != 0:
        return False
    else:
        return True


def check_1(r, c):
    br, bc = r + dx[2], c + dy[2]

    left_r, left_c = br, bc - 1
    right_r, right_c = br, bc + 1
    bot_r, bot_c = br + 1, bc

    return check(left_r, left_c) and check(right_r, right_c) and \
        check(bot_r, bot_c)


def check_2(r, c):
    lr, lc = r + dx[3], c + dy[3]

    left_r, left_c = lr, lc - 1
    bot_r, bot_c = lr + 1, lc
    top_r, top_c = lr - 1, lc

    left_bot_r, left_bot_c = left_r + 1, left_c
    bot_bot_r, bot_bot_c = bot_r + 1, bot_c

    return check(left_r, left_c) and check(bot_r, bot_c) and \
        check(top_r, top_c) and check(left_bot_r, left_bot_c) and \
        check(bot_bot_r, bot_bot_c)


def check_3(r, c):
    rr, rc = r + dx[1], c + dy[1]

    right_r, right_c = rr, rc + 1
    top_r, top_c = rr - 1, rc
    bot_r, bot_c = rr + 1, rc

    right_bot_r, right_bot_c = right_r + 1, right_c
    bot_bot_r, bot_bot_c = bot_r + 1, bot_c

    return check(right_r, right_c) and check(top_r, top_c) and \
        check(bot_r, bot_c) and check(right_bot_r, right_bot_c) and \
        check(bot_bot_r, bot_bot_c)


def check_4(r, c):

    for i in range(4):
        nr, nc = r + dx[i], c + dy[i]
        if nr <= 2:
            return False
    return True


def move_south():
    global r
    r += 1


def turn_west_and_move_south():
    global r, c, d
    r, c = r, c - 1
    d = (d - 1) % 4
    move_south()


def turn_east_and_move_south():
    global r, c, d
    r, c = r, c + 1
    d = (d + 1) % 4
    move_south()


def set_golem(r, c, d, num):
    board[r][c] = num
    for i in range(4):
        if i == d:
            exit[r + dx[i]][c + dy[i]] = 1
        board[r + dx[i]][c + dy[i]] = num


def bfs(x, y, board):
    visit = [[0]*C for _ in range(R+3)]
    max_row = x
    visit[x][y] = 1
    queue = deque([[x, y]])

    while queue:
        cx, cy = queue.popleft()
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if out_of_range(nx, ny) or visit[nx][ny]:
                continue
            if board[nx][ny] == 0:
                continue

            if board[nx][ny] == board[cx][cy] or exit[cx][cy]:
                max_row = max(max_row, nx)
                visit[nx][ny] = 1
                queue.append([nx, ny])
    # print(max_row-2)
    return max_row - 2


def move_person(r, c):
    global answer
    answer += bfs(r, c, board)


R, C, K = map(int, input().split())
golems = [list(map(int, input().split())) for _ in range(K)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

board = [[0] * C for _ in range(R + 3)]
exit = [[0] * C for _ in range(R + 3)]
answer = 0  # 행의 총합 좌표 연산 주의

for i in range(K):
    r, c, d = 0, golems[i][0] - 1, golems[i][1]

    while True:
        chk1 = check_1(r, c)
        chk2 = check_2(r, c)
        chk3 = check_3(r, c)
        if chk1:
            move_south()
        elif chk2:
            turn_west_and_move_south()
        elif chk3:
            turn_east_and_move_south()
        else:
            if check_4(r, c):
                set_golem(r, c, d, i+1)

            else:
                board = [[0] * C for _ in range(R + 3)]
                exit = [[0] * C for _ in range(R + 3)]
            break
    if check_4(r, c):
        move_person(r, c)
    # for p in range(R + 3):
    #     for q in range(C):
    #         if exit[p][q]:
    #             print("-1", end=" ")
    #         else:
    #             print(board[p][q], end=" ")
    #     print("")
    # print("====================")
print(answer)
