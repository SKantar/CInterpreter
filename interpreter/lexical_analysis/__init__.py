""" Lexical analysis is the process of analyzing a stream of individual characters (normally arranged as lines),
into a sequence of lexical tokens (tokenization. for instance of "words" and punctuation symbols that make up source code)
to feed into the parser. Roughly the equivalent of splitting ordinary text written in a natural language (e.g. English)
into a sequence of words and punctuation symbols. Lexical analysis is often done with tools such as lex, flex and jflex.
    Strictly speaking, tokenization may be handled by the parser. The reason why we tend to bother with tokenising in practice
is that it makes the parser simpler, and decouples it from the character encoding used for the source code.
"""
from . import token_type
from . import token
from . import lexer