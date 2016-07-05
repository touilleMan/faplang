from .builtins import FapClosure, DEFAULT_LOCAL
from .exceptions import FapVMError


class FapVM:
    def __init__(self, local=None):
        self.local = DEFAULT_LOCAL.copy()
        if local:
            self.local.update(local)
        self._visitor = FapASTEvalVisitor(self)

    def exec(self, ast):
        return self._visitor.visit(ast)

    def parse_and_exec(self, code):
        return self.exec(self.parse(code))


class FapASTEvalVisitor:

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

    def visit_String(self, n):
        return n.value

    def visit_Variable(self, n):
        value = self.vm.local.get(n.value)
        if not value:
            raise FapVMError('%s is not defined' % n)
        return value

    def visit_Application(self, n):
        func = self.visit_Expr(n.func)
        param = self.visit_Expr(n.param)
        if isinstance(func, FapClosure):
            return func.apply(self.vm.local, param)
        else:
            raise FapVMError('%s cannot be applied to %s' % (n.func, n.param))

    def visit_FuncDef(self, n):
        elem = self.vm.local.get(n.name)
        if elem:
            if isinstance(elem, FapClosure):
                elem.append_rule(n.params, n.body)
            else:
                raise FapVMError('%s already exist but is not a function' % n.name)
        else:
            elem = FapClosure(name=n.name)
            elem.append_rule(n.params, n.body)
            self.vm.local[n.name] = elem

    def generic_visit(self, n):
        raise RuntimeError('Unknown ast node %r' % n)
