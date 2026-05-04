from class_1 import BigFloat, BASE, BF_to_str, normalized, random_BF, BF_round
import math
from decimal import Decimal, getcontext
import sys
from time import perf_counter

sys.set_int_max_str_digits(0)

getcontext().prec = 100000

BASE_LIMIT = 10 ** BASE

def bit_reverse_permute(a):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]


def get_wlen(length, invert):
    angle = 2 * math.pi / length
    if not invert:
        angle *= -1
    return complex(math.cos(angle), math.sin(angle))


def fft_step(a, start, length, wlen):
    w = 1
    half = length // 2

    for j in range(start, start + half):
        u = a[j]
        v = a[j + half] * w

        a[j] = u + v
        a[j + half] = u - v

        w *= wlen


def fft_core(a, invert):
    n = len(a)
    length = 2

    while length <= n:
        wlen = get_wlen(length, invert)

        for i in range(0, n, length):
            fft_step(a, i, length, wlen)

        length <<= 1


def normalize(a):
    n = len(a)
    for i in range(n):
        a[i] /= n


def fft_iter(a, invert=False):
    bit_reverse_permute(a)
    fft_core(a, invert)
    if invert:
        normalize(a)
    return a


def convolve_fft(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = list(map(complex, a)) + [0] * (n - len(a))
    fb = list(map(complex, b)) + [0] * (n - len(b))
    fft_iter(fa)
    fft_iter(fb)
    for i in range(n):
        fa[i] *= fb[i]
    fft_iter(fa, True)
    return [int(x.real + 0.5) for x in fa]

def make_carrys_after_mul(mantissa):
    accum = 0
    for i in range(len(mantissa)):
        mantissa[i] += accum
        accum = mantissa[i] // BASE_LIMIT
        mantissa[i] %= BASE_LIMIT
    while accum:
        mantissa.append(accum % BASE_LIMIT)
        accum //= BASE_LIMIT
    return mantissa


def mul(a: BigFloat, b: BigFloat, precision=2050) -> BigFloat:
    sign = a.sign * b.sign
    exp = a.exp + b.exp
    res = convolve_fft(a.mantissa, b.mantissa)
    res = make_carrys_after_mul(res)
    result = normalized(BigFloat(exp, res, sign))
    if precision != 0:
        result = BF_round(result, precision)
    return result


def short_mul(number, integ, exp_delta=0):
    mantissa = number.get_mantissa()
    for i in range(len(mantissa)):
        mantissa[i] *= abs(integ)
    mantissa = make_carrys_after_mul(mantissa)
    sign = number.get_sign() * (1 if integ > 0 else -1)
    return BigFloat(number.get_exp() + exp_delta, mantissa, sign)


if __name__ == "__main__":
    getcontext().prec = 50000

    for i in range(10):
        a = random_BF()
        b = random_BF()

        re = Decimal(BF_to_str(b)) * Decimal(BF_to_str(a))
        re = f'{re:.10000f}'

        t1 = perf_counter()
        res = mul(a, b)
        t2 = perf_counter()

        bf = BF_to_str(res)

        print("OK:", bf[:10000] == re[:10000])
        print("TIME:", t2 - t1)

        print("EXPECTED:", re[:10000])
        print("RESULT  :", bf[:10000])