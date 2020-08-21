#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from os.path import realpath

cpu = CPU()
if len(sys.argv) == 2:
    print(realpath(sys.argv[1]))
    cpu.load(realpath(sys.argv[1]))
    cpu.run()

# cpu.load(sys.argv[1])
# cpu.run()