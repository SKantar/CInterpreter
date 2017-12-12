# Lexical Analysis

This first phase of compilation reads the characters of the source program and groups
them together into a stream of lexical tokens. Each lexical token is a basic syntactic
component of the programming language being processed. These are tokens such
as numbers, identifiers, punctuation, operators, strings, reserved words and so on.
Comments can be ignored unless the language defines special syntactic components
encoded in comments that may be needed later in compilation. White space (spaces,
tabs, newlines, etc.) may be ignored except, again, where they have some syntactic
significance (where spacing indicates block structure, where white space may occur
in character strings and so on).

For example, this C program fragment:
``` c++
sum = 0;
for (i=0; i<=99; i++) sum += i; /* sum array */
```