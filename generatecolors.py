import random

longstring=""
loop=0

for a in range(180):
    print(loop)
    longstring += format(random.choice([0, 63, 127, 192, 255]), '02x').upper()
    #print((hex(randrange(0,255,127))[2:]).upper())
    loop+=1

print(longstring)