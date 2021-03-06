import logging

LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: photos, collection
    """
    LOGGER.debug("parsing {}".format(file_in))
    with open(file_in, 'r') as f:
        first_line = f.readline().strip()
        num_books, num_libs, num_days = [int(i) for i in first_line.split()]
        book_worth = [int(i) for i in f.readline().split()]
        libs = []
        for lib_id in range(num_libs):
            n_books, signup_time, books_per_day = [int(i) for i in f.readline().split()]
            books = set([int(i) for i in f.readline().split()])
            libs.append({"lib_id": lib_id,
                         "num_books": n_books,
                         "signup_time": signup_time,
                         "books_per_day": books_per_day,
                         "books": books})

    LOGGER.debug("parsing {}: done".format(file_in))
    return {"num_books": num_books,
            "num_libs": num_libs,
            "num_days": num_days,
            "book_worth": book_worth,
            "libs": libs}


def parse_output(file_out):
    """
    Parse output file
    :param file_out: output file name (solution)
    :return: n, slides
    """
    LOGGER.debug("parsing {}".format(file_out))
    solution = []
    with open(file_out, 'r') as f:
        first_line = f.readline().strip()
        libs_for_signup = int(first_line)
        for lid in range(libs_for_signup):
            line = list(map(int, f.readline().strip().split(' ')))
            assert len(line) == 2
            lib_id, num_books_to_scan = line[0], line[1]
            line = list(map(int, f.readline().strip().split(' ')))
            assert len(line) == num_books_to_scan
            books_to_scan = line
            solution.append((lib_id, books_to_scan))

    LOGGER.debug("parsing {}: done".format(file_out))
    return solution


# solution is a list of tuples of (library_id, [book1, book2, book3, ...])
def write_output(file_out, solution):
    LOGGER.debug("writing solution {}".format(file_out))
    with open(file_out, 'w') as f:
        f.write(f"{len(solution)}\n")
        for library_id, books in solution:
            f.write(f"{library_id} {len(books)}\n")
            f.write(" ".join(str(b) for b in books) + "\n")
