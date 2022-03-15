import unittest

from polynomials import Polynomial, Monomial, ModuloPolynomial


class MonomialTestCase(unittest.TestCase):
    # def setUp(self) -> None:
    #     self.p = Polynomial("x+1")
    #     self.q = Polynomial("x+4")

    def test_addition(self):
        m1 = Monomial(1, 1)
        m2 = Monomial(2, 1)
        m3 = Monomial(1 / 2, 3)
        p1 = Polynomial("x+1")
        sum_m2_m3 = m2 + m3
        sum_p1_m2 = p1 + m2
        sum_m2_p1 = m2 + p1
        self.assertEqual(Monomial(3, 1), m1 + m2)
        self.assertIsInstance(sum_m2_m3, Polynomial)
        self.assertEqual(Polynomial("1/2x^3+2x"), sum_m2_m3)
        self.assertEqual(sum_p1_m2, sum_m2_p1)

    def test_multiplication(self):
        m1 = Monomial(1, 1)
        m2 = Monomial(2, 2)
        m3 = Monomial(1 / 2, 3)
        self.assertEqual(Monomial(2, 3), m1 * m2)
        self.assertEqual(Monomial(1, 5), m3 * m2)

    def test_division(self):
        pass


class PolynomialTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Polynomial("x+1")
        self.q = Polynomial("x+4")

    def test_addition(self):
        p = Polynomial("x+1")
        q = Polynomial("x+4")
        s = Polynomial("2x+5")
        self.assertEqual(s, p + q)

    def test_subtraction(self):
        p = Polynomial("3x+1")
        q = Polynomial("x+4")
        s = Polynomial("2x-3")
        self.assertEqual(s, p - q)

    def test_multiplication(self):
        p = Polynomial("x+1")
        q = Polynomial("x+4")
        m = Polynomial("x^2+5x+4")
        self.assertEqual(m, p * q)

    def test_division(self):
        p = Polynomial("3x^3+1")
        q = Polynomial("x+4")
        r = (Polynomial("3x^2-12x+48"), Polynomial("-191"))
        self.assertEqual(r, p / q)
        self.assertEqual(Polynomial("x^3+1/3"), p / 3)
        self.assertEqual(Polynomial("9/2x^3+3/2"), p / (2 / 3))

    def test_equality(self):
        self.assertEqual(0, Polynomial(0))
        self.assertEqual(0, Polynomial((Monomial(0, 0), Monomial(0, 0))))
        self.assertEqual(0, Polynomial((Monomial(-1, 4), Monomial(1, 4))))


class ModuloPolynomialTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Polynomial("x+1")
        self.q = Polynomial("x+4")

    def test_addition(self):
        p1 = ModuloPolynomial("x+1")
        p2 = ModuloPolynomial("x+4")
        p3 = ModuloPolynomial("7x-6+5x^3-15")
        s = ModuloPolynomial("2x")
        self.assertEqual(s, p1 + p2)
        self.assertEqual(ModuloPolynomial("3x+3"), p2 + p3)
        self.assertIsInstance(-p2-p3, ModuloPolynomial)

    def test_equality(self):
        self.assertEqual(0, ModuloPolynomial(0))
        self.assertEqual(ModuloPolynomial(0, 4), ModuloPolynomial(0, 6))
        self.assertEqual(ModuloPolynomial(0), ModuloPolynomial((Monomial(0, 0), Monomial(0, 0))))
        self.assertEqual(ModuloPolynomial(0), ModuloPolynomial((Monomial(4, 4), Monomial(1, 4))))
        reorder = ModuloPolynomial((Monomial(4, 4), Monomial(1, 4))).reorder()
        print(*reorder)
        self.assertEqual(1, len(reorder))


if __name__ == '__main__':
    unittest.main()
