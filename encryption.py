# en funksjon som krypterer Ek()

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Milenage import *

def E(k, m: bytes) -> bytes:
    #AES128 in ECB mode
    assert len(m) == 16, "E(k,m): Input block m must be 16 bytes long (was {:d}).".format(len(m))
    assert len(k) == 16, "E(k,m): key must be 16 bytes long"

    encryptor = Cipher(algorithms.AES128(k), modes.ECB()).encryptor()
    return(encryptor.update(m)+encryptor.finalize())


# Now we have our E() function
# From TS 35.207 test set 1 tester vi:

# Key:465b5ce8 b199b49f aa5f0a2e e238a6bc 
# Plaintext: ee36f7cf 037d37d3 692f7f03 99e7949a
# Ciphertext: 9e2980c5 9739da67 b136355e 3cede6a2 


K = a2b("465b5ce8 b199b49f aa5f0a2e e238a6bc")
m = a2b("ee36f7cf 037d37d3 692f7f03 99e7949a")
xc = a2b("9e2980c5 9739da67 b136355e 3cede6a2")

cc = E(K,m)

#cc == xc som bare viser at man ved bruk av K og m får ut riktig xpected cipher

print(b2a(cc))
print(b2a(xc))