class Proc():
    def __init__(self, name, params, body):
        self.name      = name
        self.params    = set(params)
        self.body      = body
        self.body.lazy = False
    def __repr__(self):
        return 'Proc(name={}, params={}, body={})'.format(self.name, self.params, self.body)

