#!/bin/env python3

import sys, os
import devices

debug = "DEBUG" in os.environ

if len(sys.argv) < 2:
    print(sys.argv[0], "<rom>")
    exit()

with open(sys.argv[1], "rb") as file:
    ram = bytearray(file.read())

pc = 0x0000
ps = 0x0000
rs = 0xff00

def read_byte(addr):
    global pc, ram
    return ram[addr]

def read_word(addr):
    global pc, ram
    res = read_byte(addr)
    addr = (addr + 1) % 65536
    res = res | (read_byte(addr) << 8)
    return res

def write_byte(val, addr):
    global pc, ram
    ram[addr] = val % 256

def write_word(val, addr):
    global pc, ram
    write_byte(val % 256, addr)
    addr = (addr + 1) % 65536
    val >>= 8
    write_byte(val % 256, addr)

def fetch_byte():
    global pc, ram
    res = read_byte(pc)
    pc = (pc + 1) % 65536
    return res

def fetch_word():
    global pc, ram
    res = read_word(pc)
    pc = (pc + 2) % 65536
    return res

def push_ps(word):
    global ps
    ps = (ps - 2) % 65536
    write_word(word, ps)

def pop_ps():
    global ps
    res = read_word(ps)
    ps = (ps + 2) % 65536
    return res

def push_rs(word):
    global rs
    write_word(word, rs)
    rs = (rs + 2) % 65536

def pop_rs():
    global rs
    rs = (rs - 2) % 65536
    res = read_word(rs)
    return res

def push_stack(word, is_rs):
    if is_rs:
        push_rs(word)
    else:
        push_ps(word)

def pop_stack(is_rs):
    if is_rs:
        return pop_rs()
    else:
        return pop_ps()

running = True
while running:
    if debug:
        print(f"pc: {pc}")

    opcode = fetch_byte()
    is_rs = (opcode & 0b10000000) >> 7
    func = opcode & 0b01111111

    if debug:
        print(f"func {bin(func)} is_rs {is_rs} opcode {hex(opcode)}")

    if func == 0b0000000:   # break
        running = False
    elif func == 0b0000001: # literal
        push_stack(fetch_word(), is_rs)
    elif func == 0b0000010: # set stack, pushes old one
        word = fetch_word()

        if is_rs:
            old_val = rs
            rs = word
        else:
            old_val = ps
            ps = word

        push_ps(old_val)
    elif func == 0b0000011: # drop
        pop_stack(is_rs)
    elif func == 0b0000100: # dup
        a = pop_stack(is_rs)
        push_stack(a, is_rs)
        push_stack(a, is_rs)
    elif func == 0b0000101: # over
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a, is_rs)
        push_stack(b, is_rs)
        push_stack(a, is_rs)
    elif func == 0b0000110: # rotate
        c = pop_stack(is_rs)
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(b, is_rs)
        push_stack(c, is_rs)
        push_stack(a, is_rs)
    elif func == 0b0000111: # equal
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(int(a == b), is_rs)
    elif func == 0b0001000: # not
        push_stack(pop_stack(is_rs) ^ 0xffff, is_rs)
    elif func == 0b0001001: # greater than
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(int(a > b), is_rs)
    elif func == 0b0001010: # less than
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(int(a < b), is_rs)
    elif func == 0b0001011: # jump
        pc = pop_stack(is_rs)
    elif func == 0b0001100: # jump conditionally
        a = pop_stack(is_rs)
        flag = pop_stack(is_rs)

        if flag:
            pc = a
    elif func == 0b0001101: # jump stash
        push_stack(pc, not is_rs)
        pc = pop_stack(is_rs)
    elif func == 0b0001110: # stash
        push_stack(pop_stack(is_rs), not is_rs)
    elif func == 0b0001111: # add
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a + b, is_rs)
    elif func == 0b0010000: # subtract
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a - b, is_rs)
    elif func == 0b0010001: # multiply
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a * b, is_rs)
    elif func == 0b0010010: # divide
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a // b, is_rs)
    elif func == 0b0010011: # modulo
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a % b, is_rs)
    elif func == 0b0010100: # and
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a & b, is_rs)
    elif func == 0b0010101: # or
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a | b, is_rs)
    elif func == 0b0010110: # xor
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        push_stack(a ^ b, is_rs)
    elif func == 0b0010111: # shift left
        b = pop_stack(is_rs)
        a = pop_stack(is_rs)
        if b & 0b10000000:
            is_right = True
        else:
            is_right = False
        b &= 0b01111111

        if is_right:
            push_stack(a >> b, is_rs)
        else:
            push_stack(a << b, is_rs)
    elif func == 0b0011000: # load byte
        a = pop_stack(is_rs)
        push_stack(read_byte(a), is_rs)
    elif func == 0b0011001: # load word
        a = pop_stack(is_rs)
        push_stack(read_word(a), is_rs)
    elif func == 0b0011010: # store byte
        a = pop_stack(is_rs)
        val = pop_stack(is_rs)
        write_byte(val, a), is_rs
    elif func == 0b0011011: # store word
        a = pop_stack(is_rs)
        val = pop_stack(is_rs)
        write_word(val, a)
    elif func == 0b0011100: # device in
        a = pop_stack(is_rs)
        regs = {"pc": pc, "ps": ps, "rs": rs, "ram": ram, "addr": a}
        val, changes = devices.read(regs)
        for k, v in changes.items():
            vars()[k] = v
        push_stack(val, is_rs)
    elif func == 0b0011101: # device out
        a = pop_stack(is_rs)
        val = pop_stack(is_rs)
        regs = {"pc": pc, "ps": ps, "rs": rs, "ram": ram, "addr": a, "val": val}
        changes = devices.write(regs)
        for k, v in changes.items():
            vars()[k] = v
    else:
        print(f"Unknown function {bin(func)} with rs flag set to '{is_rs}'")
        running = False

with open("ram.bin", "wb") as file:
    file.write(ram)
