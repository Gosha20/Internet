import socket
import base64
import ssl
import re
from configparser import ConfigParser
import sys

BOUNDARY = "#-#-#-#--#-#-#-#--#-#-#-#--#-#-#-#--#-#-#-#--#-#-#-#--#-#-#--#-#-"
regex = re.compile('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=')

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
    data = data_to_send.decode(encoding='utf-8')
    if data.startswith('+'):
        return data
    else:
        print(data)
        sys.exit(0)


LOGIN = 'nabgosha@yandex.ru'
PASSWORD = 'nabgosha123456'
ADDRESS = ('pop.yandex.ru', 995)


def get_headers(input):
    print(func_for_parse(r'(From: )=\?utf-8\?B\?(.*?)\?=', input, 'From: '))
    print(re.findall(r'To: .*?\n', input)[0])
    print(re.findall(r'Date: .*?\n', input)[0])
    print(func_for_parse('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=', input, 'Subject: '))


def write(masbytes, filename):
    result = base64.b64decode(masbytes)
    with open(filename, 'wb') as file:
        file.write(result)


def get_full_message(message):
    boundary = re.search('boundary="(.*?)"',message).group(1).replace('.','\.')
    blocks = re.split('--'+boundary, message)[1:-1]
    for block in blocks:
        headers, masbytes = block.split('\r\n\r\n')
        if '\r\nContent-Disposition: attachment;' in headers:
            print(headers)
            filename = re.findall('filename="(.*)"', headers)[0]
            write(bytes(masbytes, 'utf-8'), filename)
            print('file download, you can open them')
        else:
            print(headers)
            text_message = base64.b64decode(masbytes).decode()
            print(text_message)


def func_for_parse(regex, input_str, header):
    if re.findall(header + '=\?utf-8\?B', input_str) or re.findall(header + '=\?UTF-8\?B', input_str):
        input_str=input_str.replace('UTF-8','utf-8')
        string = [x[1] for x in re.findall(regex, input_str)]
        string = [bytes(x, 'utf-8') for x in string]
        return header + ''.join([base64.b64decode(x).decode('utf-8') for x in string])
    else:
        return re.findall(header + '.*\n', input_str)[0]


def main():
    global LOGIN, PASSWORD, ADDRESS
    parser = ConfigParser()
    with open('config.cfg', 'r', encoding='utf-8') as f:
        parser.readfp(f)
    LOGIN = parser['Account_from']['Login']
    PASSWORD = parser['Account_from']['Password']
    ADDRESS = (parser['Account_from']['Mail'], int(parser['Account_from']['Port']))
    # try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = ssl.wrap_socket(sock)
        sock.connect(ADDRESS)
        sock.settimeout(1)
        print(sock.recv(1024).decode(encoding='utf-8'))
        print(send_recv("USER " + LOGIN, sock))
        print(send_recv("PASS " + PASSWORD, sock))
        while True:
            command = sys.stdin.readline().rstrip()
            if command.startswith('RETR'):
                print(BOUNDARY)
                print(send_recv(command, sock))
                print(BOUNDARY)
            elif command.startswith('HEAD'):
                print(BOUNDARY)
                get_headers(send_recv('TOP ' + command.split()[1], sock))
                print(BOUNDARY)
            elif command.startswith('TOP'):
                print(BOUNDARY)
                print(send_recv(command, sock))
                print(BOUNDARY)
            elif command.startswith('FULL '):
                print(BOUNDARY)
                get_full_message(send_recv('RETR '+ command.split()[1], sock))
                print(BOUNDARY)
            elif command == 'STAT':
                print(BOUNDARY)
                print(send_recv("STAT", sock))
                print(BOUNDARY)
            elif command.startswith('LIST'):
                print(BOUNDARY)
                adds = '' if len(command.split()) < 2 else " " + command.split()[1]
                print(send_recv("LIST" + adds, sock))
                print(BOUNDARY)
            elif command == 'QUIT':
                print(send_recv("QUIT", sock))
                break
            else:
                print('unknown command')
                print(BOUNDARY)
    # except Exception:
    #     print('cant connect')


if __name__ == '__main__':
    main()
