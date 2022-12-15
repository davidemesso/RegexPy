# RegexPy
A didactic implementation of regex validation using FSM in python with backend parsing in C++

## Content
- [regexFSM.py](./regexFSM.py) The core file, handling FSM creation and simulation, actually executing the regex matching.
- [Regex.py](./Regex.py) File containing the interface for user use. 
- [Parser](./Parser/) The parser implementation which is used to obtain a polish notation stack based representation of the regex used for FSM generation, this folder only contains files used for execution.
- [ParserSource](./ParserSource/) Tools and sources used to easly generate ad hoc parser, can be used for recompile purpose. Special thanks: Professor [Mauro Leoncini](https://github.com/leoncini)
- [stack.py](./stack.py) A simple stack data structure implementation used to simplify stack operations
- [main.py](./main.py), [test.sh](./test.sh) testing files

## HOW TO USE
### From CLI
shell:
``` sh
python3 ./main.py "abcd" "a*"
False
python3 ./main.py "aaaa" "a*"
True
```
python:
```python
>>> from Regex import Regex
>>> Regex.match("abcd", "a*")
False
>>> Regex.match("aaaa", "a*")
True
```
### As module
import Regex from [Regex](./Regex.py) class and use either the instance method or the static method match() with the string and the pattern as done in [main.py](./main.py) file
### Full toolchain
- Instantiate a [FSMNotDeterministic](./regexFSM.py) object, passing all the parameters describing the regex, or using [FSMUtils](./regexFSM.py) class and use it to obtain a [FSMDeterministic](./regexFSM.py) using the [subsetConstruction](./regexFSM.py)() method.
- Use [checkRegex](./regexFSM.py)() method of the obtained object for string validation.
- RECOMPILING: Use [ParserSource/Makefile](./ParserSource/Makefile) if you need.

NOTE: you could instantiate directly a FSMDeterministic object in simple cases, but it recomended to 

## WIP
The program achieved the instantiation of a regex object just parsing a string describing it, without having to project the FSM itself.

This is computable via an algorithm that turns the regex into a not deterministic fsm, then using the subset construction to obtain a deterministic fsm, which is also simulable for string validation.

[FSMUtils](./regexFSM.py) contains everything necessary for this process.