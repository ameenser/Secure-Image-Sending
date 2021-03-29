import string
import random

from Serpent import convertToBitstring,encrypt,bitstring2hexstring

IV = "31842827315910832088601431579765"

def CBC_Serpent_encrypt(plaintextHex):
    encryptedPlaintext=[]
    key = SerpentGenerateKey()
    binIV=convertToBitstring(IV,128)
    block = plaintextHex[0:16]
    state=fixHex(block)
    state=convertToBitstring(state,128)
    state = xor_two_binaryStrings(state,binIV)
    encryptedState = encrypt(state,key)
    EncryptedIV = encrypt(binIV, key)
    encryptedPlaintext=fixHexBack(bitstring2hexstring(EncryptedIV))
    encryptedStateString = bitstring2hexstring(encryptedState)
    encryptedStateString = fixHexBack(encryptedStateString)
    for j in range(len(encryptedStateString)):
        encryptedPlaintext.append(encryptedStateString[j])
    for i in range(16,int(len(plaintextHex)) - 1,16):
        block = plaintextHex[i:i+16]
        state = fixHex(block)
        state = convertToBitstring(state,128)
        state = xor_two_binaryStrings(state,encryptedState)
        encryptedState=encrypt(state,key)

        encryptedStateString=bitstring2hexstring(encryptedState)
        encryptedStateString=fixHexBack(encryptedStateString)
        for j in range(len(encryptedStateString)):
            encryptedPlaintext.append(encryptedStateString[j])
    return encryptedPlaintext,bitstring2hexstring(key)



def xor_two_binaryStrings(a,b):
    ans = ""

    # Loop to iterate over the
    # Binary Strings
    for i in range(128):

        # If the Character matches
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans

def matrixToArrByCol(matrix,arr):
    for m in range(4):
        for n in range(4):
            arr.append(matrix[n][m])

def xor_two_Matrices(matrix1,matrix2,result):
    for i in range(4):
        for j in range(4):
            result[i][j] = hex(int(matrix1[i][j],16) ^ int(matrix2[i][j],16))
    return result


def SerpentGenerateKey():
    key = ''.join(random.choice(string.hexdigits) for _ in range(64))
    key = key.lower()
    key = convertToBitstring(key,256)
    return key


def fixHex(block):
    str=""
    for i in range(len(block)):
        str+=block[i][2:]
    return str

def fixHexBack(block):
    str = []
    for i in range(0,len(block),2):
        str.append("0x"+block[i:i+2])
    return str
