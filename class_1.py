from random import randrange, choice

class Coefs:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class SolutionState:
    INFINITE_SOLUTIONS = "infinite_solutions"
    NO_SOLUTIONS = "no_solutions"
    LINEAR_SOLUTIONS = "linear_solutions"
    QUADRATIC_SOLUTIONS = "quadratic_solutions"
    COMPLEX_SOLUTIONS = "complex_solutions"
    SAME_SOLUTIONS = "same_solutions"
    DIFFERENT_SOLUTIONS = "different_solutions"


class Solution:
    def __init__(self, sol_type, x1=None, x2=None):
        self.sol_type = sol_type
        self.x1 = x1
        self.x2 = x2

BASE = 5
class BigFloat:
    __slots__ = ('exp', 'mantissa', 'sign')
    def __init__(self, exp=0, mantissa=[0], sign=1):
        self.exp = exp
        self.mantissa = mantissa[:]
        self.sign = sign

    def get_sign(self):
        return self.sign

    def get_exp(self):
        return self.exp

    def get_mantissa(self):
        return self.mantissa

    def set_sign(self, sign):
        self.sign = sign

    def set_exp(self, exp):
        self.exp = exp

    def set_mantissa(self, mantissa):
        self.mantissa = mantissa[:]

def normalized(bigfloat_num):
    mantissa = bigfloat_num.get_mantissa()
    sign = bigfloat_num.get_sign()
    new_exp = bigfloat_num.get_exp()
    len_old_mantissa = len(mantissa)
    if mantissa_is_zero(mantissa):
        return make_zero(mantissa)
    else:
        if mantissa_starts_with_zero(mantissa):
            mantissa = processing_starting_zeros(mantissa)
            new_exp = set_new_exp_after_starting_zero_processing(bigfloat_num, len_old_mantissa, mantissa)
        if mantissa_ends_with_zero(mantissa):
            mantissa = ending_zero_processing(mantissa)
    return BigFloat(new_exp, mantissa, sign)

def mantissa_is_zero(mantissa):
    return all(x == 0 for x in mantissa)


def make_zero(mantissa):
    mantissa = [0]
    return BigFloat(0, mantissa, 1)


def mantissa_starts_with_zero(mantissa):
    return mantissa[0] == 0


def processing_starting_zeros(mantissa):
    while mantissa[0] == 0:
        del mantissa[0]
    return mantissa

def set_new_exp_after_starting_zero_processing(big_float_num, len_old_mantissa, new_mantissa):
    len_new_mantissa = len(new_mantissa)
    old_exp = big_float_num.get_exp()
    new_exp = (len_old_mantissa - len_new_mantissa) * BASE + old_exp
    return new_exp


def mantissa_ends_with_zero(mantissa):
    return mantissa[-1] == 0


def ending_zero_processing(mantissa):
    while mantissa[-1] == 0:
        del mantissa[-1]
    return mantissa


def add_zeros_to_mantissa_blocks(mantissa):
    for i in range(1, len(mantissa)):
            if len(mantissa[i]) < BASE:
                mantissa[i] = '0' * (BASE - len(mantissa[i])) + mantissa[i]
    return mantissa

def copy_BF(BF):
    exp = BF.get_exp()
    mantissa = BF.get_mantissa()
    sign = BF.get_sign()
    return BigFloat(exp, mantissa, sign)

def str_to_BF(s):
    s = s.strip().lower()
    if not s:
        return BigFloat()

    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]

    exp = 0
    if 'e' in s:
        idx = s.index('e')
        exp = int(s[idx + 1:] or 0)
        s = s[:idx]

    if '.' in s:
        idx = s.index('.')
        frac_len = len(s) - idx - 1
        s = s.replace('.', '')
        exp -= frac_len
    s = s.lstrip('0') or '0'

    mantissa = []
    for i in range(len(s), 0, -BASE):
        start = max(0, i - BASE)
        mantissa.append(int(s[start:i]))
    return BigFloat(exp, mantissa, sign)


def BF_to_str(BigFloat_num):
    mantissa = BigFloat_num.get_mantissa()
    exp = BigFloat_num.get_exp()
    sign = BigFloat_num.get_sign()
    big_num_str = mantissa_to_str(mantissa)
    if exp < 0:
        big_num_str = insert_point(big_num_str, exp)
    elif exp > 0:
        big_num_str = insert_zeros(big_num_str, exp)
    if sign == -1:
        big_num_str = insert_sign(big_num_str)
    return big_num_str


def insert_point(mantissa_str, exp):
    if abs(exp) > len(mantissa_str):
        mantissa_str = '0.' + '0' * (abs(exp) - len(mantissa_str)) + mantissa_str
    elif abs(exp) == len(mantissa_str):
        mantissa_str = '0.' + mantissa_str
    else:
        mantissa_str = mantissa_str[:exp] + '.' + mantissa_str[exp:]
    return mantissa_str


def insert_zeros(mantissa_str, exp):
    mantissa_str = mantissa_str + '0' * exp
    return mantissa_str


def insert_sign(mantissa_str):
    return '-' + mantissa_str


def mantissa_to_str(mantissa):
        mantissa = mantissa[::-1]
        mantissa = list(map(str, mantissa))
        mantissa = add_zeros_to_mantissa_blocks(mantissa)
        mantissa = ''.join(mantissa)
        return mantissa

def random_BF():
    mantissa = []
    exp = randrange(-1000, 1000)
    prec = choice([2000, 1999])
    for _ in range(prec):
        elem = randrange(10000, 100000)
        mantissa.append(elem)
    sign = choice([-1, 1])
    return normalized(BigFloat(exp, mantissa, sign))

def BF_round(num, precision):
    mantissa = num.get_mantissa()
    exp = num.get_exp()
    old_len = len(mantissa)
    if old_len < precision:
        return num
    mantissa = mantissa[-precision:]
    exp = exp + (old_len - len(mantissa)) * BASE
    num = BigFloat(exp, mantissa, num.get_sign())
    return num

def int_to_BF(number):
    return str_to_BF(str(number))

if __name__ == '__main__':
    print(BF_to_str(random_BF()), end=' ')
    print(BF_to_str(random_BF()), end=' ')
    print(BF_to_str(random_BF()))
