import socket
from select import select
from urllib.request import urlopen

import requests
import socketserver
import http.server

BLACK_LIST = ['reklama.e1.ru',
			  'googleadservices.com',
			  'doubleclick.net',
			  'reklama.ngs.ru',
			  'an.yandex.ru',
			  'mc.yandex.ru',
			  'mail.ru']
PORT = 8080


class SimpleHttpProxiHeandler(http.server.SimpleHTTPRequestHandler):
	def do_CONNECT(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			addr, port = self.path.split(':')
			port = int(port)
			try:
				if in_blacklist(addr):
					self.send_error(454, 'Page in blacklist')
					return
				sock.connect((addr, port))
				self.send_response(200, 'Connection established')
				self.send_header('Proxy-agent', 'Test HTTP proxy')
				self.end_headers()
				self.
				sock.send(self.do_GET())

			except socket.error:
				self.send_error(404, 'Not Found')
			except ConnectionError:
				pass
			finally:
				sock.close()

	def do_GET(self):
		self.copyfile(urlopen(self.path), self.wfile)


def in_blacklist(host):
	for item in BLACK_LIST:
		if item in host:
			return True
	return False


if __name__ == '__main__':
	Handler = SimpleHttpProxiHeandler
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('', 8080))
# sock.listen(1)
# while True:
# 	conn, addr = sock.accept()
# 	while True:
# 		data_to_send = b''
# 		try:
# 			data = conn.recv(128)
# 		except socket.timeout:
# 			break
# 		data_to_send += data
# 		if not data:
# 			break
# 		print(data)
