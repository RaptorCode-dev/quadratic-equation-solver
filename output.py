from time import perf_counter
from decimal import Decimal, getcontext, localcontext

from class_1 import BF_to_str, BigFloat
from solve import (
    ComplexBF,
    solve, get_solution_type, get_solution_x1, get_solution_x2,
)
from input import input_data


getcontext().prec = 100000
PRECISION = 10000

def normalize(s):
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return format(Decimal(s) + 0, f'.{PRECISION}f')


def format_value(v):
    if v is None:
        return None
    if isinstance(v, ComplexBF):
        im_s = BF_to_str(v.imag)
        sign = '-' if im_s.startswith('-') else '+'
        return f"{normalize(BF_to_str(v.real))} {sign} {normalize(im_s.lstrip('-'))}i"
    if isinstance(v, BigFloat):
        return normalize(BF_to_str(v))
    if isinstance(v, tuple):
        re, im = v
        sign = '-' if im < 0 else '+'
        return f"{normalize(str(re))} {sign} {normalize(str(abs(im)))}i"
    return normalize(str(v))


def decimal_solve(a_str, b_str, c_str):
    a, b, c = Decimal(a_str), Decimal(b_str), Decimal(c_str)
    if a == 0:
        if b == 0:
            return ('infinite_solutions' if c == 0 else 'no_solutions'), None, None
        return 'linear_solutions', -c / b, None
    d = b * b - 4 * a * c
    if d > 0:
        sq = d.sqrt()
        return 'different_solutions', (-b + sq) / (2 * a), (-b - sq) / (2 * a)
    if d == 0:
        return 'same_solutions', -b / (2 * a), None
    sq = (-d).sqrt()
    re, im = -b / (2 * a), sq / (2 * a)
    return 'complex_solutions', (re, im), (re, -im)


def output(coefs):
    t1 = perf_counter()
    sol = solve(coefs)
    my_time = perf_counter() - t1

    dec_type, dec_x1, dec_x2 = decimal_solve(BF_to_str(coefs.a), BF_to_str(coefs.b), BF_to_str(coefs.c))
    my_x1, my_x2 = format_value(get_solution_x1(sol)), format_value(get_solution_x2(sol))
    d_x1,  d_x2  = format_value(dec_x1), format_value(dec_x2)

    correct = get_solution_type(sol) == dec_type and (
        (my_x1 == d_x1 and my_x2 == d_x2) or
        (my_x1 == d_x2 and my_x2 == d_x1)
    )

    print(get_solution_type(sol))
    if my_x1 is not None: print(f"x1 = {my_x1}")
    if my_x2 is not None: print(f"x2 = {my_x2}")

    print()
    print(dec_type)
    if d_x1 is not None: print(f"x1 = {d_x1}")
    if d_x2 is not None: print(f"x2 = {d_x2}")

    print()
    print(f"мое время: {my_time:.4f} s")
    print(f"совпадение на {PRECISION} знаках: {'OK' if correct else 'FAIL'}")


if __name__ == '__main__':
    coefs = input_data()
    output(coefs)