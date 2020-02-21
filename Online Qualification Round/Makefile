SOLVER=example

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: A B C D E F

A:
	python3 main.py input/a.txt --output output/a.txt --solver $(SOLVER) $(DEBUGSTR)

B:
	python3 main.py input/b.txt --output output/b.txt --solver $(SOLVER) $(DEBUGSTR)

C:
	python3 main.py input/c.txt --output output/c.txt --solver $(SOLVER) $(DEBUGSTR)

D:
	python3 main.py input/d.txt --output output/d.txt --solver $(SOLVER) $(DEBUGSTR)

E:
	python3 main.py input/e.txt --output output/e.txt --solver $(SOLVER) $(DEBUGSTR)

F:
	python3 main.py input/f.txt --output output/f.txt --solver $(SOLVER) $(DEBUGSTR)
