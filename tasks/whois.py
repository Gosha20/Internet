import socket
import sys
from argparse import ArgumentParser
import re
import json
import urllib.request

def whois(addr, whois_server='whois.iana.org'):
    sock = socket.socket()
    sock.connect((whois_server, 43))
    if whois_server == 'whois.arin.net':
        sock.sendall(b'n '+addr.encode()+ b'\r\n')
    else:
        sock.sendall(addr.encode() + b'\r\n')
    data = ''
    while True:
        buf = sock.recv(1024)
        data += buf.decode()
        if not buf:
            break
    sock.close()
    if whois_server == "whois.iana.org":
        whois_p = re.compile(r"whois:\s*(.*)")
        server = re.findall(whois_p, data)[0]
        return whois(addr, server)
    else:
        as_name_p = re.compile(r'origin:\s*(AS\d*)')
        as_name = re.findall(as_name_p, data)[0]
        country_p = re.compile(r'country:\s*(\w*)')
        country = re.findall(country_p, data)[0]
        return as_name, country




def simple_whois(addr):
    data = json.loads(
        urllib.request.urlopen('https://stat.ripe.net/data/prefix-overview/data.json?max_related=50&resource=%s' %
                                  addr).read())
    as_name = data['data']['asns'][0]['asn']
    provider = data['data']['asns'][0]['holder']
    data = json.loads(
        urllib.request.urlopen('https://stat.ripe.net/data/rir/data.json?resource=%s&lod=2' %
                               addr).read())
    country = data['data']['rirs'][0]['country']
    return as_name, country, provider

if __name__ == '__main__':
    # print(whois('17.172.224.47','stat.tipe.net'))
    test_whois('17.172.224.47')
    # parse = init_parser()
    # args = parse.parse_args(sys.argv[1:])
    # if args.ip is not None:
    #     print(" in this as " + str(whois(agrs.ip)))
    # else:
    #     print(" in this as " + str(whois(socket.gethostbyname(args.net))))

