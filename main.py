#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser

tokens = parser.tokenize(u'''
    {1 2, (1, 2)}
''')
syntaxTree = parser.parse(tokens)

print(syntaxTree)

