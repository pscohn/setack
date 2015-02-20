# -*- coding: utf-8 -*-

import itertools
import parser
import types

# Tools
# ------------------------------------------------------------------------------

def assertType(obj, targetType):
    objType = type(obj)
    if objType != targetType:
        msg = '{} is not a {}'.format(obj, targetType.__name__)
        raise TypeError(msg)

# Stack
# ------------------------------------------------------------------------------

def showTop(stack, _):
    """show top of stack"""
    if stack: print(stack[-1])

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

def assignSymbol(stack, symbols):
    """assign value to symbol"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, parser.Symbol)
    symbols[rhs] = lhs

# Set Operations
# ------------------------------------------------------------------------------

def union(stack, _):
    """{1,2,3} and {2,3,4} is {1,2,3,4}"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs | rhs)
    stack.append(result)
    return result

def intersection(stack, _):
    """{1,2,3} and {2,3,4} is {2,3}"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs & rhs)
    stack.append(result)
    return result

def difference(stack, _):
    """{1,2,3} and {2,3,4} is {1}"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs - rhs)
    stack.append(result)
    return result

def symmetricDifference(stack, _):
    """{1,2,3} and {2,3,4} is {1,4}"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set(lhs ^ rhs)
    stack.append(result)
    return result

def cartesianProduct(stack, _):
    """{1,2} and {a,b} is {(1,a),(1,b),(2,a),(2,b)}"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = parser.Set([t for t in itertools.product(lhs, rhs)])
    stack.append(result)
    return result

def powerSet(stack, _):
    """{1,2} is {{},{1},{2},{1,2}}"""
    value = stack.pop()
    assertType(value, parser.Set)
    s = list(value)
    result = parser.Set([parser.Set(i) for i in itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1))])
    stack.append(result)
    return result

def inSet(stack, _):
    """1 in {1,2} is True"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, parser.Set)
    result = lhs in rhs
    stack.append(result)
    return result

def notInSet(stack, _):
    """0 in {1,2} is True"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, parser.Set)
    result = lhs not in rhs
    stack.append(result)
    return result

def subset(stack, _):
    """{1,2,3} and {1,2,3} is True"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = lhs <= rhs
    stack.append(result)
    return result

def properSubset(stack, _):
    """{1,2,3} and {1,2,3} is False"""
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, parser.Set)
    assertType(rhs, parser.Set)
    result = lhs < rhs
    stack.append(result)
    return result

