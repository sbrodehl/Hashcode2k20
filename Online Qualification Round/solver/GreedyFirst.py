from .basesolver import BaseSolver


class Solver(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)


    def get_worth(self,lib_num,days_left,books_used):
        lib = self.data["libs"][lib_num]
        books_left = lib["books"]-books_used
        num_books_to_scan = (days_left - lib["signup_time"])*lib["books_per_day"]
        if num_books_to_scan<=0:
            return -1,set()
        scores = [(worth,index) for index,worth in enumerate(book_worth) if index in books_left]
        scores.sort()
        scan_books = scores[-1*min(num_books_to_scan,len(scores)):]

        return sum([i[0] for i in scan_books],set([i[1] for i in scan_books]))



    def solve(self):

        result = []

        days_left = seld.data["num_days"]

        while days_left:
            books_used = set()

            libs_used = set()
            best_score = 0
            for lib in range(self.data["num_libs"]):
                if lib in libs_used:
                    continue
                score,books = self.get_worth(lib,days_left,books_used)
                if score>best_score:
                    best_score=score
                    best_lib = lib

            result.append([best_lib,list(books)])
            days_left -= self.data["libs"][lib]["signup_time"]
            books_used.update(books)
            libs_used.add(best_lib)








        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        return result
