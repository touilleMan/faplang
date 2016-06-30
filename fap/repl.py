from parsimonious.nodes import NodeVisitor

from .grammar import GRAMMAR


class ReplVMError(Exception):
    pass


class FapTypeError(ReplVMError):
    pass


class FapFunction:
    def __init__(self, name, num_params: int):
        self.name = name
        self.num_params = num_params
        self.rules = []

    def append_rule(self, params, body):
        if len(params) != self.num_params:
            raise ReplVMError('Function %s must have %s params' % (self.name, self.num_params))
        self.rules.append((params, body))

    def apply(self, local, args):
        if len(args) != self.num_params:
            raise ReplVMError('Function %s must have %s params' % (self.name, self.num_params))
        return

class PrintFapFunction(FapFunction):
    def __init__(self):
        pass

    def apply(self, local, arg):
        print(arg)
        return self


class FapClosure(FapFunction):
    def __init__(self, func):
        self.func = func

    def apply(self, local, arg):
        return self.func(arg)


class Opfunction(FapFunction):
    def __init__(self, op_func):
        self.op_func = op_func

    def apply(self, local, arg):
        Opf
        return self.op_func(arg)


class ReplVM:
    def __init__(self):
        self.local = {
            'print': PrintFapFunction(),
            '+': FapClosure(lambda x: FapClosure(lambda y: x + y)),
            '*': FapClosure(lambda x: FapClosure(lambda y: x * y))
        }
        self._visitor = ReplVisitor(self)

    def parse(self, code):
        return GRAMMAR.parseString(code)

    def exec(self, ast):
        return self._visitor.visit(ast)

    def parse_and_exec(self, code):
        return self.exec(self.parse(code))


class ReplVisitor(NodeVisitor):

    def __init__(self, vm):
        self.vm = vm
        super().__init__()

    def visit(self, ast):
        ret = None
        for node in ast:
            ret = self.visit_Expr(node)
        return ret

    def visit_Expr(self, expr):
        method = getattr(self, 'visit_' + type(expr).__name__, self.generic_visit)
        return method(expr)


    def visit_Number(self, n):
        return n.value

    def visit_Booleam(self, n):
        return n.value

    def visit_Variable(self, n):
        value = self.vm.local.get(n.name)
        if not value:
            raise ReplVMError('%s is not defined' % n)
        return value

    def visit_Application(self, n):
        value = self.visit_Expr(n.name)
        param = self.visit_Expr(n.param)
        if isinstance(value, FapFunction):
            return value.apply(self.vm.local, param)
        else:
            raise ReplVMError('%s cannot be apply to %s' % (n.name, n.param))

    def visit_FuncDef(self, n):
        elem = self.vm.local.get(n.name)
        if elem:
            if isinstance(elem, FapFunction):
                elem.append_rule(n.params, n.body)
            else:
                raise ReplVMError('%s already exist but is not a function' % n.name)
        else:
            elem = FapFunction(n.name, len(n.params))
            elem.append_rule(n.params, n.body)
            self.vm.local[n.name] = elem

    def visit_Op(self, n):
        op_map = {
            '+': (lambda a, b: a + b),
            '-': (lambda a, b: a - b),
            '*': (lambda a, b: a * b),
            '/': (lambda a, b: a / b),
            '&': (lambda a, b: a & b),
            '|': (lambda a, b: a | b),
            '&&': (lambda a, b: a and b),
            '||': (lambda a, b: a or b),
            '==': (lambda a, b: a == b)
        }
        a = self.visit_Expr(n.a)
        b = self.visit_Expr(n.b)
        return op_map[n.type](a, b)

    def generic_visit(self, n):
        print('!!! Unknown %s' % n)
        return n


def fap_repl(verbose=False):
    quit = False
    vm = ReplVM()
    verbose = verbose
    prompt_continue = False
    while not quit:
        if not prompt_continue:
            line = input('>>> ')
        else:
            line = input('... ')
        if line and line[-1] == '\\':
            prompt_continue = True
            continue
        elif line == ':verbose':
            verbose = ~verbose
            print('Verbose is %s' % ('on' if verbose else 'off'))
            continue
        elif line == ':quit':
            return
        prompt_continue = False
        try:
            ast = vm.parse(line)
            if verbose:
                print(ast)
            ret = vm.exec(ast)
            if ret is not None:
                print(ret)
        except ReplVMError as exc:
            print(exc)


def fap_eval(code, verbose=False):
    vm = ReplVM()
    ast = vm.parse(code)
    if verbose:
        print(ast)
    vm.exec(ast)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FAP interpreter.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), help='Eval given file.')
    parser.add_argument('-c', help='Eval given line.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()
    if args.infile:
        fap_eval(args.infile.read(), verbose=args.verbose)
    elif args.c:
        fap_eval(args.c, verbose=args.verbose)
    else:
        fap_repl(verbose=args.verbose)
