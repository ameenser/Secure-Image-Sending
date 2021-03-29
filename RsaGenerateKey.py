
import random

max_PrimLength = 1000000000000

'''
calculates the modular inverse from e and phi
'''


def egcd(a,b):
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = egcd(b % a,a)
        return (g,x - (b // a) * y,y)


'''
calculates the gcd of two ints
'''


def gcd(a,b):
    while b != 0:
        a,b = b,a % b
    return a


'''
checks if a number is a prime
'''


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3,int(num ** 0.5) + 2,2):
        if num % n == 0:
            return False
    return True


def generateRandomPrim():
    while (1):
        ranPrime = random.randint(0,max_PrimLength)
        if is_prime(ranPrime):
            return ranPrime


def generate_keyPairs():
    p = generateRandomPrim()
    q = generateRandomPrim()

    n = p * q
    '''phi(n) = phi(p)*phi(q)'''
    phi = (p - 1) * (q - 1)

    '''choose e coprime to n and 1 > e > phi'''
    e = random.randint(1,phi)
    g = gcd(e,phi)
    while g != 1:
        e = random.randint(1,phi)
        g = gcd(e,phi)

    '''d[1] = modular inverse of e and phi'''
    d = egcd(e,phi)[1]

    '''make sure d is positive'''
    d = d % phi
    if (d < 0):
        d += phi

    return ((e,n),(d,n))
