import numpy as np

# 符号表
codes = {'a': 0b0000000,
        'b': 0b0001011,
        'c': 0b0010111,
        'd': 0b0011100,
        'e': 0b0100101,
        'f': 0b0101110,
        'g': 0b0110010,
        'h': 0b0111001,
        'i': 0b1000110,
        'j': 0b1001101,
        'k': 0b1010001,
        'l': 0b1011010,
        'm': 0b1100011,
        'n': 0b1101000,
        'o': 0b1110100,
        'p': 0b1111111}

# 符号化
def encode(data):
    return codes[data]

# 復号化
def decode(data):
    candidate = []

    # ハミング距離が1以下の文字を選出
    for k, v in codes.items():
        if humming(data, v) <= 1:
            candidate.append(k)

    # 候補が2以上 or 0なら?を出力
    if len(candidate) >= 2 or len(candidate) == 0:
        return '?'

    else:
        return candidate[0]

# 伝送(確率でnビット反転)
def denso(data, n):
    # 一様な確率で0か1を出力
    a = np.random.choice(2)

    if a == 1:
        # 7桁のうちいずれかn個を反転
        b = np.random.choice(7, n, replace=False)
        error_data = bit_error(data, b)
        print("{} -> {}".format(bin(data), bin(error_data)))
        return error_data

    else:
        print("反転なし")
        return data

# aとbのハミング距離
def humming(a, b):
    return bin(a ^ b).count('1')

# bit_listにある桁を反転させる
# 例 data     : 0b0001
#    bit_list : [0, 2]
#    出力     : 0b0100
def bit_error(data, bit_list):

    for bit in bit_list:
        data = data ^ (1 << bit)

    return data

if __name__ == '__main__':
    # 入力
    input_data = 'o'
    # 符号化
    coding_data = encode(input_data)
    # 伝送
    trans_data = denso(coding_data, 1)
    # 復号化
    decode_data = decode(trans_data)
    print(decode_data)
