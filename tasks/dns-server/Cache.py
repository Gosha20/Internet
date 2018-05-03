import time
import pickle

class Cache:
    def __init__(self):
        self.cache = dict(dict())
        self.load_file()

    def write_file(self):
        with open('pickle.p', 'wb') as file:
            pickle.dump(self.cache, file)

    def load_file(self):
        with open('pickle.p', 'rb') as file:
            try:
                cache = pickle.load(file)
                self.cache = cache
            except Exception:
                print('some problems with chache file')

    def append(self, key, answer, answer_type, flags):
        if key in self.cache:
            if answer_type in self.cache[key]:
                self.cache[key][answer_type].append((answer, time.time() + answer.ttl, flags))
            else:
                self.cache[key][answer_type] = [(answer, time.time() + answer.ttl, flags)]
        else:
            self.cache[key] = {answer_type: [(answer, time.time() + answer.ttl, flags)]}

    def __contains__(self, item):
        if item.name in self.cache:
            if item.type in self.cache[item.name]:
                for answer in self.cache[item.name][item.type]:
                    if answer[1] < time.time():
                        self.cache[item.name].pop(item.type)
                        return False
                return True
            if 'SOA' in self.cache[item.name]:
                for answer in self.cache[item.name]['SOA']:
                    if answer[1] < time.time():
                        self.cache[item.name].pop('SOA')
                        return False
                    return True
