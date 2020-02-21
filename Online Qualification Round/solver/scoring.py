#!/usr/bin/env python3
import logging
import numpy as np
from .parsing import parse_input, parse_output


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


def set_log_level(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


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
