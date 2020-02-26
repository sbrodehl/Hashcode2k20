from .basesolver import BaseSolver
from .scoring import Markup
import numpy as np
import logging


LOGGER = logging.getLogger(__name__)


class Statistics(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        libraries = self.data['libs']
        books = np.zeros(self.data['num_books'], np.int)
        lib_hashes = np.zeros((self.data['num_libs'], self.data['num_books']))
        signup_sum = 0
        for lib in libraries:
            _books = np.zeros_like(books)
            indices = list(map(int, lib['books']))
            _books[indices] = 1
            books += _books
            signup_sum += lib['signup_time']
            lib_hashes[lib['lib_id']] = _books

        book_stat_count_na = np.sum(np.maximum((books - 1) * -1, 0))
        book_stat_count_na_freq = 100.0 * book_stat_count_na / self.data['num_books']
        book_stat_count_min = np.min(books)
        book_stat_count_max = np.max(books)
        book_stat_count_mean = np.mean(books)
        book_stat_count_mean_std = np.std(books)
        lib_signup_freq = 100.0 * signup_sum / self.data['num_days']

        book_stat_worth_sum = np.array(self.data['book_worth']).sum()
        book_stat_worth_sel = np.array(self.data['book_worth'])[books.astype(bool).astype(int) > 0]
        book_stat_worth_min = np.min(book_stat_worth_sel)
        book_stat_worth_max = np.max(book_stat_worth_sel)

        LOGGER.info(f"{Markup.BOLD}Statistics{Markup.END}:")

        LOGGER.info(f"Books: {Markup.BOLD}{self.data['num_books']:,}{Markup.END} "
                    f"Libraries: {Markup.BOLD}{self.data['num_libs']:,}{Markup.END} "
                    f"Time: {Markup.BOLD}{self.data['num_days']:,}{Markup.END}")

        LOGGER.info(f"The score of all books is {Markup.BOLD}{book_stat_worth_sum:,}{Markup.END}.")
        LOGGER.info(f"The minimum count of a book is {Markup.BOLD}{book_stat_count_min:,}{Markup.END} and "
                    f"the maximum count of a book is {Markup.BOLD}{book_stat_count_max:,}{Markup.END}.")
        LOGGER.info(f"On average a book appears {Markup.BOLD}{book_stat_count_mean:.2f} "
                    f"± {book_stat_count_mean_std:.2f}{Markup.END} times.")
        LOGGER.info(f"There are {Markup.BOLD}{book_stat_count_na:,}{Markup.END} books which do not exist "
                    f"in libraries ({book_stat_count_na_freq:,.2f}%).")
        LOGGER.info(f"The minimum score of an existing book is {Markup.BOLD}{book_stat_worth_min:,}{Markup.END} and "
                    f"the maximum score of an existing book is {Markup.BOLD}{book_stat_worth_max:,}{Markup.END}.")
        LOGGER.info(f"The signup of all libraries takes {Markup.BOLD}{signup_sum:,}{Markup.END} days, "
                    f"which is {Markup.BOLD}{lib_signup_freq:,.2f}%{Markup.END} of all {self.data['num_days']:,} days.")

        # early exit,
        # we only want to compute them statistics
        exit(0)
