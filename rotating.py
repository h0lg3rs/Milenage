
#HER VISES ROT

b = bytes([i for i in range(16)])
b2a(b)

# roterer med r1 (den som er 64)
r1 = 64
tmp = rot(b, r1)

bta(tmp)

#HER VISES EGEN IMPLEMENTERING

#r1 = 64 vi vil rotere med 8 bytes
# dette kan loses med ta bort "end" og sette "top" bakerst

top = b[0:8]
end = b[8:0]
rotated = end+top

b2a(rotated)
