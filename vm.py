# -*- coding: utf-8 -*-

import parser
import types
import stdlib

class VM():
    def __init__(self):
        self.stack   = []
        self.trace   = []
        self.parser  = parser.Parser()
        self.symbols = { '.'        : stdlib.showTop, 
                         '!'        : stdlib.assignSymbol,
                         'showstack': stdlib.showStack, 
                         'showsymbols': stdlib.showSymbols, 
                         'clear'    : stdlib.clear,
                         'depth'    : stdlib.depth,
                         'drop'     : stdlib.drop,
                         'union'    : stdlib.union }

    def printTrace(self):
        for step, inst in enumerate(self.trace, start=1):
            print('{}: {}'.format(step, inst))

    def eval(self, string):
        self.execute(self.parser.parse(string), self.stack, self.symbols)

    def execute(self, value, stack, symbols):
        
        valueType = type(value)

        if valueType in (bool, float, int):
            stack.append(value)
            return value

        elif valueType in (parser.Set, tuple):
            tempStack = []
            for v in value:
                self.execute(v, tempStack, symbols)
            value = valueType(tempStack)
            stack.append(value)
            return value

        elif valueType == parser.Symbol:

            if value not in symbols: 
                stack.append(value)
                return value
            else:
                symbolValue = symbols[value]
                symbolType  = type(symbolValue)

                if symbolType is types.FunctionType:
                    return symbolValue(stack, symbols)
                else:
                    stack.append(symbolValue)
                    return symbolValue

        elif valueType == parser.SetExp:
            returnValues = []
            for v in value:
                r = self.execute(v, stack, symbols)
                if r != None: 
                    returnValues.append(r)
                self.trace.append('{} => {}'.format(v, r))
            if len(returnValues):
                return returnValues.pop()
            else:
                return None
        else:
            raise Exception('Unexpected value: {}'.format(value))
        
