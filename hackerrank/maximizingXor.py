"""
Given two integers, LL and RR, find the maximal value of Axor BA⊕B, where AA and BB satisfy the following condition:

L≤A≤B≤R

Input Format

The input contains two lines; LL is present in the first line and RR in the second line.

Constraints
1≤L≤R≤10^3 
 
Output Format

The maximal value as mentioned in the problem statement.

Sample Input

10
15
Sample Output

7
Explanation

The input tells us that L=10L=10 and R=15R=15. All the pairs which comply to above condition are the following:
10 xor 10= 010⊕10=0
10 xor 11= 110⊕11=1
10 xor 12= 610⊕12=6
10 xor 13= 710⊕13=7
10 xor 14= 410⊕14=4
10 xor 15= 510⊕15=5
11 xor 11= 011⊕11=0
11 xor 12= 711⊕12=7
11 xor 13= 611⊕13=6
11 xor 14= 511⊕14=5
11 xor 15= 411⊕15=4
12 xor 12= 012⊕12=0
12 xor 13= 112⊕13=1
12 xor 14= 212⊕14=2
12 xor 15= 312⊕15=3
13 xor 13= 013⊕13=0
13 xor 14= 313⊕14=3
13 xor 15= 213⊕15=2
14 xor 14= 014⊕14=0
14 xor 15= 114⊕15=1
15 xor 15= 015⊕15=0

Here two pairs (10, 13) and (11, 12) have maximum xor value 7, and this is the answer.

"""
def maximizingXor(l, r):
    s = l ^ r
    p = 1
    while (s > 0):
        p<<= 1
        s>>= 1
    return p - 1