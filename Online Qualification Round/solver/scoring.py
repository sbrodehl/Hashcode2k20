#!/usr/bin/env python3
import logging
import numpy as np
from .parsing import parse_input, parse_output


class Score(object):
    def __init__(self):
        self.scores = []

    def total(self):
        return np.array(self.scores).sum()

    def add(self, interest_factor):
        self.scores.append(interest_factor)


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
    input_ = parse_input(file_in)
    output_ = parse_output(file_out)
    score_ = Score()
    # tba
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
