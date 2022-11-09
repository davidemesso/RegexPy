#include <iostream>
#include <FlexLexer.h>
#include <string>
#include <vector>
#include <cstring>
#include <exception>
#include <map>
#include "tokens.h"
#include "symbtbl.h"
#include "pparser.hpp"
using namespace std;

extern std::map<int,Token*> symbtbl;
extern int symbtblptr;

bool isterm(int v) {
    return v<BASE_VARIABLES;
}

bool iseps(int v) {
    return v==EPS;
}

FlexLexer* lexer;
int currenttok;

bool nt_N(int N, bool debug) {
  std::map<int,int> production = parsing_table[N];
  int prodnum;
  prodnum = production[currenttok];
  if(prodnum == 0) {
    std::cerr << "ERRORE: nessuna produzione specificata per la coppia (" << N << "," << currenttok << ")\n";
    std::terminate();
  }
  std::vector<int> prod = prods[prodnum];
  for(std::vector<int>::iterator t=prod.begin(); t!=prod.end(); t++) {
    if (debug) {
      std::cout << "nonterm N:" << N << "; t->" << *t << "; token->" << currenttok << endl;
    }
    if (iseps(*t)) {
      break;
    }
    if (isterm(*t) and currenttok==*t) {
      currenttok = lexer->yylex();
      cout << *t << endl;
    } else if (not isterm(*t) && nt_N(*t,debug)) {
      if (debug) {
	      cout << "Resuming production:" << N << "," << prodnum << endl;
      }
    } else {
      if (debug) {
      	cout << "Failed production:" << N << "," << prodnum << endl;
      }
      return false;
    }
  }
  std::cout << display[prodnum] << endl;
  return true;
}

int main(int argc, char *argv[])
{
  bool debug = false;
  if (argc>1) {
    if (strcmp(argv[1],"-d")==0 or strcmp(argv[1],"--debug")==0) {
      debug = true;
    }
  }
  // Start parsing
  std::cout << "Starting...\n";;
  lexer = new yyFlexLexer;
  currenttok = lexer->yylex();
  set_parsing_table();
  if (nt_N(AXIOM,debug) and currenttok == tok_eof) std::cout << "Accept\n";
  else  std::cout << "Reject\n";

  return 0;
}


