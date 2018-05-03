import socket
import base64
import ssl
import re
from configparser import ConfigParser

import sys

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

LOGIN = 'nabgosha@yandex.ru'
PASSWORD = 'nabgosha123456'
ADDRESS = ('pop.yandex.ru', 995)

def get_headers(input):
    result = b''
    headers = input.split('\n\r\n')[0]
    print(re.findall(r'From: .*?\n',headers)[0])
    print(re.findall(r'To: .*?\n',headers)[0])
    print(re.findall(r'Date: .*?\n',headers)[0])
    print(re.findall(r'Subject: .*?\n', headers)[0])

COMMANDS = {
    'Get headers' : get_headers
}


def main():
    global LOGIN,PASSWORD,ADDRESS
    parser = ConfigParser()
    with open('config.cfg', 'r', encoding='utf-8') as f:
        parser.readfp(f)
    LOGIN = parser['Account_from']['Login']
    PASSWORD = parser['Account_from']['Password']
    ADDRESS = (parser['Account_from']['Mail'], int(parser['Account_from']['Port']))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = ssl.wrap_socket(sock)
        sock.connect(ADDRESS)
        sock.settimeout(1)
        print(sock.recv(1024).decode(encoding='utf-8'))
        print(send_recv("USER " + LOGIN, sock))
        print(send_recv("PASS " + PASSWORD, sock))
        while True:
            command = sys.stdin.readline().rstrip()
            if command != 'QUIT':
                (COMMANDS[command](send_recv("RETR 1", sock)))
            else:
                break
        # print(send_recv("LIST", sock))
        # data = send_recv("RETR 1", sock)
        # print(data)
        print(send_recv("QUIT", sock))
        # print(regexp.findall(data))

if __name__ == '__main__':
    main()