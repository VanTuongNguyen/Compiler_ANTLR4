import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):

    def test_19fa22d3be223238b4783b535b84b5(self):
        """ Test Valid Lowercase Keywords """
        self.assertTrue(TestLexer.test(
            r"""
function procedure
begin end
true false
if then else
for while with do to downto
return break continue
integer string real boolean
array
var of
and then
or else
and         then
or          else
div mod not and or
""",
            "function,procedure,begin,end,true,false,if,then,else,for,while,with,do,to,downto,return,break,continue,integer,string,real,boolean,array,var,of,and,then,or,else,and,then,or,else,div,mod,not,and,or,<EOF>",
            101
        ))
        

    def test_ab5425408fd60ff6091fe96554c236(self):
        """ Test Valid Keywords """
        self.assertTrue(TestLexer.test(
            r"""
FuNctiOn prOceDure
Begin END
True FalSE
IF thEn ELSE
fOR While with DO To downTo
RETURN break COntiNue
integer string REAL BOOLean
ARRAY
VAR Of
anD Then
or eLse
AND             THeN   OR   elSE
dIV mOd NOT and OR
""",

            "FuNctiOn,prOceDure,Begin,END,True,FalSE,IF,thEn,ELSE,fOR,While,with,DO,To,downTo,RETURN,break,COntiNue,integer,string,REAL,BOOLean,ARRAY,VAR,Of,anD,Then,or,eLse,AND,THeN,OR,elSE,dIV,mOd,NOT,and,OR,<EOF>",
            102
        ))
        

    def test_3908976907dd27474c62788e7b7892(self):
        """ Test Specific Characters """
        self.assertTrue(TestLexer.test(
            r"""
+ - * / := <= >= <> = < >
( ) { } [ ] ; , : , ..
""",

            "+,-,*,/,:=,<=,>=,<>,=,<,>,(,),[,],;,,,:,,,..,<EOF>",
            103
        ))
        

    def test_2ec2cd7aa2a31b00838a6fc72b5432(self):
        """ Test Inline Comments """
        self.assertTrue(TestLexer.test(
            r"""
// This is a line comment
""",

            "<EOF>",
            104
        ))
        

    def test_1b490c550ed45a6a13a3ca69635408(self):
        """ Test Block Comments 1 """
        self.assertTrue(TestLexer.test(
            r"""
(* Comment with multiple lines
    Hello comments
*)
""",

            "<EOF>",
            105
        ))
        

    def test_54627d648ccbd07bbf718917b99df4(self):
        """ Test Block Comments 2 """
        self.assertTrue(TestLexer.test(
            r"""
{ This is a block comment }

{
    Comment multiple lines
}
""",

            "<EOF>",
            106
        ))
        

    def test_eb5cd17181bdfe49c821b84208cf96(self):
        """ Test Mix Comments """
        self.assertTrue(TestLexer.test(
            r"""
(* This is a block comment *)

{ This is a block comment }

// This is a line comment

(* Comment with multiple lines
    Hello comments
*)

{
    Comment multiple lines
}

(* nest comments { 
block 
comment
    // inline comment
} 

// inline comment { block 

comment }
*)
""",

            "<EOF>",
            107
        ))
        

    def test_20efeb9e77e099a605e2a10e99c4a1(self):
        """ Test Integer Literal """
        self.assertTrue(TestLexer.test(
            r"""
0 1 2 3 4 123 123456789
""",

            "0,1,2,3,4,123,123456789,<EOF>",
            108
        ))
        

    def test_38f100b0d15ba503b2a362a9642dc7(self):
        """ Test Real Literal """
        self.assertTrue(TestLexer.test(
            r"""
1.2 1. .1 1e2 1.2E-2 1.2e-2 .1E2 9.0 12e8 0.33E-3 128e-42
12.     .05     12.05 1e-5      1.5e-6  0.0005e3   2e21
""",

            "1.2,1.,.1,1e2,1.2E-2,1.2e-2,.1E2,9.0,12e8,0.33E-3,128e-42,12.,.05,12.05,1e-5,1.5e-6,0.0005e3,2e21,<EOF>",
            109
        ))
        

    def test_a7860a7de474f5586c4065ae0c0621(self):
        """ Test String Literal """
        self.assertTrue(TestLexer.test(
            r"""
""      "A"     
"Mulitiple Characters"
""",

            ',A,Mulitiple Characters,<EOF>',
            110
        ))
        

    def test_66eb5d481d39b89e5fadbcf6a4ea22(self):
        """ Test Identifiers """
        self.assertTrue(TestLexer.test(
            r"""
a abc a123 a_ a_bc a_bc123 a_123 a_123bc a_bc_123
_ _abc _123 _abc123 _abc_123 _123_abc
__ ____ ____123____
abc ABC aBC Abc _ABC __ABc __123ABc

h98f394__VWT_b5_VT_YGU87udhf__T_
""",

            "a,abc,a123,a_,a_bc,a_bc123,a_123,a_123bc,a_bc_123,_,_abc,_123,_abc123,_abc_123,_123_abc,__,____,____123____,abc,ABC,aBC,Abc,_ABC,__ABc,__123ABc,h98f394__VWT_b5_VT_YGU87udhf__T_,<EOF>",
            111
        ))
        

    def test_9b0fc035dbdce17d1b0d36c4640fbb(self):
        """ Test Invalid Identifiers """
        self.assertTrue(TestLexer.test(
            r"""
123abc 123_abc 00000123_123abc
""",

            "123,abc,123,_abc,00000123,_123abc,<EOF>",
            112
        ))
        

    def test_805c7f827e194e9fc5251dc94bd062(self):
        """ Test Invalid Comments """
        self.assertTrue(TestLexer.test(
            r"""
// inline comment but
    is multiple lines
( block comment missing *
{ comment without close
(* comment not correct close )
""",

            "is,multiple,lines,(,block,comment,missing,*,{,comment,without,close,(,*,comment,not,correct,close,),<EOF>",
            113
        ))
        

    def test_e3f5ec36163266903d6172edda0187(self):
        """ Test Invalid Real Literal """
        self.assertTrue(TestLexer.test(
            r"""
e-12 e12 . 1e 12e 12.05e .05e ee e01
""",

            "e,-,12,e12,.,1,e,12,e,12.05,e,.05,e,ee,e01,<EOF>",
            114
        ))
        

    def test_f2ac1d0d23639fe5a63919b46200b9(self):
        """ Test Array Declare """
        self.assertTrue(TestLexer.test(
            r"""
array [1 .. 3] of integer
""",

            "array,[,1,..,3,],of,integer,<EOF>",
            115
        ))
        

    def test_4dd433621840d3fb3a5943f1d25057(self):
        """ Test Unclose String without endline """
        self.assertTrue(TestLexer.test(
            r"""  " hello lexer """,

            "Unclosed String:  hello lexer ",
            116
        ))
        

    def test_03d5cacc865b133e88ba6437db191e(self):
        """ Test Unclose String with endline """
        self.assertTrue(TestLexer.test(
            r"""
" abcxyz
""",

            r"""Unclosed String:  abcxyz
""",
            117
        ))
        

    def test_817d5d263735a4facefb154e049f76(self):
        """ Test Escape String """
        self.assertTrue(TestLexer.test(
            r"""
" abc \n xyz "
" abc \\n xyz "
""",

            r''' abc \n xyz , abc \\n xyz ,<EOF>''',
            118
        ))
        

    def test_6178029a86ffd8e9d34e4db7d1d34c(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
" hello lexer \t "     asdf 
""",

            r' hello lexer \t ,asdf,<EOF>',
            119
        ))
        

    def test_0e2e42b499e79aaf4b885f5de62915(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
"Backspace  \b"
""",

            r'Backspace  \b,<EOF>',
            120
        ))
        

    def test_0fac686d5e039fdb57a21d5d8faa43(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
"Formfeed   \f"
""",

            r'Formfeed   \f,<EOF>',
            121
        ))
        

    def test_3c896c9d448d403cde5b8df67e36d3(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
"Return     \r"
""",

            r'''Return     \r,<EOF>''',
            122
        ))
        

    def test_02b8578cc461cbcca947cdec3880c6(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
"Newline    \n"
""",

            r'''Newline    \n,<EOF>''',
            123
        ))
        

    def test_eccd50daea4a962b87daff701503b8(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"Newline
    multiple lines
"           """,

            r'''Unclosed String: Newline
''',
            124
        ))
        

    def test_09c39f4f87c0f620cc4f4c51bf150d(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
"Tab        \t"
""",

            r'Tab        \t,<EOF>',
            125
        ))
        

    def test_f746bd479a21013b3157d717484702(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
"Backslash  \\ "
""",

            r"Backslash  \\ ,<EOF>",
            126
        ))
        

    def test_096fc16b425401e810a8ec33b75d09(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
Illegal: "\a"
""",

            r'''Illegal,:,Illegal Escape In String: \a''',
            127
        ))
        

    def test_e5bf543e7de102ba5893adc94b1dcc(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
" Hi Hi \c \d "
""",

            "Illegal Escape In String:  Hi Hi \c",
            128
        ))
        

    def test_b18a070c10dbcc453dd1078ebbb7ff(self):
        """ Test Illegal Escape """
        self.assertTrue(TestLexer.test(
            r"""
" Hi Hi \m\n\c\s\d\\f "
""",

            "Illegal Escape In String:  Hi Hi \m",
            129
        ))
        

    def test_ec738c4fddfe9b8ea4936450c06c94(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
" asdf ` asdf"
""",

            " asdf ` asdf,<EOF>",
            130
        ))
        

    def test_03beaaf27b34153d6e7fbc7d2f668c(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
" abc ' xyz "
""",

            "Illegal Escape In String:  abc '",
            131
        ))
        

    def test_f3edc6813320ae2498c46a5ed5fcfe(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
" abc \' xyz "
""",

            r" abc \' xyz ,<EOF>",
            132
        ))
        

    def test_227505ae311064b1cbfd82bbc3f249(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
" abc \" xyz " ghi
""",

            r" abc \" xyz ,ghi,<EOF>",
            133
        ))
        

    def test_efceefd3419775ba928a3ebef28d55(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"abc" 123 __123 "abc xyz"
" abc\m "
""",

            "abc,123,__123,abc xyz,Illegal Escape In String:  abc\m",
            134
        ))
        

    def test_12423e3bcb866dc1547efae0fb6cfd(self):
        """ Test Error Token """
        self.assertTrue(TestLexer.test(
            r"""
!== != & ^ % $ # ... \
""",

            "Error Token !",
            135
        ))
        

    def test_929e63ee08fd0f9ff7fc0876157933(self):
        """ Test Error Token """
        self.assertTrue(TestLexer.test(
            r"""
if a != b then
""",

            "if,a,Error Token !",
            136
        ))
        

    def test_f26fc3fedf7ebe38083d1f0d0af316(self):
        """ Test Error Token """
        self.assertTrue(TestLexer.test(
            r"""
a := a & 1
""",

            "a,:=,a,Error Token &",
            137
        ))
        

    def test_bfbd655052b7f54c940afced747142(self):
        """ Test Error Token """
        self.assertTrue(TestLexer.test(
            r"""
xyz
$a = 5
""",

            "xyz,Error Token $",
            138
        ))
        

    def test_fa9c5954d57fb9c9b94462fcec2f0f(self):
        """ Test Error Token """
        self.assertTrue(TestLexer.test(
            r"""
#define for 1
""",

            "Error Token #",
            139
        ))
        

    def test_9c7fef249daff512cc6b1e414e86e5(self):
        """ Test Number leading 0 """
        self.assertTrue(TestLexer.test(
            r"""
1234 0000001234 0000043123
""",

            "1234,0000001234,0000043123,<EOF>",
            140
        ))
        

    def test_6f0910a4c43f03339125b038faaa29(self):
        """ Test Real Leading 0 """
        self.assertTrue(TestLexer.test(
            r"""
00001.1111000000
0e-4
000000001e-40000
""",

            "00001.1111000000,0e-4,000000001e-40000,<EOF>",
            141
        ))
        

    def test_e997357876dd32fb706da21b11bf2c(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"abc - xyz"
"abc \ xyz"
""",

            "abc - xyz,Illegal Escape In String: abc \ ",
            142
        ))
        

    def test_e2f731f0f9fdadc87640a6f379d3c0(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"abc - xyz"
"abc \yyz"
""",

            "abc - xyz,Illegal Escape In String: abc \y",
            143
        ))
        

    def test_334601d1f61dfbb24bcd2a659c0986(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"abc \\ xyz"
""",

            r"abc \\ xyz,<EOF>",
            144
        ))
        

    def test_e54b34aa83c8c1e3d03badd583b7f9(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"\\"
""",

            r'''\\,<EOF>''',
            145
        ))
        

    def test_38187f6336aef4dea27740c728cee1(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"\\ "
""",

            r"\\ ,<EOF>",
            146
        ))
        

    def test_142305af4c9d488c9a8d773c4ed086(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"\"
""",

            r"""Unclosed String: \"
""",
            147
        ))
        

    def test_43c4495be79b79863df29caf42d2d3(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
"\""
""",

            r"""\",<EOF>""",
            148
        ))
        

    def test_869ed6e6596a85c60858e36be900a6(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
s = "string           
"a = 4
g = 9
""",

            r'''s,=,Unclosed String: string           
''',
            149
        ))
        

    def test_c62dddd5de21656fa70da0818fedd2(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
var a, b, c: real;

var x, y, z: Boolean;
    g, h, y: Integer;

function nty(): Real;
var x, y, z: Integer;
begin
    readLine();
    // This is readLine()

    fs := readStdin();
    
    with i: integer; do begin
        for i := 4 downto -5 do h := 6;
        if i > 6 then return 0;
    end

    return 1;
end

var q, w : integer;

var a: string;
begin 
    (*
        =======================================
        Comment here
        =======================================
    *)
end
""",

            r"var,a,,,b,,,c,:,real,;,var,x,,,y,,,z,:,Boolean,;,g,,,h,,,y,:,Integer,;,function,nty,(,),:,Real,;,var,x,,,y,,,z,:,Integer,;,begin,readLine,(,),;,fs,:=,readStdin,(,),;,with,i,:,integer,;,do,begin,for,i,:=,4,downto,-,5,do,h,:=,6,;,if,i,>,6,then,return,0,;,end,return,1,;,end,var,q,,,w,:,integer,;,var,a,:,string,;,begin,end,<EOF>",
            150
        ))
        

    def test_1bbeddbc8c4e4828e7b2988eee0573(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    while i do begin
        ok()
    end
end
""",

            r"procedure,foo,(,),;,begin,while,i,do,begin,ok,(,),end,end,<EOF>",
            151
        ))
        

    def test_14383d8ec6a48db6079ae7594e491e(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
s = "abc""",

            r"s,=,Unclosed String: abc",
            152
        ))
        

    def test_351c5af958bd792191ac8d4b4a0e32(self):
        """ Test Error String """
        self.assertTrue(TestLexer.test(
            r"""
s = "abc                   ;
a = "xyz"
""",

            r"""s,=,Unclosed String: abc                   ;
""",
            153
        ))
        

    def test_f7cc101106d5578e8d3da3ef1ab426(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    while 1<2<3<4<5 do ok();
end
""",

            r"procedure,foo,(,),;,begin,while,1,<,2,<,3,<,4,<,5,do,ok,(,),;,end,<EOF>",
            154
        ))
        

    def test_f769e60909963598d72b683902d351(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    with a: string do ok();
end
""",

            r"procedure,foo,(,),;,begin,with,a,:,string,do,ok,(,),;,end,<EOF>",
            155
        ))
        

    def test_4a0eda4f416dbaf287b3fcc5401b69(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    with a,b,c,d:string; f:integer do ok();
end
""",

            r"procedure,foo,(,),;,begin,with,a,,,b,,,c,,,d,:,string,;,f,:,integer,do,ok,(,),;,end,<EOF>",
            156
        ))
        

    def test_9cdb9453b7378cf76f924410e7bdfb(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
var a: real;
begin
    for i := 1 to 10 do begin
        for j := i downto 1 do
            if (i + j) mod 2 = 1 then continue break;
    end
end
""",

            r"procedure,foo,(,),;,var,a,:,real,;,begin,for,i,:=,1,to,10,do,begin,for,j,:=,i,downto,1,do,if,(,i,+,j,),mod,2,=,1,then,continue,break,;,end,end,<EOF>",
            157
        ))
        

    def test_d96c33cc0c016eaef59b19db2668ad(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    a := a[d < y(5 > 3) + 3 * n(12)] := 5[3] := 3[2] := b;
end
""",

            r"procedure,foo,(,),;,begin,a,:=,a,[,d,<,y,(,5,>,3,),+,3,*,n,(,12,),],:=,5,[,3,],:=,3,[,2,],:=,b,;,end,<EOF>",
            158
        ))
        

    def test_93e1567ba293acfe7b155d19091f75(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    s = "asdfghjklwertyuio  xcvbnm,dfghjkl;567"
    t = " dfghjk\n\t\rsdfghjkl\bsdfghjklfgh    "
    y = "dfghjkl 
    
    
    ";
end
""",

            r"""procedure,foo,(,),;,begin,s,=,asdfghjklwertyuio  xcvbnm,dfghjkl;567,t,=, dfghjk\n\t\rsdfghjkl\bsdfghjklfgh    ,y,=,Unclosed String: dfghjkl 
""",
            159
        ))
        

    def test_4fc940d698045cc1110e887bc88803(self):
        """ Test Complex Function """
        self.assertTrue(TestLexer.test(
            r"""
procedure foo();
begin
    s = "asdfghjklwertyuio  xcvbnm,dfghjkl;567"
    t = " dfghjk\n\t\rsdfghjkl\bsdfghjklfgh    "
    y = "dfghjkl 
    
    
    ";

    begin end
    ok();
    break;
end
""",

            r"""procedure,foo,(,),;,begin,s,=,asdfghjklwertyuio  xcvbnm,dfghjkl;567,t,=, dfghjk\n\t\rsdfghjkl\bsdfghjklfgh    ,y,=,Unclosed String: dfghjkl 
""",
            160
        ))
        

    def test_99f500a4e02be1290affce1107120c(self):
        """ Test Real Number """
        self.assertTrue(TestLexer.test(
            r"""
12.
12.e05
12.e-05
12.05e05
12.05e-05
12.05
.05
.05e05
.05e-05
""",

            r"12.,12.e05,12.e-05,12.05e05,12.05e-05,12.05,.05,.05e05,.05e-05,<EOF>",
            161
        ))
        

    def test_8319b433cbf5b4579bb606fae9ff0b(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            162
        ))
        

    def test_ebd771602a6562c13e264acdb419ab(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            163
        ))
        

    def test_07fb59d89588322ac7ebaf857b438e(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            164
        ))
        

    def test_bcd459046443c1f82d0a96a449b92d(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            165
        ))
        

    def test_e44b21f9ee8b1ee3d65a91ffd8be1b(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            166
        ))
        

    def test_2cb61de8d1f7ddf27de9d686d68a8a(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            167
        ))
        

    def test_3aa06a998305e226302889fb24f5d6(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            168
        ))
        

    def test_dbcd228507be55555d007a3cb3467d(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            169
        ))
        

    def test_650c6ee0c398344f01d88353c4d09f(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            170
        ))
        

    def test_96b62a0499841654384179c5a34bba(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            171
        ))
        

    def test_aaebea13b1f3ef2319abf2a126c88d(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            172
        ))
        

    def test_cc798143bb02dbae1125ead3abb9b9(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            173
        ))
        

    def test_2d4009c38c42aeca090532862ba7f9(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            174
        ))
        

    def test_8b5b2797749d171a78a9f48868f537(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            175
        ))
        

    def test_5a1f82003cd929789d728367827f76(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            176
        ))
        

    def test_596253dacea87b3fc6e9835cabe163(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            177
        ))
        

    def test_32188febacbdfeef19659d8647acb3(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            178
        ))
        

    def test_d9c19090d4ff7a0679232ebc1c4fd4(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            179
        ))
        

    def test_ea23705d343b069d896cb439cad74b(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            180
        ))
        

    def test_3c9d187a3f5bd6757d8f0b6a611c0f(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            181
        ))
        

    def test_39a4f9349deb4b34d639ba594fa19e(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            182
        ))
        

    def test_254d1d0ae3fb457903ea5f800cf835(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            183
        ))
        

    def test_114a635b56a747d868f42505781839(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            184
        ))
        

    def test_09de9e57476d5c7460960bc6ac9365(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            185
        ))
        

    def test_34085c78d1d580e3ded85b7bf8f6c5(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            186
        ))
        

    def test_417a63b4f65da41df2c5d01cedeeed(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            187
        ))
        

    def test_6be788654218f57e46c7d554d8ba78(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            188
        ))
        

    def test_99fc46d374bb83a1386bb9dd21ba44(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            189
        ))
        

    def test_34b600545599c7422addeee785d009(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            190
        ))
        

    def test_44efba40c2f614150698bbd6531b33(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            191
        ))
        

    def test_311efa90ccf557133727c11a9f3506(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            192
        ))
        

    def test_6a5538a9dc95998517606c9abb8295(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            193
        ))
        

    def test_a13e8a5ac11733a2d34b5e0820058e(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            194
        ))
        

    def test_a4bd41531a44cc0c6409202dc93b35(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            195
        ))
        

    def test_b62552d5d78899304c2501f255474c(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            196
        ))
        

    def test_62202c9a18fc5ee1eaa0dc14e9dfde(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            197
        ))
        

    def test_559972aa18e4b7d992086823c5e426(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            198
        ))
        

    def test_46a0e3bf9037b655fcffbfaa38524d(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            199
        ))
        

    def test_09b1ee16b315dde1130bd3e7b641eb(self):
        """ Test  """
        self.assertTrue(TestLexer.test(
            r"""
""",

            "<EOF>",
            200
        ))
        
