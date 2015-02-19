# -*- coding: utf-8 -*-

import types

def formatItem(item):
    if type(item) == frozenset:
        result = '{{{}}}'.format(', '.join([formatItem(a) for a in item]))
    else:
        result = str(item)
    return result

# Stack
# ------------------------------------------------------------------------------

def showTop(stack, _):
    if stack: print(formatItem(stack[-1]))

def showStack(stack, _):
    if stack == []:
        return
    for n, item in enumerate(reversed(stack)):
        print('{}: {}'.format(n, formatItem(item)))

def showSymbols(_, symbols):
    for symbol, value in symbols.items():
        valueType = type(value)
        if valueType == types.FunctionType:
            print('{}: {}'.format(symbol, '<function>'))
        else:
            print('{}: {}'.format(symbol, value))

def clear(stack, _):
    while stack: stack.pop()

def depth(stack, _):
    print(len(stack))

def drop(stack, _):
    if stack: stack.pop()

def assignSymbol(stack, symbols):
    symbol = stack.pop()
    value  = stack.pop()
    symbols[symbol] = value

# Set Operations
# ------------------------------------------------------------------------------

def union(stack, _):
    a = stack.pop()
    b = stack.pop()
    if type(a) != frozenset:
        raise TypeError("{} is not a set".format(formatItem(a)))
    elif type(b) != frozenset:
        raise TypeError("{} is not a set".format(formatItem(b)))
    result = a | b
    stack.append(result)
    return result

