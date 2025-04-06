from collections import deque


def find_3d_start():
    for i in range(M):
        for j in range(M):
            if arr3[4][i][j] == 2:
                return 4, i, j


def find_2d_end():
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 4:
                arr[i][j] = 0
                return i, j


def find_3d_base():
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 3:
                return i, j


def find_3d_end_2d_start():
    bi, bj = find_3d_base()

    for i in range(bi, bi + M):
        for j in range(bj, bj + M):
            if arr[i][j] != 3:
                continue
            if arr[i][j + 1] == 0:
                si, sj = i, j + 1
                ek_3d, ei_3d, ej_3d = 0, M - 1, (M - 1) - (i - bi)
                return ek_3d, ei_3d, ek_3d, si, sj

            elif arr[i][j - 1] == 0:
                si, sj = i, j - 1
                ek_3d, ei_3d, ej_3d = 1, M - 1, (i - bi)
                return ek_3d, ei_3d, ek_3d, si, sj

            elif arr[i + 1][j] == 0:
                si, sj = i + 1, j
                ek_3d, ei_3d, ej_3d = 2, M - 1, (j - bj)
                return ek_3d, ei_3d, ek_3d, si, sj

            elif arr[i - 1][j] == 0:
                si, sj = i - 1, j
                ek_3d, ei_3d, ej_3d = 3, M - 1, (M - 1) - (j - bj)
                return ek_3d, ei_3d, ek_3d, si, sj


def bfs_3d(sk, si, sj, ek, ei, ej):
    left_next = {0: 2, 2: 1, 1: 3, 3: 0}
    right_next = {0: 3, 3: 1, 1: 2, 2: 0}

    q = deque()
    v = [[[0] * M for _ in range(M)] for __ in range(5)]
    q.append((sk, si, sj))
    v[sk][si][sj] = 1
    while q:
        ck, ci, cj = q.popleft()
        if (ck, ci, cj) == (ek, ei, ej):
            return v[ck][ci][cj]
        # 네 방향, 범위 내/범위 밖이면 다른 평면으로 이동 , 미방문
        for i in range(4):
            ni, nj = ci + dx[i], cj + dy[i]

            # 범위 밖
            if ni < 0:
                if ck == 0:
                    nk, ni, nj = 4, (M - 1) - cj, M - 1
                elif ck == 1:
                    nk, ni, nj = 4, cj, 0
                elif ck == 2:
                    nk, ni, nj = 4, M - 1, cj
                elif ck == 3:
                    nk, ni, nj = 4, 0, (M - 1) - cj
                elif ck == 4:
                    nk, ni, nj = 3, 0, (M - 1) - cj
            elif ni >= M:
                if ck == 4:
                    nk, ni, nj = 2, 0, cj
                else:
                    continue
            elif nj < 0:
                if ck == 4:
                    nk, ni, nj = 1, 0, ci
                else:
                    nk, ni, nj = left_next[ck], ci, M - 1
            elif nj >= M:
                if ck == 4:
                    nk, ni, nj = 0, 0, (M - 1) - ci
                else:
                    nk, ni, nj = right_next[ck], ci, 0
            else:  # 범위 내
                nk = ck
            # 미방문, 조건 맞으면 인큐
            if v[nk][ni][nj] == 0 and arr3[nk][ni][nj] == 0:
                v[nk][ni][nj] = v[ck][ci][cj] + 1
                q.append([nk, ni, nj])
    return -1


def bfs_2d(v, dist, si, sj, ei, ej):
    q = deque()

    q.append((si, sj))
    v[si][sj] = dist
    while q:
        ci, cj = q.popleft()
        if (ci, cj) == (ei, ej):
            return v[ci][cj]
        # 네 방향, 빈땅, 범위 내, 미방문/조건에 맞으면 인큐

        for i in range(4):
            ni, nj = ci + dx[i], cj + dy[i]
            if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 0 and v[ci][cj] + 1 < v[ni][nj]:
                q.append((ni, nj))
                v[ni][nj] = v[ci][cj] + 1
    return -1


N, M, F = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
arr3 = [[list(map(int, input().split())) for _ in range(M)] for __ in range(5)]
wall = [list(map(int, input().split())) for _ in range(F)]
dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

di = [0, 0, 1, -1]
dj = [1, -1, 0, 0]
# [1] 주요 위치들 찾기
# 3차원 시작, 3차원 끝, 2차원 시작, 2차원 끝 좌표 탐색
sk_3d, si_3d, sj_3d = find_3d_start()
ei, ej = find_2d_end()

ek_3d, ei_3d, ej_3d, si, sj = find_3d_end_2d_start()

# [2] 3차원 공간 탐색: 시작 위치 -> 탈출 위치 거리 탐색


dist = bfs_3d(sk_3d, si_3d, sj_3d, ek_3d, ei_3d, ej_3d)

if dist != -1:
    # [3] 2차원 탐색 준비: 시간 이상 현상 처리해서 v에 시간 표시
    v = [[401] * N for _ in range(N)]
    for wi, wj, wd, wv in wall:
        v[wi][wj] = 1
        for mul in range(1, N + 1):
            wi, wj = wi + di[wd], wj + dj[wd]
            if 0 <= wi < N and 0 <= wj < N and arr[wi][wj] == 0 and (wi, wj) != (ei, ej):
                if v[wi][wj] > wv*mul:
                    v[wi][wj] = wv * mul
            else:
                break
    # [4] 2차원 시작위치에서 BFS로 탈출구 탐색(V에 적혀있는 값보다 작을 때)
    dist = bfs_2d(v, dist, si, sj, ei, ej)
print(dist)
