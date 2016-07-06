
class FapClosure:
    def __init__(self, func, name=None, local=None):
        self.func = func
        self.name = name
        self.local = local

    def apply(self, local, arg):
        # local.update(self.local)
        # TODO resolve variables
        return self.func(arg)


DEFAULT_LOCAL = {
    'print': FapClosure(lambda x: print(x)),
    '+': FapClosure(lambda x: FapClosure(lambda y: x + y)),
    '-': FapClosure(lambda x: FapClosure(lambda y: x - y)),
    '*': FapClosure(lambda x: FapClosure(lambda y: x * y)),
    '/': FapClosure(lambda x: FapClosure(lambda y: x / y)),
    '&&': FapClosure(lambda x: FapClosure(lambda y: x and y)),
    '||': FapClosure(lambda x: FapClosure(lambda y: x or y)),
    '|': FapClosure(lambda x: FapClosure(lambda y: x | y)),
    '&': FapClosure(lambda x: FapClosure(lambda y: x | y)),
    '==': FapClosure(lambda x: FapClosure(lambda y: x == y)),
    '%': FapClosure(lambda x: FapClosure(lambda y: x % y)),
}
