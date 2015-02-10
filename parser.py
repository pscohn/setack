# -*- coding: utf-8 -*-

import collections
import enum
import re

class TokenType(enum.Enum):
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

Token = collections.namedtuple('Token', ['type', 'value', 'start', 'end', 'lineno'])

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
            yield Token(TokenType[key], value, match.start(key), match.end(key), lineno)

class stex(tuple): 
    def __repr__(self):
        return 'stex({})'.format(' '.join(map(str, self)))

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
                    args.append(stex(curr))
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
        if token.type == TokenType.RightBracket: 
            result.append('}')
            break
        if token.type == TokenType.RightParen:
            result.append(')')
            break
        if token.type == TokenType.BooleanLiteral:
            if token.value == 'True':
                result.append(True)
            elif token.value == 'False':
                result.append(False)
        elif token.type == TokenType.Comma:
            result.append(token.value)
        elif token.type == TokenType.Symbol:
            result.append(token.value)
        elif token.type == TokenType.FloatLiteral:
            result.append(float(token.value))
        elif token.type == TokenType.IntegerLiteral:
            result.append(int(token.value))
        elif token.type == TokenType.EmptySet:
            result.append(frozenset())
        elif token.type == TokenType.LeftBracket:
            result.append(parseCommaSepSeq(tokens, frozenset, '}'))
        elif token.type == TokenType.LeftParen:
            result.append(parseCommaSepSeq(tokens, tuple, ')'))
        else:
            raise Exception('Error: Unexpected token: %s' % (token,))
        token = next(tokens, None)
    return result

