from class_1 import BF_to_str, BigFloat
from solve import (
    ComplexBF,
    solve, get_solution_type, get_solution_x1, get_solution_x2,
)
from input import input_data


def _increment_digits(digits: str) -> str:
    """Прибавляет 1 к строке цифр (может добавиться ведущая 1)."""
    out = list(digits)
    i = len(out) - 1
    while i >= 0:
        d = int(out[i])
        if d < 9:
            out[i] = str(d + 1)
            return ''.join(out)
        out[i] = '0'
        i -= 1
    return '1' + ''.join(out)


def smart_round_string(s: str, threshold: int = 50) -> str:
    """Чистит артефакты конечной точности в десятичной записи:
       длинные серии девяток округляются вверх, длинные серии нулей в хвосте — обрезаются.
       Серия из >= threshold одинаковых цифр считается артефактом."""
    sign = ''
    if s.startswith('-'):
        sign, s = '-', s[1:]

    if '.' not in s:
        return sign + s

    int_part, frac = s.split('.')

    # 1) Длинная серия девяток внутри дробной части — округление вверх
    n = len(frac)
    i = 0
    while i < n:
        if frac[i] == '9':
            j = i
            while j < n and frac[j] == '9':
                j += 1
            if j - i >= threshold:
                head = int_part + frac[:i]                 # всё до серии 9-к
                bumped = _increment_digits(head)
                # Восстанавливаем границу целой/дробной части
                if len(bumped) == len(head) + 1:
                    new_int  = bumped[:len(int_part) + 1]
                    new_frac = bumped[len(int_part) + 1:]
                else:
                    new_int  = bumped[:len(int_part)]
                    new_frac = bumped[len(int_part):]
                new_frac = new_frac.rstrip('0')
                return sign + (new_int + '.' + new_frac if new_frac else new_int)
            i = j
        else:
            i += 1

    # 2) Длинный хвост нулей — просто обрезать
    stripped = frac.rstrip('0')
    if len(frac) - len(stripped) >= threshold:
        return sign + (int_part + '.' + stripped if stripped else int_part)

    return sign + s


def format_value(v):
    if isinstance(v, ComplexBF):
        re_s = smart_round_string(BF_to_str(v.real))
        im_s = smart_round_string(BF_to_str(v.imag))
        if im_s.startswith('-'):
            return f"{re_s} - {im_s[1:]}i"
        return f"{re_s} + {im_s}i"
    if isinstance(v, BigFloat):
        return smart_round_string(BF_to_str(v))
    return str(v)


def output(solution):
    print(get_solution_type(solution))
    x1 = get_solution_x1(solution)
    x2 = get_solution_x2(solution)
    if x1 is not None:
        print(f"x1 = {format_value(x1)}")
    if x2 is not None:
        print(f"x2 = {format_value(x2)}")


if __name__ == '__main__':
    coefs = input_data()
    result = solve(coefs)
    output(result)