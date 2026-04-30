from mul import mul
from class_1 import BASE, BF_round, BF_to_str, random_BF, str_to_BF, int_to_BF
from AddandSub import sub

from decimal import Decimal, getcontext
from time import perf_counter


def div(a, b):
    guess = first_approximation(b)
    inv_b = newton_reciprocal(b, guess)
    return mul(a, inv_b)


def first_approximation(x):
    mant = x.get_mantissa()
    sign = x.get_sign()
    if len(mant) <= 2:
        val = 1 / (mant[-1] if len(mant) == 1 else mant[-1] * 10**BASE + mant[-2])
        return str_to_BF(str(val))

    top = (
        mant[-1] * 10**(BASE * (len(mant) - 2)) +
        mant[-2] * 10**(BASE * (len(mant) - 3)) +
        mant[-3] * 10**(BASE * (len(mant) - 4))
    )

    approx = 10**(BASE * len(mant) + 1) // top
    approx = int_to_BF(approx)
    new_exp = approx.get_exp() - BASE * (len(mant) + 1) - x.get_exp() - 1
    approx.set_exp(new_exp)
    approx.set_sign(sign)

    return approx


def newton_reciprocal(x, guess, iterations=11):
    # итерации Ньютона: y = y * (2 - x*y)
    precision = 2

    for _ in range(iterations):
        precision <<= 1
        correction = sub(str_to_BF('2'), mul(BF_round(x, precision + 10), guess, precision + 10))
        guess = mul(guess, correction, precision + 20)

    return guess


if __name__ == '__main__':
    getcontext().prec = 50000

    for _ in range(5):
        a = random_BF()
        b = random_BF()

        expected = Decimal(BF_to_str(a)) / Decimal(BF_to_str(b))
        expected = f'{expected:.10000f}'

        t1 = perf_counter()
        result = div(a, b)
        t2 = perf_counter()

        result_str = BF_to_str(result)

        print("OK:", result_str[:10000] == expected[:10000])
        print("TIME:", t2 - t1)
        print("EXPECTED:", expected[:10000])
        print("RESULT  :", result_str[:10000])