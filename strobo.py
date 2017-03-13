#!/bin/env python
from unicolor import *
from lights import ColorSpace
import time


while True:
	unicolor((0, 0, 127), color_space=ColorSpace.RGB)
	time.sleep(1)
	unicolor((, 0, 0), color_space=ColorSpace.RGB)
	time.sleep(1)