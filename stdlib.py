# -*- coding: utf-8 -*-

# IO
# ------------------------------------------------------------------------------
def println(stack):
    if stack: print(stack[-1])

# Debug
# ------------------------------------------------------------------------------
def dump(stack):
    print(stack)

# Set Operations
# ------------------------------------------------------------------------------
def union(stack):
    result = stack.pop() | stack.pop()
    stack.append(result)
    return result

# Arithmetic Operations
# ------------------------------------------------------------------------------
def add(stack):
    result = stack.pop() + stack.pop()
    stack.append(result)
    return result

