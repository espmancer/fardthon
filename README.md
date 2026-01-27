# fardthon
Python-built maybe esolang. Only uses the word "fard". At the moment I'm only doing control flow. 

## Structure
Each code line is prefaced with a header: 
f - Comparison Operators 
a - Boolean Operators 
r - Conditionals 
d - Variables 
F - ASCII 
A - Loops 
R - Numbers 
D - Arithmetic 
ff - Print 

Each header has a set of tokens that cycle as well:
f - Comparison Operators
    f - =
    a - !=
    r - <
    d - >
    F - <=
    A - >= 
    R - ==
a - Boolean Operators
    f - and
    a - or
    r - not
r - Conditionals
    f - if
    a - elif
    r - else
d - Variables
    f - Define: Uses ASCII structure
    a - Equals: Uses Arithmetic Operators structure
    r - Value: Uses Numbers/ASCII structure
F - ASCII
    Uses Numbers structure and converts it to ASCII.
A - Loops
    f - While
    a - For
    r - End
R - Numbers
    The 8 letters of "fardFARD" each represent a digit in base 8, starting from 0. This base 8 is then converted to base 10.
D - Arithmetic Operators
    f - +
    a - -
    r - *
    d - /
    F - ^
ff - Print
    The token after this header is what gets printed.

## Examples
### Fard Loop
Python
```py
while 1==1:
    print("fard")
```
Fardthon
```fard
A
f
a
f
R
a
ff
F
aFA aFa aAr aFF
A
r	
```
Breakdown
```
Header: Loops
	While (
    Header: Numbers
        Base 8 to be converted to Base 10
    Header: Comparison
        ==
    Header: Numbers
        Base 8 to be converted to Base 10
    )	
    {
		Header: Print
    		Header: ASCII
        		Base 8 to be converted to ASCII
    }
Header: Loops
    End     
```
