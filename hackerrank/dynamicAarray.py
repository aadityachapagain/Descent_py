"""

 ____                              _           _                         
|  _ \ _   _ _ __   __ _ _ __ ___ (_) ___     / \   _ __ _ __ __ _ _   _ 
| | | | | | | '_ \ / _` | '_ ` _ \| |/ __|   / _ \ | '__| '__/ _` | | | |
| |_| | |_| | | | | (_| | | | | | | | (__   / ___ \| |  | | | (_| | |_| |
|____/ \__, |_| |_|\__,_|_| |_| |_|_|\___| /_/   \_\_|  |_|  \__,_|\__, |
       |___/                                                       |___/ 


Create a list, seqList, of N empty sequences, where each sequence is indexed from 0 to N-1. The elements within each of the N sequences also use 0-indexing.
Create an integer, lastAns, and initialize it to 0.
The 2 types of queries that can be performed on your list of sequences (seqList) are described below:

Query: 1 x y
Find the sequence, seq, at index ((x ⊕ lastAns) % N) in seqList.
Append integer y to sequence seq.
Query: 2 x y
Find the sequence, seq, at index ((x ⊕ lastAns) % N) in seqList.
Find the value of element (y%size) in seq (where size is the size of seq) and assign it to lastAns.
Print the new value of lastAns on a new line

Sample Input:

2 5
1 0 5
1 1 7
1 0 3
2 1 0
2 1 1

Sample Output:

7
3

Explanation:

Initial Values:
N=2
lastAns=0
S0={}
S1={}

Query 0: Append 5 to sequence ((0 ⊕ 0) % 2) =0.
lastAns=0
S0={5}
S1={}

Query 1: Append 7 to sequence ((1 ⊕ 0) % 2) =1.
lastAns=0
S0={5}
S1={7}

Query 2: Append 3 to sequence ((0 ⊕ 0) % 2) =0..
lastAns=0
S0={5,3}
S1={7}

Query 3: Assign the value at index 0 of sequence ((1 ⊕ 0) % 2) =1. to lastAns, print lastAns. lastAns=7

S0={5,3}
S1={7}

7
Query 4: Assign the value at index 1 of sequence ((1 ⊕ 7) % 2) =0 to lastAns, print lastAns. lastAns=3

S0={5,3}
S1={7}

3

"""


def dynamicArray(n, queries):
    # result = []
    # Write your code here
    lastAns = 0
    seqList = [[] for _ in range(n)]

    for q, x, y in queries:
        index = (x ^ lastAns) % n
        seq = seqList[index]
        if q == 1:
            seq.append(y)
        elif q == 2:
            size = len(seq)
            lastAns = seq[y % size]
            yield lastAns
        else:
            raise ValueError()