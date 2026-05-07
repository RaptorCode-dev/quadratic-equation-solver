from mul import mul, short_mul
from class_1 import BASE, BF_round, BF_to_str,BigFloat,  random_BF, str_to_BF, copy_BF
from AddandSub import sub

from decimal import Decimal, getcontext
from time import perf_counter

root_10 = BigFloat(-18, [79331, 1683, 27766, 3162], 1)
constant_newton = BigFloat(0, [3], 1)

def sqrt_bigfloat(n):
    x = copy_BF(n)
    approximation = first_approximation(x)
    inv_sqrt = newton_reciprocal(x, approximation)
    return mul(x, inv_sqrt)


def first_approximation(x):
    mant = x.get_mantissa()

    top = mant[-1] * 10**BASE + (mant[-2] if len(mant) >= 2 else 0)
    approx = 1 / top ** 0.5
    approx = f'{approx:.50f}'
    approx = str_to_BF(approx)

    total_parity = (x.get_exp() + BASE * len(mant)) % 2
    if total_parity == 0:
        new_exp = approx.get_exp() - (x.get_exp() + BASE * (len(mant) - 2)) // 2
    else:
        new_exp = approx.get_exp() - (x.get_exp() + BASE * (len(mant) - 2)) // 2 - 1

    approx.set_exp(new_exp)
    approx.set_sign(1)

    if total_parity == 1:
        approx = mul(approx, root_10)

    return approx



def newton_reciprocal(x, guess, iterations=11):
    precision = 2
    for _ in range(iterations):
        precision <<= 1
        num = BF_round(x, precision + 10)
        yn = mul(mul(guess, guess, precision + 20), num, precision + 20)
        yn = short_mul(sub(constant_newton, yn), 5, -1)
        guess = mul(guess, yn, precision + 20)

    return guess


if __name__ == '__main__':
    getcontext().prec = 100000

    for i in range(100):
        a = random_BF()
        a.set_sign(1)

        t1 = perf_counter()
        res = sqrt_bigfloat(a)
        t2 = perf_counter()

        bf_str = BF_to_str(res)

        dec_val = Decimal(BF_to_str(a)).sqrt()
        dec_str = f'{dec_val:.15000f}'

        ok = bf_str[:10000] == dec_str[:10000]

        print(f"TEST {i + 1}:")
        print("OK:", ok)
        print("TIME:", t2 - t1)

        if not ok:
            print("INPUT   :", BF_to_str(a)[:200])
            print("EXP   :", a.exp)
            print("LEN   :", len(a.mantissa))
            print("EXPECTED:", dec_str[:200])
            print("RESULT  :", bf_str[:200])

        print("-" * 50)