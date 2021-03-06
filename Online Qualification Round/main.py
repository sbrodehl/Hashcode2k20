import importlib
import importlib.util
import pkgutil
from pathlib import Path


def get_available_solver(dirname, baseclass):
    spec = importlib.util.find_spec(Path(dirname).name)
    for (_, name, _) in pkgutil.iter_modules([dirname]):
        try:
            importlib.import_module(f'.{name}', spec.name)
        except ModuleNotFoundError:
            pass
    _classes = {str(cls.__name__).lower(): cls for cls in baseclass.__subclasses__()}
    return [str(_cls).lower() for _cls in _classes], _classes


if __name__ == '__main__':
    import argparse
    import logging

    parser = argparse.ArgumentParser()

    cls_names, classes = get_available_solver("solver", importlib.import_module("solver.basesolver").BaseSolver)

    # need to be
    parser.add_argument("input", help="input file")
    parser.add_argument("--output", help="output file")
    parser.add_argument('--debug', action='store_true', help='set debug level')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--solver", help="available solver", type=str, choices=cls_names, default="example")
    group.add_argument('--score', help="computes score and insights of given data set", action='store_true')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger(__name__)

    if args.score:
        scoring = importlib.import_module("solver.scoring")
        score = scoring.compute_score(args.input, args.output)
        score.print_insights()
        exit(0)

    # get the chosen solver
    solver = classes[args.solver]
    # solver init with filepath
    solver = solver(args.input)

    # solve the problem with given input
    success = solver.solve()
    if not success:
        raise RuntimeError("No solution found!")

    # maybe create a solution file
    if args.output:
        solver.write(args.output)
