def prinz(key):
    for i in key:
        print(hex(i).split("0x")[1], end=" ")
    print()

def sort(key):
    for ix, char in enumerate(key):
        for ix, char in enumerate(key):
            if((ix) >= 15):
                break
            if(key[ix] > key[ix + 1]):
                temp = key[ix]
                key[ix] = key[ix+1]
                key[ix+1] = temp

def resp(start, end, key):
    for ix in range(start):
        temp = key[end - ix]
        key[end - ix] = key[ix]
        key[ix] = temp

def swap(here, there, key):
    temp = key[there]
    key[there] = key[here]
    key[here] = temp

key = bytearray(b"zxyxxwwvvutstqnnmkjjiiihgggffeeeeddc")

with open("key_og", "wb") as f:
    f.write(key)

print("Length of key: ", hex(len(key)))


swap(11, 12, key)
resp(0x11, 0x23, key)
resp(0x11, 0x23, key)
resp(0x11, 0x23, key)
swap(33, 34, key)
sort(key)
resp(0x11, 0x23, key)

with open("key", "wb") as f:
    f.write(key)
