bases = {
    "x": 16,
    "b": 2,
    "o": 8
}

def shift_line(data, num):
    for i in range(0, num):
        data.opcode = data.args[0]
        data.args.pop(0)
    return data

def req_int(string, splices, tosplice, binary):
    return req_int_big(string, splices, tosplice, binary) % 65536

def req_int_const(string, splices, tosplice, binary):
    return req_int_big(string, splices, tosplice, binary, True) % 65536

def req_int_big(string, splices, tosplice, binary, const=False):
    try:
        res = int(string)       # number
        return res
    except:
        pass

    if len(string) > 2:
        if string[0] == "0":    # prefix like 0x or 0b
            if string[1] in bases.keys():
                try:
                    res = int(string[2:], bases[string[1]])
                    return res
                except:
                    pass

    if string == "$":
        return len(binary)

    if not const:
        for splice in splices:
            tosplice.append({
                "label": string,
                "at": splice
            })
        return 0xffff

    raise ValueError(f"{string} isn't a valid number!")

def pack_num(num):
    return [num & 0xff, num >> 8]
