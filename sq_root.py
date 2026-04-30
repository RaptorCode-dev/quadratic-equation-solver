from core import BASE, BF_to_str, random_BF, Big_float, big_float_copy, BF_round
from mul import mul, short_mul
from subadd import sub, add
from str_to_big_float import str_to_BF, int_to_BF
import decimal

ROOT_OF_10 = Big_float(-18, [79331, 1683, 27766, 3162], 1)
constant_for_newton = str_to_BF('3')


def sq_root(number):
    number = big_float_copy(number)
    reciprosal_aproximation = first_aproximation(number)
    # reciprosal_sq_root_of_num = householder_algorithm(number, reciprosal_aproximation)
    reciprosal_sq_root_of_num = newton_algorithm(number, reciprosal_aproximation)
    sq_root_of_num = mul(number, reciprosal_sq_root_of_num, 2040)
    return sq_root_of_num


def first_aproximation(number):
    mantissa = number.get_mantissa()
    first_digit = mantissa[-1] 
    second_digit = mantissa[-2] if len(mantissa) > 1 else 0
    if second_digit != 0:
        aproximation = 1 / ((first_digit * 10**BASE + second_digit) ** 0.5)
        aproximation = f'{aproximation:.50f}'
        aproximation = str_to_BF(aproximation)
        if (number.get_exp() + BASE * len(mantissa)) % 2 == 0:
            new_exp =  aproximation.get_exp() - (number.get_exp() + BASE * (len(mantissa) - 2)) // 2
        else: 
            new_exp =  aproximation.get_exp() - (number.get_exp() + BASE * (len(mantissa) - 2)) // 2 - 1
    else:
        aproximation = 1 / (first_digit  ** 0.5)
        aproximation = f'{aproximation:.15f}'
        aproximation = str_to_BF(aproximation)
        new_exp =  aproximation.get_exp() - number.get_exp() // 2
    aproximation.set_exp(new_exp)
    aproximation.set_sign(1)
    if number.get_exp() % 2 == 1:
        aproximation = mul(aproximation, ROOT_OF_10)
    return aproximation




def newton_algorithm(number, aproximation, precision= 11):
    accuracy = 2
    for _ in range(precision):
        accuracy *= 2
        num = BF_round(number, accuracy + 10)
        yn = mul(mul(aproximation, aproximation, accuracy + 20), num, accuracy + 10)
        yn = short_mul(sub(constant_for_newton, yn), 5, -1)
        aproximation = mul(aproximation, yn, accuracy + 10)
    return aproximation

    

if __name__ == '__main__':
    decimal.getcontext().prec = 50000
    a = Big_float(0, [4], 1)
    a = sq_root(a)
    print(BF_to_str(a))
        


