import itertools
import subprocess

OPCODES = {
    "SYS": 0x20,
    "IMM": 0x02,
    "STM": 0x08,
    "LDM": 0x04,
    "ADD": 0x01,
    "CMP": 0x10,
    "STK": 0x40,
    "JMP": 0x80,
}

REGISTER_BASE = {
    "a": 0x10,
    "s": 0x08,
    "f": 0x80,
    "i": 0x04,
}

BRUTE_REG_POOL = [0x01, 0x02, 0x20, 0x40]
brute_perms = list(itertools.permutations(BRUTE_REG_POOL, 3))

SYSCALL_GROUPS = [
    (0x10, 0x20),
    (0x20, 0x10),
]

READ_MEM_OPTIONS = [0x40, 0x80]

assembly_program = [
    ("IMM", "d", 0x2F),
    ("IMM", "b", 0x00),
    ("STM", "*b", "d"),
    ("IMM", "d", 0x66),
    ("IMM", "b", 0x01),
    ("STM", "*b", "d"),
    ("IMM", "d", 0x6C),
    ("IMM", "b", 0x02),
    ("STM", "*b", "d"),
    ("IMM", "d", 0x61),
    ("IMM", "b", 0x03),
    ("STM", "*b", "d"),
    ("IMM", "d", 0x67),
    ("IMM", "b", 0x04),
    ("STM", "*b", "d"),
    ("IMM", "d", 0x00),
    ("IMM", "b", 0x05),
    ("STM", "*b", "d"),
    ("IMM", "a", 0x00),
    ("IMM", "b", 0x00),
    ("SYS", "OPEN", "a"),
    ("IMM", "c", 0x64),
    ("SYS", "READ_MEM", "c"),
    ("IMM", "a", 0x01),
    ("SYS", "WRITE", "c"),
    ("IMM", "a", 0x00),
    ("SYS", "EXIT", "a"),
]


def assemble(program, reg_map, syscall_map, read_mem_val):
    output = bytearray()
    reg_alias = {**REGISTER_BASE}
    reg_alias["b"], reg_alias["c"], reg_alias["d"] = reg_map

    syscall_lookup = {
        "OPEN": syscall_map[0],
        "WRITE": syscall_map[1],
        "SLEEP": 0x02,
        "EXIT": 0x01,
        "READ_MEM": read_mem_val,
    }

    for instr in program:
        op = instr[0]
        if op == "IMM":
            _, r, val = instr
            output += bytes([val, reg_alias[r], OPCODES["IMM"]])
        elif op == "STM":
            _, ptr, src = instr
            output += bytes([reg_alias[src], reg_alias[ptr.strip("*")], OPCODES["STM"]])
        elif op == "SYS":
            _, syscall_name, reg = instr
            output += bytes(
                [reg_alias[reg], syscall_lookup[syscall_name], OPCODES["SYS"]]
            )
    return output


def run_binary_with_input(machine_code: bytes, name: str):
    try:
        result = subprocess.run(
            ["/challenge/babyrev-level-22-1"],
            input=machine_code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        output = result.stdout.decode(errors="ignore").strip()
        print(f"[{name}] ➜ Output:\n{output}\n{'-'*60}")
    except subprocess.CalledProcessError as e:
        print(f"[{name}] ➜ Error:\n{e.stderr.decode(errors='ignore')}\n{'-'*60}")


for bcd in brute_perms:
    for syscall_set in SYSCALL_GROUPS:
        for read_mem in READ_MEM_OPTIONS:
            b, c, d = bcd
            open_val, write_val = syscall_set
            name = (
                f"b{b:02X}_c{c:02X}_d{d:02X}_"
                f"open{open_val:02X}_write{write_val:02X}_readmem{read_mem:02X}"
            )
            machine_code = assemble(assembly_program, bcd, syscall_set, read_mem)
            run_binary_with_input(machine_code, name)
