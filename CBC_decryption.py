import numpy as np

from CBC_encryption import fixHex,xor_two_binaryStrings,fixHexBack
from Serpent import convertToBitstring,decrypt,bitstring2hexstring


def CBC_Serpent_decrypt(encryptedPlainText, key):
    decryptedPlaintext=[]
    IV = encryptedPlainText[0:16]
    IV=fixHex(IV)
    key = convertToBitstring(key,256)
    binEncryptedIV=convertToBitstring(IV,128)
    DecryptedIV=decrypt(binEncryptedIV,key)
    for i in range (16,int(len(encryptedPlainText)) - 1,16):
        block = encryptedPlainText[i:i + 16]
        block=fixHex(block)
        block=convertToBitstring(block,128)
        state=decrypt(block,key)
        lastblock = encryptedPlainText[i - 16:i]
        lastblock = fixHex(lastblock)
        lastblock = convertToBitstring(lastblock,128)
        if (i == 16):
            decryptedState = xor_two_binaryStrings(DecryptedIV, state)
        else:
            decryptedState = xor_two_binaryStrings(lastblock,state)
        decryptedStateString = bitstring2hexstring(decryptedState)
        decryptedStateString = fixHexBack(decryptedStateString)
        for j in range(len(decryptedStateString)):
            decryptedPlaintext.append(decryptedStateString[j])
    return decryptedPlaintext
