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
# A Naive recursive Python implementation of LCS problem 
  
def lcs(X, Y, m, n): 
  
    if m == 0 or n == 0: 
       return 0; 
    elif X[m-1] == Y[n-1]: 
       return 1 + lcs(X, Y, m-1, n-1); 
    else: 
       return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n)); 
  
  
# Driver program to test the above function 
X = "AGGTAB"
Y = "GXTXAYB"
print ("Length of LCS is ", lcs(X , Y, len(X), len(Y))) 