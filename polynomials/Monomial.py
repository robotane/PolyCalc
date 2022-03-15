from fractions import Fraction
from typing import Any

import polynomials.Polynomial as Polynomial


class Monomial:
    """Represent a monomial.

    A monomial has a coefficient and a degree
    The default value of the degree is 0, but you should provide
    at least a coefficient in any numeric format, it will be converted
    to a fractions.Fraction type.
    """

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
        if not isinstance(other, (Monomial, Polynomial.Polynomial)):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        if isinstance(other, Polynomial.Polynomial):
            return other * self
        return Monomial(self.coef * other.coef, self.deg + other.deg)

    def __rmul__(self, other: Any) -> Any:
        return self.__mul__(other)

    def __add__(self, other: Any) -> Any:
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, (Monomial, Polynomial.Polynomial)):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        if isinstance(other, Polynomial.Polynomial):
            return other + self
        if other.deg == self.deg:
            return Monomial(self.coef + other.coef, self.deg)
        else:
            return Polynomial.Polynomial((self, other))

    def __radd__(self, other: Any) -> Any:
        return self.__add__(other)

    def __truediv__(self, other: Any) -> Any:
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, Monomial):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        return Monomial(self.coef / other.coef, self.deg - other.deg)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, Fraction)):
            other = Monomial(other)
        if not isinstance(other, Monomial):
            raise ValueError("Cannot add monomial to...")  # TODO: Find a best Error message
        return other/self

    def __pow__(self, exponent: Any) -> Any:
        return Monomial(self.coef, self.deg * exponent)

    def __mod__(self, other: Any) -> Any:
        return Monomial(self.coef % other, self.deg)

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
