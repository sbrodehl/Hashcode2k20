#!/usr/bin/env python3
import logging
import numpy as np
from .parsing import parse_input, parse_output


class Score(object):
    def __init__(self):
        self.scores = []

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
    _is_book_scanned = [0] * problem['num_books']
    _lib_is_signed_up = [False] * problem['num_libs']
    _lib_scan_index = [0] * problem['num_libs']
    _signup_proc_running = 0
    _signup_proc_time_left = 0
    current_day = 0
    while current_day < problem['num_days']:
        for libidx, books in solution:
            # scan books if signed up
            if _lib_is_signed_up[libidx]:
                # get the current book ids to be scanned
                scanning_books = books[_lib_scan_index[libidx]:
                                       _lib_scan_index[libidx] + problem['libs'][libidx]['books_per_day']]

                for b in scanning_books:
                    if not _is_book_scanned[b]:
                        score_ += problem['book_worth'][b]
                        _is_book_scanned[b] = True
                _lib_scan_index[libidx] += problem['libs'][libidx]['books_per_day']
            else:
                if not _signup_proc_running:
                    # let's sign up that lib
                    _signup_proc_running = libidx
                    _signup_proc_time_left = problem['libs'][libidx]['signup_time']
        # advance day
        current_day += 1
        _signup_proc_time_left -= 1
        if not _signup_proc_time_left:
            # reset signup process if time evolved
            _lib_is_signed_up[_signup_proc_running] = True
            _signup_proc_running = 0

    return score_


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='print score', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file_in', type=str, help='input file e.g. a_example.in')
    parser.add_argument('file_out', type=str, help='output file e.g. a_example.out')
    parser.add_argument('--debug', action='store_true', help='set debug level')
    args = parser.parse_args()

    set_log_level(args)

    score = compute_score(args.file_in, args.file_out)

    print("Score for {}: {} points".format(args.file_out, score.total()))
