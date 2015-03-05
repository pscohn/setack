class ArityError(Exception): 
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return 'Expecting {} argument{} on the stack'.format(
            self.n, '' if self.n == 1 else 's')

def assertType(obj, *types):
    if type(obj) not in types:
        if len(types) == 1:
            raise TypeError('{} is not a {}'.format(obj, types[0].__name__))
        else:
            typeNames = [t.__name__ for t in types]
            raise TypeError('{} is not a {}'.format(obj, ' or '.join(typeNames)))

def assertArity(stack, n):
    if len(stack) < n:
        raise ArityError(n)
