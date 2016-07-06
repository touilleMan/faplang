from fap.ast import GRAMMAR
from fap.interpreter import FapVM


def _parse_and_exec(code):  
    vm = FapVM()
    ast = GRAMMAR.parseString(code)
    return vm.exec(ast)


def test_exec():
    for src, expected in (
        ("", None),  # Empty
        ("1 + 1", 2),
        ("3 + 2 * 2", 7),
        ("3 * 2 + 2", 8),
        ("3 * (2 + 2)", 12)
    ):
        res = _parse_and_exec(src)
        assert res == expected, src
