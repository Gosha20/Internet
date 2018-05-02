import socket
import base64
import ssl
import re

regexp = re.compile('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=')
def send_recv(command, sock):
    command_to_send = bytes(command, 'utf-8') + b'\n'
    sock.send(command_to_send)
    data_to_send = b''
    while True:
        try:
            data = sock.recv(1024)
        except socket.timeout:
            break
        data_to_send += data
        if not data:
            break
    return data_to_send.decode(encoding='utf-8')


my_log = 'nabgosha@yandex.ru'
my_passw = 'nabgosha123456'
address = ('pop.yandex.ru', 995)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock = ssl.wrap_socket(sock)
    sock.connect(address)
    sock.settimeout(1)
    print(sock.recv(1024).decode(encoding='utf-8'))
    # print(send_recv("USER", sock))
    # print(send_recv("USER " + my_log, sock))
    # print(send_recv("PASS " + my_passw, sock))
    # print(send_recv("STAT", sock))
    # print(send_recv("LIST", sock))
    # data = send_recv("RETR 1", sock)
    # print(send_recv("QUIT", sock))
    # print(regexp.findall(data))