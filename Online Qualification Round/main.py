if __name__ == '__main__':
    import importlib
    import argparse
    import logging

    class Markup:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    parser = argparse.ArgumentParser()

    # need to be
    parser.add_argument("input", help="input file")
    parser.add_argument("--output", help="output file")
    parser.add_argument('--debug', action='store_true', help='set debug level')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--solver", type=str, default="example")
    group.add_argument('--score', action='store_true')

    args = parser.parse_args()

    solver = None
    # try load the given solver
    try:
        solver = importlib.import_module('.'.join(["solver", args.solver]))
    except ImportError as e:
        parser.print_help()
        print(e)
        exit(1)

    # solver init with filepath
    solver = solver.Solver(args.input)

    # solve the problem with given input
    success = solver.solve()
    if not success:
        raise RuntimeError("No solution found!")

    # maybe create a solution file
    if args.output:
        solver.write(args.output)
