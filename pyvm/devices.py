import sys, termios, tty, os, random

from . import screen

'''
devices:
    0x00: console
    0x10: system registers
    0x20: screen
    0x30: rng
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
