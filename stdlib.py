# -*- coding: utf-8 -*-

import itertools
import parser
import types

from colorprint import *

# Stack
# ------------------------------------------------------------------------------

def showTop(stack, _):
    """show top of stack"""
    if stack: 
        print(stack[-1])

def showStack(stack, _):
    """show stack"""

    if stack == []: return

    s       = str(max(stack, key=lambda a: len(str(a))))
    width   = len(s)
    divider = '  ' + ('-' * (width + 4))
    side    = '|'

    print(divider)
    for item in reversed(stack):
        print('  {2} {0:^{1}} {2}'.format(str(item), width, side))
        print(divider)

def showSymbols(_, symbols):
    """show symbols""" 
    items = symbols.items()
    s, _  = max(items, key=lambda a: len(a[0]))
    width = len(s)
    for symbol, value in symbols.items():
        valueType = type(value)
        if valueType == types.FunctionType:
            name = 'function'
            doc  = value.__doc__
            if doc: name += ' ({})'.format(value.__doc__)

            print('  {0:<{2}} : {1}'.format(symbol, name, width))
        else:
            print('  {0:<{2}} : {1}'.format(symbol, value, width))

def clear(stack, _):
    """clear stack"""
    while stack: stack.pop()

def depth(stack, _):
    """show depth of stack"""
    print(len(stack))

def drop(stack, _):
    """remove top of stack"""
    if stack: stack.pop()

def assignSymbol(stack, symbols):
    """assign value to symbol"""
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Symbol:
        raise TypeError("{} is not a symbol".format(a))
    symbols[a] = b

# Set Operations
# ------------------------------------------------------------------------------

def union(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    elif type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = parser.Set(a | b)
    stack.append(result)
    return result

def intersection(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    elif type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = parser.Set(a & b)
    stack.append(result)
    return result

def difference(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    elif type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = parser.Set(a - b)
    stack.append(result)
    return result

def symmetricDifference(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    elif type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = parser.Set(a ^ b)
    stack.append(result)
    return result

def cartesianProduct(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    elif type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = parser.Set([i for i in itertools.product(a, b)])
    stack.append(result)
    return result

def powerSet(stack, _):
    a = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    s = list(a)
    result = parser.Set([i for i in itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1))])
    stack.append(result)
    return result

def inSet(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = a in b
    stack.append(result)
    return result

def notInSet(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = a not in b
    stack.append(result)
    return result

def subset(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != parser.Set:
        raise TypeError("{} is not a set".format(a))
    if type(b) != parser.Set:
        raise TypeError("{} is not a set".format(b))
    result = a <= b
    stack.append(result)
    return result

