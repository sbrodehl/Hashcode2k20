import logging
import numpy as np
from .parsing import parse_input, parse_output

LOGGER = logging.getLogger(__name__)


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


class Score(object):
    def __init__(self):
        self.scores = []
        self.insights = {}

    def total(self):
        return np.array(self.scores).sum()

    def add(self, other):
        self.scores.append(other)

    def __add__(self, other):
        self.scores.append(other)
        return self

    def print_insights(self):
        nsghs = self.insights
        LOGGER.info(f"Submission: {Markup.BOLD}Scoring & Insights{Markup.END}")
        LOGGER.info(f"Your submission scored {Markup.BOLD}{self.total():,}{Markup.END} points.")
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


def compute_score(file_in, file_out):
    """
    Compute score (with bonus) of submission
    :param file_in: input file
    :param file_out: output file (solution)
    :return: Score
    """
    # read input and output files
    problem = parse_input(file_in)
    solution = parse_output(file_out)
    score_ = Score()
    # helper variables
    _is_book_scanned = [False] * problem['num_books']
    _lib_is_signed_up = [False] * problem['num_libs']
    _lib_scan_index = [0] * problem['num_libs']
    _signup_proc_running = -1
    _signup_proc_time_left = 0
    _signup_proc_last_complete = -1
    _total_scanned = 0
    current_day = 0
    while current_day < problem['num_days']:
        for libidx, books in solution:
            # scan books if signed up
            if _lib_is_signed_up[libidx]:
                if not _lib_scan_index[libidx] < len(books):
                    continue
                # get the current book ids to be scanned
                scanning_books = books[_lib_scan_index[libidx]:
                                       _lib_scan_index[libidx] + problem['libs'][libidx]['books_per_day']]
                _total_scanned += len(scanning_books)
                for b in scanning_books:
                    if not _is_book_scanned[b]:
                        score_ += problem['book_worth'][b]
                        _is_book_scanned[b] = True
                _lib_scan_index[libidx] += problem['libs'][libidx]['books_per_day']
            else:
                if _signup_proc_running < 0:
                    # let's sign up that lib
                    _signup_proc_running = libidx
                    _signup_proc_time_left = problem['libs'][libidx]['signup_time']
        # advance day
        current_day += 1
        _signup_proc_time_left -= 1
        if not _signup_proc_time_left:
            # reset signup process if time evolved
            _lib_is_signed_up[_signup_proc_running] = True
            _signup_proc_running = -1
            _signup_proc_last_complete = current_day - 1

    # aux vars
    _scanned_book_worth = [problem['book_worth'][idx] for idx, is_scanned in enumerate(_is_book_scanned) if is_scanned]
    _insights = {
        'libs_signed_up': sum(_lib_is_signed_up),
        'signup_stats': 100 * sum(_lib_is_signed_up) / problem['num_libs'],
        'signup_proc_finish_day': _signup_proc_last_complete,
        'signup_proc_complete_stats': sum([problem['libs'][idx]['signup_time'] for idx, is_signed_up in enumerate(_lib_is_signed_up) if is_signed_up]) / sum(_lib_is_signed_up),
        'total_scanned_books': _total_scanned,
        'unique_scanned_books': sum(_is_book_scanned),
        'scanned_book_worth': _scanned_book_worth,
        'scanned_book_avg_worth': sum(_scanned_book_worth) / len(_scanned_book_worth),
        'scanned_book_worth_min': min(_scanned_book_worth),
        'scanned_book_worth_max': max(_scanned_book_worth),
        'scanned_books_freq': 100 * sum(_is_book_scanned) / problem['num_books'],
        'num_days': problem['num_days'],
        'num_libs': problem['num_libs'],
        'num_books': problem['num_books'],
    }
    score_.insights = _insights
    return score_
