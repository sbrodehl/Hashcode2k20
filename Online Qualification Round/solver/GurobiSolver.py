from .basesolver import BaseSolver
import numpy as np
import gurobipy
from IPython import embed

class Solver(BaseSolver):
    def __init__(self, input_str):
        super().__init__(input_str)
        self.signup_time = np.array([lib['signup_time'] for lib in self.data['libs']])
        self.books_per_day = np.array([lib['books_per_day'] for lib in self.data['libs']])
        self.lib_pos_book_worth = {(i,j,b): self.data['book_worth'][b] for i,lib in enumerate(self.data['libs']) for j,b in enumerate(lib['books'])}

    def solve(self):
        print('Greedy sort')
        libraries = self.data["libs"].copy()
        for lib in libraries:
            # lib["wpd_arr"]=self.wpd_lib(lib)
            lib["WPD"] = self.lib_worth(lib)
        # libraries = list(sorted(libraries, key=lambda l: self.lib_worth(l), reverse=True))
        lib = libraries
        for i in range(len(lib)):
            for j in range(i, len(lib) - 1):
                if lib[j]["WPD"] * lib[j + 1]["signup_time"] > lib[j + 1]["WPD"] * lib[j]["signup_time"]:
                    lib[j], lib[j + 1] = lib[j + 1], lib[j]

        print('Gurobi start')
        self.order = [lib['lib_id'] for lib in libraries][::-1] # why reverse here?
        self.bestv = 0
        self.done = False
        a=b=0
        while not self.done:
            cnt=0
            try:
                while True:
                    try:
                        a = np.random.randint(0, len(self.order))
                        b = np.random.randint(0, len(self.order))
                        if cnt: self.order[a], self.order[b] = self.order[b], self.order[a] # make swap
                        cnt += 1
                        nextv = self.solve_gurobi(self.order)
                        if nextv>self.bestv:
                            self.bestv = nextv
                            self.bests = self.extract_last_solution()
                            print('best sol found:', nextv, self.bestv)
                            self.order[a], self.order[b] = self.order[b], self.order[a]  # undo to keep
                    finally: self.order[a], self.order[b] = self.order[b], self.order[a]  # undo swap
            except KeyboardInterrupt: pass
            #embed()
        self.solution = self.bests
        return True

    def get_books_per_lib(self, order):
        max_books_for_lib = np.empty_like(self.signup_time)
        max_books_for_lib[order] = np.maximum(0, self.data['num_days'] - np.cumsum(self.signup_time[order]))
        max_books_for_lib *= self.books_per_day
        return max_books_for_lib

    def solve_gurobi(self, order):
        self.last_run = {'order': np.copy(order)}
        self.last_run['model'] = m = gurobipy.Model()
        m.setParam('OutputFlag', 0)
        m.setParam('LogToConsole', 0)
        m.setParam(gurobipy.GRB.Param.MIPGap, 0)
        self.last_run['vars'] = x = m.addVars(self.lib_pos_book_worth.keys(), vtype=gurobipy.GRB.BINARY, name='x')
        m.setObjective(x.prod(self.lib_pos_book_worth), gurobipy.GRB.MAXIMIZE) # maximize worth
        for i,n in enumerate(self.get_books_per_lib(order)):
            m.addConstr(x.sum(i,'*','*') <= n) # max books per library
        for b in range(self.data['num_books']):
            m.addConstr(x.sum('*','*',b) <= 1) # each book only once
        m.optimize()
        self.last_run['result'] = m.getObjective().getValue()
        return self.last_run['result']

    def extract_last_solution(self):
        solution = [[i,[]] for i in range(self.data['num_libs'])]
        for (i, j, b), v in self.last_run['vars'].items():
            if v.x>0.9: solution[i][1].append(b)
        reordered = []
        for i in self.last_run['order']:
            if solution[i][1]:
                reordered.append(solution[i])
        return reordered

    def lib_worth(self,lib):
        books = sorted([self.data["book_worth"][b_id] for b_id in lib['books']],reverse=True)
        num_books = (self.data['num_days']-lib["signup_time"])*lib["books_per_day"]
        return float(sum(books[:num_books]))/(self.data['num_days']-lib["signup_time"])
