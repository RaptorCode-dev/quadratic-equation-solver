from class_1 import Coefs, Solution, SolutionState, ComplexBF
from helper import is_zero, get_a, get_b, get_c, copy_BF, is_negative, neg, bf_to_float, make_nan, float_to_bf, has_special
from AddandSub import add, sub
from mul import mul, short_mul
from div import div
from sqrt import sqrt_bigfloat

import math


def special_solve(coefs):
    a, b, c = bf_to_float(coefs.a), bf_to_float(coefs.b), bf_to_float(coefs.c)

    if math.isnan(a) or math.isnan(b) or math.isnan(c):
        nan = make_nan()
        return Solution(sol_type=SolutionState.DIFFERENT_SOLUTIONS, x1=nan, x2=copy_BF(nan))
    d = b * b - 4 * a * c
    if math.isnan(d):
        nan = make_nan()
        return Solution(sol_type=SolutionState.DIFFERENT_SOLUTIONS, x1=nan, x2=copy_BF(nan))

    if d < 0:
        # комплексные корни: re = -b/(2a), im = sqrt(|d|)/(2a)
        re = -b / (2 * a)
        im = math.sqrt(-d) / (2 * a)
        x1 = ComplexBF(float_to_bf(re), float_to_bf(im))
        x2 = ComplexBF(float_to_bf(re), float_to_bf(-im))
        return Solution(sol_type=SolutionState.COMPLEX_SOLUTIONS, x1=x1, x2=x2)

    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    return Solution(
        sol_type=SolutionState.DIFFERENT_SOLUTIONS,
        x1=float_to_bf(x1),
        x2=float_to_bf(x2),)


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
    if has_special(coefs):
        return special_solve(coefs)
    if is_linear(coefs):
        return linear_solution(get_b(coefs), get_c(coefs))
    return quadratic_solution(get_a(coefs), get_b(coefs), get_c(coefs))