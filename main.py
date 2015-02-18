#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser
import sys
import types

def eval(value, stack, symbols):
    
    valueType = type(value)

    if valueType in (bool, float, int):
        stack.append(value)
        return value

    elif valueType in (frozenset, tuple):
        '''
        rs = []
        for v in value:
            r = eval(v, stack, symbols)
            if r != None: 
                rs.append(r)
        rs = valueType(rs)
        #stack.append(rs)
        return rs
        '''
        stack.append(value)
        return value

    elif valueType == str:
        #if value not in symbols: 
        #    raise Exception('Undefined symbol: ' + value)
        symbolValue = symbols[value]
        symbolType  = type(symbolValue)
        if symbolType is types.FunctionType:
            return symbolValue(stack)
        else:
            return symbolValue

    elif valueType == parser.SetExp:
        rs = []
        for v in value:
            r = eval(v, stack, symbols)
            #print(v, '=>', r)
            if r != None: 
                rs.append(r)
        if len(rs):
            return rs.pop()
    else:
        raise Exception('Unexpected value: ' + value)
    
def println(stack):
    if stack: print(stack[-1])

def dump(stack):
    print(stack)

def union(stack):
    a = stack.pop()
    b = stack.pop()
    r = a | b
    stack.append(r)
    return r

if __name__ == '__main__':

    input = u'''{1, 2} {3, 4} union print dump'''

    syntaxTree = parser.Parser().parse(input)

    stack   = []
    symbols = {'union': union, 'print': println, 'dump': dump}

    print('input: "{}"'.format(input))
    eval(syntaxTree, stack, symbols)

