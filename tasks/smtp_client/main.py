import os
import base64
import re
import ssl
import socket
from configparser import ConfigParser

CONFIG_FILE = 'config.cfg'
LETTER_FILE = 'letter.txt'
TYPES_CONTENTS = {'png': 'image/png', 'jpg': 'image/jpeg', 'txt': 'text/plain'}
LOGIN = base64.b64encode(b'nabgosha@yandex.ru')
PASSWORD = base64.b64encode(b'nabgosha123456')
IP_PORT = ('smtp.yandex.ru', 465)
PATH_TO_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), 'for_files'))

class Mail:
    def __init__(self, from_name, to_name, subj, attachment,letter):
        self.from_name = from_name
        self.to_names = to_name
        self.subject = subj
        self.attachments = attachment
        self.letter = self.create_letter_in_byte(letter)

    def get_from(self):
        return bytes(self.from_name, 'utf-8')

    def get_to(self):
        return bytes(self.to_names, 'utf-8')

    def get_subj(self):
        return b'=?utf-8?B?' + base64.b64encode(bytes(self.subject, 'utf-8')) + b'?='

    def create_letter_in_byte(self, letter):
        with open(os.path.join(PATH_TO_DIR, letter), 'r', encoding='utf-8') as f:
            message = f.read()
            if message[0] == '.':
                message = '.' + message
            message = message.replace('\n.', '\n..')

            letter = message.encode()
            return letter

    def create_msg(self):
        result = b'From: ' + self.get_from() + b'\n'
        result += b'To: ' + self.get_to() + b'\n'
        result += b'Subject: ' + self.get_subj() + b'\n'
        result += b'MIME-Version: 1.0' + b'\n'
        if len(self.attachments) != 0:
            result += b'Content-Type: multipart/mixed; boundary="boundary"\n\n'
            result += b'--boundary\n'
        result += b'Content-Type: text/plain;\n\n'
        result += self.letter + b'\n'
        if len(self.attachments) != 0:
            result += b'--boundary'
            result += b'\n' + self.attachments
            result += b'--'
        result+=b'\n.'
        return result


def settings():
    global PASSWORD

    path_to_config = os.path.join(PATH_TO_DIR, CONFIG_FILE)
    parser = ConfigParser()
    parser.read(path_to_config, encoding='utf-8')

    from_name = parser.get("Account_from", 'login')
    PASSWORD = base64.b64encode(parser.get("Account_from", 'password').encode())
    to_names = parser.get("Account_to", 'login')
    subject = parser.get("Message", 'subject')
    attachs = parser.get("Message", "Attachments")
    attachments_ready_to_send = b''
    for attachment in attachs.split('\n')[1:]:
        file = attachment.split(', ')[0]
        mime_type = attachment.split(', ')[1]
        with open(os.path.join(PATH_TO_DIR, file), 'rb') as f:
            file_b = base64.b64encode(f.read())
            attachments_ready_to_send += f'Content-Disposition: attachments; filename="{file}"'.encode() + b'\n'
            attachments_ready_to_send += b'Content-Transfer-Encoding: base64' + b'\n'
            attachments_ready_to_send += f'Content-Type: {mime_type}; name="{file}"'.encode()
            attachments_ready_to_send += b'\n\n' + file_b + b'\n'
            attachments_ready_to_send += b'--boundary'

    return Mail(from_name, to_names, subject, attachments_ready_to_send, parser.get('Letter', 'File_name'))


def send_recv(str, sock):
    str += b'\n'
    sock.send(str)
    return sock.recv(1024).decode(encoding='utf-8')


if __name__ == '__main__':
    mail = settings()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = ssl.wrap_socket(sock)
        sock.connect(IP_PORT)
        sock.settimeout(30)
        try:
            print(sock.recv(1024))
            print(send_recv(b'EHLO friens', sock))
            print(send_recv(b'AUTH LOGIN', sock))
            print(send_recv(LOGIN, sock))
            print(send_recv(PASSWORD, sock))
            print(send_recv(b'MAIL FROM: ' + mail.get_from(), sock))
            for recipient in mail.to_names.split(','):
                print(send_recv(b'RCPT TO: ' + recipient.encode(), sock))
            print(send_recv(b'DATA ', sock))
            print(send_recv(mail.create_msg(), sock))
            print('message is send')
        except socket.timeout:
            print('Some problem sending msg')
