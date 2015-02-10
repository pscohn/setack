# -*- coding: utf-8 -*-

import enum
import re

def __searchDict(dict, predicate):
    return [(k, v) for k, v in dict.items() if predicate(k, v)]

class TokenType(enum.Enum):
    LeftBracket     = 1
    RightBracket    = 2
    Comma           = 3
    BooleanLiteral  = 4
    FloatLiteral    = 5
    IntegerLiteral  = 6
    Symbol          = 7
    EmptySet        = 8

def tokenizeLine(line):
    pattern = re.compile(u'''
          (?P<LeftBracket>{)
        | (?P<RightBracket>})
        | (?P<Comma>,)
        | (?P<BooleanLiteral>True|False)
        | (?P<FloatLiteral>(-?)\d+\.\d+)
        | (?P<IntegerLiteral>(-?)\d+)
        | (?P<Symbol>\w+)
        | (?P<EmptySet>∅)
    ''', re.VERBOSE | re.UNICODE)
    for match in pattern.finditer(line):
        (key, value), = __searchDict(match.groupdict(), lambda k, v: v is not None)
        yield (TokenType[key], value, match.start(key), match.end(key))

def tokenize(string):
    lines = string.split('\n')
    for lineno, line in enumerate(lines):
        for token in tokenizeLine(line):
            yield token + (lineno + 1,)

def parseTokens(tokens):

    result = []
    token  = next(tokens, None)

    while token:

        type, value, start, end, lineno = token

        if type == TokenType.RightBracket: 
            result.append('}')
            break

        if type == TokenType.BooleanLiteral:
            if value == 'True':
                result.append(True)
            elif value == 'False':
                result.append(False)
        elif type == TokenType.Comma:
            result.append(value)
        elif type == TokenType.Symbol:
            result.append(value)
        elif type == TokenType.FloatLiteral:
            result.append(float(value))
        elif type == TokenType.IntegerLiteral:
            result.append(int(value))
        elif type == TokenType.EmptySet:
            result.append(frozenset())
        elif type == TokenType.LeftBracket:
            commaSeparatedTokens = parseTokens(tokens)
            if commaSeparatedTokens == []:
                result.append(frozenset())
            else:
                stexes   = []
                currStex = []
                for t in commaSeparatedTokens:
                    if t in (',', '}'):
                        if len(currStex) == 1:
                            stexes.append(currStex.pop())
                        else:
                            stexes.append(tuple(currStex))
                            currStex = []
                    else:
                        currStex.append(t)
                result.append(frozenset(stexes))
        else:
            raise Exception('Error: Unexpected token: %s' % (token,))

        token = next(tokens, None)

    return result

def parse(string):
    tokens = tokenize(string)
    return parseTokens(tokens)

