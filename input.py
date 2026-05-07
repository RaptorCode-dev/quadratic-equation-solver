from class_1 import Coefs
import interpretater


def input_data() -> Coefs:
    context = interpretater.ComputationContext()
    interpretater.ExpressionParser(input(), context).interpret()
    return Coefs(context.a, context.b, context.c)