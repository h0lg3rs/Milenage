from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from test_data import TEST_VECTORS
from datetime import datetime

#Rotasjons nummer per bit for hver enkelt av output fra f1-f5
r1 = 64;
r2 = 0;
r3 = 32;
r4 = 64;
r5 = 96

#Variablene c1-c5 ved bruk av fromhex funksjonen
c1 = bytes.fromhex("00000000000000000000000000000000")
c2 = bytes.fromhex("00000000000000000000000000000001")
c3 = bytes.fromhex("00000000000000000000000000000002")
c4 = bytes.fromhex("00000000000000000000000000000004")
c5 = bytes.fromhex("00000000000000000000000000000008")

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

#Laget en funksjon for å rotere bytes med slicing
def rot(b: bytes, r: int) -> bytes:
    #Sjekker om b er noe annet enn bare 0 
    #og at r er delelig på 8
    assert b 
    assert r % 8 == 0
    
    tmp_r = r // 8
    top = b[0:tmp_r]
    end = b[tmp_r:]
    rotated = end+top
    
    return(rotated)

#Hentet xor funksjonen fra slides for å bruke xor operatoren som er innebygd i python
def xor(a,b:bytes) -> bytes:
    """xor bytes objects, must be same length"""
    #Sjekker om lengden er lik for begge og at den ikke er 0
    assert len(a) == len(b)
    assert len(a) > 0
    
    result = bytearray(len(a))
    
    for i in range(len(result)):
        result[i] = a[i] ^ b[i]
    return bytes(result)

#Encryption
#Her er selve krypteringen ved bruk av AES128

def E(k, m: bytes) -> bytes:
    #AES128 in ECB mode
    assert len(m) == 16, "E(k,m): Input block m must be 16 bytes long (was {:d}).".format(len(m))
    assert len(k) == 16, "E(k,m): key must be 16 bytes long"

    encryptor = Cipher(algorithms.AES128(k), modes.ECB()).encryptor()
    return(encryptor.update(m)+encryptor.finalize())

#Selve funksjonen for å sjekke om svaret er lik det i test-settet
def verify(name, actual, expected):
 
    expected_bytes = a2b(expected)
 
    if actual == expected_bytes:
        print(f"   {name:<6} PASS")
        return True
 
    print(f"   {name:<6} FAIL")
    print(f"      expected {b2a(expected_bytes)}")
    print(f"      actual   {b2a(actual)}")
 
    return False
 
#Skriver ut til en tekst-fil med timestamp og om det passerte eller ikke
def write_log(message):
 
    with open("milenage_test_log.txt", "a",
              encoding="utf-8") as f:
 
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
 
        f.write(f"[{timestamp}] {message}\n")
 
#Variabler for sjekking om output og test-svar stemmer
total = 0
passed = 0
 
#En for-løkke som itererer gjennom hver av test-settene i test_data.py
for tv in TEST_VECTORS:
    #Variabler hentet fra test sett, 
    #og beregnet svar for de forskjellige variablene
    K = a2b(tv["K"])
    SQN = a2b(tv["SQN"])
    AMF = a2b(tv["AMF"])
    RAND = a2b(tv["RAND"])
    IN1 = SQN+AMF+SQN+AMF
    OP = a2b(tv["OP"])
    EOP = E(K,OP)
    OPc = xor(OP,EOP)
    TEMP = E(K,xor(RAND,OPc))
 
    #Output
    OUT1 = xor(E(K,xor(xor(TEMP,rot(xor(IN1,OPc),r1)),c1)),OPc)
    OUT2 = xor(E(K,xor(rot(xor(TEMP,OPc),r2),c2)),OPc)
    OUT3 = xor(E(K,xor(rot(xor(TEMP,OPc),r3),c3)),OPc)
    OUT4 = xor(E(K,xor(rot(xor(TEMP,OPc),r4),c4)),OPc)
    OUT5 = xor(E(K,xor(rot(xor(TEMP,OPc),r5),c5)),OPc)
 
    MACA = OUT1[0:8]  #f1
    MACS = OUT1[8:]   #f1*
    RES  = OUT2[8:]   #f2
    CK   = OUT3       #f3
    IK   = OUT4       #f4
    AK   = OUT2[0:6]  #f5
    AKS  = OUT5[0:6]  #f5*
 
    print()
    print("=" * 60)
    print(tv["name"])
    print("=" * 60)
    print("   OPc   ", b2a(OPc))
    print("   f1    ", b2a(MACA))
    print("   f1*   ", b2a(MACS))
    print("   f2    ", b2a(RES))
    print("   f3    ", b2a(CK))
    print("   f4    ", b2a(IK))
    print("   f5    ", b2a(AK))
    print("   f5*   ",b2a(AKS))
    print(" " * 60)
 
    # Verifiserer gjennom å sjekke hva som er forventet output 
    # og ser om det stemmer med faktisk output.
    # Siden ekstra testene ikke har noe expected output, så får vi ikke testet dette.
    checks = [
        ("f1", MACA, tv.get("MAC_A")),
        ("f1*", MACS, tv.get("MAC_S")),
        ("f2", RES,  tv.get("RES")),
        ("f3", CK,   tv.get("CK")),
        ("f4", IK,   tv.get("IK")),
        ("f5", AK,   tv.get("AK")),
        ("f5*", AKS, tv.get("AKS"))
    ]
 
    #Sjekker om testene passerte og skriver til tekst filen
    any_checked = False
    ok = True
    for name, actual, expected in checks:
        if expected is None:
            continue
        any_checked = True
        ok &= verify(name, actual, expected)
    
    if any_checked:
        total += 1
        if ok:
            passed += 1
            write_log(f"Dataset {tv['name']} PASS")
        else:
            write_log(f"Dataset {tv['name']} FAIL")
    else:
        print("   (no expected values on file -- nothing to verify)")
 
print()
print("=" * 60)
print(f"RESULTAT: {passed}/{total} PASS")
print("=" * 60)
 
write_log(f"SUMMARY {passed}/{total} PASS")