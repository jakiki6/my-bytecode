import sys, math, os
import utils

OPCODES = {
    "brk": 0b0000000,
    "drop": 0b0000011,
    "dup": 0b0000100,
    "over": 0b0000101,
    "rot": 0b0000110,
    "eq": 0b0000111,
    "not": 0b0001000,
    "gth": 0b0001001,
    "lth": 0b0001010,
    "jmp": 0b0001011,
    "jmpc": 0b0001100,
    "call": 0b0001101,
    "sth": 0b0001110,
    "add": 0b0001111,
    "sub": 0b0010000,
    "mul": 0b0010001,
    "div": 0b0010010,
    "mod": 0b0010011,
    "and": 0b0010100,
    "or": 0b0010101,
    "xor": 0b0010110,
    "shl": 0b0010111,
    "ldb": 0b0011000,
    "ldw": 0b0011001,
    "stb": 0b0011010,
    "stw": 0b0011011,
    "dei": 0b0011100,
    "deo": 0b0011101
}

CONSUMES = {
    "db": -1,
    "org": 1,
    "%include": -1,
    "times": -1,
    "setps": 1,
    "setrs": 1,
    "lit": 1
}

origin = 0

class OpCode(object):
    def __init__(self, opcode, args):
        self.opcode = opcode
        self.args = args
    def __str__(self):
        return f"OpCode(opcode='{self.opcode}', args={self.args})"
    def __repr__(self):
        return self.__str__()

class Label(object):   
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Label(name='{self.name}')"
    def __repr__(self):
        return self.__str__()

def consumes(opcode):
    if opcode in CONSUMES.keys():
        return CONSUMES[opcode]
    else:
        return 0    # number or non-consuming opcode?

def replace_whitespaces(line):
    nline = ""
    hit = False
    for char in line:
        if char in " \t,":
            if not hit:
                nline += " "
                hit = True
            continue
        else:
            hit = False
            nline += char
    return nline

def parse(text):
    opcodes = []
    lline = ""
    is_escape = False
    for line in text.split("\n"):
        if is_escape:
            line = lline + line
            is_escape = False
        line = line.strip()
        line = line.split(";")[0].strip()
        line = replace_whitespaces(line)
        if len(line) == 0:
            continue
        if line[-1] == "\\":
            is_escape = True
            lline = line[:-1]
        else:
            if ":" in line:
                label_name = line.split(":")[0].strip()
                line = line.split(":")[1].split(" ")
                opcodes.append(Label(label_name))
                while "" in line:
                    line.remove("")
            else:
                line = line.split(" ")

            while len(line) > 0:
                o = line.pop(0)
                cons = consumes(o)

                if cons == -1:
                    opcodes.append(OpCode(o, line))
                    break
                else:
                    args = []
                    for i in range(0, cons):
                        try:
                            args.append(line.pop(0))
                        except IndexError:
                            raise ValueError(f"Too few arguments for opcode '{o}'")
                    opcodes.append(OpCode(o, args))
    return opcodes

def merge(data):
    for index, line in enumerate(data):
        if not isinstance(line, OpCode):
            continue
        if line.opcode == "%include":
            try:
                with open(line.args[0], "r") as file:
                    for nline in parse(file.read()):
                        data.insert(index, nline)
                        index += 1
                    data.remove(line)
                    merge(data)
                    break
            except:
                print(f"Cannot open file {line.args[0]}", file=sys.stderr)

def preprocess(data):
    for index, line in enumerate(data):
        if not isinstance(line, OpCode):
            continue
        if line.opcode == "times":
            num, s = utils.req_int(line.args[0])
            if not s:
                print(line.args[0], "is not a valid number")
                exit(0)
            nline = utils.shift_line(line, 2)
            for i in range(0, num):
                data.insert(index, nline)
            data.remove(line)
            preprocess(data)
            break

def process(text):
    global origin
    origin = 0

    binary = bytearray()

    rt0 = "rt0.asm"
    text = f"%include {os.path.join(os.path.dirname(__file__), rt0)}\n" + text

    data = parse(text)
    merge(data)
    preprocess(data)

    if "DEBUG" in os.environ.keys():
        print(data)

    tosplice = []
    labels = {}

    for opcode in data:
        if isinstance(opcode, OpCode):
            if len(opcode.args) == 0:
                try:
                    num = utils.req_int_const(opcode.opcode, [], [], bytes())
                    binary += bytearray([0x01, *utils.pack_num(num)])
                    continue
                except ValueError:
                    pass

            if opcode.opcode == "db":
                for arg in opcode.args:
                    num = utils.req_int_big(arg, [len(binary)], tosplice, binary)

                    binary += bytearray(int.to_bytes(num, math.ceil((num.bit_length() + (num < 0)) / 8), "big", signed=(num < 0)))
            elif opcode.opcode == "org":
                if len(opcode.args) != 1:
                    print("org: wrong number of arguments")
                    exit(0)

                num = utils.req_int_const(opcode.args[0], [], tosplice, binary)

                origin = num % 65536
            else:
                if opcode.opcode.endswith("r"):
                    opcode.opcode = opcode.opcode[:-1]
                    flags = 0b10000000
                else:
                    flags = 0b00000000

                if opcode.opcode == "setps":
                    num = utils.req_int_big(opcode.args[0], [len(binary) + 1], tosplice, binary)

                    binary += bytearray([0x02, *utils.pack_num(num)])
                elif opcode.opcode == "setrs":
                    num = utils.req_int_big(opcode.args[0], [len(binary) + 1], tosplice, binary)

                    binary += bytearray([0x82, *utils.pack_num(num)])
                elif opcode.opcode == "lit":
                    for arg in opcode.args:
                        num = utils.req_int_big(arg, [len(binary) + 1], tosplice, binary)

                        binary += bytearray([0x01 | flags, *utils.pack_num(num)])
                elif opcode.opcode in OPCODES.keys():
                    binary += bytearray([OPCODES[opcode.opcode] | flags])
                else:
                    if flags & 0b10000000:
                        opcode.opcode += "r"
                    tosplice.append({
                        "label": opcode.opcode,
                        "at": len(binary) + 1
                    })
                    binary += bytearray([0x01, *utils.pack_num(0xffff)])
        else:
            labels[opcode.name] = len(binary)

        if len(binary) >= 0xff00:
            print("Binary size too big")
            exit(0)

    for splice in tosplice:
        if not splice["label"] in labels:
            print("undefined reference to", splice["label"])
            exit(0)

        at = splice["at"] % 65536
        val = labels[splice["label"]] + origin
        binary[at] = val & 0xff
        at = (at + 1) % 65536
        binary[at] = val >> 8

    binary += bytearray(65536 - len(binary))

    return binary
