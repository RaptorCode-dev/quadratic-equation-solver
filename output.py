from solve import solve
from input import input_data
from helper import get_solution_type, get_solution_x1, get_solution_x2, BF_to_str, decimal_solve, format_decimal, format_value, is_correct

from time import perf_counter

PRECISION = 10000

def output(coefs):
    t1 = perf_counter()
    sol = solve(coefs)
    my_time = perf_counter() - t1

    a_str = BF_to_str(coefs.a)
    b_str = BF_to_str(coefs.b)
    c_str = BF_to_str(coefs.c)

    t1 = perf_counter()
    dec_x1, dec_x2 = decimal_solve(a_str, b_str, c_str)
    dec_time = perf_counter() - t1

    my_x1_str = format_value(get_solution_x1(sol)) if get_solution_x1(sol) is not None else None
    my_x2_str = format_value(get_solution_x2(sol)) if get_solution_x2(sol) is not None else None

    dec_x1  = format_decimal(dec_x1)
    dec_x2  = format_decimal(dec_x2)

    correct = is_correct(my_x1_str, my_x2_str, dec_x1, dec_x2)

    print(get_solution_type(sol))
    if my_x1_str is not None: print(f"x1 = {my_x1_str}")
    if my_x2_str is not None: print(f"x2 = {my_x2_str}")

    print()
    if dec_x1 is not None: print(f"x1 = {dec_x1}")
    if dec_x2 is not None: print(f"x2 = {dec_x2}")

    print()
    print(f"мое время:     {my_time:.4f} s")
    print(f"время Decimal: {dec_time:.4f} s")
    print(f"совпадение на {PRECISION} знаках: {'OK' if correct else 'FAIL'}")


if __name__ == '__main__':
    coefs = input_data()
    output(coefs)