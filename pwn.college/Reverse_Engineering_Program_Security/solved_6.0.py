def prinz(key):
    for i in key:
        print(hex(i).split("0x")[1], end=" ")
    print()

# 65 5a 19 6b 4c 02 4f 6e 26 5d 63 78 0c 28 65 1b
# key = bytearray(b"\x07<}\x05;{\x038w\r1j\x13)f\x1c")

def mang_1(key):
    temp = key[8]
    key[8] = key[4]
    key[4] = temp

def mang_2(key):
    for ix, char in enumerate(key):
        for ix, char in enumerate(key):
            if((ix) >= 15):
                break
            if(key[ix] > key[ix + 1]):
                temp = key[ix]
                key[ix] = key[ix+1]
                key[ix+1] = temp

def mang_3(key):
    for ix, char in enumerate(key):
        what = ix % 3
        if(what == 2):
            key[ix] = key[ix] ^ 0x1e
        if(what == 0):
            key[ix] = key[ix] ^ 0x66
        if(what == 1):
            key[ix] = key[ix] ^ 0x5f


#key = bytearray(b"\x07<}\x05;{\x038w\r1j\x13)f\x1c")
key = bytearray(b"affghjmmqrsuuvvwxyz")

mang_3(key)
mang_2(key)
mang_1(key)

with open("key", "wb") as f:
    f.write(key)
