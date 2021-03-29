import hashlib
import numpy as np
from PIL import Image
from CBC_decryption import CBC_Serpent_decrypt
from CBC_encryption import CBC_Serpent_encrypt
from FakeServer import getPublickeyFromReciver,sendImageToReciver
from RsaDecryption import *
from RsaEncryption import *
from RsaGenerateKey import generate_keyPairs
 
class User:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        public,private = generate_keyPairs()
        self.public_key=public
        self.private_key=private

    def sendImage(self, path,reciver):
        public_key = getPublickeyFromReciver(reciver)
        width,height,plaintext=getDataFromImage(path)
        encryptedPlaintext,key=CBC_Serpent_encrypt(plaintext)
        signature= signing(key,self.private_key)
        keyAndSignature=key+str(signature)
        ckey=Rsa_encrypt(keyAndSignature,public_key)
        showHexPlaintextAsImage(encryptedPlaintext,height,width)
        return encryptedPlaintext,ckey

    def getPublickey(self):
        return self.public_key

    def getImageFromSender(self,sender,encryptedPlaintext,ckey):
        public_key = getPublickeyFromReciver(sender)
        keyAndSignature=Rsa_decrypt(ckey,self.private_key)
        key=keyAndSignature[0:64]
        signature=keyAndSignature[64:]
        signature=FixSignature(signature)
        if(verifying(signature,key,public_key)):
            decryptedPlaintext=CBC_Serpent_decrypt(encryptedPlaintext,key)
            width,height=getImageLimts(decryptedPlaintext)
            showHexPlaintextAsImage(decryptedPlaintext,height,width)


def signing(plaintext,private_key):
     digestKey = hashlib.sha256(str(plaintext).encode()).hexdigest()
     signature=Rsa_encrypt(digestKey,private_key)
     return  signature

def verifying (signature,plaintext,public_key):
    expectedDigest = Rsa_decrypt(signature,public_key)
    digestKey=hashlib.sha256(str(plaintext).encode()).hexdigest()
    if expectedDigest != digestKey:
        print("Expected Digest not equal digestKey")
        return False
    return True

def FixSignature(signature):
    listSignature = signature.strip('][').split(', ')
    for i in range(len(listSignature)):
        listSignature[i]=int(listSignature[i])
    return listSignature

def showHexPlaintextAsImage(plaintext,width,height):
    data=convertPlaintextAsImage(plaintext,width,height)
    img = Image.fromarray(data,'RGB')
    img.save('my.jpg')
    img.show()

def convertPlaintextAsImage(plaintext,width,height):
    plaintext=np.array(plaintext)
    data = np.zeros((width, height, 3),dtype=np.uint8)
    k=0
    for i in range(width):
        for j in range(height):
            for m in range(3):
                data[i][j][m]=int(plaintext[k],16)
                k=k+1
    return data

def convertImageAsPlaintext(imageAsMatrix):
    plaintext = []
    for i in range(len(imageAsMatrix)):
        for j in range(len(imageAsMatrix[0])):
            for m in range(len(imageAsMatrix[0][0])):
                plaintext.append(hex(imageAsMatrix[i][j][m]))
    return plaintext


def getImageLimts(decryptedPlaintext):
    decryptedPlaintext = hexFix(decryptedPlaintext)
    high_width = int(decryptedPlaintext[len(decryptedPlaintext) - 4],16)
    low_width = int(decryptedPlaintext[len(decryptedPlaintext) - 3],16)
    high_height = int(decryptedPlaintext[len(decryptedPlaintext) - 2],16)
    low_height = int(decryptedPlaintext[len(decryptedPlaintext) - 1],16)
    width = (high_width << 8) | (low_width);
    height = (high_height << 8) | (low_height);
    return width,height

def getDataFromImage(path):
    im = Image.open(path)
    width = im.size[0]
    height = im.size[1]
    data = list(im.getdata())
    high_width,low_width = bytes(width)
    high_height,low_height = bytes(height)
    plaintext = []
    for i in range(len(data)):
        for j in range(3):
            plaintext.append(data[i][j])
    while (len(plaintext) % 16 != 0):
        plaintext.append(0)
    for i in range(12):
        plaintext.append(0)
    plaintext.append(int(high_width,16))
    plaintext.append(int(low_width,16))
    plaintext.append(int(high_height,16))
    plaintext.append(int(low_height,16))
    plaintextHex = []
    for i in range(0,len(plaintext)):
        plaintextHex.append(hex(plaintext[i]))
    plaintextHex = hexFix(plaintextHex)
    return width,height,plaintextHex


def bytes(num):
    return hex(num >> 8), hex(num & 0xFF)


def hexFix(text):
    for i in range(0,len(text)):
        str_hex = text[i]
        text[i]='0x' + str_hex[2:].zfill(2)
    return text