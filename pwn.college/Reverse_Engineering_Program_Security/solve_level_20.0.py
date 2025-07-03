payload = b"\xde\x8f\x8c\x35\xdc\x57\x77\xd3\x4f\x9f\x06\xf8\x4e\x72\x7d\x7d\x5f\x09\x0a\xf5\x7f\xcd\x80\x91\xea\x1a\x51\x91\x48\x49\x50\x51\x52\x53"

bytes_changed = (28) * 2

with open("level_20.0.gdb", "w") as f:
    f.write("break interpret_cmp\n")
    f.write("r < ./inst.input\n")
    f.write("c\n" * bytes_changed)
    f.write("nexti\n" * 35)

added   = b"\x38\xf0\x7f\xe2\x91\x4b\x5e\xc4\xa9\xeb\xe1\xeb\xa2\x89\xe8\xbf\x3a\x95\x3c\x7f\x1c\x54\xf5\x5f\xdb\x70\x19\x67\x00\x00\x00\x00\x00\x00"

assert len(payload) == len(added)

result_bytes = bytes((p - a) % 256 for p, a in zip(payload, added))

with open("inst.input", "wb") as f:
    f.write(result_bytes)

print("".join(f"\\x{b:02x}" for b in result_bytes))

