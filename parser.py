# -*- coding: utf-8 -*-

import collections
import enum
import re
import queue

class TokenType(enum.Enum):
    End             = 0
    NewLine         = 1
    LeftBracket     = 2
    RightBracket    = 3
    LeftParen       = 4
    RightParen      = 5
    Comma           = 6
    BooleanLiteral  = 7
    FloatLiteral    = 8
    IntegerLiteral  = 9
    EmptySet        = 10
    Symbol          = 11

TokenPattern = re.compile(u'''
      (?P<End>\Z)
    | (?P<NewLine>\\n)
    | (?P<LeftBracket>{)
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

Token = collections.namedtuple('Token', 'type value start end lineno')

def tokenize(string):
    result = []
    lineno = 1
    for m in TokenPattern.finditer(string):
        items   = m.groupdict().items()
        (k, v), = [(k, v) for k, v in items if v is not None]
        token   = Token(TokenType[k], v, m.start(k), m.end(k), lineno)
        if token.type == TokenType.NewLine:
            lineno += 1
        else:
            result.append(token)
    return result

class SetExp(): 
    def __init__(self, seq):
        self.__terms = tuple(seq)
    def __repr__(self):
        return 'SetExp({})'.format(' '.join(map(str, self.__terms)))

s = [] # Todo: Remove from global scope...hacky!

def parse(tokens):
    result = []
    curr   = []
    while len(tokens):
        token = tokens.pop(0)
        if token.type == TokenType.BooleanLiteral:
            if token.value == 'True':
                curr.append(True)
            elif token.value == 'False': 
                curr.append(False)
        elif token.type == TokenType.Symbol:
            curr.append(token.value)
        elif token.type == TokenType.FloatLiteral:
            curr.append(float(token.value))
        elif token.type == TokenType.IntegerLiteral:
            curr.append(int(token.value))
        elif token.type == TokenType.EmptySet:
            curr.append(frozenset())
        elif token.type == TokenType.LeftBracket:
            s.append(token)
            curr.append(frozenset(parse(tokens)))
        elif token.type == TokenType.LeftParen:
            s.append(token)
            curr.append(tuple(parse(tokens)))
        elif token.type in (TokenType.Comma, 
                            TokenType.RightBracket,
                            TokenType.RightParen,
                            TokenType.End):

            if len(curr) == 1:
                result.append(curr[0])
            elif len(curr) > 1:
                result.append(SetExp(curr))
            curr = []

            if token.type == TokenType.End:
                if len(s):
                    t = s.pop()
                    if t.type == TokenType.LeftBracket:
                        raise SyntaxError('Closing bracket missing')
                    else:
                        raise SyntaxError('Closing paren missing')

            if token.type == TokenType.RightBracket:
                if len(s) == 0:
                    raise SyntaxError('Unexpected closing bracket')
                else:
                    t = s.pop()
                    if t.type == TokenType.LeftBracket:
                        break
                    else:
                        raise SyntaxError('Unbalanced parens')

            if token.type == TokenType.RightParen:
                if len(s) == 0:
                    raise SyntaxError('Unexpected closing paren')
                else:
                    t = s.pop()
                    if t.type == TokenType.LeftParen:
                        break
                    else:
                        raise SyntaxError('Unbalanced brackets')
        else:
            raise SyntaxError('Unexpected token: %s' % (token,))
    return result

