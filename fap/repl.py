from parsimonious.nodes import NodeVisitor

from .grammar import GRAMMAR


class ReplVMError(Exception):
    pass


class ReplVM:
    def __init__(self):
        self.local = {}
        self._visitor = ReplVisitor(self)

    def parse(self, code):
        return GRAMMAR.parseString(code)

    def exec(self, ast):
        self._visitor.visit(ast)

    def parse_and_exec(self, code):
        self.exec(self.parse(code))


class ReplVisitor(NodeVisitor):

    def __init__(self, vm):
        self.vm = vm
        super().__init__()

    def visit(self, ast):
        for node in ast:
            print(self.visit_node(node))

    def visit_node(self, node):
        method = getattr(self, 'visit_' + type(node).__name__, self.generic_visit)
        return method(node)

    def visit_AddExpr(self, n):
        return self.visit_node(n.args[0]) + self.visit_node(n.args[1])

    def visit_SubExpr(self, n):
        return self.visit_node(n.args[0]) - self.visit_node(n.args[1])

    def visit_MultExpr(self, n):
        return self.visit_node(n.args[0]) * self.visit_node(n.args[1])

    def visit_DivExpr(self, n):
        return int(self.visit_node(n.args[0]) / self.visit_node(n.args[1]))

    def generic_visit(self, n):
        return n


def fap_repl():
    quit = False
    vm = ReplVM()
    while not quit:
        line = input('>>> ')
        if line[-1] == '\\':
            line += input('... ')
        elif line == 'quit':
            return
        try:
            print(vm.parse_and_exec(line))
        except ReplVMError as exc:
            print(exc)


def fap_eval(line):
    vm = ReplVM()
    vm.parse_and_exec(line)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FAP interpreter.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), help='Eval given file.')
    parser.add_argument('-c', help='Eval given line.')
    args = parser.parse_args()
    if args.infile:
        fap_eval(args.infile.read())
    elif args.c:
        fap_eval(args.c)
    else:
        fap_repl()
