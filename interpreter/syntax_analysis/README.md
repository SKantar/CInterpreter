# Syntax Analysis

The syntax analyser groups and structures the lexical tokens according to the syntax
rules of the programming language. It performs the parsing process repeatedly grouping
together components by performing reductions according to the production rules. Assuming
that the sequence of tokens is syntactically correct, the parse should succeed.
If the sequence is not syntactically correct, then the syntax analyser should report
an error and then perform some appropriate recovery action.
The syntax analyser constructs a data structure representing the syntactic structure
of the input. This is usually based on some form of tree where the nodes represent
syntactic components defined by the grammar. This is the parse tree or abstract syntax
tree. This data structure should contain or link to all the information needed by later
phases of compilation. So, for example, a node corresponding to the occurrence of a
constant value in the original program should contain or link to information defining
that constant such as its type, value and so on.
It is clear that the lexical and syntax analysers are doing similar things. They
are both grouping together characters or tokens into larger syntactic units. So there
is an issue about whether a particular syntactic structure should be recognised by
the lexical analyser or by the syntax analyser. The traditional approach, and it is
an approach that works well, is to recognise the simpler structures in the lexical
analyser, specifically those that can be expressed in terms of a Chomsky type 3
grammar. Syntactic structures specified by a type 2 or more complex grammar are
then left for resolution by the syntax analyser. In theory, the syntax analyser could
deal with the lexical tokens using a type 2 grammar parsing approach, but this would
add significantly to the complexity of the syntax analyser. Furthermore, by leaving
the lexical analyser to deal with these tokens improves compiler efficiency because
simpler and faster type 3 parsing techniques can be used.