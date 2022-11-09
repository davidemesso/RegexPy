%{
#include <stdexcept>
#include <map>
#include <cstring>
#include <string>
#include "tokens.h"
#include "symbtbl.h"

// Forward declaration
TokenType check_ide(std::string tok);
void illegal(char c);

// Definitions used by the parser
std::map<const int,Token*> symbtbl;
int symbtblptr;

// Local only variables
Token *t;
int count = 0;

%}

char     [a-zA-Z]
%option noyywrap

%%
[ \t\n]   { /* Ignoriamo i separatori */ }
{char}    { t = new Token;
            t->toktype=tok_char;
            t->ch=yytext[0];
            symbtblptr=++count;
            symbtbl[symbtblptr]=t;
	          return tok_char; }
"*"       { return int('*'); }
"|"       { return int('|'); }
"("       { return int('('); }
")"       { return int(')'); }
<<EOF>>   { return tok_eof; }
.         { illegal(yytext[0]); }

%%

void illegal(char c) {
   throw std::invalid_argument( "Trovato un carattere illegale" );
}
