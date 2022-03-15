# (C) John Robotane 2019-2022
# Created on 5/12/2019 2:50 PM

from fractions import Fraction

from polynomials import Monomial
from polynomials import Polynomial

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
