#define EPS 0
#define BASE_VARIABLES 256

const int unio = 256;
const int concatpr = 257;
const int closure = 258;
const int unionpr = 259;
const int par = 260;
const int closurepr = 261;
const int concat = 262;
const int AXIOM = 262;

std::vector<int> prod1{256,257};	// concatpr : unio concatpr
std::vector<int> prod2{0};	// concatpr : EPS
std::vector<int> prod3{258,259};	// unio : closure unionpr
std::vector<int> prod4{124,258,259};	// unionpr : '|' closure unionpr
std::vector<int> prod5{0};	// unionpr : EPS
std::vector<int> prod6{260,261};	// closure : par closurepr
std::vector<int> prod7{42,261};	// closurepr : '*' closurepr
std::vector<int> prod8{0};	// closurepr : EPS
std::vector<int> prod9{40,262,41};	// par : '(' concat ')' 
std::vector<int> prod10{-2};	// par : 'char'
std::vector<int> prod11{256,257};	// concat : unio concatpr
std::map<int,std::vector<int>> prods = {
	{1,{prod1}},
	{2,{prod2}},
	{3,{prod3}},
	{4,{prod4}},
	{5,{prod5}},
	{6,{prod6}},
	{7,{prod7}},
	{8,{prod8}},
	{9,{prod9}},
	{10,{prod10}},
	{11,{prod11}}
};
std::map<int,std::map<int,int>> parsing_table;
void set_parsing_table() {
	parsing_table[257]={{40,1}, {-2,1}, {41,2}, {-1,2}};
	parsing_table[256]={{40,3}, {-2,3}};
	parsing_table[259]={{124,4}, {40,5}, {41,5}, {-2,5}, {-1,5}};
	parsing_table[258]={{40,6}, {-2,6}};
	parsing_table[261]={{42,7}, {40,8}, {41,8}, {-2,8}, {124,8}, {-1,8}};
	parsing_table[260]={{40,9}, {-2,10}};
	parsing_table[262]={{40,11}, {-2,11}};
};

std::map<int,std::string> display = {
	{1,"concatpr : unio concatpr"},
	{2,"concatpr : EPS"},
	{3,"unio : closure unionpr"},
	{4,"unionpr : '|' closure unionpr"},
	{5,"unionpr : EPS"},
	{6,"closure : par closurepr"},
	{7,"closurepr : '*' closurepr"},
	{8,"closurepr : EPS"},
	{9,"par : '(' concat ')'"},
	{10,"par : 'char'"},
	{11,"concat : unio concatpr"}
};
