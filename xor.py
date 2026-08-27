from Milenage import *

a = bytes([0x01])
len(a)

def xor(a,b:bytes) -> bytes:
    """xor bytes objects, must be same length"""
    assert len(a) == len(b), "xor -- input a and b must be same size"
    assert len(a) > 0,       "xor -- input cannot be zero length"
    
    result = bytearray(len(a))
    
    for i in range(len(result)):
        result[i] = a[i] ^ b[i]
    return bytes(result)

