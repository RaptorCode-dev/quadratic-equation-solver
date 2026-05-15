from random import randrange, choice
from class_1 import BigFloat, BASE, Coefs, Solution, ComplexBF
import math
from decimal import Decimal, getcontext

getcontext().prec = 100000
PRECISION = 10000

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
    return BigFloat(BF.get_exp(), BF.get_mantissa(), BF.get_sign(), BF.kind)


def make_inf(sign=1):
    return BigFloat(0, [0], sign, 'inf')


def make_nan():
    return BigFloat(0, [0], 1, 'nan')

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
    if BigFloat_num.is_nan():
        return 'nan'
    if BigFloat_num.is_inf():
        return '-inf' if BigFloat_num.get_sign() == -1 else 'inf'
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

def negative(x):
    x.set_sign(x.get_sign() * -1)
    return x



def is_zero(bf: BigFloat) -> bool:
    return mantissa_is_zero(bf.mantissa)


def is_negative(bf: BigFloat) -> bool:
    return bf.sign == -1 and not is_zero(bf)


def neg(bf: BigFloat) -> BigFloat:
    res = copy_BF(bf)
    res.set_sign(-bf.sign)
    return res


def get_a(coef: Coefs) -> BigFloat: return coef.a
def get_b(coef: Coefs) -> BigFloat: return coef.b
def get_c(coef: Coefs) -> BigFloat: return coef.c

def get_solution_type(s: Solution) -> str: return s.sol_type
def get_solution_x1(s: Solution): return s.x1
def get_solution_x2(s: Solution): return s.x2


def has_special(coefs):
    return any(not x.is_finite() for x in (coefs.a, coefs.b, coefs.c))

def float_to_bf(x):
    if math.isnan(x):
        return make_nan()
    if math.isinf(x):
        return make_inf(1 if x > 0 else -1)
    return str_to_BF(repr(x))


def bf_to_float(bf):
    if bf.is_nan():
        return math.nan

    if bf.is_inf():
        return math.inf if bf.sign == 1 else -math.inf
    s = BF_to_str(bf).strip().lower()
    if 'e' in s:
        base, exp = s.split('e')
        if int(exp) > 308:
            return math.inf if bf.sign == 1 else -math.inf

    if not s or s in {'.', '+', '-'}:
        return math.nan

    return float(s)

def format_value(v):
    if isinstance(v, ComplexBF):
        re_s = BF_to_str(v.real)
        im_s = BF_to_str(v.imag)
        if im_s.startswith('-'):
            return f"{re_s} - {im_s[1:]}i"
        return f"{re_s} + {im_s}i"
    if isinstance(v, BigFloat):
        return BF_to_str(v)
    return str(v)


def format_decimal(v):
    if v is None:
        return None
    if isinstance(v, tuple):
        re, im = v
        re_s = format(re, f'.{PRECISION + 100}f')
        im_s = format(abs(im), f'.{PRECISION + 100}f')
        sign = '-' if float(im) < 0 else '+'
        return f"{re_s} {sign} {im_s}i"
    return format(v, f'.{PRECISION + 100}f')

def is_special_str(s):
    s = s.lstrip('+-').lower()
    return s in ('inf', 'infinity', 'nan')


def special_decimal_solve(a_str, b_str, c_str):
    def to_f(s):
        s_low = s.strip().lower()
        if s_low in ('inf', '+inf', 'infinity', '+infinity'):  return math.inf
        if s_low in ('-inf', '-infinity'): return - math.inf
        if s_low == 'nan': return math.nan
        return float(s)

    a, b, c = to_f(a_str), to_f(b_str), to_f(c_str)
    def to_dec(x):
        if math.isnan(x): return Decimal('NaN')
        if math.isinf(x): return Decimal('Infinity') if x > 0 else Decimal('-Infinity')
        return Decimal(repr(x))

    if math.isnan(a) or math.isnan(b) or math.isnan(c):
        nan = Decimal('NaN')
        return nan, nan

    d = b * b - 4 * a * c
    if math.isnan(d):
        nan = Decimal('NaN')
        return nan, nan

    if d < 0:
        re = -b / (2 * a)
        im = math.sqrt(-d) / (2 * a)
        return (to_dec(re), to_dec(im)), (to_dec(re), to_dec(-im))

    sq = math.sqrt(d)
    return to_dec((-b + sq) / (2 * a)), to_dec((-b - sq) / (2 * a))


def decimal_solve(a_str, b_str, c_str):
    if is_special_str(a_str) or is_special_str(b_str) or is_special_str(c_str):
        return special_decimal_solve(a_str, b_str, c_str)

    a = Decimal(a_str)
    b = Decimal(b_str)
    c = Decimal(c_str)

    if a == 0:
        if b == 0:
            return None, None
        return -c / b, None

    d = b * b - 4 * a * c
    if d > 0:
        sq = d.sqrt()
        return (-b + sq) / (2 * a), (-b - sq) / (2 * a)
    if d == 0:
        return -b / (2 * a), None
    sq = (-d).sqrt()
    re = -b / (2 * a)
    im = sq / (2 * a)
    return (re, im), (re, -im)



def normalize_num_str(s):
    s = s.strip()
    if s.lower() in ('nan', 'inf', '-inf', '+inf', 'infinity', '-infinity'):
        return s.lower()

    sign = ''
    if s.startswith('-'):
        sign, s = '-', s[1:]
    elif s.startswith('+'):
        s = s[1:]

    if '.' in s:
        int_part, _, frac_part = s.partition('.')
        frac_part = frac_part.rstrip('0')
    else:
        int_part, frac_part = s, ''

    int_part = int_part.lstrip('0') or '0'
    result = f"{int_part}.{frac_part}" if frac_part else int_part
    if result == '0':
        return '0'
    return sign + result


def match(my_str, dec_str):
    if my_str is None and dec_str is None:
        return True
    if my_str is None or dec_str is None:
        return False
    if 'i' in my_str:
        re_a, _, im_a = my_str.partition(' ')
        sign_a, _, im_a = im_a.partition(' ')
        re_b, _, im_b = dec_str.partition(' ')
        sign_b, _, im_b = im_b.partition(' ')
        im_a = im_a.rstrip('i')
        im_b = im_b.rstrip('i')
        return (sign_a == sign_b
                and normalize_num_str(re_a)[:PRECISION] == normalize_num_str(re_b)[:PRECISION]
                and normalize_num_str(im_a)[:PRECISION] == normalize_num_str(im_b)[:PRECISION])
    return normalize_num_str(my_str)[:PRECISION] == normalize_num_str(dec_str)[:PRECISION]


def is_correct(my_x1, my_x2, dec_x1, dec_x2):
    return ((match(my_x1, dec_x1) and match(my_x2, dec_x2))
            or (match(my_x1, dec_x2) and match(my_x2, dec_x1)))

