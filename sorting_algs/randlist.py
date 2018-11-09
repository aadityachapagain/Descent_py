import random


def randlist(start=0, stop=100, length=30):
    i = 0
    list_rand = []
    while i <= length:
        i += 1
        step = 1
        if start > stop:
            step = -1
        list_rand.append(random.randrange(start, stop, step))

    return list_rand


if __name__ == '__main__':
    print(randlist())
