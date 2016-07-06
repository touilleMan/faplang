import argparse
from sys import argv

from .interpreter import fap_repl, fap_eval


def fapi_main():
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


def fapc_main():
	raise NotImplementedError('fapc is not available yet !')
