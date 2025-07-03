# Input Size : 0x14
payload = b"\x98\x55\xae\x08\xa6\x0e\x1f\xb1\xf3\x06\xfd\x92\xf9\xcb\x34\x35\x36\x37\x38\x39"

# Input stored at x/100bx 0x7fffffffd850+0x300

bytes_changed = (14) * 2
skip_to_cmp = "nexti\n" * 19

gdb_cont = []
with open("level_20.1.to_reach_cmp.gdb", "r") as f:
    gdb_cont = f.readlines()

print(gdb_cont)

for i in range(bytes_changed):
    gdb_cont.append(skip_to_cmp)
    gdb_cont.append("c\n")
    gdb_cont.append(skip_to_cmp)

with open("level_20.1.gdb", "w") as f:
    for line in gdb_cont:
        f.write(line)

added = b"\xac\x29\x0e\xdd\xfc\xa7\x87\x6e\x10\x10\x1f\xc1\x5c\xa2\x00\x00\x00\x00\x00\x00"

assert len(payload) == len(added)

result_bytes = bytes((p - a) % 256 for p, a in zip(payload, added))

with open("inst.input", "wb") as f:
    f.write(result_bytes)

print("".join(f"\\x{b:02x}" for b in result_bytes))

