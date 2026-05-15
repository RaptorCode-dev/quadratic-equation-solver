class Coefs:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class SolutionState:
    INFINITE_SOLUTIONS = "infinite_solutions"
    NO_SOLUTIONS = "no_solutions"
    LINEAR_SOLUTIONS = "linear_solutions"
    QUADRATIC_SOLUTIONS = "quadratic_solutions"
    COMPLEX_SOLUTIONS = "complex_solutions"
    SAME_SOLUTIONS = "same_solutions"
    DIFFERENT_SOLUTIONS = "different_solutions"


class Solution:
    def __init__(self, sol_type, x1=None, x2=None):
        self.sol_type = sol_type
        self.x1 = x1
        self.x2 = x2

BASE = 5
class BigFloat:
    __slots__ = ('exp', 'mantissa', 'sign', 'kind')
    def __init__(self, exp=0, mantissa=[0], sign=1, kind='finite'):
        self.exp = exp
        self.mantissa = mantissa[:]
        self.sign = sign
        self.kind = kind          # 'finite', 'inf' или 'nan'

    def get_sign(self):
        return self.sign

    def get_exp(self):
        return self.exp

    def get_mantissa(self):
        return self.mantissa

    def set_sign(self, sign):
        self.sign = sign

    def set_exp(self, exp):
        self.exp = exp

    def set_mantissa(self, mantissa):
        self.mantissa = mantissa[:]

    def is_finite(self):
        return self.kind == 'finite'

    def is_nan(self):
        return self.kind == 'nan'

    def is_inf(self):
        return self.kind == 'inf'

class ComplexBF:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag