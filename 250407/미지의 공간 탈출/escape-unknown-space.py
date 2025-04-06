def myprint_3d(arr3):
    for arr in arr3:
        for lst in arr:
            print(*lst)
        print()
    print()

def myprint_2d(arr):
        for lst in arr:
            print(*lst)
        print()

def find_3d_start():
    for i in range(M):
        for j in range(M):
            if arr3[4][i][j]==2:
                return 4,i,j

def find_2d_end():
    for i in range(N):
        for j in range(N):
            if arr[i][j]==4:
                arr[i][j]=0
                return i, j

def find_3d_base():
    for i in range(N):
        for j in range(N):
            if arr[i][j]==3:
                return i, j

def find_3d_end_2d_start():
    # [1] 3차원 시작좌표(base) 찾기
    bi,bj = find_3d_base()

    # [2] 3차원 좌표에서 2차원 연결좌표 찾기(1차 목적지)
    for i in range(bi, bi+M):
        for j in range(bj, bj+M):
            if arr[i][j]!=3:        # 3차원 위치가 아니면 skip
                continue

            if arr[i][j+1]==0:      # 우측에 2차 시작점(3차원 우측으로 1차출구)
                return 0, M-1, (M-1)-(i-bi), i, j+1     # ek(평면)=0, ei=M-1, ej=i, si=i, sj=j+1
            elif arr[i][j-1]==0:    # 좌측으로 1차출구!
                return 1, M-1, i-bi, i, j-1             # ek(평면)=1, ei=M-1, ej=i, si=i, sj=j+1
            elif arr[i+1][j]==0:    # 아래쪽으로 1차출구!
                return 2, M-1, j-bj, i+1, j             # ek(평면)=2, ei=M-1, ej=i, si=i, sj=j+1
            elif arr[i-1][j]==0:    # 위쪽으로 1차출구!
                return 3, M-1, (M-1)-(j-bj), i-1, j     # ek(평면)=3, ei=M-1, ej=i, si=i, sj=j+1

    # 여기에 올일은 없지만..
    return -1

left_nxt = {0:2, 2:1, 1:3, 3:0}
right_nxt = {0:3, 2:0, 1:2, 3:1}
# dist = bfs_3d(sk_3d, si_3d, sj_3d,ek_3d, ei_3d, ej_3d)
from collections import deque
def bfs_3d(sk, si, sj,ek, ei, ej):
    q = deque()
    v = [[[0]*M for _ in range(M)] for _ in range(5)]

    q.append((sk,si,sj))
    v[sk][si][sj]=1

    while q:
        ck,ci,cj = q.popleft()

        if (ck,ci,cj)==(ek,ei,ej):
            # myprint_3d(v)
            return v[ck][ci][cj]

        # 네방향, 범위내/범위밖->다른평명 이동처리, 미방문
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj

            # 범위밖
            if ni<0:    # 위쪽 범위 이탈
                if ck==0:   nk,ni,nj = 4,(M-1)-cj,M-1
                elif ck==1: nk,ni,nj = 4,cj,0
                elif ck==2: nk,ni,nj = 4,M-1,cj
                elif ck==3: nk,ni,nj = 4,0,(M-1)-cj
                elif ck==4: nk,ni,nj = 3,0,(M-1)-cj
            elif ni>=M: # 아래쪽 범위이탈
                if ck==4:   nk,ni,nj = 2,0,cj
                else:       continue
            elif nj<0:  # 왼쪽 범위이탈
                if ck==4:   nk,ni,nj = 1,0,ci
                else:
                    nk,ni,nj = left_nxt[ck],ci,M-1
            elif nj>=M: # 오른쪽 범위이탈
                if ck==4:   nk,ni,nj = 0,0,(M-1)-ci
                else:
                    nk,ni,nj = right_nxt[ck],ci,0
            else:       # 이탈아니면 같은 평면
                nk=ck

            # 미방문, 조건 맞으면
            if v[nk][ni][nj]==0 and arr3[nk][ni][nj]==0:
                q.append((nk,ni,nj))
                v[nk][ni][nj]=v[ck][ci][cj]+1

    # 이곳에 왔다는건? 경로 없음!
    # myprint_3d(v)
    return -1

#     dist = bfs_2d(v, dist, si, sj, ei, ej)
def bfs_2d(v, dist, si, sj, ei, ej):
    q = deque()

    q.append((si,sj))
    v[si][sj]=dist

    while q:
        ci,cj = q.popleft()
        if (ci,cj)==(ei,ej):
            return v[ci][cj]

        # 네방향, 범위내, (미방문)/조건맞으면(길이고, v[ci][cj]+1<v[ni][nj])
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0 and v[ci][cj]+1<v[ni][nj]:
                q.append((ni,nj))
                v[ni][nj]=v[ci][cj]+1

    # 목적지를 찾을 수 없는 경우
    return -1

##########################################
##########################################

N, M, F = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
arr3 = [[list(map(int, input().split())) for _ in range(M)] for _ in range(5)]
wall = [list(map(int,input().split())) for _ in range(F)]

# [1] 주요위치들 찾기
# 3차원 시작, 3차원 끝, 2차원 시작, 2차원 끝 좌표 탐색
sk_3d, si_3d, sj_3d = find_3d_start()
ei, ej = find_2d_end()
ek_3d, ei_3d, ej_3d, si, sj = find_3d_end_2d_start()

# [2] 3차원공간 탐색: 시작위치 -> 탈출위치거리 탐색(BFS 최단거리)
dist = bfs_3d(sk_3d, si_3d, sj_3d,ek_3d, ei_3d, ej_3d)

# 동 서 남 북
di=[ 0, 0, 1,-1]
dj=[ 1,-1, 0, 0]
if dist!=-1:
    # [3] 2차원 탐색 준비: 시간이상현상 처리해서 v에 시간표시: BFS확산시 그보다 작으면 통과하게표시
    v = [[401]*N for _ in range(N)]
    for wi,wj,wd,wv in wall:        # wv 단위로 wd방향으로 확산표시(출구가 아닌경우만 확산)
        v[wi][wj]=1
        for mul in range(1, N+1):
            wi,wj = wi+di[wd], wj+dj[wd]
            if 0<=wi<N and 0<=wj<N and arr[wi][wj]==0 and (wi,wj)!=(ei,ej):
                if v[wi][wj]>wv*mul:    # 더 큰 값 일때만 갱신(겹칠수있으니)
                    v[wi][wj]=wv*mul
            else:
                break

    # [4] 2차원 시작위치에서 BFS로 탈출구탐색(v에 적혀있는 값보다 작은 경우 지나감)
    dist = bfs_2d(v, dist, si, sj, ei, ej)

print(dist)