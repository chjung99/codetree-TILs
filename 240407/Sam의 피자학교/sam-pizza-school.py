n, k = map(int, input().split())
dough = [[0 for _ in range(n)] for __ in range(n - 1)]
dough.append(list(map(int, input().split())))
answer = 0
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def add_flour(dough):
    min_flour = min(dough[n - 1])
    for i in range(n):
        if dough[n - 1][i] == min_flour:
            dough[n - 1][i] += 1


def get_column_len(col):
    cnt = 0
    for i in range(n-1, -1, -1):
        if dough[i][col] == 0:
            break
        cnt += 1
    return cnt


def find_next_fy(dough):
    for i in range(n):
        if get_column_len(i) == 1:
            return i


def roll_up(dough):
    fx, fy = n - 1, 1
    upper_len, floor_len = 1, n - 1

    while upper_len <= floor_len:
        for col_diff in range(1, fy + 1, 1):
            if dough[fx][fy - col_diff] == 0:
                break
            for row_diff in range(n):
                src_x, src_y = fx - row_diff, fy - col_diff
                dest_x, dest_y = fx - col_diff, fy + row_diff
                if dough[src_x][src_y] == 0:
                    break
                dough[dest_x][dest_y] = dough[src_x][src_y]
                dough[src_x][src_y] = 0
        fy = find_next_fy(dough)
        upper_len = get_column_len(fy - 1)
        floor_len = (n - 1 - fy) + 1


def share_flour(dough):
    new_dough = [dough[i][:]for i in range(n)]
    for i in range(n):
        for j in range(n):
            if dough[i][j] == 0:
                continue
            for d in range(4):
                nx, ny = i + dx[d], j + dy[d]
                if nx < 0 or nx >= n or ny < 0 or ny >= n or dough[nx][ny] == 0:
                    continue
                diff = dough[i][j] - dough[nx][ny]
                if diff >= 5:
                    new_dough[i][j] -= diff // 5
                    new_dough[nx][ny] += diff // 5
    for i in range(n):
        for j in range(n):
            dough[i][j] = new_dough[i][j]


def spread_dough(dough):
    new_dough = [[0 for _ in range(n)] for __ in range(n)]
    new_dough_col = 0
    new_dough_row = n-1
    start = 0
    for i in range(n):
        if get_column_len(i) != 0:
            start = i
            break
    for col in range(start, n, 1):
        for row in range(n-1, -1, -1):
            if dough[row][col] == 0:
                break
            new_dough[new_dough_row][new_dough_col] = dough[row][col]
            new_dough_col += 1
    for i in range(n):
        for j in range(n):
            dough[i][j] = new_dough[i][j]


def press_down(dough):
    share_flour(dough)
    spread_dough(dough)


def fold_dough(dough, fx, fy):
    for col_diff in range(1, fy + 1, 1):
        if dough[fx][fy - col_diff] == 0:
            break
        for row_diff in range(0, n-fx, 1):
            src_x, src_y = fx + row_diff, fy - col_diff
            dest_x, dest_y = fx - (row_diff +1), fy + (col_diff-1)
            if dough[src_x][src_y] == 0:
                break
            dough[dest_x][dest_y] = dough[src_x][src_y]
            dough[src_x][src_y] = 0


def fold_twice(dough):
    fx, fy = n-1, n//2
    fold_dough(dough, fx, fy)
    fx, fy = n-2, (n+fy)//2
    fold_dough(dough, fx, fy)

while True:
    if max(dough[n - 1]) - min(dough[n - 1]) <= k:
        break
    add_flour(dough)
    roll_up(dough)
    press_down(dough)
    fold_twice(dough)
    press_down(dough)
    answer += 1
print(answer)