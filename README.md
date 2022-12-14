# RegexPy
A didactic implementation of regex validation using FSM in python with backend parsing in C++

## Content
- [regexPy](./regexpy/) Main package
  - [regex.py](./regexpy/Regex.py) Module containing the interface for the final user. 
  - [fsm.py](./regexpy/fsm.py) The core module, handling FSMs creation and simulation, actually executing the regex matching.
  - [utils](./regexpy/utils/) Package
    - [stack.py](./regexpy/utils/stack.py) A simple stack data structure implementation used to simplify stack manipulation operations.
    - [fsmutils.py](./regexpy/utils/fsmutils.py) The module containing usefull functions for manipulating FSMs in order to achieve a Regex.
  - [tests](./regexpy/tests/) Package containing unit tests. 
- [Parser](./Parser/) The parser implementation which is used to obtain a polish notation stack based representation of the regex used for FSM generation, this folder only contains files used for execution.
- [ParserSource](./ParserSource/) Tools and sources used to easly generate ad hoc parser, can be used for recompile purpose. Special thanks: Professor [Mauro Leoncini](https://github.com/leoncini)
- [main.py](./main.py), [timeTest.py](./timeTest.py) Testing files.
- [tests.py](./tests.py) Script for launching all tests.
## HOW TO USE
### From CLI
shell:
``` sh
python3 ./main.py "abcd" "a*"
False
python3 ./main.py "aaaa" "a*"
True
```
python command line:
```python
>>> from regexpy.regex import Regex
>>> Regex.match("abcd", "a*")
False
>>> Regex.match("aaaa", "a*")
True
```
### As module
import Regex from [regex](./regexpy/regex.py) class and use either the instance method validate() or the static method match() with the string and the pattern as done in [main.py](./main.py) file
### Full toolchain
- Instantiate a [FSMNotDeterministic](./regexpy/fsm.py) object, passing all the parameters describing the regex, or using [FSMUtils](./regexpy/fsm.py) class and use it to obtain a [FSMDeterministic](./regexpy/fsm.py) using the [subsetConstruction](./regexpy/fsm.py)() method.
- Use [checkRegex](./regexpy/fsm.py)() method of the obtained object for string validation.
- RECOMPILING: Use [ParserSource/Makefile](./ParserSource/Makefile) if you need.

NOTE: you could instantiate directly a FSMDeterministic object in simple cases, but it recomended to 

## New features
[regex](./regexpy/regex.py) class now implements:
- [matchAny](./regexpy/regex.py)() "One of" matching
- [matchAll](./regexpy/regex.py)() "All of" matching
Allowing for multiple regex to be evaluated at once.


## Conclusion
The program achieved the instantiation of a regex object just parsing a string describing it, without having to project the FSM itself.

This is computable via an algorithm that turns the regex into a not deterministic fsm, then using the subset construction to obtain a deterministic fsm, which is also simulable for string validation.

[FSMUtils](./regexpy/utils/fsmutils.py) contains every function necessary for this process.