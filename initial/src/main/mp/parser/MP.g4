/*
	Name: 			Nguyen Van Tuong
	Student ID: 	1614028
 */
grammar MP;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}


program:    many_declarations;
many_declarations:
    declarations many_declarations | declarations;
declarations:
    var_decl
    |func_decl
    |proc_decl;


var_decl:
    VAR list_decl;
list_decl:
    decl list_decl | decl;
decl:
    list_id COLON types SEMI;
list_id:
    ID COMMA list_id | ID;

func_decl:
    FUNCTION ID LB param_list RB COLON types SEMI var_decl compound_statement
    |FUNCTION ID LB param_list RB COLON types SEMI compound_statement;

param_list:
    not_null_param_list
    | ;
not_null_param_list:
    param_decl SEMI not_null_param_list | param_decl;
param_decl:
    list_id COLON types;

proc_decl:
    PROCEDURE ID LB param_list RB SEMI var_decl compound_statement
    |PROCEDURE ID LB param_list RB SEMI compound_statement;



fragment A: ('a'|'A');
fragment B: ('b'|'B');
fragment C: ('c'|'C');
fragment D: ('d'|'D');
fragment E: ('e'|'E');
fragment F: ('f'|'F');
fragment G: ('g'|'G');
fragment H: ('h'|'H');
fragment I: ('i'|'I');
fragment J: ('j'|'J');
fragment K: ('k'|'K');
fragment L: ('l'|'L');
fragment M: ('m'|'M');
fragment N: ('n'|'N');
fragment O: ('o'|'O');
fragment P: ('p'|'P');
fragment Q: ('q'|'Q');
fragment R: ('r'|'R');
fragment S: ('s'|'S');
fragment T: ('t'|'T');
fragment U: ('u'|'U');
fragment V: ('v'|'V');
fragment W: ('w'|'W');
fragment X: ('x'|'X');
fragment Y: ('y'|'Y');
fragment Z: ('z'|'Z');
fragment LETTER: A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z;
fragment DIGIT: [0-9];


BREAK:
    B R E A K;
CONTINUE:
    C O N T I N U E;
FOR:
    F O R;
TO:
    T O;
DOWNTO:
    D O W N T O;
DO:
    D O;
IF:
    I F;
THEN:
    T H E N;
ELSE:
    E L S E;
RETURN:
    R E T U R N;
WHILE:
    W H I L E;
BEGIN:
    B E G I N;
END:
    E N D;
FUNCTION:
    F U N C T I O N;
PROCEDURE:
    P R O C E D U R E;
VAR:
    V A R;
ARRAY:
    A R R A Y;
OF:
    O F;
REAL:
    R E A L;
BOOLEAN:
    B O O L E A N;
INTEGER:
    I N T E G E R;
STRING:
    S T R I N G;
WITH:
    W I T H;
ASSIGN: ':=';
ADD:    '+';
SUB:    '-';
MUL:    '*';
DIV:    '/';

NOT:    N O T;
MOD:    M O D;
OR:     O R;
AND:    A N D;
// ANDTHEN: A N D ' ' T H E N;
// ORELSE: O R ' ' E L S E;

NEQ:    '<>';
EQ:     '=';
LT:     '<';
GT:     '>';
LTE:    '<=';
GTE:    '>=';
IDIV:   D I V;



LSB:    '[';
RSB:    ']';
COLON:  ':';
LB:     '(';
RB:     ')';
SEMI:   ';';
DDOT:   '..';
COMMA:  ',';

INTLIT:
    DIGIT+;

fragment EXPONENT:
    [Ee] '-'? DIGIT+;

FLOATLIT:
    DIGIT+ ('.'DIGIT*)? EXPONENT?
    | '.' DIGIT+ EXPONENT?;

BOOLLIT:  
    T R U E | F A L S E;

ID:     
    (LETTER|'_')(LETTER|'_'|DIGIT)*;
fragment BSP: 
    '\\b';
    
fragment FF: 
    '\\f';
    
fragment CR: 
    '\\r';
    
fragment NEWLINE: 
    '\\n';
    
fragment TAB: 
    '\\t';
    
fragment SQUOTE: 
    '\\\'';
    
fragment DQUOTE: 
    '\\"';
    
fragment BSL: 
    '\\\\';

fragment LEGAL_ESCAPE:
    BSP
    | FF
    | CR
    | NEWLINE
    | TAB
    | SQUOTE
    | DQUOTE
    | BSL
    ;



UNCLOSE_STRING: '"'(~[\b\f\r\n\t'"\\]|LEGAL_ESCAPE)*
    {raise UncloseString(self.text[1:])};
ILLEGAL_ESCAPE: '"'(~[\b\f\r\n\t'"\\]|LEGAL_ESCAPE)*[\b\f\r\n\t'\\]
    {raise IllegalEscape(self.text[1:])};
STRINGLIT:
    UNCLOSE_STRING'"'
    {self.text = self.text[1:-1]};



types:
    primitive_types
    | compound_types;

primitive_types:
    BOOLEAN | INTEGER | REAL | STRING;

compound_types:
    array_types;

array_types:
    ARRAY LSB expression DDOT expression RSB OF primitive_types;

operand:
    INTLIT
    |FLOATLIT
    |BOOLLIT
    |STRINGLIT
    |ID
   // |element_arr
    |func_call;

expression:
    expression AND THEN expression_1
    |expression OR ELSE expression_1
    |expression_1;
expression_1:
    expression_2 EQ expression_2
    |expression_2 NEQ expression_2
    |expression_2 LT expression_2
    |expression_2 GT expression_2
    |expression_2 GTE expression_2
    |expression_2 LTE expression_2
    |expression_2;
expression_2:
    expression_2 ADD expression_3
    |expression_2 SUB expression_3
    |expression_2 OR expression_3
    |expression_3;
expression_3:
    expression_3 DIV expression_4
    |expression_3 MUL expression_4
    |expression_3 IDIV expression_4
    |expression_3 MOD expression_4
    |expression_3 AND expression_4
    |expression_4;
expression_4:
    SUB expression_4
    |NOT expression_4
    |expression_5;
expression_5:
    expression_5 LSB expression RSB
    |expression_6;
expression_6:
    LB expression RB
    | operand;

element_arr:
    expression_5 LSB expression RSB;

func_call:
    ID LB exp_list RB;
exp_list:
    not_null_exp_list | ;
not_null_exp_list:
    expression COMMA not_null_exp_list | expression;

statement:
    assignment_statement
    | if_statement
    | while_statement
    | for_statement
    | break_statement
    | continue_statement
    | return_statement
    | compound_statement
    | with_statement
    | call_statement;

assignment_statement:
    (ID | element_arr) ASSIGN assignment_statement
    |(ID | element_arr) ASSIGN expression SEMI;

if_statement:
    IF expression THEN statement ELSE statement
    |IF expression THEN statement;

while_statement:
    WHILE expression DO statement;

for_statement:
    FOR ID ASSIGN expression (TO | DOWNTO) expression DO statement;

break_statement:
    BREAK SEMI;

continue_statement:
    CONTINUE SEMI;

return_statement:
    RETURN (expression| ) SEMI;

compound_statement:
    BEGIN list_statement END;
list_statement:
    not_null_list_statement | ;
not_null_list_statement:
    statement not_null_list_statement | statement;

with_statement:
    WITH list_decl DO statement;

call_statement:
    func_call SEMI;

COMMENT1:   '(*'.*?'*)'  -> skip;
COMMENT2:   '{'.*?'}' -> skip;
COMMENT3:    '//'~[\n]* -> skip;
WS:         [ \r\n\t]+ -> skip;


ERROR_CHAR: .
    {raise ErrorToken(self.text)};