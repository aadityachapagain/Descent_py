"""Given a non-empty array of integers, every number appears twice except for one number.
 Find that single number.
Example 1:
Input: [2,2,1]
Output: 1
Example 2:
Input: [4,1,2,1,2]
Output: 4 """

import time


numbers = [4,1,2,1,2]
# Solution 1

strt_time = time.time()
d = {}
for i in numbers:
    d[i] = d.get(i,0) +1

for key, value in d.items():
    if value == 1:
        print(key)

print('Solution 1 takes time of: ',time.time() - strt_time)

# Solution 2

strt_time = time.time()
unique_id = numbers[0]
for i in range(1, len(numbers)):
    unique_id ^= numbers[i]

print(unique_id)
print('Solution 2 takes time of: ', time.time() - strt_time)