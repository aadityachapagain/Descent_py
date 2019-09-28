
"""
Starting with a 1-indexed array of zeros and a list of operations,
 for each operation add a value to each of the array element between two given indices, inclusive.
  Once all operations have been performed, return the maximum value in your array.

For example, the length of your array of zeros $n=10$. Your list of queries is as follows:

    a b k
    1 5 3
    4 8 7
    6 9 1

    Add the values of k between the indices a and b inclusive:

     1 2 3  4  5 6 7 8 9 10  <---index
    [0,0,0, 0, 0,0,0,0,0, 0]
    [3,3,3, 3, 3,0,0,0,0, 0]
    [3,3,3,10,10,7,7,7,0, 0]
    [3,3,3,10,10,8,8,8,1, 0]

    The largest value is 10 after all operations are performed.
"""

def arrayManipulation(n, queries):
    arr = [0]*n
    for i in queries:
        arr[i[0] - 1] += i[2]
        if i[1] != len(arr):
            arr[i[1]] -= i[2]
    maxval = 0
    itt = 0
    for q in arr:
        itt += q
        if itt > maxval:
            maxval = itt
    return maxval
