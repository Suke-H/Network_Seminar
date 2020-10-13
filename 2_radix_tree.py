import ipaddress

class Node:
    """ ノード """
    def __init__(self, key): 
        self.key = key 
        self.left = None 
        self.right = None

class radix_tree:
    """ radix_tree """

    def __init__(self, address_list):
        self.root = Node(None)
        for i, node in enumerate(address_list):
            self.insert(node, i+1)

    def insert(self, address, index):
        # /0はrootへ
        if address == '':
            self.root = Node(index)
            return

        tmp = self.root

        for bit in address:

            # 1なら右へ
            if bit == '1':
                # ノードがなかったら追加
                if tmp.right is None:
                    tmp.right = Node(None)
                    tmp = tmp.right

            # 0なら左へ
            else:
                if tmp.left is None:
                    tmp.left = Node(None)
                    tmp = tmp.left

        tmp.key = index

def read_txt(path):
    """ txtファイルから全アドレスを読み取る """

    # リストに読み込み
    with open(path) as f:
        l = f.readlines()

    # \nと空白を消す
    for i in range(len(l)):
        l[i] = l[i].replace('\n', '')
        l[i] = l[i].replace(' ', '')

    return l

def align_address(address):
    """
    アドレスを同じ形式に変換

    例：
    1.4/22   -> 0000000100000100000000  
    1.0.5/24 -> 000000010000000000000101
    """

    # /でaddressとmaskに分ける
    mid = address.find('/')
    address_part = address[:mid]
    mask_part = address[mid+1:]

    # .の数に応じて0埋め
    # 例：1.0.4 -> 1.0.4.0
    dot_num = address_part.count('.')
    for j in range(3-dot_num):
        address_part = address_part + ".0"

    # 32ビットを10進数に直す
    address_num = int(ipaddress.ip_address(address_part))
    # 2進数(文字列)に直す
    address_str = bin(address_num)
    address_str = address_str.replace('0b', '')
    # 32bitになるように先頭から0埋め
    address_str = '0'*(32-len(address_str)) + address_str
    # サブネットマスクを通す
    address_str = address_str[:int(mask_part)]

    return address_str

def pre_process(path):
    """ txtファイルからアドレスを読み取る前処理 """

    data_list = read_txt(path)

    address_list = []

    for data in data_list:
        address_list.append(align_address(data))

    return address_list
            
address_list = pre_process("route_test.txt")
radix_tree(address_list)
