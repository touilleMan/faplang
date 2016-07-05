import operator
from collections import OrderedDict
from pyparsing import *


### AST elements ###

class Expr:
    pass


class Value(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.value)

    def __eq__(self, other):
        return isinstance(other, type(self)) and super().__eq__(other) and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Number(Value):
    pass


class Boolean(Value):
    pass


class String(Value):
    pass


class Variable(Value):
    pass


class Application(Expr):

    def __init__(self, func, param):
        self.func = func
        self.param = param

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<%s %s %s>' % (type(self).__name__, self.func, self.param)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.func == other.func and self.param == other.param

    def __hash__(self):
        return hash(self.func) ^ hash(self.param)


class FuncDef(Expr):
    def __init__(self, name, body, params=None):
        self.name = name
        self.params = tuple(params) if params else tuple()
        self.body = body

    def __repr__(self):
        if self.params:
            return '<%s %s %r = %r>' % (type(self).__name__, self.name, self.params, self.body)
        else:
            return '<%s %s = %r>' % (type(self).__name__, self.name, self.body)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and self.name == other.name and
                self.params == other.params and self.body == other.body)

    def __hash__(self):
        return hash(self.name) ^ hash(self.params) ^ hash(self.body)


class Lambda(FuncDef):
    def __init__(self, body, params=None):
        self.params = tuple(params) if params else tuple()
        self.body = body

    def __repr__(self):
        if self.params:
            return '<%s %r = %r>' % (type(self).__name__, self.params, self.body)
        else:
            return '<%s = %r>' % (type(self).__name__, self.body)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.params == other.params and self.body == other.body)

    def __hash__(self):
        return hash(self.params) ^ hash(self.body)



OPERATORS_MAP = OrderedDict([
    ('*', Variable('mul')),
    ('/', Variable('div')),
    ('+', Variable('add')),
    ('-', Variable('sub')),
    ('&&', Variable('and')),
    ('||', Variable('or')),
    ('|', Variable('bor')),
    ('&', Variable('band')),
    ('==', Variable('equal')),
    ('%', Variable('mod'))
])


### Grammar ###


comment = (Literal('--') + restOfLine).suppress()
lparen = Literal('(').suppress()
rparen = Literal(')').suppress()

label = Word(alphas + '_', alphanums + '_').setParseAction(lambda s, l, t: ''.join(t[0])).setName('label')
# operator = oneOf(' '.join(OPERATORS_MAP.keys())).setParseAction(lambda s, l, t: t[0]).setName('operator')

expr = Forward()

number = Combine(Optional('-') + Word(nums)).setParseAction(lambda s, l, t: Number(int(t[0])))
boolean = (Literal('True') | Literal('False')).setParseAction(lambda s, l, t: Boolean(t[0] == 'True'))
variable = label.setParseAction(lambda s, l, t: Variable(t[0]))
string = QuotedString(quoteChar="\"", escChar="\\", escQuote="\\\"").setParseAction(lambda s, l, t: String(t[0]))
lambdaa = (Literal('\\').suppress() + Group(ZeroOrMore(label)) + Literal("=").suppress() + expr).setParseAction(lambda s, l, t: Lambda(params=t[0], body=t[1]))

atom = (boolean | number | string | variable | lambdaa | (lparen + expr + rparen).setParseAction(lambda s, l, t: t)).setName('atom')

func_def = (
    # label.setResultsName('name')  # TODO: token is parsed as a variable, why ?
    variable.setResultsName('name') +  # Function name
    ZeroOrMore(atom).setResultsName('params') +  # Params
    Literal('=').suppress() +
    expr.setResultsName('body')  # Body
).setParseAction(lambda s, l, t: FuncDef(t.name.value, params=t.params.asList() if t.params else None, body=t.body)).setName('func_def')

arith_op = oneOf('+ -').setParseAction(lambda s, l, t: t[0]).setName('arith_op')
term_op = oneOf('* / %').setParseAction(lambda s, l, t: t[0]).setName('term_op')

def build_op(s, l, t):
    elems = t.asList()
    last = elems.pop(0)
    while elems:
        operator = OPERATORS_MAP[elems.pop(0)]
        operand = elems.pop(0)
        last = Application(Application(operator, last), operand)
    return last

def build_applications(s, l, t):
    last = t[0]
    for param in t[1:]:
        last = Application(last, param)
    return last

application = OneOrMore(atom).setParseAction(build_applications)

term = (application + ZeroOrMore(term_op + application)).setParseAction(build_op)

arith = (term + ZeroOrMore(arith_op + term)).setParseAction(build_op)

expr << OneOrMore(arith)

GRAMMAR = Optional(func_def | expr) + Optional(comment)


if __name__ == '__main__':
    from sys import argv
    # Generate & print AST
    ast = GRAMMAR.parseString(' '.join(argv[1:]))
    print(ast)
