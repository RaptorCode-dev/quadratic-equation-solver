from mul import mul
from class_1 import BASE, BigFloat
from helper import BF_round, int_to_BF
from AddandSub import sub


TWO = BigFloat(0, [2], 1)

def div(a, b):
    guess = first_approximation(b)
    inv_b = newton_reciprocal(b, guess)
    return mul(a, inv_b)


def first_approximation(x):
    mant = x.get_mantissa()
    sign = x.get_sign()
    if len(mant) <= 2:
        top = (mant[-1] * 10**(BASE * (len(mant) - 2))  if len(mant) == 1 else mant[-1] * 10**(BASE * (len(mant) - 2)) +
            mant[-2] * 10**(BASE * (len(mant) - 3)))
    else:
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
        correction = sub(TWO, mul(BF_round(x, precision + 10), guess, precision + 10))
        guess = mul(guess, correction, precision + 20)

    return guess
