from __future__ import print_function
import sys, random

"""
The affine cipher is a type of monoalphabetic substitution cipher, wherein each letter in an alphabet is mapped to its numeric equivalent,
 encrypted using a simple mathematical function, and converted back to a letter. The formula used means that each letter encrypts to one other
  letter, and back again, meaning the cipher is essentially a standard substitution cipher with a rule governing which letter goes to which. As such,
   it has the weaknesses of all substitution ciphers
"""

SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

def main():
    message = input('Enter message: ')
    key  = int(input('Enter key[2000 - 9000]: '))
    mode = input('Encrypt/Decrypt [E/D]: ')

    if mode.lower().startswith('e'):
        mode = 'encrypt'
        translated = encryptMessage(key,message)
    elif mode.lower().startswith('d'):
        mode = 'decrypt'
        translated = decryptMessage(key,message)
    print('\n%sed text: \n%s' % (mode.title(), translated))


def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return keyA, keyB


def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        sys.exit('The affine cipher becomes weak when key A is set to 1. Choose different key')
    if keyB == 0 and mode == 'encrypt':
        sys.exit('The affine cipher becomes weak when key B is set to 0. Choose different key ')
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        sys.exit('Key A must be greater than 0 and key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
    if gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit('key A {0} and the symbol set size {1} are not relatively prime. Choose a different key.'.format(keyA,len(SYMBOLS)))


def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    cipherText = ''
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            cipherText += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            cipherText += symbol
    return cipherText


def decryptMessage(key,message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plainText = ''
    modInverseOfkeyA = findModInverse(keyA, len(SYMBOLS))
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            plainText += SYMBOLS[(symIndex - keyB) * modInverseOfkeyA % len(SYMBOLS)]
        else:
            plainText += symbol
    return plainText


def gcd(a,b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    # returns the modular inverse of  a % m , which is the number x such that a*x % m = 1
    if gcd(a,m) != 1:
        return None# no mod inverse if a & m aren't relatively prime

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q *
                                                                v3), v1, v2, v3

    return u1 % m


def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB

if __name__ == '__main__':
    main()