from setacktypes import *
from vmtools     import *

def mul(stack):
    """multiply 2 numbers"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, int, float)
    assertType(rhs, int, float)
    return lhs * rhs

def div(stack):
    """divide 2 numbers"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, int, float)
    assertType(rhs, int, float)
    return lhs / rhs

def add(stack):
    """add 2 numbers"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, int, float)
    assertType(rhs, int, float)
    return lhs + rhs

def sub(stack):
    """subtract 2 numbers"""
    assertArity(stack, 2)
    rhs, lhs = stack.pop(), stack.pop()
    assertType(lhs, int, float)
    assertType(rhs, int, float)
    return lhs - rhs
