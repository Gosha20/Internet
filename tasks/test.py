import socket
import requests

if __name__ == '__main__':
	socket.setdefaulttimeout(2)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('127.0.0.1', 8080))
	sock.sendto(b'hello', ('127.0.0.1', 8080))