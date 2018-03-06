import os
import socket
import time
import struct
import datetime

def _to_frac(timestamp, n=32):
    return int(abs(timestamp - int(timestamp)) * 2**n)



class SNTPConstants:
    _SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
    _SNTP_EPOCH = datetime.date(1900, 1, 1)

    SNTP_DELTA = (_SYSTEM_EPOCH - _SNTP_EPOCH).days * 24 * 3600
    LEAP_TABLE = {
        0: "no warning",
        1: "last minute has 61 seconds",
        2: "last minute has 59 seconds",
        3: "alarm condition (clock not synchronized)",
    }

    MODE_TABLE = {
        0: "reserved",
        1: "symmetric active",
        2: "symmetric passive",
        3: "client",
        4: "server",
        5: "broadcast",
        6: "reserved for NTP control messages",
        7: "reserved for private use",
    }
    STRATUM = {
        0: "not specified or not available",
        1: "primary standard (for example, radio clock)",
    }

class SNTPPacket():
    _PACKET_FORMAT = "!B B B b 11I"

    def __init__(self, version=3, mode=4, time_to_lie = 0):
        self.leap_indicator = 3
        self.version = version
        self.mode = mode
        self.stratum = 0

        self.poll = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0
        self.reference_id = 0
        self.reference_timestamp = time.time() + SNTPConstants.SNTP_DELTA + time_to_lie

        self.originate_timestamp = time.time() + SNTPConstants.SNTP_DELTA + time_to_lie
        self.receive_timestamp = time.time() + SNTPConstants.SNTP_DELTA + time_to_lie
        self.transmit_timestamp = time.time() + SNTPConstants.SNTP_DELTA + time_to_lie

    def pack_to_send(self):
        data = struct.pack(SNTPPacket._PACKET_FORMAT,
                           (self.leap_indicator << 6 | self.version << 3 | self.mode),
                           self.stratum,
                           self.poll,
                           self.precision,
                           self.root_delay,
                           self.root_dispersion,
                           self.reference_id,
                           int(self.reference_timestamp),
                           _to_frac(self.reference_timestamp),
                           int(self.originate_timestamp),
                           _to_frac(self.originate_timestamp),
                           int(self.receive_timestamp),
                           _to_frac(self.receive_timestamp),
                           int(self.transmit_timestamp),
                           _to_frac(self.transmit_timestamp))
        return data

    def from_data(self, data):
        try:
            unpacked = struct.unpack(SNTPPacket._PACKET_FORMAT,
                                     data)
            self.leap_indicator = unpacked[0] >> 6 & 0x3
            self.version = unpacked[0] >> 3 & 0x7
            self.poll = unpacked[2]
            self.reference_id = unpacked[6]
        except struct.error:
            raise("NTP WRONG PACKET")


time_to_lie = 0
with open("config.txt",'r',encoding="utf-8") as file:
    time_to_lie = int(file.readline().rstrip("\n"))

timeout = 60
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 123))
while True:
    print('Waiting for data ({0} seconds)...'.format(timeout))
    server.settimeout(timeout)
    try:
        data = server.recvfrom(1024)
    except socket.timeout:
        print('Time is out. {0} seconds have passed'.format(timeout))
        break
    received = data[0]
    addr = data[1]
    data = data[0]
    sendPacket = SNTPPacket(version=3, mode=4, time_to_lie=time_to_lie)
    sendPacket.from_data(data)
    server.sendto(sendPacket.pack_to_send(), addr)
server.close()
