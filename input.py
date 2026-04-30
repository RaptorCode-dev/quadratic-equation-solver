from class_1 import Coefs
import interpretater

def input_data() -> Coefs:
    context = interpretater.ComputationContext()
    interpretater.ExpressionParser(input(), context)
    a = context.a
    b = context.b
    c = context.c
    return Coefs(a, b, c)
