#!/bin/env python3
import sys, os
from asm import asmcore

if len(sys.argv) < 2:
    print(sys.argv[0], "<file>", "[<output>]")
    exit(1)
if len(sys.argv) == 2:
    sys.argv.append("/dev/stdout")
if not os.path.isfile(sys.argv[1]):
    print(sys.argv[1], "is not a file")
    exit(1)

with open(sys.argv[1], "r") as file:
    binary = asmcore.process(file.read())

with open(sys.argv[2], "wb") as file:
    file.write(binary)
