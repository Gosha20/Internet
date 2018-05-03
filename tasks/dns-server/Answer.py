from constant import *


class Answer:
    def __init__(self, name, type_answ, class_int, ttl, sec_name):
        self.name = name
        self.type = type_answ
        self.class_int = class_int
        self.ttl = ttl
        self.sec_name = sec_name
        self.in_bytes = self.generate_packet()

    def generate_packet(self):
        result, _ = url_to_bytes(self.name)
        result += int.to_bytes(R_TYPES[self.type], 2, 'big')
        result += int.to_bytes(self.class_int, 2, 'big')
        result += int.to_bytes(self.ttl, 4, 'big')
        if self.type is  'NS':
            bytes_name, count_b = url_to_bytes(self.sec_name[:-1])
            result += int.to_bytes(count_b+1, 2, 'big') + bytes_name + b'\x00'
        else:
            result += int.to_bytes(4, 2, 'big') + self.sec_name
        print(result)
        return result


    def __str__(self):
        return """ name: {0}, type: {1}, class_int: {2}, ttl: {3}, sec_name: {4}""".format(
            self.name,
            self.type,
            self.class_int,
            self.ttl,
            self.sec_name)
