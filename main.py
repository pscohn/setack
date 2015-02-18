#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser
import sys
import types

trace = []

def eval(value, stack, symbols):
    
    valueType = type(value)

    if valueType in (bool, float, int):
        stack.append(value)
        return value

    elif valueType in (frozenset, tuple):
        tempStack = []
        for v in value:
            eval(v, tempStack, symbols)
        value = valueType(tempStack)
        stack.append(value)
        return value

    elif valueType == str:
        if value not in symbols: 
            raise Exception('Undefined symbol: ' + value)
        symbolValue = symbols[value]
        symbolType  = type(symbolValue)
        if symbolType is types.FunctionType:
            return symbolValue(stack)
        else:
            stack.append(symbolValue)
            return symbolValue

    elif valueType == parser.SetExp:
        returnValues = []
        for v in value:
            r = eval(v, stack, symbols)
            if r != None: 
                returnValues.append(r)
            trace.append('{} => {}'.format(v, r))
        if len(returnValues):
            return returnValues.pop()
        else:
            return None
    else:
        raise Exception('Unexpected value: ' + value)
    
# Built-ins
# ------------------------------------------------------------------------------

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

def add(stack):
    a = stack.pop()
    b = stack.pop()
    r = a + b
    stack.append(r)
    return r

if __name__ == '__main__':

    input = u'''
        {x 2 +} {4} union println
    '''
    syntaxTree = parser.Parser().parse(input)

    stack   = []
    symbols = {'union'  : union, 
               'println': println, 
               'dump'   : dump, 
               '+'      : add, 
               'x'      : 1}

    eval(syntaxTree, stack, symbols)

    print()
    for step, inst in enumerate(trace, start=1):
        print('{}: {}'.format(step, inst))
