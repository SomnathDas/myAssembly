def prinz(key):
    for i in key:
        print(hex(i).split("0x")[1], end=" ")
    print()

def sort(key):
    for i_1 in range(0x23):
        for j in range(0x23 - i_1 - 1):
            if key[j] > key[j + 1]:
                key[j], key[j + 1] = key[j + 1], key[j]

def resp(start, end, key):
    for ix in range(start+1):
        temp = key[ix]
        key[ix] = key[end - ix]
        key[end - ix] = temp

def swap(here, there, key):
    temp = key[there]
    key[there] = key[here]
    key[here] = temp

def swi(key):
    for ix, _ in enumerate(key):
        c = ix % 6
        if(c == 0):
            key[ix] = key[ix] ^ 0x51
        if(c == 1):
            key[ix] = key[ix] ^ 0xfc
        if(c == 2):
            key[ix] = key[ix] ^ 0x4c
        if(c == 3):
            key[ix] = key[ix] ^ 0xfe
        if(c == 4):
            key[ix] = key[ix] ^ 0x43
        if(c == 5):
            key[ix] = key[ix] ^ 0xe4

def xor_1(key):
    for ix, _ in enumerate(key):
        c = ix % 3
        if(c == 2):
            key[ix] = key[ix] ^ 0xc9
        if(c == 0):
            key[ix] = key[ix] ^ 0xb7
        if(c == 1):
            key[ix] = key[ix] ^ 0xd9

def xor_2(key):
    for ix, _ in enumerate(key):
        rdx_21 = ix >> 0x1e
        rax_110 = ((ix + rdx_21) & 3) - rdx_21

        if(rax_110 == 3):
            key[ix] = key[ix] ^ 0x65
        if(rax_110 == 2):
            key[ix] = key[ix] ^ 0x18
        if(rax_110 == 0):
            key[ix] = key[ix] ^ 0x68
        if(rax_110 == 1):
            key[ix] = key[ix] ^ 0xb3

key = bytearray(b"3^\x988$8\xe9\"A\xee\xf8M<J\x8e&:+D\x8a\xe9\xebS\xe6\x94\xf9<\x96>\x81R\x97\xf4\xf0J\xff")

with open("key_og", "wb") as f:
    f.write(key)

print("Length of key: ", hex(len(key)))

resp(0x11, 0x23, key)
prinz(key)
xor_2(key)
prinz(key)
swap(0x7, 0x1a, key)
prinz(key)
xor_1(key)
prinz(key)
sort(key)
prinz(key)
swi(key)
prinz(key)
swap(0x2, 0xd, key)

with open("key", "wb") as f:
    f.write(key)
