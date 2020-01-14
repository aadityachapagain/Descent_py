"""
Let 1 represent ‘A’, 2 represents ‘B’, etc. Given a digit sequence, count the number of possible decodings of the given digit sequence.
Examples:

Input:  digits[] = "121"
Output: 3
// The possible decodings are "ABA", "AU", "LA"

Input: digits[] = "1234"
Output: 3
// The possible decodings are "ABCD", "LCD", "AWD"
"""

def count_decoding_DP(digits, n): 
          
        # A table to store results of subproblems 
    count = [0] * (n+1)  
    count[0] = 1
    count[1] = 1
  
    for i in range(2, n+1): 
      
        count[i] = 0
  
        # If the last digit is not 0, 
                # then last digit must add to 
        # the number of words 
        if (digits[i-1] > '0'): 
            count[i] = count[i-1] 
  
        # If second last digit is smaller 
                # than 2 and last digit is 
        # smaller than 7, then last two 
                # digits form a valid character 
        if (digits[i-2] == '1' or (digits[i-2] == '2' and digits[i-1] < '7') ): 
            count[i] += count[i-2] 
      
    return count[n] 
  
  
# Driver program to test above function 
digits = ['1','2','3','4'] 
n = len(digits) 
  
print("Count is ",count_decoding_DP(digits, n)) 
