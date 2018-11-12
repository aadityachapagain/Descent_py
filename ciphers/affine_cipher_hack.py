import pyperclip, affine_cipher, detectEnglish

SILENT_MODE = False


def main():
    # You might want to copy & paste already affine ciphered text
    myMessage = """W==M/Tk{@/kdx/JkTW/~J=/TnMJ=6"""

    hackedMessage = hackAffine(myMessage)

    if hackedMessage != None:
        print('Copying hacked message to clipboard: ')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')


def hackAffine(message):
    print('Hacking ..........')
    # python program can be stopped at any time in windows by pressing
    # Ctrl+C or Ctrl+D ( on Mac or Linux )
    print('(Press Ctrl+C or Ctrl+D to stop the program)')

    # brute force by looping through every possible key
    for key in range(len(affine_cipher.SYMBOLS) ** 2):
        keyA = affine_cipher.getKeyParts(key)[0]
        if affine_cipher.gcd(keyA, len(affine_cipher.SYMBOLS)) != 1:
            continue

        decryptedText = affine_cipher.decryptMessage(key,message)
        if not SILENT_MODE:
            print('Tried key {0} ....({1})'.format(key,decryptedText))

        if detectEnglish.isEnglish(decryptedText):
            # heck if the decrypted key has found
            print()
            print('Possible encryption hack:')
            print('key: {0}'.format(key))
            print('Decrypted message : ' + decryptedText[:200])
            print()
            print('Enter D for done, of just  press Enter to continue hacking: ')
            response = input('> ')
            if response.strip().upper().startswith('D'):
                return decryptedText
    return None

if __name__ == '__main__':
    main()