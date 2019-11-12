"""
Laventine distance  Given two string how many operation like  addition, substraction and 
substitution required to change one word to other word.

solving using dynamic problems
"""

def calcLaventenstineDistance(str1, str2, m, n):
    
    """
    Calculate the Laventenstine Distance of between two strings
    """
    # create a table to store the results of a subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m +1):
        for j in range(n + 1):

            # If first string is empty only way is to insert string of second string
            if i == 0:
                dp[i][j] = j
            
            # if second string is empty only way is to insert string of first string
            elif j == 0:
                djp[i][j] = i

            # if last char is same ingore the lasts char and recur for remaning char
            elif str1[i -1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            
            # if last char is not same consider all posible and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i-1][j], dp[i-1][j-1])

    return dp[m][n]