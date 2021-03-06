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
        print("DROP SESSION, PLS WORK WITHOUT MISSTAKES")
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
    boundary = re.search('boundary="(.*?)"', message)
    if boundary:
        boundary = boundary.group(1).replace('.', '\.')
        blocks = re.split('--' + boundary, message)[1:-1]
        split_by = '\r\n\r\n'
    else:
        blocks = [message]
        split_by = '\r\n\r\n'
    for block in blocks:
        headers, masbytes = block.split(split_by)
        if '\r\nContent-Disposition: attachment;' in headers:
            print(headers)
            filename = re.findall('filename="(.*)"', headers)[0]
            write(bytes(masbytes, 'utf-8'), filename)
            print('file download, you can open them')
        else:
            if 'Content-Transfer-Encoding: base64' in headers:
                print(headers)
                text_message = base64.b64decode(masbytes).decode()
            else:
                text_message = masbytes
            if text_message[0] == '.':
                text_message = text_message[1:]
            text_message = text_message.replace('\n..', '\n.')
            print(text_message.rstrip()[:-1])


def func_for_parse(regex, input_str, header):
    if re.findall(header + '=\?utf-8\?B', input_str, re.IGNORECASE):
        string = [x[1] for x in re.findall(regex, input_str, re.IGNORECASE)]
        string = [bytes(x, 'utf-8') for x in string]
        return header + ''.join([base64.b64decode(x).decode('utf-8') for x in string])
    else:
        return re.findall(header + '.*\n', input_str, re.IGNORECASE)[0]


def main():
    global LOGIN, PASSWORD, ADDRESS
    parser = ConfigParser()
    with open('config.cfg', 'r', encoding='utf-8') as f:
        parser.readfp(f)
    LOGIN = parser['Account_from']['Login']
    PASSWORD = parser['Account_from']['Password']
    ADDRESS = (parser['Account_from']['Mail'], int(parser['Account_from']['Port']))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = ssl.wrap_socket(sock)
        sock.settimeout(1)
        try:
            sock.connect(ADDRESS)
            print(sock.recv(1024).decode(encoding='utf-8'))
            print(send_recv("USER " + LOGIN, sock))
            print(send_recv("PASS " + PASSWORD, sock))
        except socket.error:
            print('cant connect')
            sys.exit(0)
        except Exception:
            print('fail on try connect')
            sys.exit(0)

        while True:
            command = sys.stdin.readline().rstrip()
            if command.startswith('RETR'):
                print(BOUNDARY)
                print(send_recv(command, sock))
                print(BOUNDARY)
                continue
            if command.startswith('HEAD'):
                print(BOUNDARY)
                get_headers(send_recv('TOP ' + command.split()[1], sock))
                print(BOUNDARY)
                continue
            if command.startswith('TOP'):
                print(BOUNDARY)
                print(send_recv(command, sock))
                print(BOUNDARY)
                continue
            if command.startswith('FULL '):
                print(BOUNDARY)
                get_full_message(send_recv('RETR ' + command.split()[1], sock))
                print(BOUNDARY)
                continue
            if command == 'STAT':
                print(BOUNDARY)
                print(send_recv("STAT", sock))
                print(BOUNDARY)
                continue
            if command.startswith('LIST'):
                print(BOUNDARY)
                adds = '' if len(command.split()) < 2 else " " + command.split()[1]
                print(send_recv("LIST" + adds, sock))
                print(BOUNDARY)
                continue
            if command == 'QUIT':
                print(send_recv("QUIT", sock))
                break
            print('unknown command')
            print(BOUNDARY)


if __name__ == '__main__':
    main()
