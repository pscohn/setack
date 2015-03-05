class Proc():
    def __init__(self, name, params, body):
        self.name      = name
        self.params    = set(params)
        self.body      = body
        self.body.lazy = False
    def __repr__(self):
        return 'Proc(name={}, params={}, body={})'.format(self.name, self.params, self.body)

class Expr(): 
    def __init__(self, seq, lazy=False):
        self.lazy  = lazy
        self.terms = tuple(seq)
    def __iter__(self):
        for item in self.terms:
            yield item
    def __repr__(self):
        if self.lazy:
            return 'Thunk({})'.format(', '.join(map(str, self.terms)))
        else:
            return 'Expr({})'.format(', '.join(map(str, self.terms)))

class Set(frozenset):
    def __repr__(self):
        return '{{{}}}'.format(', '.join(map(str, self)))

class Symbol(str):
    def __init__(self, value):
        self = value
    def __repr__(self):
        return 'Symbol({})'.format(self)

