n = int(input())
total = n * n
favorites = {}
board = [[0 for _ in range(n)] for __ in range(n)]
visit = [[0 for _ in range(n)] for __ in range(n)]
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def move_student(student_num, board, favorites, visit):
    cand = []  # [좋아하는 친구 수, 비어있는 칸 수, 행 번호, 열 번호]
    for i in range(n):
        for j in range(n):
            if visit[i][j]:
                continue
            num_of_favorites = 0
            num_of_empty = 0
            for k in range(4):
                nx, ny = i + dx[k], j + dy[k]
                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue
                if board[nx][ny] == 0:
                    num_of_empty += 1
                elif board[nx][ny] in favorites[student_num]:
                    num_of_favorites += 1
            cand.append([num_of_favorites, num_of_empty, i, j])
    cand.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]))
    fx, fy = cand[0][-2], cand[0][-1]

    visit[fx][fy] = 1
    board[fx][fy] = student_num


def calc_score(board, favorites):
    score = 0
    for i in range(n):
        for j in range(n):
            num_of_favorites = 0
            for k in range(4):
                nx, ny = i + dx[k], j + dy[k]
                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue
                if board[nx][ny] in favorites[board[i][j]]:
                    num_of_favorites += 1
            if num_of_favorites == 1:
                score += 1
            elif num_of_favorites == 2:
                score += 10
            elif num_of_favorites == 3:
                score += 100
            elif num_of_favorites == 4:
                score += 1000
    return score


for _ in range(total):
    student_num, f1, f2, f3, f4 = map(int, input().split())
    favorites[student_num] = [f1, f2, f3, f4]

for student_num in favorites.keys():
    move_student(student_num, board, favorites, visit)

answer = calc_score(board, favorites)
print(answer)