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
        # tba
        for pid, line in enumerate(f.readlines()):
            _split = line.strip().split(' ')
            # tba

    logging.debug("parsing {}: done".format(file_in))
    return None


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
        # tba
        for sid, line in enumerate(f.readlines()):
            solution = list(map(int, line.strip().split(' ')))
            # tba
    logging.debug("parsing {}: done".format(file_out))
    return solution


def write_output(file_out, solution):
    logging.debug("writing solution {}".format(file_out))
    with open(file_out, 'w') as f:
        f.write("{}\n".format(str(len(solution))))
        f.write("{}\n".format(" ".join(list(map(str, solution)))))
