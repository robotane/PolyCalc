#! /usr/bin/env python3
# -*- coding:Utf8 -*-

# (C) John Robotane 5/12/2019 2:50 PM
from fractions import Fraction
import re


class Monomial(object):
    """Represent a monomial.

    A monomial has a coefficient and a degree
    The default value of the degree is 0, but you should provide
    at least a coefficient in anny numeric format, it will be converted
    to a fractions.Fraction type.
    """

    def __init__(self, coef, deg=0):
        """Create a monomial

        :param coef:  The coefficient of the monomial
        :param deg: The degree of the monomial, with a default value of 0
        :type deg: int
        """
        coef = Fraction(coef).limit_denominator(1000000)
        self.coef = coef
        self.deg = deg
        self.var = "x"

    def __repr__(self):
        return "Monomial({},{})".format(self.coef, self.deg)

    def __eq__(self, mon):
        return self.coef == mon.coef and self.deg == mon.deg

    def __bool__(self):
        return self is not None

    def __neg__(self):
        return Monomial(-self.coef, self.deg)

    def __mul__(self, m):
        return Monomial(self.coef * m.coef, self.deg + m.deg)

    def __str__(self):
        """

        :return: A human readable string of the monomial
        """
        s = ""
        if self.deg == 0:
            return str(self.coef)

        if self.coef == 1 or self.coef == -1:
            if self.coef == -1:
                s += "-"
            s += self.var
        else:
            s += str(self.coef) + self.var
        if self.deg > 1:
            s += "^" + str(self.deg)
        return s if s else '0'

    def html_str(self):
        s = ""
        if self.deg == 0:
            return str(self.coef)

        if self.coef == 1 or self.coef == -1:
            if self.coef == -1:
                s += "-"
            s += self.var
        else:
            s += str(self.coef) + self.var
        if self.deg > 1:
            s += "<sup>" + str(self.deg) + "</sup>"
        return s

    def eval_str(self, val):
        """Used to get an evaluable string of the monomial.

        This method returns a string which which can be used with the python eval function.

        :param val: The value to substitute with the variable
        :return: an evaluable string of the monomial which can be used with eval()
        :rtype: str
        """
        s = ""
        val = Fraction(val).limit_denominator(1000000)
        if self.deg == 0:
            return repr(self.coef)

        if self.coef == 1 or self.coef == -1:
            if self.coef == -1:
                s += "-"
            s += repr(val)
        else:
            # s += repr(self.coef) if self.coef > 0 else ("-"+repr(-self.coef)) + "*(" + repr(val) + ")"
            s += repr(self.coef) + "*" + repr(val) + ""

        if self.deg > 1:
            s += "**" + str(self.deg)
        return s

    def __call__(self, val):
        val = Fraction(val).limit_denominator(1000000)
        return self.coef * (val ** self.deg)

    def derive(self, n):
        """Derive the monomial

        :param n: The number of time the monomial will be derived
        :return: The n-th derivative of the monomial
        :rtype: Monomial
        """
        m = Monomial(self.deg * self.coef, self.deg - 1)
        if n == 1:
            return m
        else:
            return m.derive(n - 1)


class Polynomial:
    """Represent a polynomial.

    A polynomial consists of monomials.

    Usage
    -----

    >>> import polynomials
    >>> p = polynomials.Polynomial("X^4+1/3X^3")
    >>> q = polynomials.Polynomial("X^2+5/2X+1")
    >>> quot , rem = p/q
    >>> print(f"({p})/({q})={quot} and the remainder is {rem}")
    (X^4+1/3X^3)/(X^2+5/2X+1)=X^2-13/6X+53/12 and the remainder is -71/8X-53/12
    >>> print(p.derive())
    4X^3+3X^2
    >>> print(p(2/3))
    8/27
    """

    def __init__(self, expr=None):
        """Create a polynomial with the given expression.

        The argument should be a polynomial expression, any numeric value or a Monomial

        :param expr: A string containing a polynomial expression, any numeric value or a Monomial
        """
        self.var = "x"
        self.monomials = []
        if not expr:
            self.append(Monomial(0))
        elif isinstance(expr, (list, tuple)):
            for val in expr:
                # if val:
                self.append(Polynomial(val))
        elif isinstance(expr, Monomial):
            self.append(expr)
        elif isinstance(expr, Polynomial):
            self.append(expr)
        elif isinstance(expr, str):
            self.append(self.str_pol(expr))
        elif isinstance(expr, (Fraction, int, float)):
            self.append(Monomial(expr, 0))
        # else:
        # self.append(Monomial(0))
        # self.monomials = [Monomial(0)] if expr is None else self.str_pol(str(expr)).monomials

    def deg(self):
        """The degree of a polynomial is the degree of the non null monomial with the highest degree

        :return: The highest degree within the non null monomials of the polynomial
        :rtype: int
        """
        return max(filter(lambda m: m.coef != 0, self), key=lambda m: m.deg).deg

    def append(self, f, c=None):
        """
        Add a monomial to the polynomial

        :param f: Any numeric value or a Monomial or any Plynomial
        :param c: Degree of the monomial
        :type c: int
        :return: None
        """
        # self.monomials.append(f if c is None else Monomial(f, c))

        # TODO Never append the monomial null Monomial(0) twice.

        if c is None:
            if isinstance(f, Monomial):
                self.monomials.append(f)
            elif isinstance(f, Polynomial):
                for m in f:
                    m.var = self.var
                    self.append(m)
            else:
                self.append(Polynomial(f))
        else:
            m = Monomial(f, c)
            m.var = self.var
            self.append(m)
        # self.reorder()

    def pol_append(self, p):
        """
        Add the polynomial p monomials to the the current polynomial monomials

        :param p: The polynomial to pol_append
        :type p: Polynomial
        :return: None
        """
        for m in p:
            self.append(m)

    def __repr__(self):
        return f'Polynomial("{self!s}")'

    def __str__(self):
        """

        :return: A human readable string of the monomial
        """
        s = ""
        for m in self:
            if not m.coef == 0:
                if m.coef > 0:
                    s += "+"
                s += str(m)
        # s = s.replace("", self.var)
        if s.startswith("+"):
            s = s[1:]
        return s if s else "0"

    def html_str(self):
        s = ""
        for m in self:
            if not m.coef == 0:
                if not m == self[0]:
                    if m.coef > 0:
                        s += "+"
                s += m.html_str()
        # s = s.replace(self.var, self.var)
        if s.startswith("+"):
            s = s[1:]
        return s if s else "0"

    def eval_str(self, val):
        """Used to get an evaluable string of the polynomial.

        This method returns a string which can be used with the python eval function.

        :param val: The value to substitute with the variable
        :return: An evaluable string of the polynomial which can be used with eval()
        :rtype: str
        """
        s = ""
        for m in self:
            if not m.coef == 0:
                # if not m == self.monomials[0] and m.coef > 0:
                s += "+"
                s += m.eval_str(val)

        return s[1:]

    def __iter__(self):
        return iter(self.monomials)

    def __getitem__(self, index):
        return self.monomials[index]

    def __setitem__(self, index, value):
        self.monomials[index] = value

    def __delitem__(self, index):
        del self.monomials[index]

    def pop(self, *args):
        return self.monomials.pop(*args)

    def __len__(self):
        return len(self.monomials)

    def __contains__(self, mon):
        return mon in self.monomials

    def copy(self):
        """
        Copy the polynomial

        :return: A copy of the polynomial
        :rtype: Polynomial
        """
        # p = Polynomial()
        return Polynomial(self.monomials.copy())

    def __eq__(self, p):
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        s = self.reorder(with_zero=True)
        p = p.reorder(with_zero=True)
        if len(p) != len(s) or p.deg() != s.deg():
            return False
        return all([s[i] == p[i] for i in range(s.deg() + 1)])

    def __add__(self, p):
        s = self.copy()
        # s.monomials = self.monomials.copy()
        if not isinstance(p, (Polynomial, Monomial)):
            p = Polynomial(p)
        s.append(p)
        return s.reorder()

    def __sub__(self, p):
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        return self.__add__(-p)

    def __neg__(self):
        # p = Polynomial()
        p = Polynomial([-m for m in self])
        return p.reorder()

    def __truediv__(self, p):
        if str(p).isalnum():
            p = Monomial(p)
            return self * Monomial(Fraction(p.coef.denominator, p.coef.numerator))

        if not isinstance(p, Polynomial):
            p = Polynomial(p)

        if self.deg() < p.deg():
            return Polynomial(0), self

        else:
            p1 = self.copy().reorder(with_zero=True)
            p2 = p.copy().reorder()
            quot = Polynomial()
            m1, m2 = p1[0], p2[0]

            while True:
                m = Monomial(m1.coef / m2.coef, m1.deg - m2.deg)
                quot.append(m)
                p1 = (p1 - p2 * m).reorder(with_zero=True, deg=p1.deg())
                p1.pop(0)
                if not p1.monomials:
                    break
                m1 = p1[0]
                if m1.deg - m2.deg < 0:
                    break
            return quot.reorder(), p1.reorder()

    def __floordiv__(self, p):
        q, _ = self / p
        return q

    def __mul__(self, f):
        if not isinstance(f, (Polynomial, Monomial)):
            f = Polynomial(f)

        if isinstance(f, Monomial):
            q = Polynomial()
            for m in self:
                q.append(f * m)

            return q.reorder()

        if isinstance(f, Polynomial):
            q = Polynomial()
            for m in f:
                q.append(self * m)

            return q.reorder()

    def __rmul__(self, f):
        return self.__mul__(f)

    def __radd__(self, f):
        return self.__add__(f)

    def __rsub__(self, f):
        return self.__sub__(f)

    def __pow__(self, n):
        pow_pol = Polynomial(1)
        for i in range(n):
            pow_pol = pow_pol * self
        return pow_pol.reorder()

    def __mod__(self, other):
        _, r = self / other
        return r

    def __call__(self, val=Fraction(0)):
        if str(val).isalpha():
            p = self.copy()
            p.var = val
            return p
        return sum(map(lambda m: m(val), self))

    def derive(self, n=1):
        """Derive the polynomial

        :param n: The number of time the polynomial will be derivated
        :return: The n-th derivative of the monomial
        :rtype: Polynomial
        """
        p = Polynomial()
        for m in self:
            p.append(m.derive(n))
        return p.reorder()

    def reorder(self, rev=True, with_zero=False, deg=None):
        """Reorder the polynomial in order to have increasing or decreasing degrees of the monomials

        :param rev: If True, the first monomial will be the monomial wit hhighest degree else it will be the opposite, the first monomial will be the monomial with the lowest degree
        :type rev: bool
        :param with_zero: If False, the returned polynomial will not contain monomials with null coefficients, else the opposite will hapen.
        :type with_zero: bool
        :param deg: The highest degree, this parameter is used essentially in the __truediv__ method
        :type deg: int
        :return: A polynomial with reordered monomial
        :rtype: Polynomial
        """
        s = []
        r = range(self.deg() if deg is None else deg + 1)
        if rev:
            r = range(self.deg() if deg is None else deg, -1, -1)
        for i in r:
            m_l = [m for m in self if m.deg == i]

            if m_l:
                c = Fraction(0)
                for m in m_l:
                    c = c + m.coef
                if with_zero or (c != Fraction(0)):
                    s.append(Monomial(c, i))
            elif with_zero:
                s.append(Monomial(0, i))

        # self.monomials = s
        # p = Polynomial()
        return Polynomial(s)
        # print(with_zero)
        # return p

    @staticmethod
    def str_pol(s):
        """Take a polynomial expression a string and return the corresponding polynomial

        :param s: The polynomial expression
        :type s: str
        :return: A polynomial which monomials are those in the expression
        :rtype: Polynomial
        """
        p = []
        # p.pop(0)
        s = s.replace(" ", "")
        mon = re.compile(r"(?P<coef>[+-]?[\d]*[./]?[\d]*)(?P<var>[Xx]?)[\^]?(?P<deg>[\d]*)")
        for monome in mon.finditer(s):
            coef = Fraction(0)
            deg = 0
            t = monome.group('coef')
            mono = t + '1' if t in ('+', '-') else t if t else '1'
            # print(monome.groupdict())
            if monome.group('var'):
                coef = Fraction(mono)
                deg = int(monome.group('deg')) if monome.group('deg') else 1
                p.append(Monomial(coef, deg))
            elif monome.group('coef'):
                coef = Fraction(mono)
                deg = 0
                p.append(Monomial(coef, deg))
        return Polynomial(p)

    @staticmethod
    def str_pol_old(s):
        """Take a polynomial expression a string and return the corresponding polynomial

        :param s: The polynomial expression
        :type s: str
        :return: A polynomial which monomials are those in the expression
        :rtype: Polynomial
        """
        p = Polynomial()
        p.monomials.pop(0)
        scoef, sdeg = "", ""
        pc, pd = False, False
        pcoef, pdeg = Fraction(0), Fraction(0)
        neg = s[0] == "-"
        l = len(s)

        for i, c in enumerate(s):
            if c.upper() == p.var:
                pc = True
            if c == "^":
                pd = True
            if (c.isdigit() or c == "." or c == "/") and not pc:
                scoef += c
            if c.isdigit() and pd:
                sdeg += c
            if (c == "+" or c == "-" or i == l - 1) and i > 0:
                if not scoef:
                    if neg:
                        pcoef = Fraction(-1)
                    else:
                        pcoef = Fraction(1)
                else:
                    pcoef = Fraction(scoef).limit_denominator(1000000)
                    if neg:
                        pcoef = -pcoef

                if pc and not pd:
                    pdeg = 1
                elif pc and pd:
                    pdeg = int(sdeg)
                if not pc:
                    pdeg = 0
                p.append(pcoef, pdeg)
                scoef, sdeg = "", ""
                pc, pd = False, False
                pcoef, pdeg = Fraction(0), Fraction(0)
                neg = c == "-"
        return p


if __name__ == "__main__":
    z = Polynomial('X-2X^3+3/8')
    p = Polynomial("-X+2X^2+X^3-2")
    w = Polynomial.str_pol_old("X^3+2X^2-2-X")
    q = Polynomial("X^2+1")
    #    for m in w:
    #        if m == w[-1]:
    #            print(m)
    #        else:
    #            print(m, end=', ')
    print(*p, sep=', ')
    # print()
    # m=p.pop()
    print(p, w, p == w)
    m = Monomial(1, 3)
    print("Testing the addition")
    print(f"({p})+({q})={p + q}")
    print("Testing the multiplication")
    print(f"({p})*({q})={p * q}")
    print("Testing the division")
    qot, rem = p // q
    print(f"({p})/({q})={qot} and the remainder is {rem}")
    print("Testing derive once")
    print(f"{p}(2/3)={p(2 / 3)}")
    print("Testing derive twice")
    print(f"({p * q})''={(p * q).derive(2)}")

    t = Polynomial((m, '-x^6 -7', '7/3x', q, '', '', '', ''))
    g = (Polynomial(-1) + 'x+2') * 'x+2'
    # t = Polynomial(['',''])
    print(isinstance(Monomial('5/6').coef, Fraction))
    print(t, len(t), 'and', t.reorder(), len(t.reorder()))
    m = Monomial(0, 10)
    p = Polynomial((m, 'x', '2x^2'))
    print(p, p.deg())
