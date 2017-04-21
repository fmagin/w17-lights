#!/bin/env python3
from lights import Client, ColorSpace
import random
import time
import math


class GameOfLife():
    """Game of Life Animation"""
    RULE30 = {0b111: 0, 0b110: 0, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
    RULE90 = {0b111: 0, 0b110: 1, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 1, 0b000: 0}
    RULE110 = {0b111: 0, 0b110: 1, 0b101: 1, 0b100: 0, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
    RULE184 = {0b111: 1, 0b110: 0, 0b101: 1, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 0, 0b000: 0}
    hue, saturation = 0.1, 0.8
    LEDCOUNT = 1600
    state = [] # type: List[(float, float, float)]
    def __init__(self):
        """Initialize with a random start state"""
        self.connection = Client("light.w17.io", 1337)
        self.state = [(self.hue, self.saturation, 1.0) if random.random() < 0.5
                      else (self.hue, self.saturation, 0.0) for _ in range(self.LEDCOUNT)]

    def push(self):
        """Pushes the current state to the remote server"""
        self.connection.push(self.state, ColorSpace.HSV)


    def tick(self, rule, ticklength):
        """ Continues the game one tick according to a set of rules """
        time.sleep(ticklength)
        hue = self.hue
        saturation = self.saturation
        new_state = []
        for a in range(len(self.state)):
            try:
                l_parent, top_parent, r_parent = self.state[a-1], self.state[a], self.state[a+1]
            except IndexError:
                l_parent, top_parent, r_parent = self.state[a-1], self.state[a], self.state[0]
            parent_value = (int(math.ceil(l_parent[2])) <<2) + (int(math.ceil(top_parent[2])) << 1) + int(math.ceil(r_parent[2]))
            value = rule[parent_value]
            new_state.append((hue, saturation, value))
        self.state = new_state
        self.hue = (self.hue + 0.1) % 360

if __name__ == "__main__":
    animation = GameOfLife()
    while True:
        animation.tick(GameOfLife.RULE30, 0.2)
        animation.push()

"""
H,S,V = 0.1, 0.8, 0.8 
while True:
    time.sleep(0.2)
    #print(field)
    self.state = tick(self.state,rule)
    H,S,V = ((H + 1) % 360), (S) % 1, V
    print("Hue is: ", H)
    print("Saturation is: ", S)
    print("Value is: ", )    
    data = map(lambda cell:(H,S,V) if cell==1 else (0,0,0), self.state)
    client.push(data, ColorSpace.HSV)
"""
