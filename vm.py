# -*- coding: utf-8 -*-

import core
import inspect
import parser
import types

from setacktypes import *
from vmtools     import *

class VM():

    def __init__(self):
        self.stack   = []
        self.parser  = parser.Parser()
        self.symbols = { 'run-file'             : self.runFile,
                         'help'                 : core.showSymbols,
                         'define-symbol'        : core.defineSymbol,
                         'define-proc'          : core.defineProc,
                         'write'                : core.write,
                         'print'                : core.showTop, 
                         'show-stack'           : core.showStack, 
                         'show-symbols'         : core.showSymbols, 
                         'show-type'            : core.showType,
                         'clear'                : core.clear,
                         'depth'                : core.depth,
                         'drop'                 : core.drop,
                         'union'                : core.union,
                         'intersection'         : core.intersection,
                         'difference'           : core.difference,
                         'symmetric-difference' : core.symmetricDifference,
                         'cartesian-product'    : core.cartesianProduct,
                         'power-set'            : core.powerSet,
                         'in'                   : core.inSet,
                         'not-in'               : core.notInSet,
                         'subset'               : core.subset,
                         'proper-subset'        : core.properSubset }

    def runFile(self, stack, symbols):
        """run file"""
        assertArity(stack, 1)
        lhs = stack.pop()
        assertType(lhs, str)
        lhs = lhs.replace('"', "")
        with open(lhs, 'r') as f:
            for line in f.readlines():
                self.eval(line)

    def eval(self, string):
        syntaxTree = self.parser.parse(string)
        return self.execute(syntaxTree, self.stack, self.symbols)

    def execute(self, value, stack, symbols):
        
        valueType = type(value)

        if valueType in (bool, float, int, str):
            stack.append(value)
            return value

        elif valueType == Symbol:
            if value not in symbols: 
                stack.append(value)
                return value
            else:
                symbolValue = symbols[value]
                symbolType  = type(symbolValue)

                if symbolType == Proc:
                    # Todo: This is rough!
                    proc = symbolValue
                    bindings = dict(symbols)
                    for p in proc.params:
                        bindings[p] = stack.pop()
                    localStack = []
                    r = self.execute(proc.body, localStack, bindings)
                    if r != None:
                        stack.append(r)
                    return r

                elif symbolType == types.FunctionType or inspect.ismethod(symbolValue):
                    r = symbolValue(stack, symbols)
                    if r != None: 
                        stack.append(r)
                    return r
                else:
                    stack.append(symbolValue)
                    return symbolValue

        elif valueType in (Set, tuple):
            results = []
            for v in value:
                localStack = []
                r = self.execute(v, localStack, symbols)
                if r != None: 
                    results.append(r)
            value = valueType(results)
            stack.append(value)
            return value

        elif valueType == Expr:
            if value.lazy:
                stack.append(value)
                return value
            else:
                localStack = []
                for v in value:
                    self.execute(v, localStack, symbols)
                if localStack: 
                    localStackTop = localStack.pop()
                    stack.append(localStackTop)
                    return localStackTop

        else:
            raise Exception('Unexpected value: {}'.format(value))
        

