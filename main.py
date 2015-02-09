# -*- coding: utf-8 -*-

import tokenize
from   token    import tok_name as tokenName
from   StringIO import StringIO

def generateTokens(input):
    return tokenize.generate_tokens(StringIO(input).readline)

def parse(tokens):
    result = []
    token = next(tokens, None)
    while token:
        number, value, start, end, line = token
        if value is '}':
            break
        elif value in (',', '', '\n') or number is 5: # 5: indent
            token = next(tokens, None)
            continue
        elif number is 1:
            result.append(value)
        elif number is 2:
            try:
                n = int(value)
            except ValueError:
                n = float(value)
            result.append(n)
        elif value is '{':
            s = set(parse(tokens))
            result.append(s)
        else:
            raise Exception('Error: Unexpected token: %s' % (token,))
        token = next(tokens, None)
    return result

if __name__ == '__main__':

    result = parse(generateTokens('''

        {1, 2} {3, 4} union

    '''))

    print result

