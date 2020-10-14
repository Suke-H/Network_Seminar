import ipaddress
from tqdm import tqdm
import numpy as np

class Node:
    ''' ノード '''
    def __init__(self, key): 
        self.key = key 
        self.left = None 
        self.right = None

class radix_tree:
    ''' radix_tree '''

    def __init__(self, address_list):
        self.root = Node(None)
        for i, node in enumerate(address_list):
            self.insert(node, i+1)

    def insert(self, address, index):
        ''' ノードを挿入 '''
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

    def search(self, address):
        ''' ノードの検索 '''
        # /0ならrootのインデックスを返す
        if address == '':
            print("omg")
            return self.root.key
        
        # インデックスの候補
        candidate = self.root.key
        tmp = self.root

        for bit in address:
            # 1なら右へ
            if bit == '1':
                # ノードがなかったら終了
                if tmp.right is None:
                    break

                tmp = tmp.right

            # 0なら左へ
            else:
                if tmp.left is None:
                    break

                tmp = tmp.left

            # 最後にたどったノードが持つkeyがインデックスになる
            if tmp.key is not None:
                candidate = tmp.key

            print(tmp.key)

        return candidate

def read_txt(path):
    ''' txtファイルから全アドレスを読み取る '''

    # リストに読み込み
    with open(path) as f:
        l = f.readlines()

    # 無駄な文字を消す
    for i in range(len(l)):
        if l[i].count(' ') >= 1:
            l[i] = l[i][l[i].find(' ')+1:]
            l[i] = l[i][:l[i].find(' ')]
        else:
            l[i] = l[i].replace('\n', '')

    l = [s for s in l if s != '']

    return l

def align_address(address):
    '''
    アドレスを同じ形式に変換

    例：
    1.4/22   -> 0000000100000100000000  
    1.0.5/24 -> 000000010000000000000101
    '''

    # 特殊なデータへの対応(/がない,/の後に数字がない)
    if address.count('/') == 0 or address.find('/') == len(address)-1:
        address_part = address.replace('/', '')
        mask_part = '32'

    else:
        # /でaddressとmaskに分ける
        mid = address.find('/')
        address_part = address[:mid]
        mask_part = address[mid+1:]

    # .の数に応じて0埋め
    # 例：1.0.4 -> 1.0.4.0
    dot_num = address_part.count('.')
    for j in range(3-dot_num):
        address_part = address_part + '.0'

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
    ''' txtファイルからアドレスを読み取る前処理 '''

    data_list = read_txt(path)
    print(np.random.choice(data_list, 5, replace=False))
    address_list = []

    for data in tqdm(data_list):
        address_list.append(align_address(data))

    return address_list, data_list

if __name__ == '__main__':
    # txtファイルからアドレスを読み取る
    address_list, _ = pre_process('route.txt')
    # address_list, _ = pre_process('route-01.txt')
    # 全アドレスをradix_treeに格納
    RT = radix_tree(address_list)

    # 検索するアドレスの読み込み
    # (route_search.txtの記載内容: 
    #  41.74.1.1
    #  66.31.10.3
    #  133.5.1.1
    #  209.143.75.1
    #  221.121.128.1
    # )
    search_list, data_list = pre_process('route_search.txt')

    # 検索
    for (query, data) in zip(search_list, data_list):
        result_index = RT.search(query)
        print('{}: {}'.format(data, result_index))
