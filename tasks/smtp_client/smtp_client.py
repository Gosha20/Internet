import socket
import ssl
import base64

ipPort = ('smtp.yandex.ru', 465)

image = base64.b64encode(open('picture.png', 'rb').read())


def send_recv(str, s):
    str += b'\n'
    s.send(str)
    return s.recv(1024).decode(encoding='utf-8')


def create_msg():
    return b'''From: nabgosha@yandex.ru
To: nabgosha@yandex.ru
Subject: Test Msg1
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="bound.195987.web7g.yandex.ru"

--bound.195987.web7g.yandex.ru
Content-Type: text/plain;

Some Text
--bound.195987.web7g.yandex.ru
Content-Disposition: attachment; filename="test-img.jpg"
Content-Transfer-Encoding: base64
Content-Type: image/png; name="picture.png"

''' + image + b'\n--bound.195987.web7g.yandex.ru--\n.'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s = ssl.wrap_socket(s)
    s.connect(ipPort)
    print(s.recv(1024))
    login = base64.b64encode(b'nabgosha@yandex.ru')
    password = base64.b64encode(b'nabgosha123456')
    print(send_recv(b'EHLO nabgosha@yandex.ru', s))
    print(send_recv(b'AUTH LOGIN', s))
    print(send_recv(login, s))
    print(send_recv(password, s))
    print(send_recv(b'MAIL FROM: nabgosha@yandex.ru', s))
    print(send_recv(b'RCPT TO: nabgosha@yandex.ru', s))
    print(send_recv(b'DATA', s))
    print(send_recv(create_msg(), s))
