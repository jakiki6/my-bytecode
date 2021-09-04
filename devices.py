import sys, termios, tty, os

def read(regs):
    if "DEBUG" in os.environ.keys():
        print(f"read: pc=0x{hex(regs['pc'])[2:].zfill(4)} addr=0x{hex(regs['addr'])[2:].zfill(4)}")

    res = 0
    mods = {}

    if regs["addr"] == 0x0000:
        res = getch()[0]
    elif regs["addr"] == 0x0001:
        res = regs["ps"]
    elif regs["addr"] == 0x0002:
        res = regs["rs"]

    return res, mods

def write(regs):
    if "DEBUG" in os.environ.keys():
        print(f"write: pc=0x{hex(regs['pc'])[2:].zfill(4)} addr=0x{hex(regs['addr'])[2:].zfill(4)} val=0x{hex(regs['val'])[2:].zfill(4)}")

    mods = {}

    if regs["addr"] == 0x0000:
        print(chr(regs["val"] & 0xff), end="")
    elif regs["addr"] == 0x0001:
        mods["ps"] = regs["val"]
    elif regs["addr"] == 0x0002:
        mods["rs"] = regs["val"]

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
