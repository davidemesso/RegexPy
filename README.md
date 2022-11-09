# RegexPy
A didactic implementation of regex validation using FSM in python

##Content
- [regexFSM.py](./regexFSM.py) The core file, handling FSM creation and simulation, actually executing the regex matching.
- [Parser](./Parser/) The parser implementation which is used to obtain a polish notation stack based representation of the regex used for FSM generation, this folder only contains files used for execution.
- [ParserSource](./ParserSource/) Tools and sources used to easly generate ad hoc parser, can be used for recompile purpose. Special thanks: Professor [Mauro Leoncini](https://github.com/leoncini)

### HOW TO USE
- Instantiate a [FSMNotDeterministic](./regexFSM.py) object, passing all the parameters describing the regex and use it to obtain a [FSMDeterministic](./regexFSM.py) using the [subsetConstruction](./regexFSM.py)() method.
- Use [checkRegex](./regexFSM.py)() method of the obtained object for string validation.
- Use [test.sh](./test.sh) with a regex as parameter for testing parser-python interaction.
- RECOMPILING: Use [ParserSource/Makefile](./ParserSource/Makefile) if you need.

NOTE: you could instantiate directly a FSMDeterministic object in simple cases, but this is temporary

## WIP
The objective is to achieve the instantiation of a regex object just parsing a string describing it, without having to project the FSM itself.

This is computable via an algorithm that turns the regex into a not deterministic fsm, then using the subset construction to obtain a deterministic fsm, which is also simulable for string validation.

See https://deniskyashif.com/2019/02/17/implementing-a-regular-expression-engine/