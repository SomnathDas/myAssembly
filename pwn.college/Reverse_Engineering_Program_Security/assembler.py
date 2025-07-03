import sys, os, struct
from itertools import product
import shutil

def usage():
    print(sys.argv[0] + " <file>")

try:
    insts = open(sys.argv[1], "r").readlines()
except IndexError:
    usage()
    exit()

def chunkstring(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))


operations = {
    "imm":0x02,
    "stm":0x01,
    "sys":0x20
}

registers = {
    "a":0x40,
    "b":0x02,
    "c":0x10,
    "d":0x80,
    "s":0x4,
    "i":0x8,
    "f":0x40
}

syscalls = {
    "open":0x4,
    "read_code":0x20,
    "read_mem":0x20,
    "write":0x80,
    "sleep":0x8,
    "exit":0x1
}

def regCheck(val):

    for k,v in registers.items():
        if val.lower() == k:
            return(hex(v))
        
def jmp(arg1):
    for k,v in jmp_ops.items():
        if k == arg1:
            return hex(v)

def syscall(arg1):
    for k,v in syscalls.items():
        if v == int(arg1,16):
            return hex(v)
        
        elif k == arg1.lower():
            return hex(v)

def genReg(op):
    for k,v in registers.items():
        if op.lower() == k:
            return(hex(v))
        
def operation(op):
    for k,v in operations.items():
        if op.lower() == k:
            return(hex(v))


def assemb(op, arg1, arg2):
    opcode = []

    #opcode.append( operation(op) )
    op = op.lower()

    if regCheck(arg1) != None:
        opcode.append( regCheck(arg1) )
    else:
        opcode.append( (arg1) )

    #elif op == "sys":
        #opcode.append(syscall(arg1))

    if regCheck(arg2) != None:
        opcode.append( regCheck(arg2) )
    else:
        opcode.append( (arg2) )

    opcode.append(operation(op))

    if op == "jmp":
        opcode.append(jmp(arg1))

    return opcode

def main():
    noOfLiens = len(insts)
    outBytes = b''
    for i in range(noOfLiens):
        op, arg1, arg2 = insts[i].split()

        print(op, arg1, arg2)

        arg1 = arg1.replace("*", "")
        arg2 = arg2.replace("*", "")

        opcode = assemb(op, arg1, arg2)

        for b in opcode:
            outBytes += struct.pack('B', int(b, 16))
    
    # print(outBytes)
    fileName = sys.argv[1]+'-assem'
    with open(fileName, 'wb') as outFile:
        outFile.write(outBytes)
        outFile.close()

    print(f"[+] File ({fileName}) is created")

value_space = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]

original_registers = ["a", "b", "c", "d"]
syscalls_to_bruteforce = ["open", "read_mem", "write"]

combos = list(product(value_space, repeat=4))  # for registers a, b, c, d
syscall_combos = list(product(value_space, repeat=3))  # for open, read_mem, write

counter = 0
for reg_vals in combos:
    for syscall_vals in syscall_combos:
        # Inject register values
        registers["a"] = reg_vals[0]
        registers["b"] = reg_vals[1]
        registers["c"] = reg_vals[2]
        registers["d"] = reg_vals[3]

        # Inject syscall values
        syscalls["open"] = syscall_vals[0]
        syscalls["read_mem"] = syscall_vals[1]
        syscalls["write"] = syscall_vals[2]

        # Call the main assembler
        try:
            main()
            output_name = f"{sys.argv[1]}-assem_{counter:04d}.bin"
            shutil.move(sys.argv[1]+'-assem', output_name)
            print(f"[+] Saved: {output_name}")
        except Exception as e:
            print(f"[-] Failed on combo #{counter}: {e}")

        counter += 1

