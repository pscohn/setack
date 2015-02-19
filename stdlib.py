# -*- coding: utf-8 -*-

def formatItem(item):
    if type(item) == frozenset:
        result = '{{{}}}'.format(', '.join([formatItem(a) for a in item]))
    else:
        result = str(item)
    return result

# Stack
# ------------------------------------------------------------------------------

def showTop(stack):
    if stack: print(formatItem(stack[-1]))

def showStack(stack):
    if stack == []:
        return
    for n, item in enumerate(reversed(stack)):
        print('{}: {}'.format(n, formatItem(item)))

def clear(stack):
    while stack: stack.pop()

def depth(stack):
    print(len(stack))

def drop(stack):
    if stack: stack.pop()

# Set Operations
# ------------------------------------------------------------------------------

def union(stack):
    a = stack.pop()
    b = stack.pop()
    if type(a) != frozenset:
        raise TypeError("{} is not a set".format(formatItem(a)))
    elif type(b) != frozenset:
        raise TypeError("{} is not a set".format(formatItem(b)))
    result = a | b
    stack.append(result)
    return result

# Arithmetic Operations
# ------------------------------------------------------------------------------

def add(stack):
    a = stack.pop()
    b = stack.pop()
    if type(a) not in (float, int):
        raise TypeError("{} is not a number".format(formatItem(a)))
    elif type(b) not in (float, int):
        raise TypeError("{} is not a number".format(formatItem(b)))
    result = a + b
    stack.append(result)
    return result

