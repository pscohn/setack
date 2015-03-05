# -*- coding: utf-8 -*-

import inspect
import libset
import parser
import types

from setacktypes import *
from vmtools     import *

class VM():

    def __init__(self):
        self.parser  = parser.Parser()
        self.stack   = []
        self.symbols = { 'run-file'             : self.runFile,
                         'define-symbol'        : self.defineSymbol,
                         'define-proc'          : self.defineProc,
                         'print'                : self.showTop, 
                         'help'                 : self.showHelp,
                         'show-stack'           : self.showStack, 
                         'show-symbols'         : self.showSymbols, 
                         'union'                : libset.union,
                         'intersection'         : libset.intersection,
                         'difference'           : libset.difference,
                         'symmetric-difference' : libset.symmetricDifference,
                         'cartesian-product'    : libset.cartesianProduct,
                         'power-set'            : libset.powerSet,
                         'in'                   : libset.inSet,
                         'not-in'               : libset.notInSet,
                         'subset'               : libset.subset,
                         'proper-subset'        : libset.properSubset }
        self.builtins = set()
        for k, v in self.symbols.items():
            self.builtins.add(k)

    def showTop(self, stack):
        """show top of stack"""
        if stack: print(stack[-1])

    def showStack(self, stack):
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

    def showSymbols(self, stack):
        """show user defined symbols""" 
        ss = {k:v for k,v in self.symbols.items() if k not in self.builtins}
        if ss:
            print(self.formatSymbols(ss))

    def showHelp(self, stack):
        """show built-in functions and symbols"""
        ss = {k:v for k,v in self.symbols.items() if k in self.builtins}
        print(self.formatSymbols(ss))

    def formatSymbols(self, symbols):
        result = ''
        items = symbols.items()
        s, _  = max(items, key=lambda a: len(a[0]))
        width = len(s)
        for symbol, value in sorted(items):
            valueType = type(value)
            if valueType == types.FunctionType or inspect.ismethod(value):
                name = 'function'
                if value.__doc__: 
                    name += ' : {}'.format(value.__doc__)
                result += '  {0:<{2}} : {1}\n'.format(symbol, name, width)
            else:
                result += '  {0:<{2}} : {1}\n'.format(symbol, value, width)
        return result

    def defineSymbol(self, stack):
        """X 1 define-symbol"""
        assertArity(stack, 2)
        rhs, lhs = stack.pop(), stack.pop()
        assertType(lhs, parser.Symbol)
        self.symbols[lhs] = rhs

    def defineProc(self, stack):
        """define procedure"""
        assertArity(stack, 3)
        lazy, params, name = stack.pop(), stack.pop(), stack.pop()
        self.symbols[name] = Proc(name, params, lazy)

    def runFile(self, stack):
        """\"file/path.setack\" run-file"""
        assertArity(stack, 1)
        lhs = stack.pop()
        assertType(lhs, str)
        lhs = lhs.replace('"', "")
        with open(lhs, 'r') as f:
            for line in f.readlines():
                self.eval(line)

    def eval(self, string):
        syntaxTree = self.parser.parse(string)
        result = self.execute(syntaxTree, self.stack, self.symbols)
        self.stack.append(result)
        return result

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
                    r = symbolValue(stack)
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
        

