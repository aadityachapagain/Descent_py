from __future__ import print_function

from inspect.TimeIt import timeit


@timeit
def cocktail_shaker_sort(unsorted):
    """
    implementation of cocktail shaker sort algo in pure python
    :param unsorted: unsorted list
    :return: sorted list
    """

    for i in range(len(unsorted)-1,0,-1):
        swapped = False

        for j in range(i,0,-1):
            if unsorted[j] < unsorted[j-1]:
                unsorted[j], unsorted[j-1] = unsorted[j-1], unsorted[j]
                swapped = True

        for j in range(i):
            if unsorted[j] > unsorted[j+1]:
                unsorted[j], unsorted[j+1] = unsorted[j+1], unsorted[j]
                swapped = True

        if not swapped:
            return unsorted


if __name__=="__main__":
    try:
        raw_input       # python 2
    except NameError:
        raw_input = input

    user_input = raw_input('Enters a numbers seperated by comma : \n').strip()
    unsorted = [int(item) for item in user_input.split(',')]
    cocktail_shaker_sort(unsorted)
    print(unsorted)