"""
There are N strings. Each string's length is no more than 20 characters.
 There are also Qqueries. For each query, you are given a string,
  and you need to find out how many times this string occurred previously.


INPUT FORMAT

The first line contains N, the number of strings.
The next N lines each contain a string.
The N+2nd line contains Q, the number of queries.
The following Q lines each contain a query string.

SAMPLE INPUT

4
aba
baba
aba
xzxb
3
aba
xzxb
ab

SAMPLE OUTPUT

2
1
0

"""

from collections import Counter

# Complete the matchingStrings function below.
def matchingStrings(strings, queries):
    ctr = Counter(strings)
    for query in queries:
        yield ctr[query]