from .basesolver import BaseSolver


class Solver(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)
        self.sorted_books = list(sorted(list(zip(self.data["book_worth"],range(len(self.data["book_worth"]))))))


    def wpd_lib(self,lib):
        #books = [worth for worth,id in self.sorted_books if id in lib["books"]]
        books = sorted([self.data["book_worth"][b_id] for b_id in lib['books']],reverse=True)

        wpd = []
        for i in range(self.data["num_days"]+1):
            if i<lib["signup_time"]:
                wpd.append(0)
            else:
                #print(len(books))
                if len(books)>i-lib["signup_time"]:
                    if len(wpd)>0:
                        wpd.append(wpd[-1]+books[i-lib["signup_time"]])
                    else:
                        wpd.append(books[i-lib["signup_time"]])
                else:
                    wpd.append(wpd[-1])
        return wpd


    def lib_worth(self,lib):
        books = sorted([self.data["book_worth"][b_id] for b_id in lib['books']],reverse=True)
        num_books = (self.data['num_days']-lib["signup_time"])*lib["books_per_day"]

        return float(sum(books[:num_books]))/(self.data['num_days']-lib["signup_time"])

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        libraries = self.data["libs"]
        for lib in libraries:
            lib["wpd_arr"]=self.wpd_lib(lib)
            lib["WPD"]=self.lib_worth(lib)
        #libraries = list(sorted(libraries, key=lambda l: self.lib_worth(l), reverse=True))
        lib = libraries
        for i in range(len(lib)):
            for j in range(i,len(lib)-1):
                if lib[j]["WPD"]*lib[j+1]["signup_time"]>lib[j+1]["WPD"]*lib[j]["signup_time"]:
                    lib[j],lib[j+1]=lib[j+1],lib[j]


        #libraries = sorted(libraries, key=lambda l: l['books_per_day'], reverse=True)
        used_books = set()
        used_libs = set()
        days_spend = 0
        while days_spend < self.data['num_days']:
            if not libraries:
                break
            days_left = self.data['num_days'] - days_spend

            cur_ind = -1
            for i in range(len(libraries)):
                if not i in used_libs:
                    if cur_ind==-1:
                        cur_ind=i
                    else:
                        if libraries[cur_ind]["wpd_arr"][days_left]*libraries[i]["signup_time"]>libraries[i]["wpd_arr"][days_left]*libraries[cur_ind]["signup_time"]:
                            cur_ind=i

            if cur_ind==-1:
                return True

            lib = libraries[cur_ind]
            used_libs.add(cur_ind)
            days_left -= lib['signup_time']
            if days_left < 0:
                break

            books_left = [(self.data["book_worth"][b_id],b_id) for b_id in lib['books'] if b_id not in used_books]
            books_left = list(reversed(sorted(books_left)))

            books = [b[1] for b in books_left[:days_left * lib['books_per_day']]]
            if len(books)!=0:
                self.solution.append((lib['lib_id'], books))
                days_spend += lib['signup_time']
        return True
