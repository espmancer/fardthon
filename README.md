# fardthon
Python-built maybe esolang. Only uses the word "fard". At the moment I'm only doing control flow. 
NOTE: All of the actual code is generated from ChatGPT, if this wasn't a joke language I'd actually work to learn how to make a parser and such.

## Structure
Each code line is prefaced with a header: 
1. Comparison Operators 
2. Boolean Operators 
3. Conditionals 
4. Variables 
5. ASCII 
6. Loops 
7. Numbers 
8. Arithmetic 
9. Print 

Each header has a set of tokens that cycle based on the number of "fard"s:
1. Comparison Operators
    1 - =
    2 - !=
    3 - <
    4 - >
    5 - <=
    6 - >= 
2. Boolean Operators
    1 - and
    2 - or
    3 - not
3. Conditionals
    1 - if
    2 - elif
    3 - else
4. Variables
    1 - Define: Uses ASCII structure
    2 - Equals: Uses Arithmetic Operators structure
    3 - Value: Uses Numbers/ASCII structure
5. ASCII
    Uses Numbers structure and converts it to ASCII.
6. Loops
    1 - While
    2 - For
    3 - End
7. Numbers
    The 4 letters of "fard" each represent a digit in base 4, starting from 0. This base 4 is then converted to base 10.
8. Arithmetic Operators
    1 - +
    2 - -
    3 - *
    4 - /
    5 - ^
9. Print
    The line directly after this header is what gets printed.

## Examples
### Hello World
Python
```py
print("Hello world!")
```
Fardthon
```fard
fardfardfardfardfardfardfardfardfard
fardfardfardfardfard
afrfaraaardfardfarddfrffadadarddadfrardfaraffrfa
```
Breakdown
```
Header: Print
    Header: ASCII
        Base 4 to be converted to text        
```
### Fard Loop
Python
```py
while 1==1:
    print("fard")
```
Fardthon
```fard
fardfardfardfardfardfard
fard
fard
fardfardfardfardfardfardfard
a
fardfardfardfardfardfardfard
a
fardfardfardfardfardfardfardfardfard
fardfardfardfardfard
arararfaadfraraf
fardfardfardfardfardfard
fardfardfard
```
Breakdown
```
Header: Loops
    Header: Boolean
        Comparison: ==
            Header: Numbers
                Base 4 to be converted to number
            Header: Numbers
                Base 4 to be converted to number

Header: Print
    Header: ASCII
        Base 4 to be converted to text

Header: Loops
    End     
```