from fractions import Fraction
from typing import Any

import polynomials.Polynomial
import polynomials.Monomial


class ModuloPolynomial(polynomials.Polynomial):

    def __init__(self, expr, mod=5):
        super().__init__(expr)
        self.mod = mod
        # TODO: Monomials coefficients should be integers, not full fractions or floats
        self.__module_monomials()

    def __module_monomials(self):
        self.monomials = list(map(lambda mon: mon % self.mod, self.monomials))

    def append(self, other, degree=None):
        if isinstance(other, ModuloPolynomial):
            other = other.to_polynomial()
        super().append(other, degree)

    def reorder(self, reverse=True, with_null_coefs=False, max_deg=None):
        mono_list = super().reorder(reverse, with_null_coefs, max_deg).monomials
        if not with_null_coefs:
            mono_list = list(filter(None, mono_list))
        return ModuloPolynomial(mono_list, self.mod)

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
        s_o, o_o = self.reorder(), other.reorder()
        if self.mod != other.mod:
            return len(s_o) == len(o_o) == 1 and s_o[0] == o_o[0] == 0
        return s_o.to_polynomial() == o_o.to_polynomial()

    def __mul__(self, other):
        if isinstance(other, (ModuloPolynomial, int)):
            if isinstance(other, int):
                return ModuloPolynomial(super(ModuloPolynomial, self).__mul__(other), self.mod).reorder()
            if other.mod == self.mod:
                res = super(ModuloPolynomial, self).__mul__(other.to_polynomial())
                return ModuloPolynomial(res, self.mod).reorder()
            else:
                raise ValueError(f"The Polynomials modulos values don't match: {self.mod}!={other.mod}")
        raise ValueError(f"Cannot multiply {self.__class__.__name__} with objects of type {other.__class__.__name__}")

    def __add__(self, other: Any):
        if isinstance(other, ModuloPolynomial):
            if other.mod == self.mod:
                res = super(ModuloPolynomial, self).__add__(other.to_polynomial())
                return ModuloPolynomial(res, self.mod).reorder()
            else:
                raise ValueError(f"The Polynomials modulos values don't match: {self.mod}!={other.mod}")
        raise ValueError(f"Cannot add {self.__class__.__name__} to objects of type {other.__class__.__name__}")

    def to_polynomial(self):
        return polynomials.Polynomial(self.reorder().monomials)
