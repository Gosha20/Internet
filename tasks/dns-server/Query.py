class Query:
    def __init__(self, name, type, inter, byte):
        self.name = name
        self.type = type
        self.class_int = inter
        self.in_bytes = byte

    def __str__(self):
        return """ name: {0},
         type: {1},
          class_int: {2}""".format(self.name, self.type, self.class_int)
