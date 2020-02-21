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

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger(__name__)

    if args.score:
        scoring = importlib.import_module('.'.join(["solver", "scoring"]))
        score = scoring.compute_score(args.input, args.output)
        nsghs = score.insights
        LOGGER.info(f"Submission: {Markup.BOLD}Scoring & Insights{Markup.END}")
        LOGGER.info(f"Your submission scored {Markup.BOLD}{score.total():,}{Markup.END} points.")
        LOGGER.info(
            f"The library signup has been completed for {Markup.BOLD}{nsghs['libs_signed_up']:,} out of"
            f" {nsghs['num_libs']:,}{Markup.END} libraries ({nsghs['signup_stats']:.2f}%). "
            f"The last library signup process ended on day {Markup.BOLD}{nsghs['signup_proc_finish_day']:,}{Markup.END}"
            f" of {nsghs['num_days']:,} days. Library signup took "
            f"{Markup.BOLD}{nsghs['signup_proc_complete_stats']:,.2f}{Markup.END} days on average.")
        LOGGER.info(
            f"A total of {Markup.BOLD}{nsghs['total_scanned_books']:,}{Markup.END} books have been scanned. "
            f"{Markup.BOLD}{nsghs['unique_scanned_books']:,}{Markup.END} of those books were distinct with an average "
            f"score of {Markup.BOLD}{nsghs['scanned_book_avg_worth']:,.2f}{Markup.END}. "
            f"This is {Markup.BOLD}{nsghs['scanned_books_freq']:.2f}%{Markup.END} of the {nsghs['num_books']:,} books"
            f" available across all libraries. The minimum score of a scanned book was "
            f"{Markup.BOLD}{nsghs['scanned_book_worth_min']:,}{Markup.END} and the maximum score of a scanned "
            f"book was {Markup.BOLD}{nsghs['scanned_book_worth_max']:,}{Markup.END}.")
        exit(0)

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
