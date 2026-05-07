from class_1 import BigFloat, BASE, BF_to_str, normalized, random_BF, BF_round
import math
from decimal import Decimal, getcontext
from time import perf_counter

getcontext().prec = 100000

BASE_LIMIT = 10 ** BASE

def bit_reverse(a):
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

cache = {}

def get_cache(half_len, invert):
    key = (half_len, invert)
    cached = cache.get(key)
    if cached is not None:
        return cached

    sign = 1 if invert else -1
    base_angle = sign * math.pi / half_len
    cos_b = math.cos(base_angle)
    sin_b = math.sin(base_angle)

    table = [0j] * half_len
    table[0] = 1 + 0j
    cr, ci = 1.0, 0.0
    for k in range(1, half_len):
        cr, ci = cr * cos_b - ci * sin_b, cr * sin_b + ci * cos_b
        table[k] = complex(cr, ci)

    cache[key] = table
    return table


def fft_core(a, invert):
    n = len(a)
    for idx in range(0, n, 2):
        u = a[idx]
        v = a[idx + 1]
        a[idx] = u + v
        a[idx + 1] = u - v

    length = 4
    while length <= n:
        half = length >> 1
        twiddles = get_cache(half, invert)
        start = 0
        while start < n:
            for j in range(half):
                idx = start + j
                idx2 = idx + half
                v = a[idx2] * twiddles[j]
                u = a[idx]
                a[idx] = u + v
                a[idx2] = u - v
            start += length
        length <<= 1


def fft_iter(a, invert=False):
    bit_reverse(a)
    fft_core(a, invert)
    if invert:
        n = len(a)
        inv_n = 1.0 / n
        for i in range(n):
            a[i] *= inv_n
    return a


def convolve_fft(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = [complex(x, 0) for x in a] + [0j] * (n - len(a))
    fb = [complex(x, 0) for x in b] + [0j] * (n - len(b))
    fft_iter(fa)
    fft_iter(fb)
    for i in range(n):
        fa[i] *= fb[i]
    fft_iter(fa, True)
    return [int(x.real + 0.5) for x in fa]


def make_carrys_after_mul(mantissa):
    accum = 0
    LIMIT = BASE_LIMIT
    for i in range(len(mantissa)):
        v = mantissa[i] + accum
        accum = v // LIMIT
        mantissa[i] = v - accum * LIMIT
    while accum:
        mantissa.append(accum % LIMIT)
        accum //= LIMIT
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
    abs_int = abs(integ)
    for i in range(len(mantissa)):
        mantissa[i] *= abs_int
    mantissa = make_carrys_after_mul(mantissa)
    sign = number.get_sign() * (1 if integ > 0 else -1)
    return BigFloat(number.get_exp() + exp_delta, mantissa, sign)


if __name__ == "__main__":
    getcontext().prec = 50000
    a, b = random_BF(), random_BF()
    mul(a, b)

    times = []
    for i in range(100):
        a = random_BF()
        b = random_BF()
        t1 = perf_counter()
        res = mul(a, b)
        t2 = perf_counter()
        times.append(t2 - t1)

        re = Decimal(BF_to_str(b)) * Decimal(BF_to_str(a))
        re = f'{re:.10000f}'
        bf = BF_to_str(res)
        print(f"OK: {bf[:10000] == re[:10000]}  TIME: {t2 - t1:.4f}s")

    times.sort()
    print(f"\nmedian={times[len(times)//2]:.4f}s, min={times[0]:.4f}s, mean={sum(times)/len(times):.4f}s")

