
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
    'add': FapClosure(lambda x: FapClosure(lambda y: x + y)),
    'sub': FapClosure(lambda x: FapClosure(lambda y: x - y)),
    'mul': FapClosure(lambda x: FapClosure(lambda y: x * y)),
    'div': FapClosure(lambda x: FapClosure(lambda y: x / y)),
    'and': FapClosure(lambda x: FapClosure(lambda y: x and y)),
    'or': FapClosure(lambda x: FapClosure(lambda y: x or y)),
    'bor': FapClosure(lambda x: FapClosure(lambda y: x | y)),
    'band': FapClosure(lambda x: FapClosure(lambda y: x | y)),
    'equal': FapClosure(lambda x: FapClosure(lambda y: x == y)),
    'mod': FapClosure(lambda x: FapClosure(lambda y: x % y)),
}
