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
        return False
