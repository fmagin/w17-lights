#!/bin/env python3
from lights import Client, ColorSpace
import random
import time


class GameOfLife():
    """Game of Life Animation"""
    RULE30 = {0b111: 0, 0b110: 0, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
    RULE90 = {0b111: 0, 0b110: 1, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 1, 0b000: 0}
    RULE110 = {0b111: 0, 0b110: 1, 0b101: 1, 0b100: 0, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
    RULE184 = {0b111: 1, 0b110: 0, 0b101: 1, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 0, 0b000: 0}

    @staticmethod
    def get_rand_state(length, chance):
        """ Generates random starting state"""
        return [1 if random.random() < chance else 0 for _ in range(length)]

    def __init__(self, ledcount):
        self.connection = Client("light.w17.io", 1337)
        self.state = self.get_rand_state(ledcount, 0.2)

    def push(self):
        """Pushes the current state to the remote server"""
        self.connection.push(self.state, ColorSpace.HSV)



    def tick(self, rule, ticklength):
        """ Continues the game one tick according to a set of rules """
        time.sleep(ticklength)
        new_state = []
        for a in range(len(self.state)):
            try:
                l_parent, top_parent, r_parent = self.state[a-1], self.state[a], self.state[a+1]
            except IndexError:
                l_parent, top_parent, r_parent = self.state[a-1], self.state[a], self.state[0]
            parents = (l_parent <<2) + (top_parent << 1) + r_parent
            new_state.append(rule[parents])
        self.state = new_state

    

if __name__ == "__main__":
    animation = GameOfLife(1600)
    while True:
        animation.tick(GameOfLife.RULE30, 0.2)
        animation.push()


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

