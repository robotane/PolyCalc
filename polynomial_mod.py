#! /usr/bin/env python3
# -*- coding:Utf8 -*-

# (C) John Robotane 5/12/2019 2:50 PM
from modulo import *


class Monome(object):

    def __init__(self, coef, deg=0, mod=5):
        if not type(coef) is NZ:
            coef = NZ(coef, mod)
        self.coef = coef
        self.deg = deg
        self.mod = mod

    def __repr__(self):
        s = ""
        if self.deg == 0:
            return str(self.coef)
        if (self.coef == 1):
            # s+="+"
            s += "X"
        else:
            s += str(self.coef) + "X"
        if self.deg > 1:
            s += "^" + str(self.deg)
        return s

    def __mul__(self, f):
        if not (type(f) is Polynome or type(f) is Monome):
            f = Monome(f)

        if type(f) is Monome:
            q = Polynome(mod=self.mod)
            for m in self.monomes:
                q.m_add(f.coef * m.coef, f.deg + m.deg)
            q.reduc_ord()

            return q

        if type(f) is Polynome:
            q = Polynome(mod=self.mod)
            for m in f.monomes:
                q.append(self * m)
            q.reduc_ord()
        return q


class Polynome(object):

    def __init__(self, m=None, mod=5):
        self.monomes = []
        self.var = "X"
        self.mod = mod
        if not m == None:
            if not type(m) is Monome:
                m = Monome(m, 0, mod)
            self.monomes.append(m)

    def deg(self):
        deg = 0
        for m in self.monomes:
            deg = max(deg, m.deg)
        return deg

    def m_add(self, f, c=None, mod=None):
        if mod == None:
            mod = self.mod
        if not c == None:
            if type(f) is NZ:
                self.monomes.append(Monome(f, c))
            else:
                self.monomes.append(Monome(f, c, mod))
        else:
            if type(f) is NZ:
                self.monomes.append(Monome(f))
            else:
                self.monomes.append(f)
        self.reduc_ord()

    def append(self, p):
        for m in p.monomes:
            self.m_add(m)

    def __repr__(self):
        s = ""
        for m in self.monomes:
            if not m.coef == 0:
                if not m == self.monomes[0]:
                    if m.coef > 0:
                        s += "+"
                s += str(m)
            # if not m.coef==1 or m.deg==0:
        #					s+=str(m.coef)
        #				if m.deg>1:
        #					s+=self.var+"^"+str(m.deg)
        #				elif m.deg ==1:
        #					s+=self.var
        return s

    def __add__(self, p):
        s = Polynome(0, mod=self.mod)
        s.monomes = self.monomes.copy()
        if not type(p) is type(self):
            p = Polynome(p, mod=self.mod)
        s.append(p)
        s.reduc_ord()
        return s

    def __sub__(self, p):
        return self.__add__(-p)

    def __neg__(self):
        p = Polynome(mod=self.mod)
        for m in self.monomes:
            p.m_add(-m.coef, m.deg)
        return p

    # def fill(self,rev=True):
    #		s=[]
    #		r=list(range(self.deg()+1))
    #		if rev:
    #			r.reverse()

    #		for i in r:
    #			l=[m for m in self.monomes if m.deg==i]

    #			if  len(l)==0:
    #				c=Fraction(0)
    #			else:
    #				c=Fraction(0)
    #				for m in l:
    #					c = c+m.coef
    #			s.append(Monome(c,i))
    #		self.monomes=s

    def __truediv__(self, p):
        if not (type(p) is Polynome or type(p) is Monome):
            p = Monome(p, mod=self.mod)
            return self * Monome(p.coef.inv(), -p.deg, self.mod)

        if type(p) is Monome:
            p = Polynome(p, mod=self.mod)

        if self.deg() < p.deg():
            return Polynome(0, mod=self.mod), p

        else:
            p1 = self.copy()
            p2 = p.copy()
            quot = Polynome(mod=self.mod)
            m1, m2 = p1.monomes[0], p2.monomes[0]

            while True:
                m = Monome(m1.coef / m2.coef, m1.deg - m2.deg, self.mod)
                quot.m_add(m)
                p1 = p1 - p2 * m
                p1.monomes.pop(0)
                m1 = p1.monomes[0]
                if m1.deg - m2.deg < 0:
                    break
            return quot, p1

    def __mul__(self, f):
        if not (type(f) is Polynome or type(f) is Monome):
            f = Monome(f, mod=self.mod)

        if type(f) is Monome:
            q = Polynome(mod=self.mod)
            for m in self.monomes:
                q.m_add(f.coef * m.coef, f.deg + m.deg)
            q.reduc_ord()

            return q

        if type(f) is type(Polynome()):
            q = Polynome(mod=self.mod)
            for m in f.monomes:
                q.append(self * m)
            q.reduc_ord()
            return q

    def copy(self):
        p = Polynome(mod=self.mod)
        p.monomes = self.monomes.copy()
        return p

    def reduc_ord(self, rev=True):
        s = []
        r = list(range(self.deg() + 1))
        if rev:
            r.reverse()

        for i in r:
            l = [m for m in self.monomes if m.deg == i]

            if l:
                c = NZ(0, self.mod)
                for m in l:
                    c = c + m.coef
                s.append(Monome(c, i, mod=self.mod))
        self.monomes = s
    # return s


def str_pol(s, mod=5):
    p = Polynome(mod=mod)
    scoef, sdeg = "", ""
    pc, pd = False, False
    pcoef, pdeg = NZ(0, mod), 0
    neg = s[0] == "-"
    i = 0
    # print(s)
    for c in s:

        if c.upper() == p.var:
            pc = True
        # print("var")
        if c == "^":
            pd = True
        if (c.isdigit()) and not pc:
            scoef += c
        # print("dig")
        if c.isdigit() and pd:
            sdeg += c
        if c == "+" or c == "-" or i == len(s) - 1:
            if not scoef:
                # print("vi")
                if neg:
                    pcoef = NZ(-1, mod)
                else:
                    pcoef = NZ(1, mod)
            else:
                # print(scoef)
                pcoef = NZ(int(scoef), mod)
                # print(pcoef)
                if neg:
                    pcoef = -pcoef

            if pc and not pd:
                pdeg = 1
            elif pc and pd:
                pdeg = int(sdeg)
            if not pc:
                pdeg = 0
            p.m_add(pcoef, pdeg)
            # print(scoef,sdeg)
            scoef, sdeg = "", ""
            pc, pd = False, False
            pcoef, pdeg = NZ(0, mod), 0
            neg = c == "-"
        i += 1
    # print(p)
    return p


if __name__ == "__main__":
    n = 5
    # pol1=input("Entrez p: ")
    # pol2=input("Entrez q: ")
    p = str_pol("x^4+2x^3+x^2+1", n)
    m = Monome(2, 2)

    q = str_pol("2x^2+x+1", n)

    # print("m=",m)
    print("p=", p)
    print("q=", q)
    g = str_pol("5x", 6)
    print("p/q=", p / q)
# print(g)
# print("g/m=",g/m)
