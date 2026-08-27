from Milenage import *

#HER VISES ROT

b = bytes([i for i in range(16)])
print(b2a(b))

# roterer med r1 (den som er 64)
r1 = 64
#tmp = rot(b, r1)

#b2a(tmp)

#HER VISES EGEN IMPLEMENTERING

#r1 = 64 vi vil rotere med 8 bytes
# dette kan loses med ta bort "end" og sette "top" bakerst

#top = b[0:8]
#end = b[8:]
#rotated = end+top

#b2a(rotated)

def rot(b: bytes, r: int) -> bytes:
    assert b 
    
    tmp_r = r // 8
    #print(tmp_r)       Testing av tmp_r som skal være rotasjoner man får inn av r1 og deler på 8 for å få hvor mange bytes. f.eks 64/8 = 8
    #print(type(tmp_r))
    top = b[0:tmp_r]
    end = b[tmp_r:]
    rotated = end+top
    
    return(b2a(rotated))


print(rot(b,r1))