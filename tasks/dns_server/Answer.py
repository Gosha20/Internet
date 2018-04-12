
class Answer:
    def __init__(self, name, type_answ,  class_int, ttl, byte):
        self.name = name
        self.type = type_answ
        self.ttl = ttl
        self.class_int = class_int
        self.in_bytes = byte

    def __str__(self):
        return """ name: {0}, type: {1}, class_int: {2}, ttl: {3}""".format(
            self.name,
            self.type,
            self.class_int,
            self.ttl)
