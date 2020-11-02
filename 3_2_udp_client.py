import socket
import argparse

def parse_args():
    """
    実行例：
    python 3_2_udp_client.py --ip 127.0.0.2 --port 2000
    python 3_2_udp_client.py (ipとportはデフォルト値の127.0.0.2および50000になる)
    """
    parser = argparse.ArgumentParser(description='UCP Client')

    parser.add_argument('--ip', default='127.0.0.2', help='IP address')
    parser.add_argument('--port', default=50000, type=int, help='Port number')
    
    return parser.parse_args()

args = parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b'sent a message via UDP', (args.ip, args.port))