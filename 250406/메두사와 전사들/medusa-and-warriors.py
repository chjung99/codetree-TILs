import sys
from collections import deque
from typing import List, Tuple

# 전역 상수 정의
INF = int(1e9) + 10  # 무한대를 나타내는 상수

# 방향 배열: 위, 아래, 왼쪽, 오른쪽
DX = [-1, 1, 0, 0]
DY = [0, 0, -1, 1]

# 타입 힌트
Point = Tuple[int, int]


def calculate_manhattan_distance(a: Point, b: Point) -> int:
    """
    두 점 사이의 맨해튼 거리를 계산하는 함수

    :param a: 첫 번째 점의 좌표 (x, y)
    :param b: 두 번째 점의 좌표 (x, y)
    :return: 맨해튼 거리
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute_distances(start_x: int, start_y: int, N: int, obstacle_grid: List[List[int]]) -> List[List[int]]:
    """
    BFS를 이용하여 종료 지점(start_x, start_y)에서 모든 도달 가능한 셀까지의 최단 거리를 계산하는 함수

    :param start_x: 시작 지점의 x 좌표 (종료 지점)
    :param start_y: 시작 지점의 y 좌표 (종료 지점)
    :param N: 그리드의 크기 (N x N)
    :param obstacle_grid: 장애물 그리드 (1: 장애물, 0: 자유로운 공간)
    :return: 각 셀에서의 거리 그리드
    """
    # 거리 그리드를 초기화: 장애물이 있는 셀은 INF, 그렇지 않으면 -1로 설정
    distance_grid = [[INF if obstacle_grid[i][j] else -1 for j in range(N)] for i in range(N)]

    queue = deque()
    queue.append((start_x, start_y))
    distance_grid[start_x][start_y] = 0  # 시작 지점의 거리는 0

    # BFS 알고리즘 실행
    while queue:
        current_x, current_y = queue.popleft()

        # 네 방향으로 이동
        for dir in range(4):
            next_x = current_x + DX[dir]
            next_y = current_y + DY[dir]

            # 그리드 경계를 벗어나는지 확인
            if next_x < 0 or next_y < 0 or next_x >= N or next_y >= N:
                continue
            # 이미 방문했거나 장애물이 있는지 확인
            if distance_grid[next_x][next_y] != -1:
                continue

            # 다음 셀의 거리 업데이트 및 큐에 추가
            distance_grid[next_x][next_y] = distance_grid[current_x][current_y] + 1
            queue.append((next_x, next_y))

    return distance_grid


def sight_up(x: int, y: int, N: int, is_test: bool, warrior_count_grid: List[List[int]],
             sight_map: List[List[int]]) -> int:
    """
    위쪽 방향으로 시야를 설정하는 함수

    :param x: 현재 플레이어의 x 좌표
    :param y: 현재 플레이어의 y 좌표
    :param N: 그리드의 크기
    :param is_test: 테스트 모드 여부 (True: 테스트, False: 실제 적용)
    :param warrior_count_grid: 각 셀에 있는 전사의 수
    :param sight_map: 현재 시야 상태 (1: 시야 내, 0: 시야 외)
    :return: 시야로 커버된 전사의 수
    """
    # 다이아몬드 형태로 위쪽 셀을 시야에 포함시킴
    for i in range(x - 1, -1, -1):
        left = max(0, y - (x - i))
        right = min(N - 1, y + (x - i))
        for j in range(left, right + 1):
            sight_map[i][j] = 1  # 시야 설정

    # 장애물 처리: 시야 막힘 여부 확인
    obstruction_found = False
    for i in range(x - 1, -1, -1):
        if obstruction_found:
            sight_map[i][y] = 0  # 장애물이 발견된 후에는 시야 제거
        else:
            sight_map[i][y] = 1  # 장애물이 발견되지 않으면 시야 유지

        if warrior_count_grid[i][y]:
            obstruction_found = True  # 전사가 있는 경우 장애물로 간주

    # 장애물에 따라 시야 조정
    for i in range(x - 1, 0, -1):
        left = max(0, y - (x - i))
        right = min(N - 1, y + (x - i))

        # 왼쪽 측면 조정
        for j in range(left, y):
            if not sight_map[i][j] or warrior_count_grid[i][j]:
                if j > 0:
                    sight_map[i - 1][j - 1] = 0  # 왼쪽 위 셀의 시야 제거
                sight_map[i - 1][j] = 0          # 바로 위 셀의 시야 제거

        # 오른쪽 측면 조정
        for j in range(y + 1, right + 1):
            if not sight_map[i][j] or warrior_count_grid[i][j]:
                if j + 1 < N:
                    sight_map[i - 1][j + 1] = 0  # 오른쪽 위 셀의 시야 제거
                sight_map[i - 1][j] = 0          # 바로 위 셀의 시야 제거

    # 시야로 커버된 전사 수 계산
    coverage = 0
    for i in range(x - 1, -1, -1):
        left = max(0, y - (x - i))
        right = min(N - 1, y + (x - i))
        for j in range(left, right + 1):
            if sight_map[i][j]:
                coverage += warrior_count_grid[i][j]

    # 테스트 모드인 경우 시야 맵을 원래대로 되돌림
    if is_test:
        for i in range(x - 1, -1, -1):
            left = max(0, y - (x - i))
            right = min(N - 1, y + (x - i))
            for j in range(left, right + 1):
                sight_map[i][j] = 0  # 시야 제거

    return coverage  # 커버리지 반환


def sight_down(x: int, y: int, N: int, is_test: bool, warrior_count_grid: List[List[int]],
              sight_map: List[List[int]]) -> int:
    """
    아래쪽 방향으로 시야를 설정하는 함수

    :param x: 현재 플레이어의 x 좌표
    :param y: 현재 플레이어의 y 좌표
    :param N: 그리드의 크기
    :param is_test: 테스트 모드 여부 (True: 테스트, False: 실제 적용)
    :param warrior_count_grid: 각 셀에 있는 전사의 수
    :param sight_map: 현재 시야 상태 (1: 시야 내, 0: 시야 외)
    :return: 시야로 커버된 전사의 수
    """
    # 다이아몬드 형태로 아래쪽 셀을 시야에 포함시킴
    for i in range(x + 1, N):
        left = max(0, y - (i - x))
        right = min(N - 1, y + (i - x))
        for j in range(left, right + 1):
            sight_map[i][j] = 1  # 시야 설정

    # 장애물 처리: 시야 막힘 여부 확인
    obstruction_found = False
    for i in range(x + 1, N):
        if obstruction_found:
            sight_map[i][y] = 0  # 장애물이 발견된 후에는 시야 제거
        else:
            sight_map[i][y] = 1  # 장애물이 발견되지 않으면 시야 유지

        if warrior_count_grid[i][y]:
            obstruction_found = True  # 전사가 있는 경우 장애물로 간주

    # 장애물에 따라 시야 조정
    for i in range(x + 1, N - 1):
        left = max(0, y - (i - x))
        right = min(N - 1, y + (i - x))

        # 왼쪽 측면 조정
        for j in range(left, y):
            if not sight_map[i][j] or warrior_count_grid[i][j]:
                if j > 0:
                    sight_map[i + 1][j - 1] = 0  # 왼쪽 아래 셀의 시야 제거
                sight_map[i + 1][j] = 0          # 바로 아래 셀의 시야 제거

        # 오른쪽 측면 조정
        for j in range(y + 1, right + 1):
            if not sight_map[i][j] or warrior_count_grid[i][j]:
                if j + 1 < N:
                    sight_map[i + 1][j + 1] = 0  # 오른쪽 아래 셀의 시야 제거
                sight_map[i + 1][j] = 0          # 바로 아래 셀의 시야 제거

    # 시야로 커버된 전사 수 계산
    coverage = 0
    for i in range(x + 1, N):
        left = max(0, y - (i - x))
        right = min(N - 1, y + (i - x))
        for j in range(left, right + 1):
            if sight_map[i][j]:
                coverage += warrior_count_grid[i][j]

    # 테스트 모드인 경우 시야 맵을 원래대로 되돌림
    if is_test:
        for i in range(x + 1, N):
            left = max(0, y - (i - x))
            right = min(N - 1, y + (i - x))
            for j in range(left, right + 1):
                sight_map[i][j] = 0  # 시야 제거

    return coverage  # 커버리지 반환


def sight_left(x: int, y: int, N: int, is_test: bool, warrior_count_grid: List[List[int]],
              sight_map: List[List[int]]) -> int:
    """
    왼쪽 방향으로 시야를 설정하는 함수

    :param x: 현재 플레이어의 x 좌표
    :param y: 현재 플레이어의 y 좌표
    :param N: 그리드의 크기
    :param is_test: 테스트 모드 여부 (True: 테스트, False: 실제 적용)
    :param warrior_count_grid: 각 셀에 있는 전사의 수
    :param sight_map: 현재 시야 상태 (1: 시야 내, 0: 시야 외)
    :return: 시야로 커버된 전사의 수
    """
    # 다이아몬드 형태로 왼쪽 셀을 시야에 포함시킴
    for i in range(y - 1, -1, -1):
        top = max(0, x - (y - i))
        bottom = min(N - 1, x + (y - i))
        for j in range(top, bottom + 1):
            sight_map[j][i] = 1  # 시야 설정

    # 장애물 처리: 시야 막힘 여부 확인
    obstruction_found = False
    for i in range(y - 1, -1, -1):
        if obstruction_found:
            sight_map[x][i] = 0  # 장애물이 발견된 후에는 시야 제거
        else:
            sight_map[x][i] = 1  # 장애물이 발견되지 않으면 시야 유지

        if warrior_count_grid[x][i]:
            obstruction_found = True  # 전사가 있는 경우 장애물로 간주

    # 장애물에 따라 시야 조정
    for i in range(y - 1, 0, -1):
        top = max(0, x - (y - i))
        bottom = min(N - 1, x + (y - i))

        # 상단 측면 조정
        for j in range(top, x):
            if not sight_map[j][i] or warrior_count_grid[j][i]:
                if j > 0:
                    sight_map[j - 1][i - 1] = 0  # 왼쪽 위 셀의 시야 제거
                sight_map[j][i - 1] = 0          # 바로 왼쪽 셀의 시야 제거

        # 하단 측면 조정
        for j in range(x + 1, bottom + 1):
            if not sight_map[j][i] or warrior_count_grid[j][i]:
                if j + 1 < N:
                    sight_map[j + 1][i - 1] = 0  # 왼쪽 아래 셀의 시야 제거
                sight_map[j][i - 1] = 0          # 바로 왼쪽 셀의 시야 제거

    # 시야로 커버된 전사 수 계산
    coverage = 0
    for i in range(y - 1, -1, -1):
        top = max(0, x - (y - i))
        bottom = min(N - 1, x + (y - i))
        for j in range(top, bottom + 1):
            if sight_map[j][i]:
                coverage += warrior_count_grid[j][i]

    # 테스트 모드인 경우 시야 맵을 원래대로 되돌림
    if is_test:
        for i in range(y - 1, -1, -1):
            top = max(0, x - (y - i))
            bottom = min(N - 1, x + (y - i))
            for j in range(top, bottom + 1):
                sight_map[j][i] = 0  # 시야 제거

    return coverage  # 커버리지 반환


def sight_right(x: int, y: int, N: int, is_test: bool, warrior_count_grid: List[List[int]],
               sight_map: List[List[int]]) -> int:
    """
    오른쪽 방향으로 시야를 설정하는 함수

    :param x: 현재 플레이어의 x 좌표
    :param y: 현재 플레이어의 y 좌표
    :param N: 그리드의 크기
    :param is_test: 테스트 모드 여부 (True: 테스트, False: 실제 적용)
    :param warrior_count_grid: 각 셀에 있는 전사의 수
    :param sight_map: 현재 시야 상태 (1: 시야 내, 0: 시야 외)
    :return: 시야로 커버된 전사의 수
    """
    # 다이아몬드 형태로 오른쪽 셀을 시야에 포함시킴
    for i in range(y + 1, N):
        top = max(0, x - (i - y))
        bottom = min(N - 1, x + (i - y))
        for j in range(top, bottom + 1):
            sight_map[j][i] = 1  # 시야 설정

    # 장애물 처리: 시야 막힘 여부 확인
    obstruction_found = False
    for i in range(y + 1, N):
        if obstruction_found:
            sight_map[x][i] = 0  # 장애물이 발견된 후에는 시야 제거
        else:
            sight_map[x][i] = 1  # 장애물이 발견되지 않으면 시야 유지

        if warrior_count_grid[x][i]:
            obstruction_found = True  # 전사가 있는 경우 장애물로 간주

    # 장애물에 따라 시야 조정
    for i in range(y + 1, N - 1):
        top = max(0, x - (i - y))
        bottom = min(N - 1, x + (i - y))

        # 상단 측면 조정
        for j in range(top, x):
            if not sight_map[j][i] or warrior_count_grid[j][i]:
                if j > 0:
                    sight_map[j - 1][i + 1] = 0  # 오른쪽 위 셀의 시야 제거
                sight_map[j][i + 1] = 0          # 바로 오른쪽 셀의 시야 제거

        # 하단 측면 조정
        for j in range(x + 1, bottom + 1):
            if not sight_map[j][i] or warrior_count_grid[j][i]:
                if j + 1 < N:
                    sight_map[j + 1][i + 1] = 0  # 오른쪽 아래 셀의 시야 제거
                sight_map[j][i + 1] = 0          # 바로 오른쪽 셀의 시야 제거

    # 시야로 커버된 전사 수 계산
    coverage = 0
    for i in range(y + 1, N):
        top = max(0, x - (i - y))
        bottom = min(N - 1, x + (i - y))
        for j in range(top, bottom + 1):
            if sight_map[j][i]:
                coverage += warrior_count_grid[j][i]

    # 테스트 모드인 경우 시야 맵을 원래대로 되돌림
    if is_test:
        for i in range(y + 1, N):
            top = max(0, x - (i - y))
            bottom = min(N - 1, x + (i - y))
            for j in range(top, bottom + 1):
                sight_map[j][i] = 0  # 시야 제거

    return coverage  # 커버리지 반환


def choose_best_sight(x: int, y: int, N: int, warrior_count_grid: List[List[int]],
                      sight_map: List[List[int]]) -> int:
    """
    최적의 시야 방향을 선택하여 시야를 설정하는 함수

    :param x: 현재 플레이어의 x 좌표
    :param y: 현재 플레이어의 y 좌표
    :param N: 그리드의 크기
    :param warrior_count_grid: 각 셀에 있는 전사의 수
    :param sight_map: 현재 시야 상태 (1: 시야 내, 0: 시야 외)
    :return: 최대 커버리지 (시야로 커버된 전사의 수)
    """
    # 시야 맵을 초기화 (모든 셀을 시야 외로 설정)
    for i in range(N):
        for j in range(N):
            sight_map[i][j] = 0

    max_coverage = -1  # 최대 커버리지를 저장할 변수
    best_direction = -1  # 최적의 시야 방향 (0: 위, 1: 아래, 2: 왼쪽, 3: 오른쪽)

    # 시야 방향별 함수 리스트
    sight_functions = [sight_up, sight_down, sight_left, sight_right]

    # 모든 시야 방향을 테스트하여 최대 커버리지를 찾음
    for dir in range(4):
        # 테스트를 위해 시야 맵을 초기화
        for i in range(N):
            for j in range(N):
                sight_map[i][j] = 0

        # 현재 방향으로 시야 설정하고 커버리지 계산
        coverage = sight_functions[dir](x, y, N, True, warrior_count_grid, sight_map)
        if max_coverage < coverage:
            max_coverage = coverage
            best_direction = dir

    # 유효한 방향이 선택되었는지 확인
    assert best_direction != -1, "최적의 시야 방향을 찾을 수 없습니다."

    # 최적의 방향으로 실제 시야 설정
    sight_functions[best_direction](x, y, N, False, warrior_count_grid, sight_map)

    return max_coverage


def move_warriors(player_x: int, player_y: int, N: int, M: int, warrior_positions: List[Point],
                 sight_map: List[List[int]]) -> Tuple[int, int]:
    """
    플레이어를 향해 전사들을 이동시키는 함수

    :param player_x: 플레이어의 현재 x 좌표
    :param player_y: 플레이어의 현재 y 좌표
    :param N: 그리드의 크기
    :param M: 전사의 수
    :param warrior_positions: 전사들의 현재 위치
    :param sight_map: 현재 시야 상태 (1: 시야 내, 0: 시야 외)
    :return: (총 이동한 전사 수, 플레이어에게 도달한 전사 수)
    """
    total_moved = 0  # 총 이동한 전사 수
    total_hits = 0   # 플레이어에게 도달한 전사 수

    # 전사의 이동 방향: 위, 아래, 왼쪽, 오른쪽
    move_dx = [-1, 1, 0, 0]
    move_dy = [0, 0, -1, 1]

    # 모든 전사에 대해 이동 처리
    for i in range(M):
        if warrior_positions[i][0] == -1:
            continue  # 이미 잡힌 전사는 건너뜀

        warrior_x, warrior_y = warrior_positions[i]

        # 시야 내에 있는 전사는 이동하지 않음
        if sight_map[warrior_x][warrior_y]:
            continue

        # 현재 플레이어와의 거리 계산
        current_distance = calculate_manhattan_distance((player_x, player_y), (warrior_x, warrior_y))
        has_moved = False  # 이동 여부 플래그

        # 첫 번째 이동: 거리를 줄이기 위해 이동
        for dir in range(4):
            next_x = warrior_x + move_dx[dir]
            next_y = warrior_y + move_dy[dir]

            # 이동할 위치가 그리드 내에 있고 시야 내에 있지 않은지 확인
            if next_x < 0 or next_y < 0 or next_x >= N or next_y >= N:
                continue
            if sight_map[next_x][next_y]:
                continue

            # 새로운 위치에서의 거리 계산
            new_distance = calculate_manhattan_distance((player_x, player_y), (next_x, next_y))
            if new_distance < current_distance:
                warrior_x, warrior_y = next_x, next_y
                has_moved = True
                total_moved += 1
                break  # 첫 번째 이동 후 루프 탈출

        # 두 번째 이동: 추가로 거리를 줄일 수 있는지 확인
        if has_moved:
            new_distance = calculate_manhattan_distance((player_x, player_y), (warrior_x, warrior_y))
            for dir in range(4):
                # 반대 방향으로 이동 시도
                opposite_dir = (dir + 2) % 4
                next_x = warrior_x + move_dx[opposite_dir]
                next_y = warrior_y + move_dy[opposite_dir]

                # 이동할 위치가 그리드 내에 있고 시야 내에 있지 않은지 확인
                if next_x < 0 or next_y < 0 or next_x >= N or next_y >= N:
                    continue
                if sight_map[next_x][next_y]:
                    continue

                # 새로운 위치에서의 거리 계산
                further_distance = calculate_manhattan_distance((player_x, player_y), (next_x, next_y))
                if further_distance < new_distance:
                    warrior_x, warrior_y = next_x, next_y
                    total_moved += 1
                    break  # 두 번째 이동 후 루프 탈출

        # 전사의 위치 업데이트
        warrior_positions[i] = (warrior_x, warrior_y)

    # 플레이어에게 도달한 전사 수 계산
    for i in range(M):
        if warrior_positions[i][0] == -1:
            continue  # 이미 잡힌 전사는 건너뜀

        if warrior_positions[i][0] == player_x and warrior_positions[i][1] == player_y:
            total_hits += 1
            warrior_positions[i] = (-1, -1)  # 전사를 잡힌 상태로 표시

    return total_moved, total_hits


def update_warrior_count_grid(N: int, M: int, warrior_positions: List[Point]) -> List[List[int]]:
    """
    현재 전사들의 위치를 기반으로 각 셀에 있는 전사의 수를 업데이트하는 함수

    :param N: 그리드의 크기
    :param M: 전사의 수
    :param warrior_positions: 전사들의 현재 위치
    :return: 각 셀에 있는 전사의 수 그리드
    """
    # 전사 수 그리드를 초기화
    warrior_count_grid = [[0 for _ in range(N)] for _ in range(N)]

    # 각 전사의 위치를 확인하여 전사 수 그리드에 반영
    for i in range(M):
        if warrior_positions[i][0] == -1:
            continue  # 이미 잡힌 전사는 건너뜀
        x, y = warrior_positions[i]
        warrior_count_grid[x][y] += 1

    return warrior_count_grid


# 빠른 입출력을 위해 sys.stdin을 사용
input = sys.stdin.read
data = input().split()
idx = 0

N = int(data[idx]); idx += 1  # 그리드 크기 N
M = int(data[idx]); idx += 1  # 전사 수 M

start_x = int(data[idx]); idx += 1
start_y = int(data[idx]); idx += 1
end_x = int(data[idx]); idx += 1
end_y = int(data[idx]); idx += 1

# 초기 전사 위치 입력
warrior_positions = []
for _ in range(M):
    x = int(data[idx]); idx += 1
    y = int(data[idx]); idx += 1
    warrior_positions.append((x, y))

# 장애물 그리드 입력
obstacle_grid = []
for _ in range(N):
    row = []
    for _ in range(N):
        cell = int(data[idx]); idx += 1
        row.append(cell)
    obstacle_grid.append(row)

# 시작 지점과 종료 지점이 장애물이 아닌지 확인
assert obstacle_grid[start_x][start_y] == 0, "시작 지점에 장애물이 있습니다."
assert obstacle_grid[end_x][end_y] == 0, "종료 지점에 장애물이 있습니다."

# 종료 지점으로부터 모든 셀까지의 거리를 계산
distance_grid = compute_distances(end_x, end_y, N, obstacle_grid)

# 시작 지점이 종료 지점에 도달할 수 없는 경우 종료
if distance_grid[start_x][start_y] == -1:
    print("-1")
    sys.exit()

current_x, current_y = start_x, start_y  # 현재 플레이어의 위치

# 시야 맵 초기화
sight_map = [[0 for _ in range(N)] for _ in range(N)]

# 전사 수 그리드 초기화
warrior_count_grid = update_warrior_count_grid(N, M, warrior_positions)

# 메인 루프: 플레이어가 종료 지점에 도달할 때까지 반복
while True:
    moved = False  # 플레이어가 이동했는지 여부

    # 현재 위치에서 종료 지점으로 향하는 방향으로 한 칸 이동
    for dir in range(4):
        next_x = current_x + DX[dir]
        next_y = current_y + DY[dir]
        if next_x < 0 or next_y < 0 or next_x >= N or next_y >= N:
            continue  # 그리드 경계를 벗어나면 무시
        if distance_grid[next_x][next_y] < distance_grid[current_x][current_y]:
            current_x, current_y = next_x, next_y
            moved = True
            break  # 이동 후 루프 탈출

    # 종료 지점에 도달한 경우 종료
    if current_x == end_x and current_y == end_y:
        print("0")
        break

    # 현재 위치에 있는 전사들을 잡음 (시야로 인해)
    for i in range(M):
        if warrior_positions[i][0] == current_x and warrior_positions[i][1] == current_y:
            warrior_positions[i] = (-1, -1)  # 전사를 잡힌 상태로 표시

    # 현재 전사들의 위치를 기반으로 전사 수 그리드를 업데이트
    warrior_count_grid = update_warrior_count_grid(N, M, warrior_positions)

    # 최적의 시야 방향을 선택하고 시야로 커버된 전사의 수를 계산
    sight_coverage = choose_best_sight(current_x, current_y, N, warrior_count_grid, sight_map)

    # 전사들을 이동시키고 이동한 전사 수와 플레이어에게 도달한 전사 수를 얻음
    warriors_moved, warriors_hit = move_warriors(current_x, current_y, N, M, warrior_positions, sight_map)

    # 전사 수 그리드를 업데이트
    warrior_count_grid = update_warrior_count_grid(N, M, warrior_positions)

    # 결과 출력: 이동한 전사 수, 시야 커버리지, 플레이어에게 도달한 전사 수
    print(f"{warriors_moved} {sight_coverage} {warriors_hit}")
