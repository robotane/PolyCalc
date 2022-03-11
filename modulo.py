# ! /usr/bin/env python
# -*- coding:Utf8 -*-

# (C) John Robotane 5/12/2019 1:30 PM

class NZ(object):

    def mod():
        doc = "The mod property."

        def fget(self):
            return self._mod

        def fset(self, value):
            self._mod = value

        def fdel(self):
            del self._mod

        return locals()

    mod = property(**mod())

    def val():
        doc = "The val property."

        def fget(self):
            return self._val

        def fset(self, value):
            self._val = value

        def fdel(self):
            del self._val

        return locals()

    val = property(**val())

    def __init__(self, val, mod=5):
        # if abs(val)>=mod:
        #    self.val=val%mod
        # else:
        self.val = val % mod
        self.mod = mod

    def __str__(self):
        return str(self.val)

    def __add__(self, n):
        n = self._NZide(n)
        if self.mod == n.mod:  # use assert instead
            # s=self.val+n.val
            # s=s%self.mod
            return NZ(self.val + n.val, self.mod)
        raise ValueError("Numbers modulo don't match!")

    def __mul__(self, n):
        n = self._NZide(n)
        if self.mod == n.mod:  # use assert instead
            # s=self.val*n.val
            # s=s%self.mod
            return NZ(self.val * n.val, self.mod)
        raise ValueError("Numbers modulo don't match!")

    def __eq__(self, n):
        n = self._NZide(n)
        if (self.mod == n.mod):
            return self.val == n.val
        raise ValueError("Numbers modulo don't match!")

    def __ne__(self, n):
        n = self._NZide(n)
        if self.mod == n.mod:
            return self.val != n.val
        raise ValueError("Numbers modulo don't match!")

    def __lt__(self, n):
        n = self._NZide(n)
        if (self.mod == n.mod):
            return self.val < n.val
        raise ValueError("Numbers modulo don't match!")

    def __le__(self, n):
        n = self._NZide(n)
        if (self.mod == n.mod):
            return self.val <= n.val
        raise ValueError("Numbers modulo don't match!")

    def __gt__(self, n):
        n = self._NZide(n)
        if (self.mod == n.mod):
            return self.val > n.val
        raise ValueError("Numbers modulo don't match!")

    def __ge__(self, n):
        n = self._NZide(n)
        if (self.mod == n.mod):
            return self.val <= n.val
        raise ValueError("Numbers modulo don't match!")

    def _NZide(self, n):
        m = n
        if not isinstance(n, NZ):
            m = NZ(n, self.mod)
        return m

    def _raise_mod_err(self):
        raise ValueError("Numbers modulo don't match!")

    def __neg__(self):
        return NZ(-self.val, self.mod)

    def __sub__(self, n):
        return self.__add__(-n)

    def __invert__(self):
        for i in range(self.mod):
            if self * i == 1:
                return NZ(i, self.mod)
        raise ValueError("{} is not inversible in Z/{}Z".format(self, self.mod))

    def __truediv__(self, n):
        n = self._NZide(n)
        if (self.mod == n.mod):  # use assert instead
            if not n.val == 0:
                return self * ~n
            else:
                raise ZeroDivisionError("Division by zero")
        raise ValueError("Numbers modulo don't match!")


if __name__ == "__main__":
    a = NZ(7, 8)
    b = NZ(3, 8)
    print(~b * a)
