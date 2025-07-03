def prinz(key):
    for i in key:
        print(hex(i).split("0x")[1], end=" ")
    print()

# 65 5a 19 6b 4c 02 4f 6e 26 5d 63 78 0c 28 65 1b
# key = bytearray(b"\x07<}\x05;{\x038w\r1j\x13)f\x1c")

def swap(key):
    temp = key[25]
    key[25] = key[6]
    key[6] = temp

def swap_1(key):
    temp = key[11]
    key[11] = key[6]
    key[6] = temp

def sort(key):
    for ix, char in enumerate(key):
        for ix, char in enumerate(key):
            if((ix) >= 15):
                break
            if(key[ix] > key[ix + 1]):
                temp = key[ix]
                key[ix] = key[ix+1]
                key[ix+1] = temp

def xor_old(key):
    for ix, char in enumerate(key):
        what = ix % 3
        if(what == 2):
            key[ix] = key[ix] ^ 0x1e
        if(what == 0):
            key[ix] = key[ix] ^ 0x66
        if(what == 1):
            key[ix] = key[ix] ^ 0x5f

def reverse(key):
    for i in range(9):
        temp = key[i]
        key[i] = key[0x12 - i]
        key[0x12 - i] = temp

def xor(key):
    for ix, char in enumerate(key):
        rdx_1 = ix >> 0x1f
        rax_13 = ((ix + rdx_1) & 1) - rdx_1

        if(rax_13 == 0):
            key[ix] = key[ix] ^ 0x9d
        if(rax_13 == 1):
            key[ix] = key[ix] ^ 0x5c

def xor_2(key):
    for ix, char in enumerate(key):
        rdx_1 = ix >> 0x1f
        rax_13 = ((ix + rdx_1) & 1) - rdx_1

        if(rax_13 == 0):
            key[ix] = key[ix] ^ 0xd7
        if(rax_13 == 1):
            key[ix] = key[ix] ^ 0x1f

def xor_3(key):
    for ix, char in enumerate(key):
        rax_78 = ix % 3
        if(rax_78 == 2):
            key[ix] = key[ix] ^ 0x3
        if(rax_78 == 0):
            key[ix] = key[ix] ^ 0xec
        if(rax_78 == 1):
            key[ix] = key[ix] ^ 0xcb


key = bytearray(b"\xc8\xe2\x20\xcc\xe2(\xc4\xfa&\xc7\xfb\xf9\xc8\xe48\xcb\xf5!\xc3\xef=\xde\xe5*\xd7%3\xc9\xe6")

with open("key_og", "wb") as f:
    f.write(key)

print("Length of key: ", hex(len(key)))

#xor_3(key)
#swap_1(key)
#xor_2(key)
#swap(key)
#xor(key)

xor_3(key)
swap_1(key)
xor_2(key)
swap(key)
xor(key)

with open("key", "wb") as f:
    f.write(key)
