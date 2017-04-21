#!/bin/env python3
import random
import time
import math
import _thread
from lights import Client, ColorSpace


class GameOfLife():
    """Game of Life Animation"""
    RULE30 = {0b111: 0, 0b110: 0, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
    RULE90 = {0b111: 0, 0b110: 1, 0b101: 0, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 1, 0b000: 0}
    RULE110 = {0b111: 0, 0b110: 1, 0b101: 1, 0b100: 0, 0b011: 1, 0b010: 1, 0b001: 1, 0b000: 0}
    RULE184 = {0b111: 1, 0b110: 0, 0b101: 1, 0b100: 1, 0b011: 1, 0b010: 0, 0b001: 0, 0b000: 0}
    hue, saturation = 100, 0.9
    LEDCOUNT = 1600
    REFRESHRATE = 10
    state = [] # type: List[(float, float, float)]
    def __init__(self):
        """Initialize with a random start state"""
        self.connection = Client("light.w17.io", 1337)
        self.state = [(self.hue, self.saturation, 1.0) if random.random() < 0.25
                      else (self.hue, self.saturation, 0.0) for _ in range(self.LEDCOUNT)]

    def push(self):
        """Pushes the current state to the remote server"""
        self.connection.push(self.state, ColorSpace.HSV)


    def tick(self, rule, ticklength, transition_function):
        """ Continues the game one tick according to a set of rules """
        hue = self.hue
        saturation = self.saturation
        new_state = []
        for a in range(len(self.state)):
            try:
                l_parent, top_parent, r_parent = self.state[a-1], self.state[a], self.state[a+1]
            except IndexError:
                l_parent, top_parent, r_parent = self.state[a-1], self.state[a], self.state[0]
            #TODO Make calculation of next state more robust
            parent_value = ((4 if l_parent[2] > 0.1 else 0) + (2 if top_parent[2] > 0.1 else 0) + (1 if r_parent[2] > 0.1 else 0))
            value = rule[parent_value]
            new_state.append((hue, saturation, value))

        transition_function(self.state, new_state, ticklength)
        self.hue = (self.hue + 1) % 360
        #self.saturation = 0.9

    def instant_transition(self, start_state, end_state, ticklength):
        """Instantly change the state to the new state and waits a certain time"""
        self.state = end_state
        time.sleep(ticklength)

    def interpolation_transition(self, start_state, end_state, ticklength):
        """Transition states by interpolating states in between"""
        imm_states = int(ticklength * self.REFRESHRATE) #Number of intermediate steps
        #Calculate the difference between two states
        state_diff = [(end_cell[0] - start_cell[0], end_cell[1] - start_cell[1], end_cell[2] - start_cell [2]) for start_cell, end_cell in zip(start_state, end_state)]

        for _ in range(imm_states):
            #TODO Optimize unnecessary calculation of hue and saturation
            self.state = [(cell_orig[0] + cell_diff[0]/imm_states,
                           cell_orig[1] + cell_diff[1]/imm_states,
                           cell_orig[2] + cell_diff[2]/imm_states)
                          for cell_diff, cell_orig in zip(state_diff, self.state)]
            time.sleep(ticklength/imm_states)

def thread_tick(rules, ticklength):
    while True:
        animation.tick(rules, ticklength, animation.interpolation_transition)

def thread_push():
    while True:
        animation.hue = animation.hue % 360
        animation.push()



if __name__ == "__main__":
    animation = GameOfLife()

   # while True:
   #     animation.tick(GameOfLife.RULE30, 0.9, animation.interpolation_transition)

    try:
        _thread.start_new_thread(thread_tick, (GameOfLife.RULE184, 0.9))
        _thread.start_new_thread(thread_push, ())
    except:
        print("Something failed")

    while 1:
        pass
