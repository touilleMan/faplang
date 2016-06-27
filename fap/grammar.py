import operator
# from pyparsing import Group, Word, Optional, Regex, restOfLine, nums
from pyparsing import *


number = Group(Optional('-') + Word(nums)).setParseAction(lambda s, l, t: int(''.join(t[0]))).setResultsName('number')
boolean = Group(Literal('True') | Literal('False')).setParseAction(lambda s, l, t: t[0][0] == 'True').setResultsName('boolean')

comment = Group('--' + restOfLine).suppress()

expr = Forward().setResultsName('expr')

op_map = {
    '+': None,
    '-': None,
    '*': None,
    '/': None,
    '&': None,
    '|': None,
    '&&': None,
    '||': None,
    '==': None
}
op = oneOf('+ - * / & | && || ==').setResultsName('op')

lparen = Literal('(').suppress()
rparen = Literal(')').suppress()

line = expr | comment | (expr + comment)
atom = boolean | number | Group(lparen + expr + rparen).setParseAction(lambda s, l, t: t[0])

class Expression:

    @classmethod
    def construct(cls, s, l, t):
        if len(t[0]) == 1:
            return t[0]
        else:
            return OP_MAP[t[0][1]](t[0][0], t[0][2])

    def __init__(self, *args):
        self.args = args

OP_MAP = {k: type(n + 'Expr', (Expression, ), {}) for k, n in {
    '+': 'Add',
    '-': 'Sub',
    '*': 'Mult',
    '/': 'Div',
    '==': 'Equal'
}.items()}


expr << Group(atom + ZeroOrMore(op + expr)).setParseAction(Expression.construct)

# GRAMMAR = Optional(line) + ZeroOrMore(Literal("\\n").suppress() + line)
GRAMMAR = ZeroOrMore(line)

# for code in (
#         "-- foo",
#         "1 -- foo",
#         "1",
#         "1 + 1",
#         "-1",
#         "-1 + -1",
#         "1 + 1 + 1",
#         "2 * (1 + 1)",
#         "(1 + 1) * 2",
#         'True && False',
#         'yoyo',
#         'False == True'
#     ):
#     print(line.parseString(code))
