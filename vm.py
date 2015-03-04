# -*- coding: utf-8 -*-

import inspect
import parser
import types
import stdlib

from setacktypes import *
from vmtools     import *

class VM():

    def __init__(self, autocomplete=None):

        self.parser  = parser.Parser()
        self.stack   = []
        self.symbols = { 'define-symbol'        : stdlib.defineSymbol,
                         'define-proc'          : stdlib.defineProc,
                         'space'                : ' ',
                         'new-line'             : '\n',
                         'write'                : stdlib.write,
                         'print'                : stdlib.showTop, 
                         'show-stack'           : stdlib.showStack, 
                         'show-symbols'         : stdlib.showSymbols, 
                         'show-type'            : stdlib.showType,
                         'clear'                : stdlib.clear,
                         'depth'                : stdlib.depth,
                         'drop'                 : stdlib.drop,
                         'union'                : stdlib.union,
                         'intersection'         : stdlib.intersection,
                         'difference'           : stdlib.difference,
                         'symmetric-difference' : stdlib.symmetricDifference,
                         'cartesian-product'    : stdlib.cartesianProduct,
                         'power-set'            : stdlib.powerSet,
                         'in'                   : stdlib.inSet,
                         'not-in'               : stdlib.notInSet,
                         'subset'               : stdlib.subset,
                         'proper-subset'        : stdlib.properSubset,
                         'load-file'            : self.loadFile }

        self.autocomplete = autocomplete

        for k in self.symbols.keys(): self.autocomplete.add(k)

    def loadFile(self, stack, symbols):
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
        

