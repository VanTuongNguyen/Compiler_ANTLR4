import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
    
    # test identifier
    def test_identifier_1(self):
        """test identifiers"""
        code = "abc"
        expect = "abc,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,101))
    
    def test_identifier_2(self):
        """test identifiers"""
        code = "aB123"
        expect = "aB123,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,102))

    def test_identifier_3(self):
        """test identifiers"""
        code = "___"
        expect = "___,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,103))

    def test_identifier_4(self):
        """test identifiers"""
        code = "12ab"
        expect = "12,ab,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,104))

    def test_identifier_5(self):
        """test identifiers"""
        code = "X_.l"
        expect = "X_,Error Token ."
        self.assertTrue(TestLexer.test(code,expect,105))


    # test keyword
    def test_keyword_1(self):
        """test keyword"""
        code = "break continue for to downto do if then else return while begin end function procedure var true false array of real boolean integer string not and or div mod with"
        expect = "break,continue,for,to,downto,do,if,then,else,return,while,begin,end,function,procedure,var,true,false,array,of,real,boolean,integer,string,not,and,or,div,mod,with,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,106))  

    def test_keyword_2(self):
        """test keyword"""
        code = "and anD aNd aND And AnD ANd AND"
        expect = "and,anD,aNd,aND,And,AnD,ANd,AND,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,107))  

    def test_keyword_3(self):
        """test keyword"""
        code = "BEGIN"
        expect = "BEGIN,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,108))  

    def test_keyword_4(self):
        """test keyword"""
        code = "Begi12abc"
        expect = "Begi12abc,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,109))  

    def test_keyword_5(self):
        """test keyword"""
        code = "withdo"
        expect = "withdo,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,110))  


    # test operator
    def test_operator_1(self):
        """test operator"""
        code = "-ab"
        expect = "-,ab,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,111))  

    def test_operator_2(self):
        """test operator"""
        code = "ab-12"
        expect = "ab,-,12,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,112))  

    def test_operator_3(self):
        """test operator"""
        code = "a+-*/b"
        expect = "a,+,-,*,/,b,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,113))  

    def test_operator_4(self):
        """test operator"""
        code = "12divab"
        expect = "12,divab,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,114))  

    def test_operator_5(self):
        """test operator"""
        code = "12div15"
        expect = "12,div15,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,115))  


    # test separator
    def test_separator_1(self):
        """test separator"""
        code = "ab(_12_)"
        expect = "ab,(,_12_,),<EOF>"
        self.assertTrue(TestLexer.test(code,expect,116))  

    def test_separator_2(self):
        """test separator"""
        code = "a[12];"
        expect = "a,[,12,],;,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,117))  

    def test_separator_3(self):
        """test separator"""
        code = "a[1 .. 9]"
        expect = "a,[,1,..,9,],<EOF>"
        self.assertTrue(TestLexer.test(code,expect,118))  

    def test_separator_4(self):
        """test separator"""
        code = "a,b"
        expect = "a,,,b,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,119))  

    def test_separator_5(self):
        """test separator"""
        code = "a:b"
        expect = "a,:,b,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,120))  



    # test literal
    # int literal
    def test_literal_int_1(self):
        """test literal int"""
        code = "123456"
        expect = "123456,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,121))  

    def test_literal_int_2(self):
        """test literal int"""
        code = "1-2"
        expect = "1,-,2,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,122))  

    def test_literal_int_3(self):
        """test literal int"""
        code = "+152"
        expect = "+,152,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,123))  

    def test_literal_int_4(self):
        """test literal int"""
        code = "0123"
        expect = "0123,<EOF>" # warnnig
        self.assertTrue(TestLexer.test(code,expect,124))  

    def test_literal_int_5(self):
        """test literal int"""
        code = "-123"
        expect = "-,123,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,125))  


    # floating point
    def test_literal_float_1(self):
        """test literal float"""
        code = "1.2"
        expect = "1.2,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,126))  

    def test_literal_float_2(self):
        """test literal float"""
        code = "-1.2"
        expect = "-,1.2,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,127))  

    def test_literal_float_3(self):
        """test literal float"""
        code = ".15"
        expect = ".15,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,128))  

    def test_literal_float_4(self):
        """test literal float"""
        code = "-12."
        expect = "-,12.,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,129))  

    def test_literal_float_5(self):
        """test literal float"""
        code = "1e2"
        expect = "1e2,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,130))  

    def test_literal_float_6(self):
        """test literal float"""
        code = "1.2E-2"
        expect = "1.2E-2,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,131))  

    def test_literal_float_7(self):
        """test literal float"""
        code = ".1e2"
        expect = ".1e2,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,132))  

    def test_literal_float_8(self):
        """test literal float"""
        code = "9.0"
        expect = "9.0,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,133))  

    def test_literal_float_9(self):
        """test literal float"""
        code = "123e-456"
        expect = "123e-456,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,134))  

    def test_literal_float_10(self):
        """test literal float"""
        code = "1.e123"
        expect = "1.e123,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,135))  


    # string lit
    def test_literal_string_1(self):
        """test literal string"""
        code = '"hello"'
        expect = "hello,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,136))  

    def test_literal_string_2(self):
        """test literal string"""
        code = '"begin 12 hello"'
        expect = "begin 12 hello,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,137))  

    def test_literal_string_3(self):
        """test literal string"""
        code = '"|<>-=+!"'
        expect = "|<>-=+!,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,138))  

    def test_literal_string_4(self):
        """test literal string"""
        code = """ "abc \\n \\t \\' def" """
        expect = "abc \\n \\t \\' def,<EOF>"
        self.assertTrue(TestLexer.test(code,expect,139))  

    def test_literal_string_5(self):
        """test literal string"""
        code = '""'
        expect = ",<EOF>"
        self.assertTrue(TestLexer.test(code,expect,140))  


    # test error token
    def test_error_token_1(self):
        """test error token"""
        code = "a.b"
        expect = "a,Error Token ."
        self.assertTrue(TestLexer.test(code, expect, 141))

    def test_error_token_2(self):
        """test error token"""
        code = "a|b"
        expect = "a,Error Token |"
        self.assertTrue(TestLexer.test(code, expect, 142))

    def test_error_token_3(self):
        """test error token"""
        code = "@"
        expect = "Error Token @"
        self.assertTrue(TestLexer.test(code, expect, 143))

    def test_error_token_4(self):
        """test error token"""
        code = "#"
        expect = "Error Token #"
        self.assertTrue(TestLexer.test(code, expect, 144))

    def test_error_token_5(self):
        """test error token"""
        code = "$"
        expect = "Error Token $"
        self.assertTrue(TestLexer.test(code, expect, 145))


    # test unclose string
    def test_unclosed_string_1(self):
        """test unclosed string"""
        code = '"hello world'
        expect = "Unclosed String: hello world"
        self.assertTrue(TestLexer.test(code,expect,146))  

    def test_unclosed_string_2(self):
        """test unclosed string"""
        code = '"'
        expect = "Unclosed String: "
        self.assertTrue(TestLexer.test(code,expect,147))  

    def test_unclosed_string_3(self):
        """test unclosed string"""
        code = '"hello" + "world'
        expect = "hello,+,Unclosed String: world"
        self.assertTrue(TestLexer.test(code,expect,148))  

    def test_unclosed_string_4(self):
        """test unclosed string"""
        code = '"""""""'
        expect = ",,,Unclosed String: "
        self.assertTrue(TestLexer.test(code,expect,149))  

    def test_unclosed_string_5(self):
        """test unclosed string"""
        code = 'ab + "hello\\"'
        expect = "ab,+,Unclosed String: hello\\\""
        self.assertTrue(TestLexer.test(code,expect,150))  

    def test_unclosed_string_6(self):
        """test illegal escape"""
        code = '"hello \n world"'
        expect = 'Unclosed String: hello '
        self.assertTrue(TestLexer.test(code, expect, 151))

    # test illegal escape
    def test_illegal_escape_1(self):
        """test illegal escape"""
        code = '"hello \' world"'
        expect = 'Illegal Escape In String: hello \''
        self.assertTrue(TestLexer.test(code, expect, 152))

    def test_illegal_escape_2(self):
        """test illegal escape"""
        code = '"hello" + "world \' hello'
        expect = 'hello,+,Illegal Escape In String: world \''
        self.assertTrue(TestLexer.test(code, expect, 153))

    def test_illegal_escape_3(self):
        """test illegal escape"""
        code = '"hello \\ world"'
        expect = 'Illegal Escape In String: hello \\'
        self.assertTrue(TestLexer.test(code, expect, 154))

    def test_illegal_escape_4(self):
        """test illegal escape"""
        code = '"it\\\'s me. \t and"'
        expect = 'Illegal Escape In String: it\\\'s me. \t'
        self.assertTrue(TestLexer.test(code, expect, 155))

    def test_illegal_escape_5(self):
        """test illegal escape"""
        code = '"abc \\" \\t \\n \\b \\\\ \\f \\r \\\' \\ ace"'
        expect = 'Illegal Escape In String: abc \\" \\t \\n \\b \\\\ \\f \\r \\\' \\'
        self.assertTrue(TestLexer.test(code, expect, 156))

    def test_illegal_escape_6(self):
        """test illegal escape"""
        code = '"hello \\x world"'
        expect = 'Illegal Escape In String: hello \\'
        self.assertTrue(TestLexer.test(code, expect, 157))

    def test_illegal_escape_7(self):
        """test illegal escape"""
        code = '"hello \\n world"'
        expect = 'hello \\n world,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 158))

    def test_illegal_escape_8(self):
        """test illegal escape"""
        code = '"hello \\r world"'
        expect = 'hello \\r world,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 159))


    def test_all_1(self):
        """test all"""
        code = 'a[f(1)] := 2;'
        expect = 'a,[,f,(,1,),],:=,2,;,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 160))

    def test_all_2(self):
        """test all"""
        code = 'var a,b:array[1 .. 2] of real;'
        expect = 'var,a,,,b,:,array,[,1,..,2,],of,real,;,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 161))

    def test_all_3(self):
        """test all"""
        code = '"hello \n world"'
        expect = 'Unclosed String: hello '
        self.assertTrue(TestLexer.test(code, expect, 162))

    def test_all_4(self):
        """test all"""
        code = '"hello \t world"'
        expect = 'Illegal Escape In String: hello \t'
        self.assertTrue(TestLexer.test(code, expect, 163))

    def test_all_5(self):
        """test all"""
        code = '"hello \r world"'
        expect = 'Unclosed String: hello '
        self.assertTrue(TestLexer.test(code, expect, 164))

    def test_all_6(self):
        """test all"""
        code = '"hello\b world"'
        expect = 'Illegal Escape In String: hello\b'
        self.assertTrue(TestLexer.test(code, expect, 165))

    def test_all_7(self):
        """test all"""
        code = '1.2.3.4.5'
        expect = '1.2,.3,.4,.5,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 166))

    def test_all_8(self):
        """test all"""
        code = '1..2'
        expect = '1.,.2,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 167))

    def test_all_9(self):
        """test all"""
        code = '+12.e+12'
        expect = '+,12.,e,+,12,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 168))

    def test_all_10(self):
        """test all"""
        code = '1 and then 2'
        expect = '1,and,then,2,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 169))

    def test_all_11(self):
        """test all"""
        code = '1 or else 2'
        expect = '1,or,else,2,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 170))

    def test_all_12(self):
        """test all"""
        code = 'a<>b >c <= d =>e'
        expect = 'a,<>,b,>,c,<=,d,=,>,e,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 171))

    def test_all_13(self):
        """test all"""
        code = '1.e12'
        expect = '1.e12,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 172))

    def test_all_14(self):
        """test all"""
        code = 'e+12'
        expect = 'e,+,12,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 173))

    def test_all_15(self):
        """test all"""
        code = '.e+1'
        expect = 'Error Token .'
        self.assertTrue(TestLexer.test(code, expect, 174))

    def test_all_16(self):
        """test all"""
        code = '__'
        expect = '__,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 175))

    def test_all_17(self):
        """test all"""
        code = '12a12'
        expect = '12,a12,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 176))

    def test_all_18(self):
        """test all"""
        code = '"ab\tab"'
        expect = 'Illegal Escape In String: ab\t'
        self.assertTrue(TestLexer.test(code, expect, 177))

    def test_all_19(self):
        """test all"""
        code = 'ab\hab'
        expect = 'ab,Error Token \\'
        self.assertTrue(TestLexer.test(code, expect, 178))

    def test_all_20(self):
        """test all"""
        code = '"ab\hab"'
        expect = 'Illegal Escape In String: ab\\'
        self.assertTrue(TestLexer.test(code, expect, 179))

    def test_all_21(self):
        """test all"""
        code = '"ab"cd"ef"'
        expect = 'ab,cd,ef,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 180))

    def test_all_22(self):
        """test all"""
        code = "\"\\n\\f\\\n"
        expect = 'Illegal Escape In String: \\n\\f\\'
        self.assertTrue(TestLexer.test(code, expect, 181))

    def test_all_23(self):
        """test all"""
        code = '"<EOF>"'
        expect = '<EOF>,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 182))

    def test_all_24(self):
        """test all"""
        code = 'a[1 ..2]'
        expect = 'a,[,1,..,2,],<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 183))

    def test_all_25(self):
        """test all"""
        code = '<EOF>'
        expect = '<,EOF,>,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 184))

    def test_all_26(self):
        """test all"""
        code = 's:=""'
        expect = 's,:=,,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 185))

    def test_all_27(self):
        """test all"""
        code = '+1-1*1/1div1'
        expect = '+,1,-,1,*,1,/,1,div1,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 186))

    def test_all_28(self):
        """test all"""
        code = '_=_'
        expect = '_,=,_,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 187))

    def test_all_29(self):
        """test all"""
        code = '1.E+2+.1E-1E.3'
        expect = '1.,E,+,2,+,.1E-1,E,.3,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 188))

    def test_all_30(self):
        """test all"""
        code = '1a1 1e1'
        expect = '1,a1,1e1,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 189))

    def test_all_31(self):
        """test all"""
        code = ''
        expect = '<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 190))

    def test_all_32(self):
        """test all"""
        code = '1e e2'
        expect = '1,e,e2,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 191))

    def test_all_33(self):
        """test all"""
        code = 'a\tb'
        expect = 'a,b,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 192))

    def test_all_34(self):
        """test all"""
        code = '<>><=>==<<>><>>><><><>=<>=><>'
        expect = '<>,>,<=,>=,=,<,<>,>,<>,>,>,<>,<>,<>,=,<>,=,>,<>,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 193))

    def test_all_35(self):
        """test all"""
        code = '.'
        expect = 'Error Token .'
        self.assertTrue(TestLexer.test(code, expect, 194))

    def test_all_36(self):
        """test all"""
        code = '..'
        expect = '..,<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 195))

    def test_all_37(self):
        """test all"""
        code = '{\n\n\\n\t\\t}'
        expect = '<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 196))

    def test_all_38(self):
        """test all"""
        code = '//asdfasfsefasef'
        expect = '<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 1))

    def test_all_39(self):
        """test all"""
        code = '(**********)'
        expect = '<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 198))

    def test_all_40(self):
        """test all"""
        code = '(****\\\\(***{***)'
        expect = '<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 199))

    def test_all_41(self):
        """test all"""
        code = '{{{{{{{{{{{{}'
        expect = '<EOF>'
        self.assertTrue(TestLexer.test(code, expect, 200))

    
