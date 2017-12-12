""" This is roughly the equivalent of checking that some ordinary text written in a natural language (e.g. English)
actually means something (whether or not that is what it was intended to mean).
    Semantic analysis is the activity of a compiler to determine what the types of various values are, how those types
interact in expressions, and whether those interactions are semantically reasonable. For instance, you can't reasonably
multiply a string by class name, although no editor will stop you from writing.
    To do this, the compiler must first identify declarations and scopes, and typically records the result of this step in
a set of symbol tables. This tells it what specific identifiers means in specific contexts. It must also determine the types
of various literal constants;
"""

from . import table
from . import analyzer