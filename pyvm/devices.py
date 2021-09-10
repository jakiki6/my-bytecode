import sys, termios, tty, os, random

from . import screen

'''
devices:
    0x00: console
      read:
        0x00: read from stdin
      write:
        0x00: write to stdout
    0x10: system registers
      read:
        0x11: ps register
        0x12: rs
        0x13: ws
      write:
        0x11: ps register
        0x12: rs register
        0x13: ws register
        0x14: exit with code
    0x20: screen
      read:
        0x24: screen height
        0x25: screen width
      width:
        0x20: write pixel to buffer
        0x21: red register
        0x22: green register
        0x23: blue register
        0x24: x register
        0x25: y register
        0x26: write all changes to the actual screen
        0x27: reset all screen registers
        0x28: wipe screen (you should call 0x26 to be sure)
    0x30: rng
      read:
      write:
        0x30: random number from 0x0000 to 0xffff
    0x40: storage
      read:
        0x40: read from storage
        0x42: size of storage
      write:
        0x40: write to storage
        0x41: value register (byte)
        0x42: address register
        0x43: wipe storage
'''

def read(regs):
    if "DEBUG" in os.environ.keys():
        print(f"read: pc=0x{hex(regs['pc'])[2:].zfill(4)} addr=0x{hex(regs['addr'])[2:].zfill(4)}")

    res = 0
    mods = {}

    if regs["addr"] == 0x0000:
        res = getch()[0]
    elif regs["addr"] == 0x0011:
        res = regs["ps"]
    elif regs["addr"] == 0x0012:
        res = regs["rs"]
    elif regs["addr"] == 0x0013:
        res = regs["ws"]
    elif regs["addr"] == 0x0024:
        res = screen.width
    elif regs["addr"] == 0x0025:
        res = screen.height
    elif regs["addr"] == 0x0030:
        res = random.randint(0x0000, 0xffff)

    return res, mods

def write(regs):
    if "DEBUG" in os.environ.keys():
        print(f"write: pc=0x{hex(regs['pc'])[2:].zfill(4)} addr=0x{hex(regs['addr'])[2:].zfill(4)} val=0x{hex(regs['val'])[2:].zfill(4)}")

    mods = {}

    if regs["addr"] == 0x0000:
        print(chr(regs["val"] & 0xff), end="")
    elif regs["addr"] == 0x0011:
        mods["ps"] = regs["val"]
    elif regs["addr"] == 0x0012:
        mods["rs"] = regs["val"]
    elif regs["addr"] == 0x0013:
        mods["ws"] = regs["val"]
    elif regs["addr"] == 0x0014:
        exit(regs["val"])
    elif regs["addr"] == 0x0020:
        screen.draw()
    elif regs["addr"] == 0x0021:
        screen.red = regs["val"] % 256
    elif regs["addr"] == 0x0022:
        screen.green = regs["val"] % 256
    elif regs["addr"] == 0x0023:
        screen.blue = regs["val"] % 256
    elif regs["addr"] == 0x0024:
        screen.x = regs["val"]
    elif regs["addr"] == 0x0025:
        screen.y = regs["val"]
    elif regs["addr"] == 0x0026:
        screen.refresh()
    elif regs["addr"] == 0x0027:
        screen.init_regs()
    elif regs["addr"] == 0x0027:
        screen.wipe()

    return mods

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.buffer.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char
