from typing import Any
import polynomials.Polynomial


class RationalPolynomial:
    def __init__(self, numerator, denominator: Any = 1):
        self.numerator = numerator if isinstance(numerator, polynomials.Polynomial)\
            else polynomials.Polynomial(numerator)
        self.denominator = denominator if isinstance(denominator, polynomials.Polynomial) \
            else polynomials.Polynomial(denominator)

    def __str__(self):
        return f"({self.numerator!s})/({self.denominator!s})"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.numerator!s}", "{self.denominator!s}")'

    def __neg__(self):
        return RationalPolynomial(-self.numerator, self.denominator)

    def __sub__(self, other):
        if not isinstance(other, RationalPolynomial):
            other = RationalPolynomial(other)
        return -other + self

    def __add__(self, other):
        if not isinstance(other, RationalPolynomial):
            other = RationalPolynomial(other)
        ds, do = self.denominator, other.denominator
        return RationalPolynomial(self.numerator * do + other.numerator * ds, ds * do)

    def __mul__(self, other):
        if not isinstance(other, RationalPolynomial):
            other = RationalPolynomial(other)
        return RationalPolynomial(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        if not isinstance(other, RationalPolynomial):
            other = RationalPolynomial(other)
        return RationalPolynomial(self.numerator * other.denominator, self.denominator * other.numerator)


if __name__ == "__main__":
    rp = RationalPolynomial("x+1/4", "x+1")
    rq = RationalPolynomial("x+4", "x-2")

    print(rp * rq)
    print(rp / rq)
    print(rq / 4)
    print(rp + rq)
    print(rp - rq)
    print(rp * 4)
    print(rp + 4)
