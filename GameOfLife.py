#!/bin/env python3
from lights import Client, ColorSpace
import random
import time
rule30 = {0b111: 0, 0b110: 0, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
rule90 = {0b111: 0, 0b110: 1, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 1, 0b000: 0}
rule110= {0b111: 0, 0b110: 1, 0b101: 1, 0b100: 0, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
rule184= {0b111: 1, 0b110: 0, 0b101: 1, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 0, 0b000: 0}




def rand_field(length, chance):
	return [ 1 if random.random() < chance else 0 for _ in range(length)]


def tick(field,rules):
	new_field = []
	for a in range(len(field)):
		try:
			x1,x2,x3 = field[a-1],field[a], field[a+1]
		except IndexError:
			x1,x2,x3 =field[a-1],field[a], field[0]
		#print(x1,x2,x3)
		parent = (x1 <<2) + (x2 << 1) + x3
		#print(parent)
		#print(bin(x1 < 2 + x2 < 1 + x3)) # 
		new_field.append(rules[parent])
	return new_field


init = rand_field(1600, 0.01)

client = Client("172.23.97.109", 1337)

rule = rule110
field = tick(init,rule)
H,S,V = 0.1, 0.8, 0.8 
while True:
	time.sleep(0.2)
	#print(field)
	field = tick(field,rule)
	H,S,V = H+10, S, V
	print("Hue is: ", H)
	data = map(lambda cell:(H,S,V) if cell==1 else (0,0,0), field)
	client.push(data, ColorSpace.HSV)

