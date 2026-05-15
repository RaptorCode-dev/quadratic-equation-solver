from class_1 import (
    Coefs, Solution, SolutionState,
    BigFloat, copy_BF, mantissa_is_zero
)
from AddandSub import add, sub
from mul import mul, short_mul
from div import div
from sqrt import sqrt_bigfloat


class ComplexBF:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag


def is_zero(bf: BigFloat) -> bool:
    return mantissa_is_zero(bf.mantissa)


def is_negative(bf: BigFloat) -> bool:
    return bf.sign == -1 and not is_zero(bf)


def neg(bf: BigFloat) -> BigFloat:
    res = copy_BF(bf)
    res.set_sign(-bf.sign)
    return res


def get_a(coef: Coefs) -> BigFloat: return coef.a
def get_b(coef: Coefs) -> BigFloat: return coef.b
def get_c(coef: Coefs) -> BigFloat: return coef.c

def get_solution_type(s: Solution) -> str: return s.sol_type
def get_solution_x1(s: Solution): return s.x1
def get_solution_x2(s: Solution): return s.x2


def calc_discriminant(a, b, c):
    b_sq = mul(b, b)
    four_ac = short_mul(mul(a, c), 4)
    return sub(b_sq, four_ac)


def is_linear(coefs):
    return is_zero(get_a(coefs))


def linear_solution(b, c):
    if is_zero(b):
        if is_zero(c):
            return Solution(sol_type=SolutionState.INFINITE_SOLUTIONS)
        return Solution(sol_type=SolutionState.NO_SOLUTIONS)
    return Solution(sol_type=SolutionState.LINEAR_SOLUTIONS, x1=div(neg(c), b))


def quadratic_solution(a, b, c):
    d = calc_discriminant(a, b, c)
    two_a = short_mul(copy_BF(a), 2)

    if is_negative(d):
        abs_d = copy_BF(d); abs_d.set_sign(1)
        sqrt_abs_d = sqrt_bigfloat(abs_d)
        real_part = div(neg(b), two_a)
        imag_part = div(sqrt_abs_d, two_a)
        x1 = ComplexBF(real_part, imag_part)
        x2 = ComplexBF(copy_BF(real_part), neg(imag_part))
        return Solution(sol_type=SolutionState.COMPLEX_SOLUTIONS, x1=x1, x2=x2)

    if is_zero(d):
        x1 = div(neg(b), two_a)
        return Solution(sol_type=SolutionState.SAME_SOLUTIONS, x1=x1)

    sqrt_d = sqrt_bigfloat(d)
    if is_negative(b):
        x1 = div(add(neg(b), sqrt_d), two_a)         # -b + √D, оба положительные
    else:
        x1 = div(sub(neg(b), sqrt_d), two_a)         # -b - √D, оба ≤ 0
    #x2 = c / (a * x1)
    x2 = div(c, mul(a, x1))
    return Solution(sol_type=SolutionState.DIFFERENT_SOLUTIONS, x1=x1, x2=x2)


def solve(coefs: Coefs) -> Solution:
    if is_linear(coefs):
        return linear_solution(get_b(coefs), get_c(coefs))
    return quadratic_solution(get_a(coefs), get_b(coefs), get_c(coefs))
