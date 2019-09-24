# This is the solution code for hackerrank hourglass code 
"""

@author: Aaditya Chapagain
@company: AstralGod Inc
consider an array 

111001101
010111010
110000000
100001001
111011101

than hourglass of above array is considered a structure inside array which look like
abc
 d 
efg

so we calculate hourglass like a convolution of computer vision 
consider a matrix of 
111
010
111
and convolute that matrix over the whole array to get hourglass
"""

def hourglass_sum(arr):
    sum_hourglass = []
    j, i = len(arr) - 3 + 1, len(arr[0]) -3 + 1
    for idx in range(i):
        for jdx in range(j):
            diagonal  = arr[jdx][idx] + arr[jdx + 1][idx + 1] + arr[jdx + 2][idx + 2]
            remains = arr[jdx][idx + 1] + arr[jdx + 2][idx + 1] + arr[jdx][idx + 2] + arr[jdx + 2][idx]
            sum_hourglass.append(diagonal + remains)

    return sorted(sum_hourglass, reversed = True)

