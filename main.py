#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parser import Parser

parser     = Parser('<string>')
syntaxTree = parser.parse(u'''
    {1, 2, 3} {1, 1 2 add} U
''')

print(syntaxTree)

