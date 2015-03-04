class ArityError(Exception): 

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return 'Expecting {} argument{} on the stack'.format(
            self.n, '' if self.n == 1 else 's')

def assertType(obj, targetType):
    if type(obj) != targetType:
        raise TypeError('{} is not a {}'.format(obj, targetType.__name__))

def assertArity(stack, n):
    if len(stack) < n:
        raise ArityError(n)
