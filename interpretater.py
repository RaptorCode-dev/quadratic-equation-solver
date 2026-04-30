from abc import ABC, abstractmethod
from class_1 import BigFloat, BASE
import sys


def fail(msg):
    print(msg)
    sys.exit(1)


def find_sep(text):
    for ch in ('.', ','):
        if ch in text:
            return text.index(ch)
    return -1


def find_exp(text):
    for ch in ('e', 'E'):
        if ch in text:
            return text.index(ch)
    return -1


class Interpreter(ABC):
    @abstractmethod
    def interpret(self):
        pass


class ComputationContext:
    def __init__(self):
        self.a = BigFloat()
        self.b = BigFloat()
        self.c = BigFloat()

    def set_a(self, v): self.a = v
    def set_b(self, v): self.b = v
    def set_c(self, v): self.c = v


class ExpressionParser(Interpreter):
    def __init__(self, expression, context):
        self.expression = expression
        self.context = context

    def interpret(self):
        parts = self.expression.split()
        if len(parts) != 3:
            fail("Ожидалось 3 числа")

        a = NumberParser(parts[0]).interpret()
        b = NumberParser(parts[1]).interpret()
        c = NumberParser(parts[2]).interpret()

        self.context.set_a(a)
        self.context.set_b(b)
        self.context.set_c(c)


class NumberParser(Interpreter):
    def __init__(self, text):
        self.text = text.strip()

    def interpret(self):
        if not self.text:
            fail("Пустая строка")

        sign, core = self.parse_sign(self.text)
        mant, exp_part = self.split_exp(core)

        exp = ExponentParser(exp_part).interpret()
        dot = DotParser(mant).interpret()

        mant = self.remove_dot(mant)
        mant = MantissaParser(mant).interpret()

        bf = BigFloat()
        bf.set_sign(sign)
        bf.set_exp(exp + dot)
        bf.set_mantissa(mant)

        return bf

    def parse_sign(self, text):
        if text[0] in '+-':
            return (-1 if text[0] == '-' else 1), text[1:]
        return 1, text

    def split_exp(self, text):
        idx = find_exp(text)
        if idx == -1:
            return text, None

        mant = text[:idx]
        exp = text[idx + 1:]

        if not exp:
            fail("Ошибка: отсутствует экспонента")

        return mant, exp

    def remove_dot(self, text):
        idx = find_sep(text)
        if idx == -1:
            return text
        return text[:idx] + text[idx + 1:]


class DotParser(Interpreter):
    def __init__(self, text):
        self.text = text

    def interpret(self):
        idx = find_sep(self.text)
        left = self.text if idx == -1 else self.text[:idx]

        if len(left) > 1 and left.startswith('0'):
            fail("Ошибка: ведущие нули")
        if idx == -1:
            return 0

        return idx - len(self.text) + 1


class ExponentParser(Interpreter):
    def __init__(self, text):
        self.text = text

    def interpret(self):
        if self.text is None:
            return 0
        sign = 1
        text = self.text
        if text[0] in '+-':
            sign = -1 if text[0] == '-' else 1
            text = text[1:]
        if not text or not text.isdigit():
            fail("Некорректная экспонента")

        return sign * int(text)


class MantissaParser(Interpreter):
    def __init__(self, text):
        self.text = text

    def interpret(self):
        if not self.text:
            fail("Пустая мантисса")

        res = []
        n = len(self.text)
        for i in range(n, 0, -BASE):
            chunk = self.text[max(0, i - BASE):i]
            res.append(DigitChunkParser(chunk).interpret())

        return res


class DigitChunkParser(Interpreter):
    def __init__(self, chunk):
        self.chunk = chunk

    def interpret(self):
        if not self.chunk.isdigit():
            fail("Ошибка: недопустимые символы")
        return int(self.chunk)


class SignParser(Interpreter):
    def __init__(self, text):
        self.text = text

    def interpret(self):
        return -1 if self.text[0] == '-' else 1


if __name__ == '__main__':
    s = '123.45e-2 21424 14134'

    ctx = ComputationContext()
    ExpressionParser(s, ctx).interpret()

    print(ctx.a.sign, ctx.a.exp, ctx.a.mantissa)