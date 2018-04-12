import socket


TYPES = {
    1: 'A',
    2: 'NS',
    6: 'SOA'
}

def get_info(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, ('212.193.163.7', 53))
    sock.settimeout(2)
    try:
        recieve = sock.recvfrom(1024)[0]
        return recieve
    except TimeoutError:
        print("server ne otvechaet")

flags_to_send = b'\x81\x80'