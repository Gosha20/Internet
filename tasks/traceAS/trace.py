import os
import socket
import whois
from argparse import ArgumentParser
import sys
def trace(dist_ip):
    "seq_num=180 id=1"
    icmp_packet = b'\x08\x00\xf7\x4a\x00\x01\x00\xb4'
    connetion = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    ttl = 1
    cur_ip = None
    connetion.settimeout(10)
    while ttl != 30 and cur_ip != dist_ip:
        connetion.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        connetion.sendto(icmp_packet, (dist_ip, 33434))
        try:
            packet, ipPort = connetion.recvfrom(1024)
            cur_ip = ipPort[0]
            message = '%d)   %i' % (ttl, cur_ip)
            if public_ip(cur_ip):
                message += ' ' + str(whois.simple_whois(cur_ip))
            yield message + " its not public ip"
        except socket.timeout:
            yield '*****   TimeOUT   *****'
        ttl += 1
    connetion.close()

def public_ip(ip):
    local_ip_addresses_diapasons = (
        ('10.0.0.0', '10.255.255.255'),
        ('127.0.0.0', '127.255.255.255'),
        ('172.16.0.0', '172.31.255.255'),
        ('192.168.0.0', '192.168.255.255'))

    for diapason in local_ip_addresses_diapasons:
        if diapason[0] <= ip <= diapason[1]:
            return False
    return True

def init_parser():
    parser = ArgumentParser(prog="trace.py")
    parser.add_argument("-ip", action="store", help="IP address, to which need to check whois.")
    parser.add_argument("-net", action="store", help="Net address, to which need to check whois.")
    return parser


if __name__ == '__main__':
    parse = init_parser()
    args = parse.parse_args(sys.argv[1:])
    if args.ip is not None:
        for message in trace(args.ip):
            print(message)
    else:
        for message in trace(socket.gethostbyname(args.net)):
            print(message)
