from .basesolver import BaseSolver
import numpy as np
import gurobipy
import time
import zlib
from pathlib import Path
from IPython import embed


class GurobiSolver(BaseSolver):
    def __init__(self, input_str, improve=True, dtype=np.int64):  # int64 required to prevent overflows
        super().__init__(input_str)
        self.improve = improve

        # caching of best solution
        self.data_hash = zlib.adler32(str(self.data).encode('utf-8'))
        self.cache_file = cache_fn = Path("output") / f'cache_{abs(self.data_hash)}.npy'

        # store some library data as numpy array for faster processing
        self.signup_time = np.array([lib['signup_time'] for lib in self.data['libs']], dtype=dtype)
        self.books_per_day = np.array([lib['books_per_day'] for lib in self.data['libs']], dtype=dtype)
        self.book_worth = np.array(self.data['book_worth'], dtype=dtype)

        # prepare data for gurobi
        self.weights, self.bookset = self.build_weights_and_bookset()

    def build_weights_and_bookset(self, libs=None):
        if libs is None: libs = range(self.data['num_libs'])
        weights = {(l, p, b): self.data['book_worth'][b] for l in libs for p, b in enumerate(self.data['libs'][l]['books'])}
        bookset = set([b for l, p, b in weights])
        return weights, bookset

    def lib_worth(self, lib, book_worth, remaining_days, update_book_worth=False):
        # calculate maximum worth of scanned books for a library, taking into account
        # the number of days remaining and which books are already scanned by another library
        max_books = max(0, remaining_days - lib['signup_time']) * lib['books_per_day']
        use_books = sorted(lib['books'], key=lambda x: book_worth[x], reverse=True)[:max_books]
        sum_worth = sum(book_worth[use_books])
        if update_book_worth: book_worth[use_books] = 0
        return sum_worth

    def lib_heuristic(self, lib, *args, **kwargs):
        # worth divided by signup_time as heuristic, if identical, prefer libs with lower signup time
        worth = self.lib_worth(lib, *args, **kwargs)
        return worth / lib['signup_time'], -lib['signup_time']

    def sort_libs_greedy(self):
        print('greedy library selection (days_remain>min_worth):', end='', flush=True)
        order = []
        unused = dict(enumerate(self.data['libs']))
        book_worth = np.copy(self.book_worth)
        remaining_days = self.data['num_days']
        min_worth = 0

        while unused and remaining_days>0:
            # greedy selection of next library
            order.append(max(unused.items(), key=lambda x:self.lib_heuristic(x[1], book_worth, remaining_days))[0])
            lib = unused.pop(order[-1])

            # update remaining_days and worth of scanned books
            remaining_days -= lib['signup_time']
            min_worth += self.lib_worth(lib, book_worth, remaining_days, update_book_worth=True)

            if remaining_days > 0 : print(f' {remaining_days}>{min_worth}', end='', flush=True)
            else: order.pop()  # remove library if there is no time to scan any books

        print()
        return np.array(order)

    def solve(self):
        try:  # load from cache file if possible, as the calculation is not optimized and can take long
            order = np.load(self.cache_file); print('order recovered from cache')
        except:  # use greedy library selection as starting point
            order = self.sort_libs_greedy()
            try: np.save(self.cache_file, order)
            except: pass

        result = self.fixed_order_optimal_solve(order)

        a = b = 0
        while self.improve:
            try:
                while self.improve:
                    order = np.copy(result['order'])

                    # random swaps
                    #b = np.random.randint(1, len(order))
                    #a = np.random.randint(max(0, b - 100), b)

                    # adjacent swaps
                    b = max(1, (b+1) % len(order)); a = max(0, b-1)

                    order[a], order[b] = order[b], order[a]
                    print(f'swap {a}<>{b}: ', end='')
                    new_result = self.fixed_order_optimal_solve(order)
                    if new_result['value']>result['value']:
                        b -= 2
                        print(f'NEW BEST VALUE: {result["value"]} -> {new_result["value"]}')
                        result = new_result
                        np.save(self.cache_file, result['order'])
            except KeyboardInterrupt: embed() # open interactive shell

        self.solution = self.extract_solution(result)
        return True

    def get_books_per_lib(self, order):
        max_books_for_lib = np.zeros_like(self.books_per_day)
        max_books_for_lib[order] = np.maximum(0, self.data['num_days'] - np.cumsum(self.signup_time[order]))
        max_books_for_lib *= self.books_per_day
        return max_books_for_lib

    def fixed_order_optimal_solve(self, order, use_full_model=False):
        start = time.time()

        # store order for solution extraction
        run_data = {'order': np.copy(order)}

        # init model
        run_data['model'] = m = gurobipy.Model()
        print('Build model...', end='', flush=True)
        weights, bookset = (self.weights, self.bookset) if use_full_model else self.build_weights_and_bookset(order)
        print(f' {len(weights)} vars...', end='', flush=True)

        # turn off logging
        m.setParam('OutputFlag', 0)
        m.setParam('LogToConsole', 0)

        # always solve optimally
        m.setParam(gurobipy.GRB.Param.MIPGap, 0)

        # create a variable for each possible library/book combination
        run_data['vars'] = x = m.addVars(weights, vtype=gurobipy.GRB.BINARY, name='x')

        print(' set_obj...', end='', flush=True)
        # objective: maximize worth
        m.setObjective(x.prod(weights), gurobipy.GRB.MAXIMIZE)

        # constraint: max. number of books per library
        lib_constr = range(self.data['num_libs']) if use_full_model else order
        print(f' {len(lib_constr)} lib_cs...', end='', flush=True)
        books_per_lib = self.get_books_per_lib(order)
        for i in lib_constr:
            m.addConstr(x.sum(i, '*', '*') <= books_per_lib[i])

        # constraint: each book can be scanned only once
        print(f' {len(bookset)} book_cs...', end='', flush=True)
        for b in bookset:
            m.addConstr(x.sum('*', '*', b) <= 1)

        # optimize, return result
        print(' solve...', end='', flush=True)
        m.optimize()
        run_data['value'] = val = int(m.getObjective().getValue()+0.5)
        print(f' val: {val} ({time.time()-start:.3f}s)')
        return run_data

    def extract_solution(self, run_data):
        solution = [[i, []] for i in range(self.data['num_libs'])]
        for (i, j, b), v in run_data['vars'].items():
            if v.x > 0.9: solution[i][1].append(b)
        return [solution[i] for i in run_data['order'] if solution[i][1]]
