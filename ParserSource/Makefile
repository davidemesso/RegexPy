#by M. Leoncini, for teaching purposes only

.PHONY: clean all

all: ../Parser/pparser

../Parser/pparser: pparser.o lexer.o
	g++ -o ../Parser/pparser pparser.o lexer.o

pparser.o: pparser.hpp pparser.cpp tokens.h
	g++ -c pparser.cpp

lexer.o: lexer.cpp tokens.h
	g++ -c lexer.cpp

lexer.cpp: lexer.l
	flex++ -o lexer.cpp lexer.l

pparser.hpp: regex.pg
	python3 first_and_follow.py -o regex.pg.pickle regex.pg
	python3 makeparser.py regex.pg.pickle

clean:
	rm -f *~ *.o pparser lexer.cpp tokens.h pparser.hpp *.pickle
