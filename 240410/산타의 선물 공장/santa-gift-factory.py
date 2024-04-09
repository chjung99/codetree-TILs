class Node:
    def __init__(self, id, w):
        self.id = id
        self.w = w
        self.left = None
        self.right = None


class LinkedList:
    def __init__(self, head, tail, crash, size):
        self.head = head
        self.tail = tail
        self.crash = crash
        self.size = size

    def pop_front(self):
        if self.size == 1:
            tmp = self.head
            self.head = None
            self.tail = None
            self.size = 0
            return tmp
        else:
            tmp = self.head
            nxt = self.head.right
            self.head = nxt
            self.head.left = None
            self.size -= 1
            return tmp

    def pop_back(self):
        if self.size == 1:
            tmp = self.head
            self.head = None
            self.tail = None
            self.size = 0
            return tmp
        else:
            tmp = self.tail
            prev = self.tail.left
            self.tail = prev
            self.tail.right = None
            self.size -= 1
            return tmp

    def push_back(self, node):
        if self.size == 0:
            node.left = None
            node.right = None
            self.head = node
            self.tail = node
        else:
            node.left = self.tail
            node.right = None

            self.tail.right = node

            self.tail = node

        self.size += 1

    def push_front(self, node):
        if self.size == 0:
            node.left = None
            node.right = None
            self.head = node
            self.tail = node
        else:
            node.left = None
            node.right = self.head

            self.head.left = node

            self.head = node

            self.size += 1

    def pop_node(self, node):
        if self.size == 1:
            self.head = None
            self.tail = None
            self.size = 0
        else:
            if self.head == node:
                self.pop_front()
            elif self.tail == node:
                self.pop_back()
            else:
                cur = node
                prev = cur.left
                nxt = cur.right
                prev.right = nxt
                nxt.left = prev
                self.size -= 1

    def cut_nodes(self, node):
        if self.size == 1:
            return
        else:
            if self.head == node:
                return
            elif self.tail == node:
                self.push_front(self.pop_back())
            else:
                cur = node
                prev = cur.left
                self.tail.right = self.head
                self.head.left = self.tail
                prev.right = None

                self.tail = prev
                cur.left = None
                self.head = cur


def set_factory(n, m, ids, ws, belts, table, nodes):
    cnt = n // m
    start, end = 0, cnt
    for i in range(1, m + 1):
        ids_tmp = ids[start:end]
        ws_tmp = ws[start:end]
        for j in range(cnt):
            nodes[i][j].id = ids_tmp[j]
            nodes[i][j].w = ws_tmp[j]
            table[i][nodes[i][j].id] = nodes[i][j]  # 노드
        for j in range(cnt):
            if j != 0:
                nodes[i][j].left = nodes[i][j - 1]
            if j != cnt - 1:
                nodes[i][j].right = nodes[i][j + 1]
        belts[i].head = nodes[i][0]
        belts[i].tail = nodes[i][cnt - 1]
        belts[i].crash = False
        belts[i].size = cnt

        start = end
        end += cnt


def pop_present(w_max, belts, table):
    total_weight = 0
    for i in range(1, m + 1):
        if belts[i].crash or belts[i].size == 0:
            continue
        node = belts[i].pop_front()
        if node.w <= w_max:
            total_weight += node.w
            table[i].pop(node.id)
        else:
            belts[i].push_back(node)
    return total_weight


def remove_present(r_id, belts, table):
    for i in range(1, m + 1):
        if r_id in table[i].keys():
            node = table[i][r_id]
            belts[i].pop_node(node)

            table[i].pop(r_id)
            return r_id

    return -1


q = int(input())
belts = []
table = []
nodes = []


def check_present(f_id, belts, table):
    for i in range(1, m + 1):
        if f_id in table[i].keys():
            node = table[i][f_id]
            belts[i].cut_nodes(node)
            return i

    return -1


def move_nodes(b_num, nxt_num, belts, table):
    if belts[b_num].size == 0:
        return
    elif belts[nxt_num].size == 0:
        belts[nxt_num] = belts[b_num]
        table[nxt_num].update(table[b_num])
    else:
        belts[nxt_num].tail.right = belts[b_num].head
        belts[b_num].head.left = belts[nxt_num].tail

        belts[b_num].head = None
        belts[b_num].tail = None
        belts[b_num].size = 0

        table[nxt_num].update(table[b_num])
        table[b_num] = {}


def break_belt(b_num, belts, table):
    if belts[b_num].crash:
        return -1
    else:
        nxt_num = b_num % m + 1
        while belts[nxt_num].crash:
            nxt_num = nxt_num % m + 1
        belts[b_num].crash = True
        move_nodes(b_num, nxt_num, belts, table)
        return b_num


for _ in range(q):
    tmp = list(map(int, input().split()))
    opt = tmp[0]

    if opt == 100:
        n, m = tmp[1], tmp[2]
        cnt = n // m
        belts = [LinkedList(None, None, True, 0) for _ in range(m + 1)]
        nodes = [[Node(0, 0) for _ in range(cnt)] for __ in range(m + 1)]
        table = [{} for _ in range(m + 1)]
        ids, ws = tmp[3: 3 + n], tmp[3 + n:3 + 2 * n]

        set_factory(n, m, ids, ws, belts, table, nodes)
    elif opt == 200:
        w_max = tmp[1]
        print(pop_present(w_max, belts, table))
    elif opt == 300:
        r_id = tmp[1]
        print(remove_present(r_id, belts, table))
    elif opt == 400:
        f_id = tmp[1]
        print(check_present(f_id, belts, table))
    elif opt == 500:
        b_num = tmp[1]
        print(break_belt(b_num, belts, table))