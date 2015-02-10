# -*- coding: utf-8 -*-

import enum
import re

class Token(enum.Enum):
    LeftBracket     = 1
    RightBracket    = 2
    Comma           = 3
    BooleanLiteral  = 4
    FloatLiteral    = 5
    IntegerLiteral  = 6
    Symbol          = 7
    EmptySet        = 8

__tokenPattern = re.compile(u'''
      (?P<LeftBracket>{)
    | (?P<RightBracket>})
    | (?P<Comma>,)
    | (?P<BooleanLiteral>True|False)
    | (?P<FloatLiteral>(-?)\d+\.\d+)
    | (?P<IntegerLiteral>(-?)\d+)
    | (?P<EmptySet>∅)
    | (?P<Symbol>[^\s]+)
''', re.VERBOSE | re.UNICODE)

def __searchDict(dict, predicate):
    return [(k, v) for k, v in dict.items() if predicate(k, v)]

def tokenize(string):
    lines = string.split('\n')
    for lineno, line in enumerate(lines, start=1):
        for match in __tokenPattern.finditer(line):
            (key, value), = __searchDict(match.groupdict(), lambda k, v: v is not None)
            yield (Token[key], value, match.start(key), match.end(key), lineno)

def parse(tokens):
    result = []
    token  = next(tokens, None)
    while token:
        type, value, start, end, lineno = token
        if type == Token.RightBracket: 
            result.append('}')
            break
        if type == Token.BooleanLiteral:
            if value == 'True':
                result.append(True)
            elif value == 'False':
                result.append(False)
        elif type == Token.Comma:
            result.append(value)
        elif type == Token.Symbol:
            result.append(value)
        elif type == Token.FloatLiteral:
            result.append(float(value))
        elif type == Token.IntegerLiteral:
            result.append(int(value))
        elif type == Token.EmptySet:
            result.append(frozenset())
        elif type == Token.LeftBracket:
            commaSeparatedTokens = parse(tokens)
            if commaSeparatedTokens == []:
                result.append(frozenset())
            else:
                stexes   = []
                currStex = []
                for t in commaSeparatedTokens:
                    if t in (',', '}'): # End of stex
                        if len(currStex) == 1:
                            stexes.append(currStex.pop())
                        elif len(currStex) > 1:
                            stexes.append(tuple(currStex))
                            currStex = []
                    else:
                        currStex.append(t)
                result.append(frozenset(stexes))
        else:
            raise Exception('Error: Unexpected token: %s' % (token,))
        token = next(tokens, None)
    return result

