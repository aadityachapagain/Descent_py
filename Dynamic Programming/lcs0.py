
"""
Problem Defination

LCS Problem Statement: Given two sequences, find the length of longest subsequence present in both of them.
A subsequence is a sequence that appears in the same relative order, but not necessarily contiguous. For example,
 “abc”, “abg”, “bdf”, “aeg”, ‘”acefg”, .. etc are subsequences of “abcdefg”.

In order to find out the complexity of brute force approach, we need to first know the number of possible different
subsequences of a string with length n, i.e., find the number of subsequences with lengths ranging from 1,2,..n-1.
Recall from theory of permutation and combination that number of combinations with 1 element are nC1. Number of combinations
with 2 elements are nC2 and so forth and so on. We know that nC0 + nC1 + nC2 + … nCn = 2n. So a string of length n has 2n-1
different possible subsequences since we do not consider the subsequence with length 0. This implies that the time complexity
of the brute force approach will be O(n * 2n). Note that it takes O(n) time to check if a subsequence is common to both the strings.
This time complexity can be improved using dynamic programming.

Examples:

LCS for input Sequences “ABCDGH” and “AEDFHR” is “ADH” of length 3.
LCS for input Sequences “AGGTAB” and “GXTXAYB” is “GTAB” of length 4.
"""

# Dynamic Programming implementation of LCS problem


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in range(m + 1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
            print('for Iternation {i} {j}')
            print(L)
    return L[m][n]
# end of function lcs


# Driver program to test the above function
X = "AGGTAB"
Y = "GXTXAYB"
print("Length of LCS is ", lcs(X, Y))
