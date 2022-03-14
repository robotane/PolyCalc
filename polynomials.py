# (C) John Robotane 2019-2022
# Created on 5/12/2019 2:50 PM

from fractions import Fraction
import re
from typing import Any


class Monomial:
    """Represent a monomial.

    A monomial has a coefficient and a degree
    The default value of the degree is 0, but you should provide
    at least a coefficient in any numeric format, it will be converted
    to a fractions.Fraction type.
    """

    def __mod__(self, other: Any) -> Any:
        pass

    def __rmod__(self, other: Any) -> Any:
        pass

    def __init__(self, coef, deg=0):
        """Create a monomial

        :param coef:  The coefficient of the monomial
        :param deg: The degree of the monomial, with a default value of 0
        :type deg: int
        """
        if isinstance(coef, Monomial):
            self.coef = coef.coef
            self.deg = coef.deg
        else:
            self.coef = Fraction(coef).limit_denominator(1000000)
            self.deg = int(deg)
        self.var = "x"

    def __repr__(self):
        return "Monomial({},{})".format(self.coef, self.deg)

    def __eq__(self, other: Any):
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, Monomial):
            return False
        return self.coef == other.coef and self.deg == other.deg

    def __bool__(self):
        return bool(self.coef)

    def __neg__(self):
        return Monomial(-self.coef, self.deg)

    def __mul__(self, other: Any):
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, (Monomial, Polynomial)):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        if isinstance(other, Polynomial):
            return other * self
        return Monomial(self.coef * other.coef, self.deg + other.deg)

    def __rmul__(self, other: Any) -> Any:
        return self.__mul__(other)

    def __add__(self, other: Any) -> Any:
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, (Monomial, Polynomial)):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        if isinstance(other, Polynomial):
            return other + self
        if other.deg == self.deg:
            return Monomial(self.coef + other.coef, self.deg)
        else:
            return Polynomial((self, other))

    def __radd__(self, other: Any) -> Any:
        return self.__add__(other)

    def __truediv__(self, other: Any) -> Any:
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, Monomial):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        return Monomial(self.coef / other.coef, self.deg - other.deg)

    def __pow__(self, exponent: Any) -> Any:
        return Monomial(self.coef, self.deg * exponent)

    def __str__(self):
        """

        :return: A human readable string of the monomial
        """
        string = ""
        if self.deg == 0:
            return str(self.coef)

        if self.coef == 1 or self.coef == -1:
            if self.coef == -1:
                string += "-"
            string += self.var
        else:
            string += str(self.coef) + self.var
        if self.deg > 1:
            string += "^" + str(self.deg)
        return string if string else '0'

    def html_str(self):
        string = ""
        if self.deg == 0:
            return str(self.coef)

        if self.coef == 1 or self.coef == -1:
            if self.coef == -1:
                string += "-"
            string += self.var
        else:
            string += str(self.coef) + self.var
        if self.deg > 1:
            string += "<sup>" + str(self.deg) + "</sup>"
        return string

    def eval_str(self, val):
        """Used to get an evaluable string of the monomial.

        This method returns a string which which can be used with the python eval function.

        :param val: The value to substitute with the variable
        :return: an evaluable string of the monomial which can be used with eval()
        :rtype: str
        """
        string = ""
        val = Fraction(val).limit_denominator(1000000)
        if self.deg == 0:
            return repr(self.coef)

        if self.coef == 1 or self.coef == -1:
            if self.coef == -1:
                string += "-"
            string += repr(val)
        else:
            string += repr(self.coef) + "*" + repr(val) + ""

        if self.deg > 1:
            string += "**" + str(self.deg)
        return string

    def __call__(self, val: Any):
        val = Fraction(val).limit_denominator(1000000)
        return self.coef * (val ** self.deg)

    def derive(self, n: int):
        """Derive the monomial

        :param n: The number of time the monomial will be derived
        :type n: int
        :return: The n-th derivative of the monomial
        :rtype: Monomial
        """
        mono = Monomial(self.deg * self.coef, self.deg - 1)
        if n == 1:
            return mono
        else:
            return mono.derive(n - 1)


class Polynomial:
    """Represent a polynomial.

    A polynomial consists of monomials.

    Usage
    -----

    >>> import polynomials
    >>> p = polynomials.Polynomial("x^4+1/3x^3")
    >>> q = polynomials.Polynomial("x^2+5/2x+1")
    >>> quot , rest = p/q
    >>> print(f"({p})/({q})={quot} and the remainder is {rest}")
    (x^4+1/3x^3)/(x^2+5/2x+1)=x^2-13/6x+53/12 and the remainder is -71/8x-53/12
    >>> print(p.derive())
    4x^3+x^2
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
                self.append(Polynomial(val))
        elif isinstance(expr, (Monomial, Polynomial)):
            self.append(expr)
        elif isinstance(expr, str):
            self.append(self.str_pol(expr))
        elif isinstance(expr, (Fraction, int, float)):
            self.append(Monomial(expr, 0))

    def deg(self):
        """The degree of a polynomial is the degree of the non null monomial with the highest degree

        :return: The highest degree within the non null monomials of the polynomial
        :rtype: int
        """
        return max(filter(lambda mono: mono.coef != 0, self), default=Monomial(0), key=lambda mono: mono.deg).deg

    def append(self, other, degree=None):
        """
        Add a monomial to the polynomial

        :param other: Any numeric value or a Monomial or any Polynomial
        :param degree: Degree of the monomial
        :type degree: int
        :return: None
        """
        if degree is None:
            if isinstance(other, Monomial):
                self.monomials.append(other)
            elif isinstance(other, Polynomial):
                self.monomials.extend(other)
            else:
                self.append(Polynomial(other))
        else:
            mono = Monomial(other, degree)
            mono.var = self.var
            self.append(mono)

    def pol_append(self, other):
        """
        Add the polynomial p monomials to the the current polynomial monomials

        :param other: The polynomial to pol_append
        :type other: Polynomial
        :return: None
        """
        for mono in other:
            self.append(mono)

    def __repr__(self):
        return f'Polynomial("{self!s}")'

    def __str__(self):
        """

        :return: A human readable string of the monomial
        """
        string = ""
        for mono in self:
            if not mono.coef == 0:
                if mono.coef > 0:
                    string += "+"
                string += str(mono)
        if string.startswith("+"):
            string = string[1:]
        return string if string else "0"

    def html_str(self):
        string = ""
        for mono in self:
            if not mono.coef == 0:
                if not mono == self[0]:
                    if mono.coef > 0:
                        string += "+"
                string += mono.html_str()
        if string.startswith("+"):
            string = string[1:]
        return string if string else "0"

    def eval_str(self, val):
        """Used to get an evaluable string of the polynomial.

        This method returns a string which can be used with the python eval function.

        :param val: The value to substitute with the variable
        :return: An evaluable string of the polynomial which can be used with eval()
        :rtype: str
        """
        string = ""
        for mono in self:
            if not mono.coef == 0:
                string += "+"
                string += mono.eval_str(val)

        return string[1:]

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

    def __contains__(self, monomial: Any):
        if isinstance(monomial, (int, float, Fraction)):
            monomial = Monomial(monomial)
        if not isinstance(monomial, Monomial):
            return False
        return monomial in self.monomials

    def copy(self):
        """
        Copy the polynomial

        :return: A copy of the polynomial
        :rtype: Polynomial
        """
        return Polynomial(self.monomials.copy())

    def __eq__(self, other: Any):
        if not isinstance(other, (Monomial, Polynomial, int, float, Fraction, str)):
            return False
        if not isinstance(other, Polynomial):
            other = Polynomial(other)
        reordered_self = self.reorder(with_null_coefs=True)
        other = other.reorder(with_null_coefs=True)
        if len(other) != len(reordered_self) or other.deg() != reordered_self.deg():
            return False
        return all([reordered_self[i] == other[i] for i in range(len(reordered_self))])

    def __add__(self, other: Any):
        self_copy = self.copy()
        self_copy.append(other)
        return self_copy.reorder()

    def __sub__(self, other: Any):
        return self.__neg__().__add__(other).__neg__()

    def __neg__(self):
        return Polynomial([-mono for mono in self])

    def __truediv__(self, other: Any):
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
            return self * Monomial(1 / other.coef)

        if not isinstance(other, Polynomial):
            other = Polynomial(other)

        if self.deg() < other.deg():
            return Polynomial(0), self

        else:
            self_copy = self.copy().reorder(with_null_coefs=True)
            other_copy = other.copy().reorder()
            quot = Polynomial()
            m1, m2 = self_copy[0], other_copy[0]

            while self_copy and m1.deg - m2.deg >= 0:
                m3 = m1 / m2
                quot.append(m3)
                max_deg = max(self_copy, key=lambda mono: mono.deg).deg
                self_copy = (self_copy - other_copy * m3).reorder(reverse=True, with_null_coefs=True, max_deg=max_deg)
                self_copy.pop(0)
                m1 = self_copy[0]

            if self_copy == 0:
                return quot.reorder()
            return quot.reorder(), self_copy.reorder()

    def __floordiv__(self, other: Any):
        quotient, _ = self / other
        return quotient

    def __mul__(self, other: Any):
        if not isinstance(other, (Polynomial, Monomial)):
            other = Polynomial(other)

        if isinstance(other, Monomial):
            poly = Polynomial()
            for mono in self:
                poly.append(other * mono)
            return poly.reorder()

        if isinstance(other, Polynomial):
            poly = Polynomial()
            for mono in other:
                poly.append(self * mono)
            return poly.reorder()

    def __rmul__(self, other: Any):
        return self.__mul__(other)

    def __radd__(self, other: Any):
        return self.__add__(other)

    def __rsub__(self, other: Any):
        return self.__sub__(other)

    def __pow__(self, exponent: int):
        pow_pol = Polynomial(1)
        for i in range(exponent):
            pow_pol = pow_pol * self
        return pow_pol.reorder()

    def __bool__(self):
        return bool(self.monomials)

    def __mod__(self, other):
        _, rest = self / other
        return rest

    def __call__(self, val: Any = Fraction(0)):
        if str(val).isalpha():
            poly = self.copy()
            poly.var = val
            return poly
        return sum(map(lambda mono: mono(val), self))

    def derive(self, n=1):
        """Derive the polynomial

        :param n: The number of time the polynomial will be derived
        :return: The n-th derivative of the monomial
        :rtype: Polynomial
        """
        poly = Polynomial()
        for mono in self:
            poly.append(mono.derive(n))
        return poly.reorder()

    # TODO: Separate 'reduce' and 'order' so that reduce will just add Monomial with same degree together and order will
    #  order monomials
    def reorder(self, reverse=True, with_null_coefs=False, max_deg=None):
        """Reorder the polynomial in order to have increasing or decreasing degrees of the monomials

        :param reverse: If True, the first monomial will be the monomial with the highest degree else it will be the
                        opposite, the first monomial will be the monomial with the lowest degree
        :type reverse: bool
        :param with_null_coefs: If False, the returned polynomial will not contain monomials with null coefficients.
        :type with_null_coefs: bool
        :param max_deg: The highest degree. The polynomial will be truncated and only monomial which degree are less or
                        equal to max_max_deg will be kept.
        :type max_deg: int
        :return: A polynomial with reordered monomial
        :rtype: Polynomial
        """
        monomials_list = []
        rg = range(self.deg() if max_deg is None else max_deg + 1)
        if reverse:
            rg = range(self.deg() if max_deg is None else max_deg, -1, -1)
        for i in rg:
            m_l = [mono for mono in self if mono.deg == i]

            mono = Monomial(0, i)
            for mon in m_l:
                mono = mono + mon
            if with_null_coefs or (mono != 0):
                monomials_list.append(mono)

        if max_deg is not None:
            return Polynomial(monomials_list)

        # trimming unnecessary null monomials
        stop = len(monomials_list)
        if reverse:
            monomials_list.reverse()
        for i in range(stop + 1):
            if not any(monomials_list[i:stop]):
                monomials_list = monomials_list[0:i]
                break
        if reverse:
            monomials_list.reverse()
        return Polynomial(monomials_list)

    @staticmethod
    def str_pol(expression):
        """Take a polynomial expression as a string and return the corresponding polynomial Object

        :param expression: The polynomial expression
        :type expression: str
        :return: A polynomial which monomials are those in the expression
        :rtype: Polynomial
        """
        monomials_list = []
        expression = expression.replace(" ", "")
        mono_regex = re.compile(r"(?P<coef>[+-]?[\d]*[./]?[\d]*)(?P<var>[Xx]?)[\^]?(?P<deg>[\d]*)")
        for mon in mono_regex.finditer(expression):
            mono_coef_string = mon.group('coef')
            mono = mono_coef_string + '1' if mono_coef_string in ('+', '-') else mono_coef_string \
                if mono_coef_string else '1'
            if mon.group('var'):
                coef = Fraction(mono)
                deg = int(mon.group('deg')) if mon.group('deg') else 1
                monomials_list.append(Monomial(coef, deg))
            elif mon.group('coef'):
                coef = Fraction(mono)
                deg = 0
                monomials_list.append(Monomial(coef, deg))
        return Polynomial(monomials_list)


class ModuloPolynomial(Polynomial):

    def __init__(self, expr, mod=5):
        super().__init__(expr)
        self.mod = mod
        # TODO: Monomials coefficients should be integers, not full fractions or floats
        self.__module_monomials()

    def __module_monomials(self):
        def mon_to_mod(mon, mod):
            mon.coef = mon.coef % mod
            return mon

        self.monomials = list(map(lambda mon: mon_to_mod(mon, self.mod), self.monomials))

    def reorder(self, reverse=True, with_null_coefs=False, max_deg=None):
        return ModuloPolynomial(super().reorder(reverse, with_null_coefs, max_deg), self.mod)

    def __repr__(self):
        pol_str = super(ModuloPolynomial, self).__repr__()
        return f"Modulo{pol_str[:-1]}, mod={self.mod})"

    def __neg__(self):
        return ModuloPolynomial(super(ModuloPolynomial, self).__neg__(), self.mod)

    def __eq__(self, other):
        if not isinstance(other, ModuloPolynomial):
            if isinstance(other, int):
                if other == 0:
                    s_o = self.reorder()
                    return len(s_o) == 1 and s_o[0] == 0
            return False
        if self.mod != other.mod:
            s_o, o_o = self.reorder(), other.reorder()
            return len(s_o) == len(o_o) == 1 and s_o[0] == o_o[0] == 0
        return super(ModuloPolynomial, self).__eq__(other.reorder().to_polynomial())

    def __mul__(self, other):
        if isinstance(other, (ModuloPolynomial, int)):
            if isinstance(other, int):
                return ModuloPolynomial(super(ModuloPolynomial, self).__mul__(other), self.mod).reorder()
            if other.mod == self.mod:
                res = super(ModuloPolynomial, self).__mul__(other.to_polynomial())
                return self.pol_mod_pol(res, self.mod).reorder()
            else:
                raise ValueError(f"The Polynomials modulos values don't match: {self.mod}!={other.mod}")
        raise ValueError(f"Cannot multiply {self.__class__.__name__} with objects of type {other.__class__.__name__}")

    def __add__(self, other: Any):
        if isinstance(other, ModuloPolynomial):
            if other.mod == self.mod:
                res = super(ModuloPolynomial, self).__add__(other.to_polynomial())
                return self.pol_mod_pol(res, self.mod).reorder()
            else:
                raise ValueError(f"The Polynomials modulos values don't match: {self.mod}!={other.mod}")
        raise ValueError(f"Cannot add {self.__class__.__name__} to objects of type {other.__class__.__name__}")

    @staticmethod
    def pol_mod_pol(pol: Polynomial, mod=5):
        return ModuloPolynomial(pol.monomials, mod)

    def to_polynomial(self):
        return Polynomial(self.monomials)


if __name__ == "__main__":
    z = Polynomial('X-2X^3+3/8')
    p1 = Polynomial("-X+2X^2+X^3-2+0x^5+0+0+0")
    w = Polynomial.str_pol("X^3+2X^2-2-X")
    p2 = Polynomial("X^2+1")
    print(*p1, p1.deg(), sep=', ')
    print(*p1.reorder(), sep=', ')
    print(p1, w, p1 == w)
    m = Monomial(1, 3)
    print("Testing the addition")
    print(f"({p1})+({p2})={p1 + p2}")
    print("Testing the multiplication")
    print(f"({p1})*({p2})={p1 * p2}")
    print("Testing the division")
    qot, rem = p1 / p2
    print(f"({p1})/({p2})={qot} and the remainder is {rem}")
    print("Testing derive once")
    print(f"{p1}(2/3)={p1(2 / 3)}")
    print("Testing derive twice")
    print(f"({p1 * p2})''={(p1 * p2).derive(2)}")

    t = Polynomial((m, '-x^6 -7', '7/3x', p2, '', '', '', ''))
    g = (Polynomial(-1) + 'x+2') * 'x+2'
    print(isinstance(Monomial('5/6').coef, Fraction))
    print(t, len(t), 'and', t.reorder(), len(t.reorder()))
    m = Monomial(0, 10)
    p1 = Polynomial((m, 'x', '2x^2')).reorder()
    print(p1, p1.deg(), len(p1))
