import itertools

from setacktypes import *
from vmtools     import *

def union(stack):
    """{1,2,3} and {2,3,4} is {1,2,3,4}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return Set(lhs | rhs)

def intersection(stack):
    """{1,2,3} and {2,3,4} is {2,3}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return Set(lhs & rhs)

def difference(stack):
    """{1,2,3} and {2,3,4} is {1}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return Set(lhs - rhs)

def symmetricDifference(stack):
    """{1,2,3} and {2,3,4} is {1,4}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return Set(lhs ^ rhs)

def cartesianProduct(stack):
    """{1,2} and {a,b} is {(1,a),(1,b),(2,a),(2,b)}"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return Set([t for t in itertools.product(lhs, rhs)])

def powerSet(stack):
    """{1,2} is {{},{1},{2},{1,2}}"""
    assertArity(stack, 1)
    value = stack.pop()
    assertType(value, Set)
    s = list(value)
    result = Set([Set(i) for i in itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1))])
    return result

def inSet(stack):
    """1 in {1,2} is True"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, Set)
    return lhs in rhs

def notInSet(stack):
    """0 not in {1,2} is True"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(rhs, Set)
    return lhs not in rhs

def subset(stack):
    """{1,2,3} and {1,2,3} is True"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return lhs <= rhs

def properSubset(stack):
    """{1,2,3} and {1,2,3} is False"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, Set)
    assertType(rhs, Set)
    return lhs < rhs
