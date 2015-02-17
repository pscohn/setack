#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser

def evalSyntaxTree(syntaxTree):
    print(syntaxTree)

syntaxTree = parser.Parser('<string>').parse(u'''
    {1, 2} {1 2 +} union
''')

evalSyntaxTree(syntaxTree)

