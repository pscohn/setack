# -*- coding: utf-8 -*-

import collections
import enum
import re

from setacktypes import *

class TokenType(enum.Enum):
    End             = 0
    NewLine         = 1
    LeftBrace       = 2
    RightBrace      = 3
    LeftBracket     = 4
    RightBracket    = 5
    LeftParen       = 6
    RightParen      = 7
    Comma           = 8
    BooleanLiteral  = 9
    FloatLiteral    = 10
    IntegerLiteral  = 11
    StringLiteral   = 12
    Symbol          = 13

Token = collections.namedtuple(
    'Token', ['type', 'value', 'start', 'end', 'lineno', 'line'])

class Parser():

    tokenPattern = re.compile(u'''
          (?P<End>\Z)
        | (?P<LeftBrace>\[)
        | (?P<RightBrace>\])
        | (?P<LeftBracket>{)
        | (?P<RightBracket>})
        | (?P<LeftParen>\()
        | (?P<RightParen>\))
        | (?P<Comma>,)
        | (?P<BooleanLiteral>True|False)
        | (?P<FloatLiteral>(-?)\d+\.\d+)
        | (?P<IntegerLiteral>(-?)\d+)
        | (?P<StringLiteral>"[^"]*")
        | (?P<Symbol>[\w\-\*\/\+%]+)
    ''', re.VERBOSE | re.UNICODE)

    def __init__(self, source=None):
        self.stack  = []
        self.source = source

    def tokenize(self, string):
        result = []
        lines  = string.split('\n')
        for lineno, line in enumerate(lines, start=1):
            for m in self.tokenPattern.finditer(line):
                items         = m.groupdict().items()
                (key, value), = [(k, v) for k, v in items if v is not None]
                token         = Token(TokenType[key], 
                                      value, 
                                      m.start(key), 
                                      m.end(key), 
                                      lineno, 
                                      line)
                result.append(token)
        return result

    def parse(self, string):
        self.stack = []
        return self.__parse(self.tokenize(string))

    def __parse(self, tokens):

        result = []
        curr   = []

        while len(tokens):

            token = tokens.pop(0)

            e = SyntaxError('Unexpected {}'.format(token.type))
            e.filename = self.source
            e.lineno   = token.lineno
            e.offset   = token.start
            e.text     = token.line

            if token.type == TokenType.BooleanLiteral:
                if token.value == 'True':
                    curr.append(True)
                elif token.value == 'False': 
                    curr.append(False)
            elif token.type == TokenType.FloatLiteral:
                curr.append(float(token.value))
            elif token.type == TokenType.IntegerLiteral:
                curr.append(int(token.value))
            elif token.type == TokenType.StringLiteral:
                curr.append(token.value)
            elif token.type == TokenType.Symbol:
                curr.append(Symbol(token.value))
            elif token.type == TokenType.LeftBrace:
                self.stack.append(token)
                e = self.__parse(tokens)
                curr.append(Expr(e.terms, lazy=True))
            elif token.type == TokenType.LeftBracket:
                self.stack.append(token)
                curr.append(Set(self.__parse(tokens)))
            elif token.type == TokenType.LeftParen:
                self.stack.append(token)
                curr.append(tuple(self.__parse(tokens)))
            elif token.type in (TokenType.Comma, 
                                TokenType.RightBrace,
                                TokenType.RightBracket,
                                TokenType.RightParen,
                                TokenType.End):

                if token.type == TokenType.Comma and len(self.stack) == 0:
                    raise e # Top-level comma

                if len(curr) == 1:
                    result.append(curr.pop())
                elif len(curr) > 1:
                    result.append(Expr(curr))
                    curr = []

                if token.type == TokenType.End and len(self.stack):
                    raise e # { or (

                if token.type == TokenType.RightBrace:
                    if len(self.stack) == 0:
                        raise e # ()}
                    else:
                        t = self.stack.pop()
                        if t.type == TokenType.LeftBrace:
                            break
                        else:
                            raise e # ( }

                if token.type == TokenType.RightBracket:
                    if len(self.stack) == 0:
                        raise e # ()}
                    else:
                        t = self.stack.pop()
                        if t.type == TokenType.LeftBracket:
                            break
                        else:
                            raise e # ( }

                if token.type == TokenType.RightParen:
                    if len(self.stack) == 0:
                        raise e # {})
                    else:
                        t = self.stack.pop()
                        if t.type == TokenType.LeftParen:
                            break
                        else:
                            raise e # { )
            else:
                raise e

        return Expr(result)
