from solve import *

def output(solution: Solution):
    sol_type = get_solution_type(solution)
    print(sol_type)
    if get_solution_x1(solution) is not None: print(f"x1 = {get_solution_x1(solution)}")
    if get_solution_x2(solution) is not None: print(f"x2 = {get_solution_x2(solution)}")

coefs = input_data()
result = solve(coefs)
output(result)