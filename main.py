#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser

if __name__ == '__main__':

    syntaxTree = parser.parse(parser.tokenize(u'''
        (1 2 add, (1, 2, add))
    '''))

    print(syntaxTree)

