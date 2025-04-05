# 변수 선언 및 입력:
n, m, h, k = tuple(map(int, input().split()))

# 각 칸에 있는 도망자 정보를 관리합니다.
# 도망자의 방향만 저장하면 충분합니다.
hiders = [
    [[] for _ in range(n)]
    for _ in range(n)
]
next_hiders = [
    [[] for _ in range(n)]
    for _ in range(n)
]
tree = [
    [False] * n
    for _ in range(n)
]

# 정방향 기준으로
# 현재 위치에서 술래가 움직여야 할 방향을 관리합니다.
seeker_next_dir = [
    [0] * n
    for _ in range(n)
]
# 역방향 기준으로
# 현재 위치에서 술래가 움직여야 할 방향을 관리합니다.
seeker_rev_dir = [
    [0] * n
    for _ in range(n)
]

# 술래의 현재 위치를 나타냅니다.
seeker_pos = (n // 2, n // 2)
# 술래가 움직이는 방향이 정방향이면 True / 아니라면 False입니다.
forward_facing = True

ans = 0

# 술래 정보를 입력받습니다.
for _ in range(m):
    x, y, d = tuple(map(int, input().split()))
    hiders[x - 1][y - 1].append(d)

# 나무 정보를 입력받습니다.
for _ in range(h):
    x, y = tuple(map(int, input().split()))
    tree[x - 1][y - 1] = True


# 정중앙으로부터 끝까지 움직이는 경로를 계산해줍니다.
def initialize_seeker_path():
    # 상우하좌 순서대로 넣어줍니다.
    dxs, dys = [-1, 0, 1, 0], [0, 1, 0, -1]

    # 시작 위치와 방향, 
    # 해당 방향으로 이동할 횟수를 설정합니다. 
    curr_x, curr_y = n // 2, n // 2
    move_dir, move_num = 0, 1

    while curr_x or curr_y:
        # move_num 만큼 이동합니다.
        for _ in range(move_num):
            seeker_next_dir[curr_x][curr_y] = move_dir
            curr_x, curr_y = curr_x + dxs[move_dir], curr_y + dys[move_dir]
            seeker_rev_dir[curr_x][curr_y] = move_dir + 2 if move_dir < 2 else move_dir - 2

            # 이동하는 도중 (0, 0)으로 오게 되면,
            # 움직이는 것을 종료합니다.
            if not curr_x and not curr_y:
                break
        
        # 방향을 바꿉니다.
        move_dir = (move_dir + 1) % 4
        # 만약 현재 방향이 위 혹은 아래가 된 경우에는
        # 특정 방향으로 움직여야 할 횟수를 1 증가시킵니다.
        if move_dir == 0 or move_dir == 2:
            move_num += 1


# 격자 내에 있는지를 판단합니다.
def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


def hider_move(x, y, move_dir):
    dxs, dys = [0, 0, 1, -1], [-1, 1, 0, 0]
    # 좌우하상 순서대로 넣어줍니다.

    nx, ny = x + dxs[move_dir], y + dys[move_dir]
    # Step 1.
    # 만약 격자를 벗어난다면
    # 우선 방향을 틀어줍니다.
    if not in_range(nx, ny):
        # 0 <. 1 , 2 <. 3이 되어야 합니다.
        move_dir = 1 - move_dir if move_dir < 2 else 5 - move_dir
        nx, ny = x + dxs[move_dir], y + dys[move_dir]
    
    # Step 2.
    # 그 다음 위치에 술래가 없다면 움직여줍니다.
    if (nx, ny) != seeker_pos:
        next_hiders[nx][ny].append(move_dir)
    # 술래가 있다면 더 움직이지 않습니다.
    else:
        next_hiders[x][y].append(move_dir)


def dist_from_seeker(x, y):
     # 현재 술래의 위치를 불러옵니다.
    seeker_x, seeker_y = seeker_pos
    return abs(seeker_x - x) + abs(seeker_y - y)


def hider_move_all():
    # Step 1. next hider를 초기화해줍니다.
    for i in range(n):
        for j in range(n):
            next_hiders[i][j] = []
    
    # Step 2. hider를 전부 움직여줍니다.
    for i in range(n):
        for j in range(n):
            # 술래와의 거리가 3 이내인 도망자들에 대해서만
            # 움직여줍니다.
            if dist_from_seeker(i, j) <= 3:
                for move_dir in hiders[i][j]:
                    hider_move(i, j, move_dir)
            # 그렇지 않다면 현재 위치 그대로 넣어줍니다.
            else:
                for move_dir in hiders[i][j]:
                    next_hiders[i][j].append(move_dir)

    # Step 3. next hider값을 옮겨줍니다.
    for i in range(n):
        for j in range(n):
            hiders[i][j] = next_hiders[i][j]


# 현재 술래가 바라보는 방향을 가져옵니다.
def get_seeker_dir():
    # 현재 술래의 위치를 불러옵니다.
    x, y = seeker_pos

    # 어느 방향으로 움직여야 하는지에 대한 정보를 가져옵니다.
    move_dir = 0
    if forward_facing:
        move_dir = seeker_next_dir[x][y] 
    else:
        move_dir = seeker_rev_dir[x][y]
    
    return move_dir


def check_facing():
    global forward_facing
    
    # Case 1. 정방향으로 끝에 다다른 경우라면, 방향을 바꿔줍니다.
    if seeker_pos == (0, 0) and forward_facing:
        forward_facing = False
    # Case 2. 역방향으로 끝에 다다른 경우여도, 방향을 바꿔줍니다.
    if seeker_pos == (n // 2, n // 2) and not forward_facing:
        forward_facing = True


def seeker_move():
    global seeker_pos

    x, y = seeker_pos

    # 상우하좌 순서대로 넣어줍니다.
    dxs, dys = [-1, 0, 1, 0], [0, 1, 0, -1]

    move_dir = get_seeker_dir()

    # 술래를 한 칸 움직여줍니다.
    seeker_pos = (x + dxs[move_dir], y + dys[move_dir])
    
    # 끝에 도달했다면 방향을 바꿔줘야 합니다.
    check_facing()


def get_score(t):
    global ans

    # 상우하좌 순서대로 넣어줍니다.
    dxs, dys = [-1, 0, 1, 0], [0, 1, 0, -1]

    # 현재 술래의 위치를 불러옵니다.
    x, y = seeker_pos
    
    # 술래의 방향을 불러옵니다.
    move_dir = get_seeker_dir()
    
    # 3칸을 바라봅니다.
    for dist in range(3):
        nx, ny = x + dist * dxs[move_dir], y + dist * dys[move_dir]
        
        # 격자를 벗어나지 않으며 나무가 없는 위치라면 
        # 도망자들을 전부 잡게 됩니다.
        if in_range(nx, ny) and not tree[nx][ny]:
            # 해당 위치의 도망자 수 만큼 점수를 얻게 됩니다.
            ans += t * len(hiders[nx][ny])

            # 도망자들이 사라지게 됩니다.
            hiders[nx][ny] = []


def simulate(t):
    # 도망자가 움직입니다.
    hider_move_all()

    # 술래가 움직입니다.
    seeker_move()
    
    # 점수를 얻습니다.
    get_score(t)


# 술래잡기 시작 전에
# 구현상의 편의를 위해
# 술래 경로 정보를 미리 계산합니다.
initialize_seeker_path()

# k번에 걸쳐 술래잡기를 진행합니다.
for t in range(1, k + 1):
    simulate(t)

print(ans)
