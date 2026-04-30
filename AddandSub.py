from class_1 import BigFloat, BASE, normalized, copy_BF, BF_to_str, str_to_BF, random_BF
from mul import short_mul
from decimal import Decimal, getcontext

from time import perf_counter

getcontext().prec = 100000

def add(a, b):
    sign_a = a.get_sign()
    sign_b = b.get_sign()
    a_copy = copy_BF(a)
    b_copy = copy_BF(b)
    a_aligned, b_aligned = align_numbers(a_copy, b_copy)

    if sign_a == sign_b:
        result = add_aligned_same_sign(a_aligned, b_aligned)
    else:
        result = subtract_aligned_same_sign(a_aligned, b_aligned)
    return normalized(result)


def sub(a, b):
    sign_a = a.get_sign()
    sign_b = b.get_sign()
    a_copy = copy_BF(a)
    b_copy = copy_BF(b)
    a_aligned, b_aligned = align_numbers(a_copy, b_copy)

    if sign_a == sign_b:
        result = subtract_aligned_same_sign(a_aligned, b_aligned)
    else:
        result = add_aligned_same_sign(a_aligned, b_aligned)
    return normalized(result)


def align_numbers(a, b):
    exp_a = a.get_exp()
    exp_b = b.get_exp()

    if exp_b > exp_a:
        b = shift_number_to_exponent(b, exp_b, exp_a)
    elif exp_a > exp_b:
        a = shift_number_to_exponent(a, exp_a, exp_b)
    return a, b


def shift_number_to_exponent(number, current_exp, target_exp):
    exp_diff = current_exp - target_exp
    whole_blocks = exp_diff // BASE
    remainder = exp_diff % BASE
    shifted = short_mul(number, 10**remainder, -exp_diff)
    mantissa = shifted.get_mantissa()[::-1]
    mantissa += [0] * whole_blocks
    shifted.mantissa = mantissa[::-1]

    return shifted


def add_aligned_same_sign(a, b):
    mantissa_a = a.get_mantissa()
    mantissa_b = b.get_mantissa()

    if len(mantissa_a) >= len(mantissa_b):
        result_mantissa = add_mantissas(mantissa_a, mantissa_b)
    else:
        result_mantissa = add_mantissas(mantissa_b, mantissa_a)

    return BigFloat(a.get_exp(), result_mantissa, a.get_sign())


def subtract_aligned_same_sign(a, b):
    exp = a.get_exp()
    sign = a.get_sign()
    mantissa_a = a.get_mantissa()
    mantissa_b = b.get_mantissa()

    if is_greater_or_equal_aligned(a, b):
        result_mantissa = subtract_mantissas(mantissa_a, mantissa_b)
    else:
        result_mantissa = subtract_mantissas(mantissa_b, mantissa_a)
        sign = -sign
    return BigFloat(exp, result_mantissa, sign)


def subtract_mantissas(minuend, subtrahend):
    borrow = 0

    for i in range(len(subtrahend)):
        minuend[i] -= subtrahend[i] + borrow
        borrow = 0
        if minuend[i] < 0:
            minuend[i] += 10**BASE
            borrow = 1
    if borrow == 1:
        i = len(subtrahend)
        while i < len(minuend) - 1 and minuend[i] == 0:
            minuend[i] = 99999
            i += 1
        try:
            minuend[i] -= 1
        except IndexError:
            return [0]
    return minuend

def add_mantissas(longer, shorter):
    carry = 0
    for i in range(len(shorter)):
        longer[i] += shorter[i] + carry
        carry = 0
        if longer[i] >= 10**BASE:
            longer[i] -= 10**BASE
            carry = 1
    if carry == 1:
        if len(longer) == len(shorter):
            longer.append(1)
        else:
            longer[i + 1] += 1
    return longer


def is_greater_or_equal_aligned(a, b):
    mantissa_a = a.get_mantissa()
    mantissa_b = b.get_mantissa()

    if len(mantissa_a) > len(mantissa_b):
        return True
    elif len(mantissa_a) < len(mantissa_b):
        return False
    else:
        i = 0
        while True:
            i -= 1
            if -i == len(mantissa_a) and mantissa_a[i] == mantissa_b[i]:
                return True
            if mantissa_a[i] > mantissa_b[i]:
                return True
            elif mantissa_a[i] < mantissa_b[i]:
                return False


if __name__ == "__main__":
    t_fft = 0
    for _ in range(50):
        a = random_BF()
        b = random_BF()

        expected = Decimal(BF_to_str(a)) - Decimal(BF_to_str(b))
        expected = f'{expected:.50000f}'

        start = perf_counter()
        result = BF_to_str(sub(a, b))
        t_fft += perf_counter() - start

        print(expected[:10000])
        print(result[:10000])

        print(expected[:10000] == result[:10000])
    print("sub:", t_fft / 50)