class Player:
    def __init__(self, x, y, d, s, gun_num, score):
        self.x = x
        self.y = y
        self.d = d
        self.s = s
        self.gun_num = gun_num
        self.score = score


class Gun:
    def __init__(self, x, y, ability, player_num):
        self.x = x
        self.y = y
        self.ability = ability
        self.player_num = player_num


dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
guns = []  # x, y, 공격력, 주인번호 -1
players = []  # x, y, 방향, 초기 능력치, 총 번호, 점수
n, m, k = map(int, input().split())
for i in range(n):
    tmp = list(map(int, input().split()))
    for j in range(n):
        if tmp[j] != 0:
            # guns.append([i, j, tmp[j], -1])
            guns.append(Gun(i, j, tmp[j], -1))
for _ in range(m):
    x, y, d, s = map(int, input().split())
    x, y = x - 1, y - 1
    # players.append([x, y, d, s, -1, 0])
    players.append(Player(x, y, d, s, -1, 0))



def out_of_range(nx, ny):
    return nx < 0 or nx >= n or ny < 0 or ny >= n


def find_move_dir(p_num, players):
    cur_dir = players[p_num].d
    cx, cy = players[p_num].x, players[p_num].y
    nx, ny = cx + dx[cur_dir], cy + dy[cur_dir]
    if out_of_range(nx, ny):
        cur_dir = (cur_dir + 2) % 4
    return cur_dir


def move_player_with_gun(p_num, move_dir, players, guns):
    cx, cy = players[p_num].x, players[p_num].y
    nx, ny = cx + dx[move_dir], cy + dy[move_dir]
    # 방향도 업데이트 해줘야함
    players[p_num].d = move_dir

    players[p_num].x, players[p_num].y = nx, ny
    g_num = players[p_num].gun_num
    # 총을 들고 있다면, 총까지 이동
    if g_num != -1:
        guns[g_num].x, guns[g_num].y = nx, ny
    return nx, ny


def find_another_player(cx, cy, p_num, players):
    another_p_num = -1
    for i in range(m):
        if i == p_num:
            continue
        if [players[i].x, players[i].y] == [cx, cy]:
            another_p_num = i
            break
    return another_p_num


def find_max_gun(cx, cy, guns):
    max_g_num = -1
    max_val = 0
    for i in range(len(guns)):
        if guns[i].player_num != -1:
            continue
        if [guns[i].x, guns[i].y] == [cx, cy]:
            if max_val < guns[i].ability:
                max_g_num = i
                max_val = guns[i].ability
    return max_g_num


def get_gun(max_g_num, p_num, players, guns):
    players[p_num].gun_num = max_g_num
    guns[max_g_num].player_num = p_num
    return


def put_ant_get_max_gun(cx, cy, p_num, players, guns):
    # 해당 위치에 총이 있다는 가정하에 시작
    g_num = players[p_num].gun_num
    # 플레이어가 총을 들고 있다면 일단 내려놈
    if g_num != -1:
        put_gun(p_num, players, guns)
    max_g_num = find_max_gun(cx, cy, guns)
    get_gun(max_g_num, p_num, players, guns)


def get_player_gun_ability(p_num, players, guns):
    gun_ability = 0
    if players[p_num].gun_num != -1:
        g_num = players[p_num].gun_num
        gun_ability = guns[g_num].ability
    return gun_ability


def find_win_lose(p_num, another_p_num, players):
    p_num_s = players[p_num].s
    another_p_num_s = players[another_p_num].s
    p_num_ability = get_player_gun_ability(p_num, players, guns)
    another_p_nun_ability = get_player_gun_ability(another_p_num, players, guns)

    w_p_num, l_p_num = -1, -1
    score = (p_num_s + p_num_ability) - (another_p_num_s + another_p_nun_ability)
    if score > 0:
        w_p_num = p_num
        l_p_num = another_p_num
    elif score < 0:
        w_p_num = another_p_num
        l_p_num = p_num
    else:
        if p_num_s > another_p_num_s:
            w_p_num = p_num
            l_p_num = another_p_num
        else:
            w_p_num = another_p_num
            l_p_num = p_num

    return w_p_num, l_p_num, abs(score)


def get_score(w_p_num, score, players):
    players[w_p_num].score += score
    return


def put_gun(p_num, players, guns):
    g_num = players[p_num].gun_num
    # 총의 주인을 없애고
    guns[g_num].player_num = -1
    # 플레이어가 가지고 있는 총도 없앰
    players[p_num].gun_num = -1


def find_lose_move_dir(l_p_num, players):
    cx, cy, cur_dir = players[l_p_num].x, players[l_p_num].y, players[l_p_num].d
    nx, ny = cx + dx[cur_dir], cy + dy[cur_dir]
    for i in range(4):
        if out_of_range(nx, ny) or find_another_player(nx, ny, -1, players) != -1:
            cur_dir = (cur_dir + 1) % 4
            nx, ny = cx + dx[cur_dir], cy + dy[cur_dir]
        else:
            break
    return cur_dir


def is_gun_there(cx, cy, guns):
    for gun in guns:
        if [gun.x, gun.y] == [cx, cy] and gun.player_num == -1:
            return True
    return False


for _ in range(k):
    for p_num in range(m):
        # 본인이 향하고 있는 방향 또는 격자를 벗어나는 경우 정반대 방향 선택
        move_dir = find_move_dir(p_num, players)
        # 해당 방향으로 해당 방향으로 가지고 있던 총이 있으면 총과 함께 이동
        cx, cy = move_player_with_gun(p_num, move_dir, players, guns)
        # 해당 위치에 다른 플레이어가 있는 지 확인, 없으면 -1 반환
        another_p_num = find_another_player(cx, cy, p_num, players)
        # 해당 위치에 다른 플레이어가 없다면
        if another_p_num == -1:
            # 해당 위치에 총이 있는 지 확인 하고 있다면 최대 공격력을 가진 총으로 변경
            if is_gun_there(cx, cy, guns):
                put_ant_get_max_gun(cx, cy, p_num, players, guns)
        # 해당 위치에 다른 플레이어가 있으면
        else:
            # 기존 능력치 + 총 공격력을 기준으로 승자, 패자 구하고, 얻게될 점수 구함
            w_p_num, l_p_num, score = find_win_lose(p_num, another_p_num, players)
            # 승리자에게 점수 업데이트
            get_score(w_p_num, score, players)
            # 패배자가 총을 들고 있다면, 총을 현재 위치에 버림
            if players[l_p_num].gun_num != -1:
                put_gun(l_p_num, players, guns)
            # 패배자는 원래 가지고 있던 방향 또는 다른 플레이어나 격자밖인 경우 시계방향 돌면서 다음 방향 구하기
            lose_move_dir = find_lose_move_dir(l_p_num, players)
            # 해당 방향으로 가지고 있던 총이 있으면 총과 함께 이동
            lose_cx, lose_cy = move_player_with_gun(l_p_num, lose_move_dir, players, guns)
            if is_gun_there(lose_cx, lose_cy, guns):
                put_ant_get_max_gun(lose_cx, lose_cy, l_p_num, players, guns)
            if is_gun_there(cx, cy, guns):
                put_ant_get_max_gun(cx, cy, w_p_num, players, guns)

for player in players:
    print(player.score, end=" ")