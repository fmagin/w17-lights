#!/bin/env python
import socket
import struct
import colorsys
from enum import Enum

class ColorSpace(Enum):
    HSV = 0,
    RGB = 1

class Client:
    LEDCount = 1600
    def __init__(self, server, port):
        self.destination = (server, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def push(self, data, color_space=ColorSpace.HSV):
        #assert(instanceof(data, list))
        payload = bytes()
        for entry in data:
            if color_space is ColorSpace.RGB:
                entry = colorsys.rgb_to_hsv(entry[0], entry[1], entry[2])
                entry = (entry[0] * 360, entry[1], entry[2])

            payload += struct.pack("fff", entry[0], entry[1], entry[2])
        self.sock.sendto(payload, self.destination)
