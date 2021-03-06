import socket
import argparse

def parse_args():
    """
    実行例：
    python 3_1_udp_server.py --ip 127.0.0.2 --port 2000
    python 3_1_udp_server.py (ipとportはデフォルト値の127.0.0.2および50000になる)
    """
    parser = argparse.ArgumentParser(description='UCP Server')

    parser.add_argument('--ip', default='127.0.0.2', help='IP address')
    parser.add_argument('--port', default=50000, type=int, help='Port number')
    
    return parser.parse_args()

args = parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((args.ip, args.port))
    while True:
        data, address = s.recvfrom(1024)
        print("data: {}, address: {}".format(data, address))