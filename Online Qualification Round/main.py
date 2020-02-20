if __name__ == '__main__':
    import importlib
    import argparse

    parser = argparse.ArgumentParser()

    # need to be
    parser.add_argument("input", help="input file")

    parser.add_argument("--output", help="output file")
    parser.add_argument("--solver", type=str, default="example")
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
