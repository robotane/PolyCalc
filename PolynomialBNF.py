from polynomials import *
from pyparsing import *

import math
import operator

expr_stack = []


def push_first(toks):
    expr_stack.append(toks[0])


def push_unary_minus(toks):
    for t in toks:
        if t == "-":
            expr_stack.append("unary -")
        else:
            break


bnf = None


def poly_BNF():
    plus, minus = map(Literal, '+-')
    sign = plus | minus
    number = Regex('[0-9/.]+')
    exponent = Optional('^' + number)
    power = CaselessLiteral('x') + exponent
    atom = number('coeff') + Optional(power) | power
    monomial = Combine(Optional(sign('sign')) + atom, adjacent=False)
    polynomial = Combine(monomial + ZeroOrMore(sign + monomial), adjacent=False)
    return monomial, polynomial


def get_BNF():
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    global bnf
    if not bnf:
        ident = Word(alphas, alphanums + "_$")
        monoexpr, polyexpr = poly_BNF()

        plus, minus, mult, div = map(Literal, "+-*/")
        lpar, rpar = map(Suppress, "()")
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")

        expr = Forward()
        expr_list = delimitedList(Group(expr))

        # add parse action that replaces the function identifier with a (name, number of args) tuple
        def insert_fn_argcount_tuple(t):
            fn = t.pop(0)
            num_args = len(t[0])
            t.insert(0, (fn, num_args))

        fn_call = (ident + lpar - Group(expr_list) + rpar).setParseAction(
            insert_fn_argcount_tuple
        )
        atom = (
                addop[...] +
                (
                        (monoexpr | ident).setParseAction(push_first)
                        | Group(lpar + expr + rpar)
                )
        ).setParseAction(push_unary_minus)

        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
        # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor <<= atom + (expop + factor).setParseAction(push_first)[...]
        term = factor + (multop + factor).setParseAction(push_first)[...]
        expr <<= term + (addop + term).setParseAction(push_first)[...]
        bnf = expr
    return bnf


# map operator symbols to corresponding arithmetic operations
epsilon = 1e-12
opn = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}

fn = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "abs": abs,
    "trunc": int,
    "round": round,
    "sgn": lambda a: -1 if a < -epsilon else 1 if a > epsilon else 0,
    # functionsl with multiple arguments
    "multiply": lambda a, b: a * b,
    "hypot": math.hypot,
    # functions with a variable number of arguments
    "all": lambda *a: all(a),
}


def prepare_input(s):
    rg_par = Suppress(")") + Suppress("(")
    rg_par.setParseAction(lambda _: ") * (")
    prepared = rg_par.transformString(s)
    return prepared


def evaluate_stack(s):
    op, num_args = s.pop(), 0
    if isinstance(op, tuple):
        op, num_args = op
    if op == "unary -":
        return -evaluate_stack(s)
    if op in "+-*/^":
        # note: operands are pushed onto the stack in reverse order
        op2 = evaluate_stack(s)
        op1 = evaluate_stack(s)
        return opn[op](op1, op2)
    elif op == "PI":
        return math.pi  # 3.1415926535
    elif op == "E":
        return math.e  # 2.718281828
    elif op in fn:
        # note: args are pushed onto the stack in reverse order
        args = reversed([evaluate_stack(s) for _ in range(num_args)])
        return fn[op](*args)
    # elif op[0].isalpha():
    #     raise Exception("invalid identifier '%s'" % op)
    else:
        # try to evaluate as int first, then as float if int fails, else as Polynomial
        try:
            return int(op)
        except ValueError:
            try:
                return float(op)
            except ValueError:
                try:
                    return Monomial(op)
                except ValueError:
                    return Polynomial(op)


if __name__ == "__main__":

    def test(s, expected):
        s = prepare_input(s)
        expr_stack[:] = []
        try:
            results = get_BNF().parseString(s, parseAll=True)
            val = evaluate_stack(expr_stack[:])
        except ParseException as pe:
            print(s, "failed parse:", str(pe))
        except Exception as e:
            print(s, "failed eval:", str(e), expr_stack)
        else:
            if val == expected:
                print(s, "=", val, results, "=>", expr_stack)
            else:
                print(s + "!!!", val, "!=", expected, results, "=>", expr_stack)


    test("9x+2", Polynomial("9x+2"))
    test("(9/2x +2)", Polynomial("9/2x+2"))
    test("-9x+2", Polynomial("-9x+2"))
    test("-(9x+2)", -Polynomial("9x+2"))
    test("(9x +2) + x+2", Polynomial("9x+2") + Polynomial("x+2"))
    test("(9x +2) + (x+2)", Polynomial("9x+2") + Polynomial("x+2"))
    test("(9X +2) - (2x+1)", Polynomial("9x+2") - "2x+1")
    test("(9X +2) - 2x+1", Polynomial("9x+2") + "-2x+1")
    test("(9x +2) * (x^3+2)", Polynomial("9x+2") * Polynomial("x^3+2"))
    test("((9x +2)(x+2)         (x-2))^2", (Polynomial("9x+2") * Polynomial("x+2") * "x-2") ** 2)
    test("(9x^3 +2) / (x+2)", Polynomial("9x^3+2") / Polynomial("x+2"))
    test("((9X +2/3)^2 +1/7x^3)^2", (Polynomial("9x+2/3") ** 2 + "1/7x^3") ** 2)
    test("(9X +2)^2 - 2x+1", Polynomial("9x+2") ** 2 + "-2x+1")
    test("(9X +2)^2 - (2x+1)", Polynomial("9x+2") ** 2 - "2x+1")

    test("-9", -9)
    test("--9", 9)
    test("-E", -math.e)
    test("9 + 3 + 6", 9 + 3 + 6)
    test("9 + 3 / 11", 9 + 3.0 / 11)
    test("(9 + 3)", (9 + 3))
    test("(9+3) / 11", (9 + 3.0) / 11)
    test("9 - 12 - 6", 9 - 12 - 6)
    test("9 - (12 - 6)", 9 - (12 - 6))
    test("2*3.14159", 2 * 3.14159)
    test("3.1415926535*3.1415926535 / 10", 3.1415926535 * 3.1415926535 / 10)
    test("PI * PI / 10", math.pi * math.pi / 10)
    test("PI*PI/10", math.pi * math.pi / 10)
    test("PI^2", math.pi ** 2)

    # test("round(PI^2)", round(math.pi ** 2))
    # test("6.02E23 * 8.048", 6.02e23 * 8.048)

#    test("e / 3", math.e / 3)

# test("sin(PI/2)", math.sin(math.pi / 2))
# test("10+sin(PI/4)^2", 10 + math.sin(math.pi / 4) ** 2)
# test("trunc(E)", int(math.e))
# test("trunc(-E)", int(-math.e))
# test("round(E)", round(math.e))
# test("round(-E)", round(-math.e))
# test("E^PI", math.e ** math.pi)
# test("exp(0)", 1)
# test("exp(1)", math.e)


#    test("(2^3)^2", (2 ** 3) ** 2)
#    test("2^3+2", 2 ** 3 + 2)
#    test("2^3+5", 2 ** 3 + 5)
#    test("2^9", 2 ** 9)


# test("sgn(-2)", -1)
# test("sgn(0)", 0)
# test("sgn(0.1)", 1)
# test("foo(0.1)", None)
# test("round(E, 3)", round(math.e, 3))
# test("round(PI^2, 3)", round(math.pi ** 2, 3))
# test("sgn(cos(PI/4))", 1)
# test("sgn(cos(PI/2))", 0)
# test("sgn(cos(PI*3/4))", -1)
# test("+(sgn(cos(PI/4)))", 1)
# test("-(sgn(cos(PI/4)))", -1)
# test("hypot(3, 4)", 5)
# test("multiply(3, 7)", 21)
# test("all(1,1,1)", True)
# test("all(1,1,1,1,1,0)", False)

"""
Test output:
>python PolynomialBNF.py
9 = 9 ['9'] => ['9']
-9 = -9 ['-', '9'] => ['9', 'unary -']
--9 = 9 ['-', '-', '9'] => ['9', 'unary -', 'unary -']
-E = -2.718281828459045 ['-', 'E'] => ['E', 'unary -']
9 + 3 + 6 = 18 ['9', '+', '3', '+', '6'] => ['9', '3', '+', '6', '+']
9 + 3 / 11 = 9.272727272727273 ['9', '+', '3', '/', '11'] => ['9', '3', '11', '/', '+']
(9 + 3) = 12 [['9', '+', '3']] => ['9', '3', '+']
(9+3) / 11 = 1.0909090909090908 [['9', '+', '3'], '/', '11'] => ['9', '3', '+', '11', '/']
9 - 12 - 6 = -9 ['9', '-', '12', '-', '6'] => ['9', '12', '-', '6', '-']
9 - (12 - 6) = 3 ['9', '-', ['12', '-', '6']] => ['9', '12', '6', '-', '-']
2*3.14159 = 6.28318 ['2', '*', '3.14159'] => ['2', '3.14159', '*']
3.1415926535*3.1415926535 / 10 = 0.9869604400525172 ['3.1415926535', '*', '3.1415926535', '/', '10'] => ['3.1415926535', '3.1415926535', '*', '10', '/']
PI * PI / 10 = 0.9869604401089358 ['PI', '*', 'PI', '/', '10'] => ['PI', 'PI', '*', '10', '/']
PI*PI/10 = 0.9869604401089358 ['PI', '*', 'PI', '/', '10'] => ['PI', 'PI', '*', '10', '/']
PI^2 = 9.869604401089358 ['PI', '^', '2'] => ['PI', '2', '^']
round(PI^2) = 10 [('round', 1), [['PI', '^', '2']]] => ['PI', '2', '^', ('round', 1)]
6.02E23 * 8.048 = 4.844896e+24 ['6.02E23', '*', '8.048'] => ['6.02E23', '8.048', '*']
e / 3 = 0.9060939428196817 ['E', '/', '3'] => ['E', '3', '/']
sin(PI/2) = 1.0 [('sin', 1), [['PI', '/', '2']]] => ['PI', '2', '/', ('sin', 1)]
10+sin(PI/4)^2 = 10.5 ['10', '+', ('sin', 1), [['PI', '/', '4']], '^', '2'] => ['10', 'PI', '4', '/', ('sin', 1), '2', '^', '+']
trunc(E) = 2 [('trunc', 1), [['E']]] => ['E', ('trunc', 1)]
trunc(-E) = -2 [('trunc', 1), [['-', 'E']]] => ['E', 'unary -', ('trunc', 1)]
round(E) = 3 [('round', 1), [['E']]] => ['E', ('round', 1)]
round(-E) = -3 [('round', 1), [['-', 'E']]] => ['E', 'unary -', ('round', 1)]
E^PI = 23.140692632779263 ['E', '^', 'PI'] => ['E', 'PI', '^']
exp(0) = 1.0 [('exp', 1), [['0']]] => ['0', ('exp', 1)]
exp(1) = 2.718281828459045 [('exp', 1), [['1']]] => ['1', ('exp', 1)]
2^3^2 = 512 ['2', '^', '3', '^', '2'] => ['2', '3', '2', '^', '^']
(2^3)^2 = 64 [['2', '^', '3'], '^', '2'] => ['2', '3', '^', '2', '^']
2^3+2 = 10 ['2', '^', '3', '+', '2'] => ['2', '3', '^', '2', '+']
2^3+5 = 13 ['2', '^', '3', '+', '5'] => ['2', '3', '^', '5', '+']
2^9 = 512 ['2', '^', '9'] => ['2', '9', '^']
sgn(-2) = -1 [('sgn', 1), [['-', '2']]] => ['2', 'unary -', ('sgn', 1)]
sgn(0) = 0 [('sgn', 1), [['0']]] => ['0', ('sgn', 1)]
sgn(0.1) = 1 [('sgn', 1), [['0.1']]] => ['0.1', ('sgn', 1)]
foo(0.1) failed eval: invalid identifier 'foo' ['0.1', ('foo', 1)]
round(E, 3) = 2.718 [('round', 2), [['E'], ['3']]] => ['E', '3', ('round', 2)]
round(PI^2, 3) = 9.87 [('round', 2), [['PI', '^', '2'], ['3']]] => ['PI', '2', '^', '3', ('round', 2)]
sgn(cos(PI/4)) = 1 [('sgn', 1), [[('cos', 1), [['PI', '/', '4']]]]] => ['PI', '4', '/', ('cos', 1), ('sgn', 1)]
sgn(cos(PI/2)) = 0 [('sgn', 1), [[('cos', 1), [['PI', '/', '2']]]]] => ['PI', '2', '/', ('cos', 1), ('sgn', 1)]
sgn(cos(PI*3/4)) = -1 [('sgn', 1), [[('cos', 1), [['PI', '*', '3', '/', '4']]]]] => ['PI', '3', '*', '4', '/', ('cos', 1), ('sgn', 1)]
+(sgn(cos(PI/4))) = 1 ['+', [('sgn', 1), [[('cos', 1), [['PI', '/', '4']]]]]] => ['PI', '4', '/', ('cos', 1), ('sgn', 1)]
-(sgn(cos(PI/4))) = -1 ['-', [('sgn', 1), [[('cos', 1), [['PI', '/', '4']]]]]] => ['PI', '4', '/', ('cos', 1), ('sgn', 1), 'unary -']
"""
