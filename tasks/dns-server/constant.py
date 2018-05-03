import socket

TYPES = {
    1: 'A',
    2: 'NS',
    6: 'SOA',
    28: 'AAAA'
}
R_TYPES = {
    'A': 1,
    'NS': 2,
    'SOA': 6
}


def url_to_bytes(url):
    chuncs = url.split('.')
    count_bytes = 0
    result = b''
    for chunc in chuncs:
        count_simbol = len(chunc)
        result += int.to_bytes(count_simbol, 1, 'big')
        count_bytes+=1
        for symbol in chunc:
            result += bytes(symbol, 'utf-8')
            count_bytes += 1
    return result, count_bytes
# 212.193.163.7
def get_info(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, ('212.193.163.7', 53))
    sock.settimeout(2)
    try:
        recieve = sock.recvfrom(1024)[0]
        return recieve, True
    except socket.timeout:
        print('server unrichable')
        return b'', False
