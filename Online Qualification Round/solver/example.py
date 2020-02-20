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
        libraries = sorted(self.data['libs'], key=lambda l: l['signup_time'], reverse=True)

        days_spend = 0
        while days_spend < self.data['num_days']:
            if not libraries:
                break
            days_left = self.data['num_days'] - days_spend
            lib = libraries.pop()
            days_left -= lib['signup_time']
            if days_left < 0:
                break
            books = list(lib['books'])[:days_left * lib['books_per_day']]
            self.solution.append((lib['lib_id'], books))
            days_spend += lib['signup_time']
        return True
