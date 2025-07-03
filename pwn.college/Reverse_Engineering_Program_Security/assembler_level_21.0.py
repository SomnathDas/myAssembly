import sys, os, struct


def usage():
    print(sys.argv[0] + " <file>")


OP_ORDER = [0, 1, 2]

try:
    insts = open(sys.argv[1], "r").readlines()
except IndexError:
    usage()
    exit()


def chunkstring(string, length):
    return list(string[0 + i : length + i] for i in range(0, len(string), length))


operations = {
    "imm": 0x10,
    "add": 0x20,
    "stk": 0x08,
    "stm": 0x80,
    "ldm": 0x04,
    "cmp": 0x40,
    "jmp": 0x01,
    "sys": 0x02,
}
registers = {
    "a": 0x20,
    "b": 0x01,
    "c": 0x10,
    "d": 0x04,
    "s": 0x08,
    "i": 0x40,
    "f": 0x02,
}
syscalls = {
    "open": 0x02,
    "read_code": 0x08,
    "read_mem": 0x04,
    "write": 0x20,
    "sleep": 0x10,
    "exit": 0x01,
}
jmp_ops = {"L": 0x08, "G": 0x04, "E": 0x10, "N": 0x02, "Z": 0x01}


def regCheck(val):

    for k, v in registers.items():
        if val.lower() == k:
            return hex(v)


def jmp(arg1):
    for k, v in jmp_ops.items():
        if k == arg1:
            return hex(v)


def syscall(arg1):
    for k, v in syscalls.items():
        if v == int(arg1, 16):
            return hex(v)

        elif k == arg1.lower():
            return hex(v)


def genReg(op):
    for k, v in registers.items():
        if op.lower() == k:
            return hex(v)


def operation(op):
    for k, v in operations.items():
        if op.lower() == k:
            return hex(v)


def assemb(op, arg1, arg2):
    opcode = []

    # opcode.append( operation(op) )
    op = op.lower()

    if regCheck(arg1) != None:
        opcode.append(regCheck(arg1))
    else:
        opcode.append((arg1))

    # elif op == "sys":
    # opcode.append(syscall(arg1))

    if regCheck(arg2) != None:
        opcode.append(regCheck(arg2))
    else:
        opcode.append((arg2))

    opcode.append(operation(op))

    if op == "jmp":
        opcode.append(jmp(arg1))

    return opcode


def main():
    noOfLiens = len(insts)
    outBytes = b""
    for i in range(noOfLiens):
        op, arg1, arg2 = insts[i].split()

        print(op, arg1, arg2)

        arg1 = arg1.replace("*", "")
        arg2 = arg2.replace("*", "")

        opcode = assemb(op, arg1, arg2)

        for b in opcode:
            outBytes += struct.pack("B", int(b, 16))

    # print(outBytes)
    fileName = sys.argv[1] + "-asm"
    with open(fileName, "wb") as outFile:
        outFile.write(outBytes)
        outFile.close()

    print(f"[+] File ({fileName}) is created")


main()
