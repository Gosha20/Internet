import socket
import struct
import argparse

def main ():
    argParser = argparse.ArgumentParser()
    argParser.add_argument('address', type=str, help="ipv4 or name address")
    argParser.add_argument('--start', type=int, help="left port zone")
    argParser.add_argument('--end', type=int, help="right port zone")
    args = argParser.parse_args()
    portscan=PortScaner(args.address)
    for i in range(args.start, args.end+1):
        port, protocol = portscan.scan_tcp('',i)
        print(f'TCP port {port} is open. Protocol: {protocol}')

class PortScaner:

    Tcp = {
        'POP3': b'AUTH',
        'DNS': 
        }
    UDP = {
        'SNTP': b'\x1b' + 47 * b'\0'
    }
    def __init__(self, dest_name):
        self.dest = dest_name

    def scan_tcp(self, packet, port):
        socket.setdefaulttimeout(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.dest,port))
            except socket.timeout:
                return (port, None)
            sock.send(PortScaner.Tcp['POP3'])
            packet = sock.recv(128)
            if packet.startswith(b'+'):
                return (port, 'Pop3')
if __name__ == '__main__':
    main()