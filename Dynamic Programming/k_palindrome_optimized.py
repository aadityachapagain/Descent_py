# Python program to find if given 
# string is K-Palindrome or not 
  
# Find if given string is 
# K-Palindrome or not 
def isKPalDP(str1, str2, m, n): 
      
    # Create a table to store 
    # results of subproblems 
    dp = [[0] * (n + 1) for _ in range(m + 1)] 
  
    # Fill dp[][] in bottom up manner 
    for i in range(m + 1): 
          
        for j in range(n + 1): 
              
            # If first string is empty, 
            # only option is to remove 
            # all characters of second string 
            if not i : 
                dp[i][j] = j    # Min. operations = j 
  
            # If second string is empty, 
            # only option is to remove 
            # all characters of first string 
            elif not j : 
                dp[i][j] = i    # Min. operations = i 
  
            # If last characters are same, 
            # ignore last character and 
            # recur for remaining string 
            elif (str1[i - 1] == str2[j - 1]): 
                dp[i][j] = dp[i - 1][j - 1] 
  
            # If last character are different,  
            # remove it and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i - 1][j],  # Remove from str1 
                                  (dp[i][j - 1])) # Remove from str2 
  
    return dp[m][n] 
  
# Returns true if str 
# is k palindrome. 
def isKPal(string, k): 
      
    revStr = string[::-1] 
    l = len(string) 
      
    return (isKPalDP(string, revStr, l, l) <= k * 2) 
  
  
# Driver program 
string = "acdcb"
k = 2
print("Yes" if isKPal(string, k) else "No")