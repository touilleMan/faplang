from .ast import GRAMMAR
from .interpreter import FapVM, FapVMError


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
:quit\tleave the interpreter
""")
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


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FAP interpreter.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), help='Eval given file.')
    parser.add_argument('-c', help='Eval given line.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()
    if args.infile:
        ret = fap_eval(args.infile.read(), verbose=args.verbose)
    elif args.c:
        ret = fap_eval(args.c, verbose=args.verbose)
    else:
        ret = fap_repl(verbose=args.verbose)
    raise SystemExit(ret)
