import struct

from constant import *
import socket
from Query import *
from Answer import *
from Cache import *


class DnsParse:
    """give me dns packet pls"""

    def __init__(self, data):
        "header"
        self.data = data
        self.transaction_id = data[:2]
        self.flags = data[2:4]
        self.questions = int.from_bytes(data[4:6], 'big')
        self.answer_rrs = int.from_bytes(data[6:8], 'big')
        self.authority_rrs = int.from_bytes(data[8:10], 'big')
        self.additional_rrs = int.from_bytes(data[10:12], 'big')

        "query"
        point, query = read_query(data[12:])

        self.query = query
        "answers"

        self.answers = []
        self.auth = []
        if self.answer_rrs != 0:
            for i in range(self.answer_rrs):
                index, answer = self.read_answer(12+point, data[12 + point:])
                self.answers.append(answer)
                cache.append(query.name, answer, answer.type)
                point += index

        if self.authority_rrs != 0:
            for i in range(self.authority_rrs):
                index, answer = self.read_answer(12 + point, self.data[point + 12:])
                self.auth.append(answer)
                cache.append(query.name, answer, answer.type)
                # cache.append(query.name, answer, query.type)
                point += index

    def read_answer(self, point, data):
        count_readed, site_name = read_name_2(point, self.data)
        type = TYPES[int.from_bytes(data[count_readed:count_readed+2], 'big')]
        class_int = int.from_bytes(data[count_readed + 2:count_readed + 4], 'big')
        ttl = int.from_bytes(data[count_readed + 4:count_readed + 8], 'big')
        data_len = int.from_bytes(data[count_readed + 8:count_readed + 10], 'big')
        _data = data[:count_readed+10+data_len]
        answer = Answer(site_name, type, class_int, ttl, _data)
        return count_readed+10+data_len, answer

    def complete_to_full_packet(self):
        result = self.transaction_id + flags_to_send + b'\x00\x01'
        answers_bytes = b''
        auth_bytes = b''
        count_answ_rrs = 0
        count_auth_rrs = 0
        if self.query.type in cache.cache[self.query.name]:
            count_answ_rrs = len(cache.cache[self.query.name][self.query.type])
            for answ in cache.cache[self.query.name][self.query.type]:
                answers_bytes += answ[0].in_bytes

        count_addt_rrs = self.additional_rrs.to_bytes(2, byteorder='big')
        result += struct.pack('!h', count_answ_rrs) + struct.pack('!h', count_auth_rrs) + count_addt_rrs + query.in_bytes
        result += answers_bytes
        result += auth_bytes
        return result

    def __str__(self):
        result = str(self.transaction_id) + "  " + \
                 str(self.flags) + "  " + \
                 str(self.questions) + "  " + \
                 str(self.answer_rrs) + "  " + \
                 str(self.authority_rrs) + "  " + \
                 str(self.additional_rrs) + "\n" + \
                 str(self.query) + "\n"
        for answer in self.answers:
            result += str(answer) + "\n"
        return result


def read_name_2(d_index, data):
        index = d_index
        site_name = ''
        current_byte = data[index]
        """"есть смысл обдумать"""
        while current_byte != 0:
            count_symbol = data[index]
            if count_symbol == 192:
                point = int.from_bytes(data[index:index + 2], 'big')
                _, name = read_name_2(point-49152, data)
                return index+2-d_index, site_name + name
            for i in range(count_symbol):
                site_name += chr(data[1 + index + i])
            index += 1 + count_symbol
            current_byte = data[index]
            site_name += '.'
        return index-d_index, site_name

def read_addt():
    pass


def read_query(data):
    index, site_name = read_name_2(0,data)
    type = TYPES[int.from_bytes(data[index + 1:index + 3], 'big')]
    class_int = int.from_bytes(data[index + 3:index + 5], 'big')
    query = Query(site_name, type, class_int, data[:index + 5])
    return index + 5, query


port = 53
ip = '127.0.0.1'
cache = Cache()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))
timeout=5
while True:
    print('Waiting for data ({0} seconds)...'.format(timeout))
    sock.settimeout(timeout)
    try:
        data = sock.recvfrom(1024)
    except socket.timeout:
        print('Time is out. {0} seconds have passed'.format(timeout))
        cache.write_file()
        break
    addr = data[1]
    data = data[0]
    _, query = read_query(data[12:])
    if query in cache:
        print("from cache")
        query_parsed = DnsParse(data)
        data_to_send = query_parsed.complete_to_full_packet()
    else:
        print("from server")
        data_to_send = get_info(data)
        DnsParse(data_to_send)

    sock.sendto(data_to_send, addr)
sock.close()
