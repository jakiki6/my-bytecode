import sys, termios, tty

def read(regs):
    res = 0

    if regs["addr"] == 0x0000:
        res = getch()[0]

    return res, {}

def write(regs):
    if regs["addr"] == 0x0000:
        print(chr(regs["val"] & 0xff), end="")

    return {}

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.buffer.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char
