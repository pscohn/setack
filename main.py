# -*- coding: utf-8 -*-

'''
Semantics of setack

built-in sets:
    * Natural Numbers
    * Real Numbers

built-in types:
    empty set (∅)
    Int
    Float
    Set
    Booleans and associated operations, throw runtime error if sets

operations:
    membership              (∈):
    not-member              (∉):
    subset                  (⊆): A ⊆ B means every element of A is also an element of B
    union                   (∪): A ∪ B means the set of those elements which are either in A, or in B, or in both.
    intersection            (∩): A ∩ B means the set that contains all those elements that A and B have in common.
    difference              (\): In the left set and not in the right set
    symmetric difference    (∆): In either set but not in both
    power set               (ℙ): All possible subsets
'''

import tokenize
from   token    import tok_name as tokenName
from   StringIO import StringIO

def generateTokens(input):
    return tokenize.generate_tokens(StringIO(input).readline)

def parse(tokens):
    result = []
    token = next(tokens, None)
    while token:
        number, value, start, end, line = token
        if value is '}':
            break
        elif value in (',', '', '\n') or number is 5: # 5: indent
            token = next(tokens, None)
            continue
        elif number is 1:
            result.append(value)
        elif number is 2:
            try:
                n = int(value)
            except ValueError:
                n = float(value)
            result.append(n)
        elif value is '{':
            s = set(parse(tokens))
            result.append(s)
        else:
            raise Exception('Error: Unexpected token: %s' % (token,))
        token = next(tokens, None)
    return result

if __name__ == '__main__':

    result = parse(generateTokens('''

        {1, 2} {3, 4} union

    '''))

    print result




