# Google \# Hash Code 2020

Solutions and code for the [Google \# Hash Code 2020](https://codingcompetitions.withgoogle.com/hashcode).

![Hash Code 2020 Banner](HashCode2020.png)

> Hash Code is a team programming competition, organized by Google, for students and professionals around the world.
> You pick your team and programming language and we pick an engineering problem for you to solve.
>
> _from [\# Hash Code](https://codingcompetitions.withgoogle.com/hashcode)_

## Practice Round

tba.

## Online Qualification Round

tba.

## Getting Started

The current version requires the following libraries.
See [requirements.txt](requirements.txt) for the full list of requirements.

The easiest way to install those dependencies is by using the [requirements.txt](requirements.txt) file with `pip3`.
```shell
pip3 install -r requirements.txt
```

### Code \& Solver Structure

We use python to import various different methods to actually solve a given problem.
In that way we can quickly iterate through different approaches and find the best way of solving the problem.

The _solvers_ are imported from the `main.py` program of the corresponding round,
e.g. [Practice Round/main.py](Practice%20Round/main.py),
with the `--solver SOLVER` argument describing a solver in the [solver](Practice%20Round/solver) directory
and `input` being an input file from the [input](Practice%20Round/input) directory.

See the `help` below for more details.

```shell
$ python3 main.py -h
usage: main.py [-h] [--output OUTPUT] [--solver SOLVER] input

positional arguments:
  input            input file

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  output file
  --solver SOLVER
```

The `main.py` imports the solver with the input parameter string, e.g. `Solver(args.input)`.
Then the `solve()` method is invoked, and in if an `--output` path is set,
the `write(args.output)` method is called with the given output parameter string.

Therefor each solver/approach to a problem needs to inherit from the `class BaseSolver`
in the `solver` directory of the corresponding round (Final, Qualification, Practice).

This base class ensures, that the solver has a `__init__` method, which has `input_str` as an argument,
which is the the filepath of the given input.
This methods needs to take care of e.g. input parsing.

Each solver then needs to implements at least the two following methods:

- The `solve()` method solves the *problem* and holds the solution in memory.  
- The `write()` method writes a correct output file which can be submitted
online.

Together with the output file one can then submit the corresponding solver file
(no need to zip various random files ... *Sorry Google!*).
  
**Happy coding!**

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details
