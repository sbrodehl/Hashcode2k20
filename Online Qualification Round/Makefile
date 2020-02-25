SOLVER=example

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: A B C D E F

zip:
	zip -r output/submission.zip . --exclude @.exclude.lst

A: zip
	python3 main.py input/a.txt --output output/a.txt --solver $(SOLVER) $(DEBUGSTR)

B: zip
	python3 main.py input/b.txt --output output/b.txt --solver $(SOLVER) $(DEBUGSTR)

C: zip
	python3 main.py input/c.txt --output output/c.txt --solver $(SOLVER) $(DEBUGSTR)

D: zip
	python3 main.py input/d.txt --output output/d.txt --solver $(SOLVER) $(DEBUGSTR)

E: zip
	python3 main.py input/e.txt --output output/e.txt --solver $(SOLVER) $(DEBUGSTR)

F: zip
	python3 main.py input/f.txt --output output/f.txt --solver $(SOLVER) $(DEBUGSTR)
