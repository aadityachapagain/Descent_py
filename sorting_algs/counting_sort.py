"""
pure implementation of counting sort in python
"""

from __future__ import print_function

def counting_sort(collection):
    """
    pure implementation of counting sort algorighm in python
    :param collection: some mutable ordered collection with heterogenous
    comparable items inside
    :return: the same collection ordered by ascending
    """

    #if collection is empty , returns empty
    if collection == []:
        return []

    #get some information about the collection
    coll_len = len(collection)
    coll_max = max(collection)
    coll_min = min(collection)

    #create counting array
    counting_arr_length = coll_max + 1 - coll_min
    counting_arr = [0] * counting_arr_length

    #count how much a number appears in the collection
    for number in collection:
        counting_arr[number - coll_min] += 1

    # sum each position with its predecessors .now , counting_arr[i] tells
    # us how many elements  <= i has in the collection
    for i in range(1, counting_arr_length):
        counting_arr[i] = counting_arr[i] + counting_arr[i-1]

    # create the output collection
    ordered = [0]* coll_len

    #place the elements in the output , respecting the original order
    # from the end to begin, updating counting_arr
    for i in reversed(range(0,coll_len)):
        ordered[counting_arr[collection[i] - coll_min] - 1] = collection[i]
        counting_arr[collection[i] - coll_min] -= 1

    return ordered


def counting_sort_string(string):
    return ''.join([chr(i) for i in counting_sort([ord(c) for c in string])])

if __name__ == '__main__':
    # Test string sort
    assert "eghhiiinrsssttt" == counting_sort_string("thisisthestring")

    try:
        raw_input          # Python 2
    except NameError:
        raw_input = input  # Python 3

    user_input = raw_input('Enter numbers separated by a comma:\n').strip()
    unsorted = [int(item) for item in user_input.split(',')]
    print(counting_sort(unsorted))