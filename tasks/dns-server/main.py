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
        point, query = read_query(data)
        self.query = query
        "answers"

        self.answers = []
        self.auth = []
        self.add = []
        if self.answer_rrs != 0:
            for i in range(self.answer_rrs):
                index, answer = self.read_answer(point, data)
                self.answers.append(answer)
                cache.append(answer.name, answer, answer.type, self.flags)
                point = index

        if self.authority_rrs != 0:
            for i in range(self.authority_rrs):
                index, answer = self.read_answer(point, self.data)
                self.auth.append(answer)
                cache.append(answer.name, answer, answer.type, self.flags)
                point = index

        if self.additional_rrs != 0:
            for i in range(self.additional_rrs):
                index, answer = self.read_answer(point, self.data)
                self.add.append(answer)
                cache.append(answer.name, answer, answer.type, self.flags)
                point = index

    def read_answer(self, point, data):
        count_readed, site_name = read_name_2(point, self.data)
        type = TYPES[int.from_bytes(data[count_readed:count_readed + 2], 'big')]
        class_int = int.from_bytes(data[count_readed + 2:count_readed + 4], 'big')
        ttl = int.from_bytes(data[count_readed + 4:count_readed + 8], 'big')
        data_len = int.from_bytes(data[count_readed + 8:count_readed + 10], 'big')
        if type is 'A':
            sec_name = data[count_readed+10:count_readed+10+data_len]
        else:
            _, sec_name = read_name_2(count_readed+10,self.data)
        answer = Answer(site_name, type, class_int, ttl, sec_name)
        return count_readed + 10 + data_len, answer

    def complete_to_full_packet(self, query):
        answers_bytes = b''
        auth_bytes = b''
        count_answ_rrs = 0
        count_auth_rrs = 0
        count_addt_rrs = struct.pack('!h', 0)
        flags = b'\x85\x80'

        if self.query.type in cache.cache[self.query.name]:
            count_answ_rrs = len(cache.cache[self.query.name][self.query.type])
            for answ in cache.cache[self.query.name][self.query.type]:

                answers_bytes += answ[0].in_bytes
                # flags = cache.cache[self.query.name][self.query.type][0][2]
        result = self.transaction_id + flags + b'\x00\x01'
        result += struct.pack('!h', count_answ_rrs) \
                  + struct.pack('!h', count_auth_rrs)\
                  + count_addt_rrs \
                  + query.in_bytes
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


def read_name_2(d_index, data, recurce=False):
    index = d_index
    site_name = ''
    count_bytes = data[index]
    while count_bytes != 0 and count_bytes < 192:
        for i in range(count_bytes):
            site_name += chr(data[1+index+i])
        index += count_bytes + 1
        count_bytes = data[index]
        site_name += '.'
    if count_bytes >= 192:
        point_offset = int.from_bytes(data[index: index+2],'big') - 49152
        site_name += read_name_2(point_offset, data, True)[1]
        index += 1
    return index+1, site_name

def parse_short(bytes, offset):
    return (struct.unpack_from('!H', bytes, offset)[0], offset + 2)

def read_query(data):
    index, site_name = read_name_2(12, data)
    type = TYPES[int.from_bytes(data[index :index + 2], 'big')]
    class_int = int.from_bytes(data[index + 2:index + 4], 'big')
    query = Query(site_name, type, class_int, data[12:index + 4])
    return index + 4, query


def run_server():
    port = 53
    ip = '127.0.0.2'
    timeout = 2
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        sock.settimeout(timeout)
        while True:
            try:
                data = sock.recvfrom(1024)
            except socket.timeout:
                continue
            addr = data[1]
            data = data[0]
            _, query = read_query(data)
            if query in cache:
                print("from cache")
                query_parsed = DnsParse(data)
                data_to_send = query_parsed.complete_to_full_packet(query)
            else:
                print("from server")
                data_to_send, status = get_info(data)
                if status:
                    DnsParse(data_to_send)
            sock.sendto(data_to_send, addr)


if __name__ == '__main__':
    cache = Cache()
    try:
        run_server()
    except KeyboardInterrupt:
        cache.write_file()
        exit()


