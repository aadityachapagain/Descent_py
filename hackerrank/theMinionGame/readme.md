Kevin and Stuart want to play the 'The Minion Game'.

## Game Rules

Both players are given the same string, **_S_**.  
Both players have to make substrings using the letters of the string **_S_**.  
Stuart has to make words starting with consonants.  
Kevin has to make words starting with vowels.  
The game ends when both players have made all possible substrings.

## Scoring
A player gets `+1` point for each occurrence of the substring in the string **_S_**.

## For Example:
String **_S_** = BANANA  
Kevin's vowel beginning word = ANA  
Here, ANA occurs twice in BANANA. Hence, Kevin will get `2` Points.

For better understanding, see the image below:

![image src: HackerRank](https://github.com/aadityachapagain/Descent_py/tree/master/hackerrank/theMinionGame/image.png)

Your task is to determine the winner of the game and their score.

## Input Format

A single line of input containing the string **_S_**.  
**Note**: The string  will contain only uppercase letters: **[A-Z]**.

## Output Format

Print one line: the name of the winner and their score separated by a space.  
If the game is a draw, print Draw.

## Sample Input 

``` BANANA ```

## Sample Output

``` Stuart 12 ```

I have provided my version of code here. If you can, do try to optimize my code further. Happy Coding!