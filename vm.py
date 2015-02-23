# -*- coding: utf-8 -*-

import parser
import setacktypes
import types
import stdlib

class VM():
    def __init__(self):
        self.parser  = parser.Parser()
        self.stack   = []
        self.symbols = { 'define-symbol'        : stdlib.defineSymbol,
                         'define-proc'          : stdlib.defineProc,
                         'show-top'             : stdlib.showTop, 
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
                         'proper-subset'        : stdlib.properSubset }

    def eval(self, string):
        syntaxTree = self.parser.parse(string)
        self.execute(syntaxTree, self.stack, self.symbols)

    def execute(self, value, stack, symbols):
        
        valueType = type(value)

        if valueType in (bool, float, int):
            stack.append(value)
            return value

        elif valueType == parser.Symbol:
            if value not in symbols: 
                stack.append(value)
                return value
            else:
                symbolValue = symbols[value]
                symbolType  = type(symbolValue)

                if symbolType == setacktypes.Proc:
                    
                    proc = symbolValue
                    bindings = dict(symbols)
                    # Need to raise if not enough arguments
                    for p in proc.params:
                        bindings[p] = stack.pop()
                    localStack = []
                    r = self.execute(proc.body, localStack, bindings)
                    if r != None:
                        stack.append(r)
                    return r

                elif symbolType == types.FunctionType:
                    r = symbolValue(stack, symbols)
                    if r != None: 
                        stack.append(r)
                    return r
                else:
                    stack.append(symbolValue)
                    return symbolValue

        elif valueType in (parser.Set, tuple):
            results = []
            for v in value:
                localStack = []
                r = self.execute(v, localStack, symbols)
                if r != None: 
                    results.append(r)
            value = valueType(results)
            stack.append(value)
            return value

        elif valueType == parser.Expr:
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
        

