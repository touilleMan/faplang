from ..ast import GRAMMAR
from .backend import FapVM, FapVMError


def fap_repl(verbose=False):
    quit = False
    vm = FapVM()
    verbose = verbose
    prompt_continue = False
    print("type `:help` if you're lost")
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
        elif line == ':help':
            print(""":help\tdisplay this message
:verbose\ttoggle debug verbosity
:quit\tleave the interpreter""")
            continue
        elif line == ':quit':
            return
        prompt_continue = False
        try:
            ast = GRAMMAR.parseString(line)
            if verbose:
                print(ast)
            ret = vm.exec(ast)
            if ret is not None:
                print(ret)
        except FapVMError as exc:
            print(exc)


def fap_eval(code, verbose=False):
    vm = FapVM()
    ast = GRAMMAR.parseString(code)
    if verbose:
        print(ast)
    return vm.exec(ast)
