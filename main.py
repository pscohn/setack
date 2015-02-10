'''
Semantics of Setack

expr = atom expr*
     | atom
atom = boolean
     | float
     | integer
     | symbol
     | set
set  = '{' expr [, expr]* '}'
     | '∅'

Built-in sets: Empty set, Natural numbers, Real numbers

Built-in symbols:
    membership              (∈):
    not-member              (∉):
    subset                  (⊆): A ⊆ B means every element of A is also an element of B
    union                   (∪): A ∪ B means the set of those elements which are either in A, or in B, or in both.
    intersection            (∩): A ∩ B means the set that contains all those elements that A and B have in common.
    difference              (\): In the left set and not in the right set
    symmetric difference    (∆): In either set but not in both
    power set               (ℙ): All possible subsets
'''

import parser

if __name__ == '__main__':

    syntaxTree = parser.parse(u'''

        {True, False, 01, -2, {-3.5, 4.0}} union

    ''')

    print(syntaxTree)

