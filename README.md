# stalgcm
Major Course Output for STALGCM - S13
Author: Ralph Dawson G. Pineda
Date: July 2023

Model of Computation: 2-way deterministic finite automata
Programming Language used: Python

Instructions to run the program: 

## :rocket: clone the repository
After cloning, install the necessary pip packages for the GUI:

```
pip install -r requirements.txt
```
or 
```
pip3 install -r requirements.txt
```

After installing of the necessary dependencies, run program with:
```
python main.py
```
or
```
python3 main.py
```


## :trident: text input format
**Q**     *This is the list of states separated by space characters*
**Sigma**    *This is the alphabet separated by space characters*
**(Start, Final, Reject)**     *Tuple (a,b, c) representing the start, accepting, and reject states. These should exist in Q*
**n**      *integer n that represents how many transistion functions will follow below*
**transition functions**    *current state, input, next state, direction*
.
.  *n times*
.
**transition functions** 

## :x: restrictions
1. let s be an element from sigma, s should never be = '-' or '+'
   - '-' is reserved for the left end marker
   - '+' is reserved for the right end marker
   - if your string input uses these symbols, replace them with some other symbol.
  
2. transition function reading left end marker '-' as input should always result to 'right' direction
3. transition function reading right end marker '+' as input should always result to 'left' direction
4. transition function from the accepting state should never move into another non accepting state
5. transition function from the reject state should enver move into anbother non reject state
  
## :dragon: test cases
the tests folder contains two directories: one for the machine definitions, and the other is for sample inputs
with expected outputs. The machine definition files will be named similarly along with their respective sample inputs
for easy reference.

1. sigma = {a,b} and w = even number 'a' and 'b' is divisible by 3
2. sigma = {a,b} and w = starts with 'b' and ends with 'a' where 'a' always come in pairs
3. sigma = {a,b} and w = (a+b)<sup>\*</sup>δ(a+b)<sup>\*</sup> and δ = baab