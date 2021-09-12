import os

flash_name = os.path.join(os.path.dirname(__file__), "flash.bin")
if not os.path.isfile(flash_name):
    with open(flash_name, "wb") as file:
        file.write(bytes(0x200))

flash = open(flash_name, "rb+")
flash.seek(0, 2)

size = flash.tell()
addr = 0x0000

def read():
    flash.seek(addr)
    return flash.read(1)[0]

def write(val):
    flash.seek(addr)
    flash.write(bytes([val & 0xff]))

def wipe():
    flash.seek(0)
    flash.write(bytes(size))
