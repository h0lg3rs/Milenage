#Tok funksjon fra presentasjon slides for å omgjøre ascii til bytes
def a2b(s:str) -> bytes:
    """"Ascii to bytes"""
    s = s.replace(" ","").strip()
    assert(len(s)%2==0)
    bytelist = list()
    for i in range(0,len(s),2):
        bytelist.append(int("0x"+s[i]+s[i+1],16))
        
    return bytes(bytelist)

hexdig = "0123456789abcdef"

#Tok funskjon 2 fra presentasjonen for å omgjøre bytes tilbake til ascii
def b2a(b: bytes) -> str:
    """Bytes to ascii"""
    assert(len(b) > 0)
    #hexstr = Bits(b).hex
    hexstr = ""
    for byte in b:
        lo = hexdig[byte & 0x0F]
        hi = hexdig[byte >> 4]
        hexstr += hi+lo
    
    #Our "default"
    if len(hexstr) == 32:
        hexstr = hexstr[0:8] + " " + hexstr[8:16] + " " + hexstr[16:24] + " " + hexstr[24:]
    else:
        hs = ""
        while len(hexstr) >=8:
            hs = hs + hexstr[0:8] + " "
            hexstr = hexstr[8:]
        hexstr = hs + hexstr
    return(hexstr)

#Testing av a2b og b2a funksjonene
#print(a2b("6cd1c6ce b1e01e14 f1b82316 a90b7f3d"))
#print(b2a(b'l\xd1\xc6\xce\xb1\xe0\x1e\x14\xf1\xb8#\x16\xa9\x0b\x7f='))

"""Bytes vs bytearray"""

#b = bytes(8)
#print(len(b))
#print(b)
#print(b[0])

#b[0] = 1
#print(b[0])