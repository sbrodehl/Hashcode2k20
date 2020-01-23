import logging


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: photos, collection
    """
    logging.debug("parsing {}".format(file_in))
    input_items = []
    with open(file_in, 'r') as f:
        first_line = f.readline().strip()
        l_ = list(map(int, list(first_line.split(" "))))
        m = l_[0]
        n = l_[1]
        logging.debug("The hub needs {} slices from {} pizza types.".format(m, n))

        for pid, line in enumerate(f.readlines()):
            _split = line.strip().split(' ')
            input_items = list(map(int, list(line.strip().split(' '))))
            # check if amount of pizzas matches number of pizza types
            assert len(input_items) == n
            # check that only one line is read
            assert pid == 0
    logging.debug("parsing {}: done".format(file_in))
    return m, input_items


def parse_output(file_out):
    """
    Parse output file
    :param file_out: output file name (solution)
    :return: n, slides
    """
    logging.debug("parsing {}".format(file_out))
    solution = []
    with open(file_out, 'r') as f:
        first_line = f.readline().strip()
        n = int(first_line)

        for sid, line in enumerate(f.readlines()):
            solution = list(map(int, line.strip().split(' ')))
            # check if amount of pizzas matches number of pizza types
            assert len(solution) == n, "Submission file is not valid: Incorrect number of items" \
                                       " (expected:{}, found:{})".format(n, len(solution))
            # check that only one line is read
            assert sid == 0
    logging.debug("parsing {}: done".format(file_out))
    return solution


def write_output(file_out, solution):
    logging.debug("writing solution {}".format(file_out))
    with open(file_out, 'w') as f:
        f.write("{}\n".format(str(len(solution))))
        f.write("{}\n".format(" ".join(list(map(str, solution)))))
