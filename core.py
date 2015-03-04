# -*- coding: utf-8 -*-

import inspect
import itertools
import parser
import sys
import types

from setacktypes import *
from vmtools     import *

# Stack
# ------------------------------------------------------------------------------

def showTop(stack, _):
    """show top of stack"""
    if stack: print(stack[-1])

def write(stack, _):
    """write top of stack to stdout"""
    if stack: sys.stdout.write(str(stack[-1]))

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
        if valueType == types.FunctionType or inspect.ismethod(value):
            name = 'function'
            if value.__doc__: 
                name += ' : {}'.format(value.__doc__)
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
    """drop top of stack"""
    if stack: stack.pop()

def defineSymbol(stack, symbols):
    """assign value to symbol"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Symbol)
    symbols[lhs] = rhs

def defineProc(stack, symbols):
    assertArity(stack, 3)
    lazy, params, name = stack.pop(), stack.pop(), stack.pop()
    symbols[name] = Proc(name, params, lazy)

def showType(stack, _):
    assertArity(stack, 1)
    value = stack.pop()
    print(type(value))

# Set Operations
# ------------------------------------------------------------------------------

def union(stack, _):
    """{1,2,3} and {2,3,4} is {1,2,3,4}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs | rhs)
    return result

def intersection(stack, _):
    """{1,2,3} and {2,3,4} is {2,3}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs & rhs)
    return result

def difference(stack, _):
    """{1,2,3} and {2,3,4} is {1}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs - rhs)
    return result

def symmetricDifference(stack, _):
    """{1,2,3} and {2,3,4} is {1,4}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs ^ rhs)
    return result

def cartesianProduct(stack, _):
    """{1,2} and {a,b} is {(1,a),(1,b),(2,a),(2,b)}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set([t for t in itertools.product(lhs, rhs)])
    return result

def powerSet(stack, _):
    """{1,2} is {{},{1},{2},{1,2}}"""
    assertArity(stack, 1)
    value = stack.pop()
    assertType(value, parser.Set)
    s = list(value)
    result = parser.Set([parser.Set(i) for i in itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1))])
    return result

def inSet(stack, _):
    """1 in {1,2} is True"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, parser.Set)
    result = lhs in rhs
    return result

def notInSet(stack, _):
    """0 in {1,2} is True"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, parser.Set)
    result = lhs not in rhs
    return result

def subset(stack, _):
    """{1,2,3} and {1,2,3} is True"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = lhs <= rhs
    return result

def properSubset(stack, _):
    """{1,2,3} and {1,2,3} is False"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = lhs < rhs
    return result

