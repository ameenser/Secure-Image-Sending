

def getPublickeyFromReciver(reciver):
    return reciver.getPublickey()


def sendImageToReciver(sender,encryptedMatrix,ckey,reciver):
    reciver.getImageFromSender(sender,encryptedMatrix,ckey)