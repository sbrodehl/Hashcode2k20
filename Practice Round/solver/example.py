import logging
import sys
import resource
from functools import lru_cache
from .basesolver import BaseSolver


class Solver(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        maxweight = self.data[0]
        items = self.data[1]
        _, chosen_items = self.knapsack(items, maxweight)
        self.solution = chosen_items
        return True

    @staticmethod
    def knapsack(items, maxweight):
        """Solve the knapsack problem by finding the most valuable subsequence
        of items that weighs no more than maxweight.

        Taken from https://codereview.stackexchange.com/a/20581

        items must be a sequence of values, where value is a non-negative integer.

        maxweight is a non-negative integer.

        Return a pair whose first element is the sum of values in the most
        valuable subsequence, and whose second element is the subsequence.

        >>> items = [4, 2, 6, 1, 2]
        >>> knapsack(items, 15)
        (15, [4, 2, 6, 1, 2])

        """
        print("sys.getrecursionlimit: {}".format(sys.getrecursionlimit()))
        resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
        sys.setrecursionlimit(10**6)
        print("sys.getrecursionlimit: {}".format(sys.getrecursionlimit()))

        @lru_cache(maxsize=None)
        def bestvalue(i, j):
            # Return the value of the most valuable subsequence of the first
            # i elements in items whose weights sum to no more than j.
            if j < 0:
                return float('-inf')
            if i == 0:
                return 0
            value = items[i - 1]
            return max(bestvalue(i - 1, j), bestvalue(i - 1, j - value) + value)

        j = maxweight
        result = []
        for i in reversed(range(len(items))):
            if bestvalue(i + 1, j) != bestvalue(i, j):
                result.append(items[i])
                j -= items[i]
        result.reverse()
        ret = bestvalue(len(items), maxweight), result
        logging.debug(bestvalue.cache_info())
        return ret
