def minion_game(string):
    kevin = 0
    stuart = 0
    n = list(string)
    vowel = list("AEIOU")
    allsubstrings = [n[i:j]
                     for i in range(len(n)) for j in range(i + 1, len(n) + 1)]
    for substring in allsubstrings:
        if substring[0] in vowel:
            kevin = kevin + 1
        else:
            stuart = stuart + 1

    if stuart > kevin:
        print(f'Stuart {stuart}')
    elif kevin > stuart:
        print(f'Kevin {kevin}')
    else:
        print("Draw")


if __name__ == '__main__':
    s = input()
    minion_game(s)
