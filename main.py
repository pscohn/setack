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

import re

def tokensFromLine(line):

    pattern = re.compile(u'''
          (?P<LeftBracket>{)
        | (?P<RightBracket>})
        | (?P<Comma>,)
        | (?P<Bool>True|False)
        | (?P<Float>\d+\.\d+)
        | (?P<Int>\d+)
        | (?P<Word>\w+)
        | (?P<EmptySet>∅)
    ''', re.VERBOSE | re.UNICODE)

    for m in pattern.finditer(line):
        ((key, value),) = [(k, v) for k, v in m.groupdict().items() if v is not None]
        yield (key, value, m.start(key), m.end(key))

def generateTokens(input):
    """(type, value, start, end, line)"""
    lines = input.split('\n')
    for lineno, line in enumerate(lines):
        for tok in tokensFromLine(line):
            yield tok + (lineno,)

def parse(tokens):

    result = []
    tok    = next(tokens, None)

    while tok:

        type, value, start, end, lineno = tok

        if type == 'RightBracket': 
            result.append('}')
            break
        elif type == 'Bool':
            if value == 'True':
                result.append(True)
            elif value == 'False':
                result.append(False)
        elif type == 'Word':
            result.append(value)
        elif type == 'Float':
            result.append(float(value))
        elif type == 'Int':
            result.append(int(value))
        elif type == 'Comma':
            result.append(value)
        elif type == 'LeftBracket':
            resultSet      = frozenset()
            commaSepStexes = parse(tokens)
            if commaSepStexes:
                stexes   = []
                currStex = []
                for item in commaSepStexes:
                    if item in (',', '}'):
                        stexes.append(tuple(currStex))
                        currStex = []
                    else:
                        currStex.append(item)
                resultSet = frozenset(stexes)
            result.append(resultSet)
        elif type == 'EmptySet':
            result.append(frozenset())
        else:
            raise Exception('Error: Unexpected token: %s' % (tok,))

        tok = next(tokens, None)

    return result

if __name__ == '__main__':

    tokens = generateTokens(u'''

        {1, 2 3 op, ∅}

    ''')
    syntaxTree = parse(tokens)

    print syntaxTree
