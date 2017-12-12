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
will be read by the lexical analyser and it would generate this stream of tokens:
```
Token(ID, 'sum'),   Token(ASSIGN, '='), Token(INTEGER_CONST, 0), TOKEN(SEMICOLON, ';'), Token(FOR, 'for'),
Token(LPAREN, '('), Token(ID, 'i'), Token(ASSIGN, '='), Token(INTEGER_CONST, 0), TOKEN(SEMICOLON, ';'),
Token(ID, 'i'), Token(LE_OP, '<='), Token(INTEGER_CONST, 99), TOKEN(SEMICOLON, ';'), Token(ID, 'i'),
Token(INC_OP, '++'), Token(RPAREN, ')'), Token(ID, 'sum'), Token(ADD_ASSIGN, '+='), Token(ID, 'i')
```

The syntax of these basic lexical tokens is usually simple, and the expectation
is that the syntax can be specified formally in terms of a Chomsky type 3 grammar
(i.e. in terms of regular expressions). This considerably simplifies the coding of the
lexical analyser.

The output of the lexical analyser is a stream of tokens, passed to the syntax
analyser. The interface could be such that the lexical analyser tokenises the entire
input file and then passes the whole list of tokens to the syntax analyser. Alternatively,
the tokens could be passed on to the syntax analyser one at a time, when demanded
by the syntax analyser.