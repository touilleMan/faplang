from fap.ast import *


def test_empty():
    for src in (
            '',
            '-- comment',
            ' -- comment',
            '\t\t-- 1 + 1'
        ):
        ast = GRAMMAR.parseString(src)
        assert not ast, src


def test_atom():
    for src, expected in (
            ('1', Number(1)),
            ('-2', Number(-2)),
            ('1234', Number(1234)),
            ('True', Boolean(True)),
            ('False', Boolean(False)),
            ('my_var', Variable('my_var'))
        ):
        ast = GRAMMAR.parseString(src)
        assert ast.asList() == [expected], src


def test_operation():
    for src, expected in (
            ('1 + 2', Application(Application(Variable('add'), Number(1)), Number(2))),
            ('-1 - -2', Application(Application(Variable('min'), Number(-1)), Number(-2))),
            ('1 + 2 / 3', Application(
                Application(
                    Variable('add'),
                    Number(1)
                ),
                Application(
                    Application(
                        Variable('div'),
                        Number(2)
                    ),
                    Number(3)
                )
            )),
            ('1 / 2 + 3', Application(
                Application(
                    Variable('add'),
                    Application(
                        Application(
                            Variable('div'),
                            Number(1)
                        ),
                        Number(2)
                    )
                ),
                Number(3)
            )),
            ('(1 + 2) / 3', Application(
                Application(
                    Variable('div'),
                    Application(
                        Application(
                            Variable('add'),
                            Number(1)
                        ),
                        Number(2)
                    )
                ),
                Number(3)
            )),
        ):
        ast = GRAMMAR.parseString(src)
        assert ast.asList() == [expected], src


def test_func_def():
    for src, expected in (
            ('f = 1', FuncDef('f', body=Number(1))),
            ('f x 1 = y', FuncDef(
                'f',
                params=[Variable('x'), Number(1)],
                body=Variable('y'))
            ),
            ('f x = x * 2', FuncDef(
                'f',
                params=[Variable('x')],
                body=Application(Application(Variable('mul'), Variable('x')), Number(2)))
            ),
            ('my_f x y z = z(x * y)', FuncDef(
                'my_f',
                params=[Variable('x'), Variable('y'), Variable('z')],
                body=Application(Variable('z'), Application(Application(Variable('mul'), Variable('x')), Variable('y'))))
            )
        ):
        ast = GRAMMAR.parseString(src)
        assert ast.asList() == [expected], src


def test_lambda():
    for src, expected in (
            ('\ x = 1', Lambda(params=[Variable('x')], body=Number(1))),
            ('\ = 1', Lambda(body=Number(1))),
            ('\ x y = x * 2', Lambda(
                params=[Variable('x'), Variable('y')],
                body=Application(Application(Variable('mul'), Variable('x')), Number(2)))
            ),
            ('(\= 3 * f True) 4', Application(
                Lambda(body=Application(
                    Application(
                        Variable('mul'),
                        Number(3)
                    ),
                    Application(
                        Variable('f'),
                        Boolean(True)
                    )
                )),
                Number(4)
                )
            )
        ):
        ast = GRAMMAR.parseString(src)
        assert ast.asList() == [expected], src
