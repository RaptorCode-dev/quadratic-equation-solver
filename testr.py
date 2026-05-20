from class_1 import Coefs
from helper import random_BF, BF_to_str
from AddandSub import sub, add
from mul import mul
from div import div
from sqrt import sqrt_bigfloat
from solve import solve

from decimal import Decimal, getcontext
from time import perf_counter


getcontext().prec = 100000
PRECISION = 10000


def compare(my_bf, true_dec, precision=PRECISION):
    my_norm  = format(Decimal(BF_to_str(my_bf)) + 0, f'.{precision}f')
    dec_norm = format(true_dec, f'.{precision}f')
    return my_norm[:precision] == dec_norm[:precision]


def timed(op, *args):
    t1 = perf_counter()
    res = op(*args)
    return res, perf_counter() - t1


def run_op(name, my_op, dec_op):
    if name == 'sqrt':
        a = random_BF(); a.set_sign(1)
        my_res, t = timed(my_op, a)
        true_res = dec_op(Decimal(BF_to_str(a)))
    else:
        a, b = random_BF(), random_BF()
        my_res, t = timed(my_op, a, b)
        true_res = dec_op(Decimal(BF_to_str(a)), Decimal(BF_to_str(b)))
    return t, compare(my_res, true_res)


def benchmark(prec=10):
    ops = [
        ('сложение',  'add',  add,           lambda a, b: a + b),
        ('вычитание', 'sub',  sub,           lambda a, b: a - b),
        ('умножение', 'mul',  mul,           lambda a, b: a * b),
        ('деление',   'div',  div,           lambda a, b: a / b),
        ('корень',    'sqrt', sqrt_bigfloat, lambda a: a.sqrt()),
    ]
    for label, name, my_op, dec_op in ops:
        times, fails = [], 0
        for _ in range(prec):
            t, ok = run_op(name, my_op, dec_op)
            times.append(t)
            if not ok:
                fails += 1
        avg = sum(times) / prec
        status = 'OK' if fails == 0 else f'FAIL ({fails}/{prec})'
        print(f"{avg:.6f}s  {label:10s}  {status}")


def sq_solve_bench(prec=100):
    times, fails = [], 0
    for _ in range(prec):
        a, b, c = random_BF(), random_BF(), random_BF()

        sol, t = timed(solve, Coefs(a, b, c))
        times.append(t)

        ad, bd, cd = Decimal(BF_to_str(a)), Decimal(BF_to_str(b)), Decimal(BF_to_str(c))

        if ad == 0:
            ok = bd == 0 or compare(sol.x1, -cd / bd)
        else:
            d = bd * bd - 4 * ad * cd
            if d > 0:
                sq = d.sqrt()
                x1d, x2d = (-bd + sq) / (2 * ad), (-bd - sq) / (2 * ad)
                ok = ((compare(sol.x1, x1d) and compare(sol.x2, x2d)) or
                      (compare(sol.x1, x2d) and compare(sol.x2, x1d)))
            else:
                re = -bd / (2 * ad)
                im = (-d).sqrt() / (2 * ad)
                re_ok = compare(sol.x1.real, re) and compare(sol.x2.real, re)
                im_ok = ((compare(sol.x1.imag,  im) and compare(sol.x2.imag, -im)) or
                         (compare(sol.x1.imag, -im) and compare(sol.x2.imag,  im)))
                ok = re_ok and im_ok
        if not ok:
            fails += 1

    avg = sum(times) / prec
    status = 'OK' if fails == 0 else f'FAIL ({fails})'
    print(f"{avg:.6f}s  квадратка   {status}")


if __name__ == '__main__':
    #benchmark()
    sq_solve_bench()