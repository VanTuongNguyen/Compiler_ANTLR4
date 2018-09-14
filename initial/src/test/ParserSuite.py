import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_(self):
        code = \
        """\
        procedure main();
        begin

        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,201))

    def test_index_exp_1(self):
        code = \
        """\
        procedure main();
        begin
            a := foo(1+a[i-goo(t*hoo(t[x]))]*6-(a[(2+1)*3]+1)*a[2])[(2-5)+a[x]];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,202))

    def test_index_exp_2(self):
        code = \
        """\
        procedure main();
        begin
            a := a[1][2][3];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,203))

    def test_index_exp_3(self):
        code = \
        """\
        procedure main();
        begin
            a := a[a[a[a[a[a[a[a[1]]]]]]]];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,204))

    def test_index_exp_4(self):
        code = \
        """\
        procedure main();
        begin
            a := a[a[a]][a[a[a]]];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,205))

    def test_index_exp_5(self):
        code = \
        """\
        procedure main();
        begin
            a:=a[[[[a]]]]
        end
        """
        expect = "Error on line 3 col 17: ["
        self.assertTrue(TestParser.test(code,expect,206))

    def test_index_exp_6(self):
        code = \
        """\
        procedure main();
        begin
            a := 1[1];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,207))

    def test_index_exp_7(self):
        code = \
        """\
        procedure main();
        begin
            a:= (Not 5 + 1)[2];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,208))

    def test_index_exp_8(self):
        code = \
        """\
        procedure main();
        begin
            a[1] := a[a[a]] := a[a][a] := (a)[a] := a()[a] := a[(a)];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,209))

    def test_expression_1(self):
        code = \
        """\
        procedure main();
        begin
            a := not - a + b * -d div 2 mod a >= - not 3 + 4;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,210))

    def test_expression_2(self):
        code = \
        """\
        procedure main();
        begin
            a := not Not NOT nOt - - - - - a;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,211))

    def test_expression_3(self):
        code = \
        """\
        procedure main();
        begin
            a := ((((((((a+b))))))));
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,212))

    def test_expression_4(self):
        code = \
        """\
        procedure main();
        begin
            a := (a)div(a)mod(a)/a-a+a*a;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,213))

    def test_expression_5(self):
        code = \
        """\
        procedure main();
        begin
            a:=
            -
            -
            -
            -
            a;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,214))

    def test_if_statement_1(self):
        code = \
        """\
        procedure main();
        begin
            if a then b();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,215))

    def test_if_statement_2(self):
        code = \
        """\
        procedure main();
        begin
            if a then
                if b then
                    fo();
                else
                    go();
            else
                ho();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,216))

    def test_if_statement_3(self):
        code = \
        """\
        procedure main();
        begin
            if a then
                if b then
                    fo();
                else
                    ho();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,217))

    def test_if_statement_4(self):
        code = \
        """\
        procedure main();
        begin
            if a then
                if b then
                    if c then
                        f();
                    else g();
                else c();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,218))

    def test_if_statement_5(self):
        code = \
        """\
        procedure main();
        begin
            if a then
                if b then
                    if c then
                        f();
                    else g();
                else c();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,219))

    def test_if_statement_6(self):
        code = \
        """\
        procedure main();
        begin
            if a then
                begin
                    f(); g();
                end
            else
                if b then
                    f();
                else
                    begin
                        c(); d();
                    end
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,220))

    def test_if_statement_7(self):
        code = \
        """\
        procedure main();
        begin
            if a then
                if b then
                    if c then
                        if d then
                            e();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,221))

    def test_loop_statement_1(self):
        code = \
        """\
        procedure main();
        begin
            while a do b();
            while a do
                begin
                    c();
                end
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,222))

    def test_loop_statement_2(self):
        code = \
        """\
        procedure main();
        begin
            while a do while b do while c do d();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,223))

    def test_loop_statement_3(self):
        code = \
        """\
        procedure main();
        begin
            for i:=1 to 2 do c();
            for i:=2 downto 1 do c();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,224))

    def test_loop_statement_4(self):
        code = \
        """\
        procedure main();
        begin
            for i:=a[1] to a[2] do c();
            for i:=foo(a[1]+1)[1] to 1 do c();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,225))

    def test_loop_statement_5(self):
        code = \
        """\
        procedure main();
        begin
            for i:=a to b do
                for j:=1 to 2 do
                    for k:=1 to 3 do
                        begin
                            c();
                        end
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,226))

    def test_loop_statement_6(self):
        code = \
        """\
        procedure main();
        begin
            while 1 do 
                begin
                    break;
                    continue;
                    return;
                end
            return a[1] + 2 * b;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,227))

    def test_statement_1(self):
        code = \
        """\
        procedure main();
        begin
            foo(1,2,3,4);
            with a,b,c:integer; d:real; e:array[1 .. 2] of boolean; g: string; do
                begin
                    return foo(12,3,a,b);
                end
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,228))

    def test_statement_2(self):
        code = \
        """\
        procedure main();
        begin
            foo(1,2,3,4);
            with a,b,c:integer; d:real; e:array[1 .. 2] of boolean; g: string; do
                begin
                    return foo(12,3,a,b);
                end
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,229))

    def test_statement_3(self):
        code = \
        """\
        procedure main();
        begin
            with a:real; do with b:real; do with c:real; do fo();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,230))

    def test_func_proc_1(self):
        code = \
        """\
        procedure main(a:array[1 .. 3] of real);
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,231))

    def test_func_proc_2(self):
        code = \
        """\
        procedure main();
            var h,c: integer;
            j,k: real;
            c: array[1 .. 3] of string;
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,232))

    def test_func_proc_3(self):
        code = \
        """\
        procedure main(a,b:real; d:string);
            var h,c: integer;
            j,k: real;
            c: array[1 .. 3] of string;
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,233))

    def test_func_proc_4(self):
        code = \
        """\
        function main():real;
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,234))

    def test_func_proc_5(self):
        code = \
        """\
        function main(a,b,d:integer):string;
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,235))

    def test_func_proc_6(self):
        code = \
        """\
        function main(a,c:string):integer;
            var c:string;
            e: integer;
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,236))

    def test_func_proc_7(self):
        code = \
        """\
        function main(): string;
        var a: string;
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,237))

    def test_all_1(self):
        code = \
        """\
        procedure main();
        begin
            print("hello world");
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,238))

    def test_all_2(self):
        code = \
        """\
        procedure main();
        begin
            print("hello );
        end
        """
        expect = "hello );"
        self.assertTrue(TestParser.test(code,expect,239))


    def test_all_3(self):
        code = \
        """\
        procedure main();
        begin
            print("hello
            world");
        end
        """
        expect = "hello"
        self.assertTrue(TestParser.test(code,expect,240))


    def test_all_4(self):
        code = \
        """\
        procedure main();
        begin
            a := := b;
        end
        """
        expect = "Error on line 3 col 17: :="
        self.assertTrue(TestParser.test(code,expect,241))


    def test_all_5(self):
        code = \
        """\
        procedure main();
        begin
            return return 1;
        end
        """
        expect = "Error on line 3 col 19: return"
        self.assertTrue(TestParser.test(code,expect,242))


    def test_all_6(self):
        code = \
        """\
        procedure main();
        begin
            a : = 1;
        end
        """
        expect = "Error on line 3 col 14: :"
        self.assertTrue(TestParser.test(code,expect,243))


    def test_all_7(self):
        code = \
        """\
        procedure main();
        begin
            a + 1 := b;
        end
        """
        expect = "Error on line 3 col 14: +"
        self.assertTrue(TestParser.test(code,expect,244))


    def test_all_8(self):
        code = \
        """\
        procedure main();
        begin
            a := b = a;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,245))


    def test_all_9(self):
        code = \
        """\
        begin
            begin
                begin
                end
            end
        end
        """
        expect = "Error on line 1 col 8: begin"
        self.assertTrue(TestParser.test(code,expect,246))


    def test_all_10(self):
        code = \
        """\
        procedure 1();
        begin
            
        end
        """
        expect = "Error on line 1 col 18: 1"
        self.assertTrue(TestParser.test(code,expect,247))


    def test_all_11(self):
        code = \
        """\
        procedure main(): string;
        begin
            
        end
        """
        expect = "Error on line 1 col 24: :"
        self.assertTrue(TestParser.test(code,expect,248))


    def test_all_12(self):
        code = \
        """\
        procedure main();
        begin
            a:= a<>1;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,249))


    def test_all_13(self):
        code = \
        """\
        procedure main();
        begin
            print("hello world \\n hello \\t hello \\' hello \\\" hello ");
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,250))

    def test_all_14(self):
        code = \
        """\
        procedure main();
        begin
            a.b;
        end
        """
        expect = "."
        self.assertTrue(TestParser.test(code,expect,251))

    def test_all_15(self):
        code = \
        """\
        procedure main();
        begin
            print("!@##%$^#^$&*&(*&*)()+_~,.<?<;:[]{}|");
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,252))

    def test_all_16(self):
        code = \
        """\
        procedure main();
        begin
            12a := a12;
        end
        """
        expect = "Error on line 3 col 14: a"
        self.assertTrue(TestParser.test(code,expect,253))

    def test_all_17(self):
        code = \
        """\
        procedure main();
        begin
            a:= foo(12,12a,abc);
        end
        """
        expect = "Error on line 3 col 25: a"
        self.assertTrue(TestParser.test(code,expect,254))

    def test_all_18(self):
        code = \
        """\
        procedure main();
        begin
            a:= 1 and then 2;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,255))

    def test_all_19(self):
        code = \
        """\
        procedure main();
        begin
            f(1 or else 2);
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,256))

    def test_all_20(self):
        code = \
        """\
        procedure main();
        begin
            a:= a or b or c or else d;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,257))

    def test_all_21(self):
        code = \
        """\
        procedure main();
        begin
            f(f(f(f())));
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,258))

    def test_all_22(self):
        code = \
        """\
        procedure main();
        var a: array[ 1 . . 2] of real;
        begin
            
        end
        """
        expect = "."
        self.assertTrue(TestParser.test(code,expect,259))

    def test_all_23(self):
        code = \
        """\
        procedure main();
        begin
            f()[f()] := a[f(a[a])];
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,260))

    def test_all_24(self):
        code = \
        """\
        procedure main();
        begin
            {
                hello 
                word
            }
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,261))

    def test_all_25(self):
        code = \
        """\
        procedure main();
        begin
            (*
                // alala
            *)
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,262))

    def test_all_26(self):
        code = \
        """\
        procedure main();
        begin
            // {asdfasdf
            }
        end
        """
        expect = "}"
        self.assertTrue(TestParser.test(code,expect,263))

    def test_all_27(self):
        code = \
        """\
        procedure main();
        begin
            ///////////
            ///
            //
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,264))

    def test_all_28(self):
        code = \
        """\
        procedure main();
        begin
            a := "a:=b";
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,265))

    def test_all_29(self):
        code = \
        """\
        procedure main();
        begin
            a := 1+2+3+
            4+5+6
            ;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,266))

    def test_all_30(self):
        code = \
        """\
        procedure main();
        begin
            ;
        end
        """
        expect = "Error on line 3 col 12: ;"
        self.assertTrue(TestParser.test(code,expect,267))

    def test_all_31(self):
        code = \
        """\
        procedure main();
        begin
            procedure main();
        end
        """
        expect = "Error on line 3 col 12: procedure"
        self.assertTrue(TestParser.test(code,expect,268))

    def test_all_32(self):
        code = \
        """\
        procedure main();
        """
        expect = "Error on line 2 col 8: <EOF>"
        self.assertTrue(TestParser.test(code,expect,269))

    def test_all_33(self):
        code = \
        """\
        var a,b,c:real;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,270))

    def test_all_34(self):
        code = \
        """\
        var ____:real;
        procedure main();
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,271))

    def test_all_35(self):
        code = \
        """\
        var a:real;
        procedure main();
        begin
            
        end
        var b:real;
        function main():string;
        begin
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,272))

    def test_all_36(self):
        code = \
        """\
        procedure main();
        var a:real;
        var b:real;
        begin
            
        end
        """
        expect = "Error on line 3 col 8: var"
        self.assertTrue(TestParser.test(code,expect,273))

    def test_all_37(self):
        code = \
        """\
        procedure main();
        a();
        """
        expect = "Error on line 2 col 8: a"
        self.assertTrue(TestParser.test(code,expect,274))

    def test_all_38(self):
        code = \
        """\
        procedure main();
        begin
            
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,275))

    def test_all_39(self):
        code = \
        """\
        procedure ma_i^n();
        begin
            
        end
        """
        expect = "^"
        self.assertTrue(TestParser.test(code,expect,276))

    def test_all_40(self):
        code = \
        """\
        procedure main();
        begin
            var a: real;
        end
        """
        expect = "Error on line 3 col 12: var"
        self.assertTrue(TestParser.test(code,expect,277))

    def test_all_41(self):
        code = \
        """\
        procedure main();
        begin
            1[1] := 1;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,278))

    def test_all_42(self):
        code = \
        """\
        procedure main();
        begin
            true[a] := false[b] := (----a)[a] := 1;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,279))

    def test_all_43(self):
        code = \
        """\
        procedure main();
        begin
            foo()[1] := 1;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,280))

    def test_all_44(self):
        code = \
        """\
        procedure main();
        begin
            f()[1] := f[2] := f(20)[2] := f(2[2])[1] :=1;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,281))

    def test_all_45(self):
        code = \
        """\
        procedure main();
        begin
            true();
        end
        """
        expect = "Error on line 3 col 16: ("
        self.assertTrue(TestParser.test(code,expect,282))

    def test_all_46(self):
        code = \
        """\
        procedure main();
        var a:array[1 .. 3] of array[1 .. 5] of array[1 .. 6] of real;
        begin
            __:=__;
        end
        """
        expect = "Error on line 2 col 31: array"
        self.assertTrue(TestParser.test(code,expect,283))

    def test_all_47(self):
        code = \
        """\
        procedure main();
        begin
            @
        end
        """
        expect = "@"
        self.assertTrue(TestParser.test(code,expect,284))

    def test_all_48(self):
        code = \
        """\
        procedure main();
        begin
            a := a => b;
        end
        """
        expect = "Error on line 3 col 20: >"
        self.assertTrue(TestParser.test(code,expect,285))

    def test_all_49(self):
        code = \
        """\
        procedure main();
        begin
            ()
        end
        """
        expect = "Error on line 3 col 13: )"
        self.assertTrue(TestParser.test(code,expect,286))

    def test_all_50(self):
        code = \
        """\
        procedure main();
        begin
            f("a")["b"] := c("");
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,287))

    def test_all_51(self):
        code = \
        """\
        var main:Integer;
        begin
             main := f();
             return ;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,288))

    def test_all_52(self):
        code = \
        """\
        var a: array[-1..2] of real;
        procedure main();
        begin
            
        end
        """
        expect = "Error on line 1 col 23: .2"
        self.assertTrue(TestParser.test(code,expect,289))

    def test_all_53(self):
        code = \
        """\
        var a,,b: real;
        procedure main();
        begin
            
        end
        """
        expect = "Error on line 1 col 14: ,"
        self.assertTrue(TestParser.test(code,expect,290))

    def test_all_54(self):
        code = \
        """\
        procedure main();
        begin
            a := a and              then 1;
            c := 1 or          else 2;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,291))

    def test_all_55(self):
        code = \
        """\
        """
        expect = "Error on line 1 col 8: <EOF>"
        self.assertTrue(TestParser.test(code,expect,292))

    def test_all_56(self):
        code = ""
        expect = "Error on line 1 col 0: <EOF>"
        self.assertTrue(TestParser.test(code,expect,293))

    def test_all_57(self):
        code = \
        """\
function greatestCommonDivisor(a, b: integer): integer;
var
  temp: integer;
begin
  while b <> 0 do
  begin
    temp := b;
    b := a mod b;
    a := temp;
  end
  result := a;
end
 
function greatestCommonDivisor_euclidsSubtractionMethod(a, b: integer): integer;
begin
  // only works with positive integers
  if (a < 0) then a := -a;
  if (b < 0) then b := -b;
  // don't enter loop, since subtracting zero won't break condition
  if (a = 0) then exit(b);
  if (b = 0) then exit(a);
  while not (a = b) do
  begin
    if (a > b) then
     a := a - b;
    else
     b := b - a;
  end
  result := a;
end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,294))

    def test_all_58(self):
        code = \
        """\

var
   M: array[1 .. 3] of integer;

function GCD(M: array[1 .. 3] of integer ): integer;
   var i,min : integer;
begin
    min := M[0];
    for i := 1 to Length(M)-1 do begin
         if min > M[i] then
            min := M[i];
        end
    i := 1;

end

procedure main();
begin
  M:=Create(15, 45, 25);
  writeln("GCD: ", GCD(M));
end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,295))

    def test_all_59(self):
        code = \
        """\
        procedure main();
        begin
            pass();
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,296))

    def test_all_60(self):
        code = \
        """\
        procedure main();
        begin
            print('hello');
        end
        """
        expect = "'"
        self.assertTrue(TestParser.test(code,expect,297))

    def test_all_61(self):
        code = \
        """\
        procedure main();
        begin
            a:= - not - a;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,298))

    def test_all_62(self):
        code = \
        """\
        procedure main();
        begin
            a := +b;
        end
        """
        expect = "Error on line 3 col 17: +"
        self.assertTrue(TestParser.test(code,expect,299))

    def test_all_63(self):
        code = \
        """\
        procedure main();
        begin
            a := .2e1 + 1.e2;
        end
        """
        expect = "successful"
        self.assertTrue(TestParser.test(code,expect,300))
















































