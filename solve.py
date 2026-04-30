from class_1 import *

def get_a(coef: Coefs) -> BigFloat:
    return coef.a

def get_b(coef: Coefs) -> BigFloat:
    return coef.b

def get_c(coef: Coefs) -> BigFloat:
    return coef.c

def get_solution_type(solution: Solution) -> str:
    return solution.sol_type

def get_solution_x1(solution: Solution) -> BigFloat:
    return solution.x1

def get_solution_x2(solution: Solution) -> BigFloat:
    return solution.x2

def calc_discriminant(a, b, c):
    four = BigFloat('4') * a * c
    return b * b - four

def is_linear(coef: Coefs) -> bool:
    return get_a(coef).is_zero

def liner_solution(b, c) -> Solution:
    if b.is_zero:
        if c.is_zero:
            return Solution(sol_type=SolutionState.INFINITE_SOLUTIONS)
        else:
            return Solution(sol_type=SolutionState.NO_SOLUTIONS)
    return Solution(sol_type=SolutionState.LINEAR_SOLUTIONS, x1= -c / b)

def get_roots_by_discriminant(a, b, d):
    if d < 0:
        real = -b / (BigFloat('2') * a)
        imag = d / (BigFloat('2') * a)
        x1 = complex(real, imag)
        x2 = complex(real, -imag)
    else:
        sqrt_d = d ** 0.5
        x1 = (-b + sqrt_d) / (BigFloat('2') * a)
        x2 = (-b - sqrt_d) / (BigFloat('2') * a)

    return x1, x2

def quadratic_solution(a, b, c) -> Solution:
    discr = BigFloat(str(calc_discriminant(a, b, c)))
    x1, x2 = get_roots_by_discriminant(a, b, discr)
    if discr < 0:
        return Solution(sol_type=SolutionState.COMPLEX_SOLUTIONS, x1=x1, x2=x2)
    if mantissa_is_zero(discr.mantissa):
        return Solution( sol_type=SolutionState.SAME_SOLUTIONS, x1=x1)
    else:
        return Solution(sol_type=SolutionState.DIFFERENT_SOLUTIONS, x1=x1, x2=x2)




def solve(coefs: Coefs) -> Solution:
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    if is_linear(coefs):
        return liner_solution(b, c)
    else:
        return quadratic_solution(a, b, c)