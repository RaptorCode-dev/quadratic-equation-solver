from class_1 import BigFloat, BASE, normalized, copy_BF, BF_to_str, random_BF
from mul import short_mul
from decimal import Decimal, getcontext

from time import perf_counter

getcontext().prec = 100000

def add(a, b):
    a, b = align(copy_BF(a), copy_BF(b))
    if a.get_sign() == b.get_sign():
        return normalized(aligned_add(a, b))
    return normalized(aligned_sub(a, b))


def sub(a, b):
    b_neg = copy_BF(b)
    b_neg.set_sign(-b_neg.get_sign())
    return add(a, b_neg)


def align(a, b):
    exp_a, exp_b = a.get_exp(), b.get_exp()
    if exp_a > exp_b:
        a = shift_to_exponent(a, exp_a, exp_b)
    elif exp_b > exp_a:
        b = shift_to_exponent(b, exp_b, exp_a)
    return a, b


def shift_to_exponent(number, current_exp, target_exp):
    exp_diff = current_exp - target_exp
    whole_blocks = exp_diff // BASE
    remainder = exp_diff % BASE
    shifted = short_mul(number, 10**remainder, -exp_diff)
    mantissa = shifted.get_mantissa()[::-1] + [0] * whole_blocks
    shifted.mantissa = mantissa[::-1]
    return shifted


def aligned_add(a, b):
    ma, mb = a.get_mantissa(), b.get_mantissa()
    longer, shorter = (ma, mb) if len(ma) >= len(mb) else (mb, ma)
    return BigFloat(a.get_exp(), add_mantissas(longer, shorter), a.get_sign())


def aligned_sub(a, b):
    ma, mb = a.get_mantissa(), b.get_mantissa()
    sign = a.get_sign()
    if mantissa_ge(a, b):
        result = subtract_mantissas(ma, mb)
    else:
        result = subtract_mantissas(mb, ma)
        sign = -sign
    return BigFloat(a.get_exp(), result, sign)


def add_mantissas(longer, shorter):
    carry = 0
    for i in range(len(shorter)):
        longer[i] += shorter[i] + carry
        carry = 0
        if longer[i] >= 10**BASE:
            longer[i] -= 10**BASE
            carry = 1
    if carry:
        if len(longer) == len(shorter):
            longer.append(1)
        else:
            longer[i + 1] += 1
    return longer


def subtract_mantissas(minuend, subtrahend):
    borrow = 0
    for i in range(len(subtrahend)):
        minuend[i] -= subtrahend[i] + borrow
        borrow = 0
        if minuend[i] < 0:
            minuend[i] += 10**BASE
            borrow = 1
    if borrow:
        i = len(subtrahend)
        while i < len(minuend) - 1 and minuend[i] == 0:
            minuend[i] = 99999
            i += 1
        try:
            minuend[i] -= 1
        except IndexError:
            return [0]
    return minuend


def mantissa_ge(a, b):
    ma, mb = a.get_mantissa(), b.get_mantissa()
    if len(ma) != len(mb):
        return len(ma) > len(mb)
    for i in range(len(ma) - 1, -1, -1):
        if ma[i] != mb[i]:
            return ma[i] > mb[i]
    return True


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