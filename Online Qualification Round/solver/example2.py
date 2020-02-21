from .basesolver import BaseSolver


class Example2(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)
        self.sorted_books = list(sorted(list(zip(self.data["book_worth"],range(len(self.data["book_worth"])))),reverse=True))



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
        #lib = libraries
        libraries = sorted(libraries, key=lambda l: l['WPD'], reverse=True)

        #for i in range(len(libraries)):
        #    for j in range(i,len(libraries)-1):
        #        if libraries[j]["WPD"]*libraries[j+1]["signup_time"]>libraries[j+1]["WPD"]*libraries[j]["signup_time"]:
        #            libraries[j],libraries[j+1]=libraries[j+1],libraries[j]


        used_books = set()
        used_libs = set()
        days_spend = 0

        while days_spend < self.data['num_days']:
            #print(days_spend,self.data["num_days"])
            libraries_here = libraries[:max(int(len(libraries)/10+1),1)]

            if not libraries:
                break
            days_left = self.data['num_days'] - days_spend
            cur_lib =None
            best_ind=0
            for i in range(len(libraries_here)):

                if libraries_here[i]["lib_id"] in used_libs:
                    continue
                if cur_lib==None or cur_lib["wpd_arr"][max(days_left-libraries_here[i]["signup_time"],0)]<libraries_here[i]["wpd_arr"][max(days_left-cur_lib["signup_time"],0)]:
                    cur_lib=libraries_here[i]
                    best_ind=i
            #print(best_ind)
            #print(cur_lib["lib_id"])
            cur_lib = libraries[0]
            used_libs.add(cur_lib["lib_id"])
            lib = cur_lib
            if lib==None:
                break
            #print(lib['lib_id'])
            days_left -= lib['signup_time']
            if days_left < 0:
                break

            books_left = [(self.data["book_worth"][b_id],b_id) for b_id in lib['books'] if b_id not in used_books]
            books_left = list(reversed(sorted(books_left)))

            books = [b[1] for b in books_left[:days_left * lib['books_per_day']]]
            for ind in range(len(libraries)):
                if libraries[ind]["lib_id"]==lib["lib_id"]:
                    break

            del libraries[ind]

            if len(books)!=0:
                self.solution.append((lib['lib_id'], books))
                days_spend += lib['signup_time']
        #print(self.solution)
        return True
