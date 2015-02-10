# -*- coding: utf-8 -*-

import enum
import re

class Token(enum.Enum):
    LeftBracket     = 1
    RightBracket    = 2
    LeftParen       = 3
    RightParen      = 4
    Comma           = 5
    BooleanLiteral  = 6
    FloatLiteral    = 7
    IntegerLiteral  = 8
    EmptySet        = 9
    Symbol          = 10

__tokenPattern = re.compile(u'''
      (?P<LeftBracket>{)
    | (?P<RightBracket>})
    | (?P<LeftParen>\()
    | (?P<RightParen>\))
    | (?P<Comma>,)
    | (?P<BooleanLiteral>True|False)
    | (?P<FloatLiteral>(-?)\d+\.\d+)
    | (?P<IntegerLiteral>(-?)\d+)
    | (?P<EmptySet>∅)
    | (?P<Symbol>[^\s{}(),]+)
''', re.VERBOSE | re.UNICODE)

def __searchDict(dict, predicate):
    return [(k, v) for k, v in dict.items() if predicate(k, v)]

def tokenize(string):
    lines = string.split('\n')
    for lineno, line in enumerate(lines, start=1):
        for match in __tokenPattern.finditer(line):
            (key, value), = __searchDict(match.groupdict(), lambda k, v: v is not None)
            yield (Token[key], value, match.start(key), match.end(key), lineno)

class Stex(tuple): 
    def __repr__(self):
        return 'Stex(' + ' '.join(map(str, self)) + ')'

def parseCommaSepSeq(tokens, typeConstructor, delimiter):
    result = None
    commaSepTokens = parse(tokens)
    if commaSepTokens == []:
        result = typeConstructor()
    else:
        args = []
        curr = []
        for token in commaSepTokens:
            if token in (',', delimiter):
                if len(curr) == 1:
                    args.append(curr.pop())
                elif len(curr) > 1:
                    args.append(Stex(curr))
                    curr = []
            else:
                curr.append(token)
        result = typeConstructor(args)
    return result

def parse(tokens):
    result = []
    token  = next(tokens, None)
    while token:
        type, value, start, end, lineno = token
        if type == Token.RightBracket: 
            #todo if I had peek I wouldn't have to do this
            result.append('}')
            break
        if type == Token.RightParen:
            result.append(')')
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
            result.append(parseCommaSepSeq(tokens, frozenset, '}'))
        elif type == Token.LeftParen:
            result.append(parseCommaSepSeq(tokens, tuple, ')'))
        else:
            raise Exception('Error: Unexpected token: %s' % (token,))
        token = next(tokens, None)
    return result

