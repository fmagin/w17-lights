#!/bin/env python3
from lights import Client, ColorSpace
import sys

def unicolor(color, color_space=ColorSpace.HSV):
	client = Client("172.23.97.109", 1337)
	data = [color for c in range(client.LEDCount)]
	client.push(data, color_space)


if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Usage:", sys.argv[0], "val1 val2 val3 colorspace")
	unicolor((float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])), color_space=ColorSpace.RGB)