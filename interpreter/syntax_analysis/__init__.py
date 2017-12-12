""" This is alternatively known as parsing. It is roughly the equivalent of checking that some ordinary text written in
a natural language (e.g. English) is grammatically correct (without worrying about meaning).
    The purpose of syntax analysis or parsing is to check that we have a valid sequence of tokens. Tokens are valid sequence
of symbols, keywords, identifiers etc. Note that this sequence need not be meaningful; as far as syntax goes, a phrase such
as "true + 3" is valid but it doesn't make any sense in most programming languages.
    The parser takes the tokens produced during the lexical analysis stage, and attempts to build some kind of in-memory
structure to represent that input. Frequently, that structure is an 'abstract syntax tree' (AST).
    The parser needs to be able to handle the infinite number of possible valid programs that may be
presented to it. The usual way to define the language is to specify a grammar. A grammar is a set of rules
(or productions) that specifies the syntax of the language (i.e. what is a valid sentence in the language).
    There can be more than one grammar for a given language. Furthermore, it is easier to build parsers for some grammars
than for others.
"""
from . import tree
from . import parser