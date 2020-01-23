import logging
from ortools.algorithms import pywrapknapsack_solver
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
    def knapsack(values, maxweight):
        solver = pywrapknapsack_solver.KnapsackSolver(
            pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
            'Knapsack')

        weights = [values]

        solver.Init(values, weights, [maxweight])
        computed_value = solver.Solve()

        packed_items = []
        total_weight = 0
        for i in range(len(values)):
            if solver.BestSolutionContains(i):
                packed_items.append(i)
                total_weight += weights[0][i]
        assert computed_value == total_weight
        logging.debug("Total value: {}".format(computed_value))
        logging.debug("Packed items: {}".format(packed_items))
        return total_weight, packed_items
