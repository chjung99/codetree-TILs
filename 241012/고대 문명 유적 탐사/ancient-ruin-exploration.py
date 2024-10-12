from collections import deque

N_large = 5  # 고대 문명 전체 격자 크기입니다.
N_small = 3  # 회전시킬 격자의 크기입니다.

# 고대 문명 격자를 정의합니다
class Board:
    def __init__(self):
        self.a = [[0 for _ in range(N_large)] for _ in range(N_large)]

    def in_range(self, y, x):
        # 주어진 y, x가 고대 문명 격자의 범위안에 있는지 확인하는 함수 입니다.
        return 0 <= y < N_large and 0 <= x < N_large

    # 현재 격자에서 sy, sx를 좌측상단으로 하여 시계방향 90도 회전을 cnt번 시행했을때 결과를 return 합니다.
    def rotate(self, sy, sx, cnt):
        result = Board()
        result.a = [row[:] for row in self.a]
        for _ in range(cnt):
            # sy, sx를 좌측상단으로 하여 시계방향 90도 회전합니다.
            tmp = result.a[sy + 0][sx + 2]
            result.a[sy + 0][sx + 2] = result.a[sy + 0][sx + 0]
            result.a[sy + 0][sx + 0] = result.a[sy + 2][sx + 0]
            result.a[sy + 2][sx + 0] = result.a[sy + 2][sx + 2]
            result.a[sy + 2][sx + 2] = tmp
            tmp = result.a[sy + 1][sx + 2]
            result.a[sy + 1][sx + 2] = result.a[sy + 0][sx + 1]
            result.a[sy + 0][sx + 1] = result.a[sy + 1][sx + 0]
            result.a[sy + 1][sx + 0] = result.a[sy + 2][sx + 1]
            result.a[sy + 2][sx + 1] = tmp
        return result

    # 현재 격자에서 유물을 획득합니다.
    # 새로운 유물 조각을 채우는것은 여기서 고려하지 않습니다.
    def cal_score(self):
        score = 0
        visit = [[False for _ in range(N_large)] for _ in range(N_large)]
        dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]

        for i in range(N_large):
            for j in range(N_large):
                if not visit[i][j]:
                    # BFS를 활용한 Flood Fill 알고리즘을 사용하여 visit 배열을 채웁니다.
                    # 이때 trace 안에 조각들의 위치가 저장됩니다.
                    q, trace = deque([(i, j)]), deque([(i, j)])
                    visit[i][j] = True
                    while q:
                        cur = q.popleft()
                        for k in range(4):
                            ny, nx = cur[0] + dy[k], cur[1] + dx[k]
                            if self.in_range(ny, nx) and self.a[ny][nx] == self.a[cur[0]][cur[1]] and not visit[ny][nx]:
                                q.append((ny, nx))
                                trace.append((ny, nx))
                                visit[ny][nx] = True
                    # 위에서 진행된 Flood Fill을 통해 조각들이 모여 유물이 되고 사라지는지 확인힙니다.
                    if len(trace) >= 3:
                        # 유물이 되어 사라지는 경우 가치를 더해주고 조각이 비어있음을 뜻하는 0으로 바꿔줍니다.
                        score += len(trace)
                        while trace:
                            t = trace.popleft()
                            self.a[t[0]][t[1]] = 0
        return score

    # 유물 획득과정에서 조각이 비어있는 곳에 새로운 조각을 채워줍니다.
    def fill(self, que):
        # 열이 작고 행이 큰 우선순위로 채워줍니다.
        for j in range(N_large):
            for i in reversed(range(N_large)):
                if self.a[i][j] == 0:
                    self.a[i][j] = que.popleft()

def main():
    # 입력을 받습니다.
    K, M = map(int, input().split())
    board = Board()
    for i in range(N_large):
        board.a[i] = list(map(int, input().split()))
    q = deque()
    for t in list(map(int, input().split())):
        q.append(t)

    # 최대 K번의 탐사과정을 거칩니다.
    for _ in range(K):
        maxScore = 0
        maxScoreBoard = None
        # 회전 목표에 맞는 결과를 maxScoreBoard에 저장합니다.
        # (1) 유물 1차 획득 가치를 최대화
        # (2) 회전한 각도가 가장 작은 방법을 선택
        # (3) 회전 중심 좌표의 열이 가장 작은 구간을, 그리고 열이 같다면 행이 가장 작은 구간을 선택
        for cnt in range(1, 4):
            for sx in range(N_large - N_small + 1):
                for sy in range(N_large - N_small + 1):
                    rotated = board.rotate(sy, sx, cnt)
                    score = rotated.cal_score()
                    if maxScore < score:
                        maxScore = score
                        maxScoreBoard = rotated
        # 회전을 통해 더 이상 유물을 획득할 수 없는 경우 탐사를 종료합니다.
        if maxScoreBoard is None:
            break
        board = maxScoreBoard
        # 유물의 연쇄 획득을 위해 유물 조각을 채우고 유물을 획득하는 과정을 더이상 획득할 수 있는 유물이 없을때까지 반복합니다.
        while True:
            board.fill(q)
            newScore = board.cal_score()
            if newScore == 0:
                break
            maxScore += newScore

        print(maxScore, end=" ")

if __name__ == '__main__':
    main()