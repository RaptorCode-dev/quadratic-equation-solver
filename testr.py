from class_1 import random_BF, BF_to_str
from AddandSub import sub, add
from mul import mul
from div import div


from decimal import Decimal
from time import perf_counter


def compare(ans, trueans, precision = 10000):
    ans = BF_to_str(ans)
    trueans = f"{trueans:.10000f}"
    if ans[:precision] != trueans[:precision]:
        print("Ошибка")


def add_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = add(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a + b
    compare(ans, trueans)

def sub_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = sub(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a - b
    compare(ans, trueans)

def mul_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = mul(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a * b
    compare(ans, trueans)

def div_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = div(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a / b
    compare(ans, trueans)


def benchmark(prec = 100):
    add_t = []
    sub_t = []
    mul_t = []
    div_t = []
    sq_root_t = []
    for _ in range(prec):
        a = random_BF()
        b = random_BF()
        time1 = perf_counter()
        res = add(a, b)
        time2 = perf_counter()
        add_t.append(time2 - time1)
        time1 = perf_counter()
        res = sub(a, b)
        time2 = perf_counter()
        sub_t.append(time2 - time1)
        time1 = perf_counter()
        res = mul(a, b)
        time2 = perf_counter()
        mul_t.append(time2 - time1)
        time1 = perf_counter()
        res = div(a, b)
        time2 = perf_counter()
        div_t.append(time2 - time1)
    print(sum(add_t) / prec, 'сложение')
    print(sum(sub_t) / prec, 'вычитание')
    print(sum(mul_t) / prec, 'умножение')
    print(sum(div_t) / prec, 'деление')

if __name__ == '__main__':
    # benchmark()
    for _ in range(10):
        add_test()
        sub_test()
        mul_test()
        div_test()

n
