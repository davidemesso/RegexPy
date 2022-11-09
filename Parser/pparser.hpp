#define EPS 0
#define BASE_VARIABLES 256

const int par = 256;
const int concat = 257;
const int closurepr = 258;
const int closure = 259;
const int unionpr = 260;
const int unio = 261;
const int concatpr = 262;
const int AXIOM = 257;

std::vector<int> prod1{-2};	// par : 'char'
std::vector<int> prod2{40,257,41};	// par : '(' concat ')' 
std::vector<int> prod3{0};	// closurepr : EPS
std::vector<int> prod4{42,258};	// closurepr : '*' closurepr
std::vector<int> prod5{256,258};	// closure : par closurepr
std::vector<int> prod6{0};	// unionpr : EPS
std::vector<int> prod7{124,259,260};	// unionpr : '|' closure unionpr
std::vector<int> prod8{259,260};	// unio : closure unionpr
std::vector<int> prod9{0};	// concatpr : EPS
std::vector<int> prod10{261,262};	// concatpr : unio concatpr
std::vector<int> prod11{261,262};	// concat : unio concatpr
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
	parsing_table[256]={{-2,1}, {40,2}};
	parsing_table[258]={{40,3}, {41,3}, {-2,3}, {124,3}, {-1,3}, {42,4}};
	parsing_table[259]={{40,5}, {-2,5}};
	parsing_table[260]={{40,6}, {41,6}, {-2,6}, {-1,6}, {124,7}};
	parsing_table[261]={{40,8}, {-2,8}};
	parsing_table[262]={{41,9}, {-1,9}, {40,10}, {-2,10}};
	parsing_table[257]={{40,11}, {-2,11}};
};

std::map<int,std::string> display = {
	{1,"par : 'char'"},
	{2,"par : '(' concat ')'"},
	{3,"closurepr : EPS"},
	{4,"closurepr : '*' closurepr"},
	{5,"closure : par closurepr"},
	{6,"unionpr : EPS"},
	{7,"unionpr : '|' closure unionpr"},
	{8,"unio : closure unionpr"},
	{9,"concatpr : EPS"},
	{10,"concatpr : unio concatpr"},
	{11,"concat : unio concatpr"}
};
