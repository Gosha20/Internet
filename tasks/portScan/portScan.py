import socket
import struct
import argparse
from multiprocessing import Pool
import re

def main():
	argParser = argparse.ArgumentParser()
	argParser.add_argument('address', type=str, help="ipv4 or name address")
	argParser.add_argument('--start', type=int, help="left port zone")
	argParser.add_argument('--end', type=int, help="right port zone")
	args = argParser.parse_args()
	portscan = PortScanner(args.address)
	process_pool = Pool(processes=2)
	for port, protocol in process_pool.imap(portscan.scan_tcp, range(args.start, args.end + 1)):
		if protocol:
			print(f'TCP port {port} is open. Protocol: {protocol}')

	for port, protocol in process_pool.imap(portscan.scan_udp, range(args.start, args.end + 1)):
		if protocol:
			print(f'UDP port {port} is open. Protocol: {protocol}')


class PortScanner:

	SEQ_NUMBER_DNS = b'\x20\x25'

	dns_packet = SEQ_NUMBER_DNS + b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x02e1\x02ru\x00\x00\x01\x00\x01'
	TCP = {
		'POP3': b'AUTH',
		'DNS': struct.pack('!H', len(dns_packet))+dns_packet,
		'HTTP': b'GET http://solod.zz.mu/ http/1.1\r\n\r\n',
		'SMTP':b'EHLO'
	}
	UDP = {
		'DNS': struct.pack('!H', len(dns_packet))+dns_packet,
		'SNTP': b'\x1b' + 47 * b'\0'
	}

	CHECKER_PROTOCOLS = {
		'SMTP': lambda packet: re.match(b'[0-9]{3}', packet[0:3]),
		'POP3': lambda packet: packet.startswith(b'+'),
		'HTTP': lambda packet: b'HTTP' in packet,
		'SNTP': lambda packet: PortScanner.sntp_check(packet),
		'DNS': lambda packet: packet[2:].startswith(PortScanner.SEQ_NUMBER_DNS)
	}

	def __init__(self, dest_name):
		self.dest = dest_name

	def scan_udp(self, port):
		socket.setdefaulttimeout(0.1)
		for protocol, packet in PortScanner.UDP.items():
			with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
				sock.sendto(packet, (self.dest, port))
				try:
					if PortScanner.CHECKER_PROTOCOLS[protocol](sock.recv(128)):
						return port, protocol
				except socket.error:
					continue
		return port, None

	def scan_tcp(self, port):
		socket.setdefaulttimeout(0.1)
		for protocol, packet in PortScanner.TCP.items():
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				try:
					sock.connect((self.dest, port))
				except socket.timeout:
					return port, None
				try:
					sock.send(packet)
					recv_packet = sock.recv(512)
					if PortScanner.CHECKER_PROTOCOLS[protocol](recv_packet):
						return port, protocol
					continue
				except socket.error:
					continue

		return port, 'dont know protocol'
	@staticmethod
	def sntp_check(packet):
		try:
			struct.unpack("!12I", packet)
			return True
		except struct.error:
			return False

if __name__ == '__main__':
	main()
