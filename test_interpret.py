from decimal import Decimal, getcontext
import pytest

from interpretater import NumberParser
from helper import random_BF, BF_to_str


@pytest.mark.parametrize("value", [
    "0",
    "1",
    "9",
    "10",
    "123",
    "+123",
    "-123",
    "1.5",
    "1,5",
    "0.5",
    "0,5",
    "1e2",
    "1e+2",
    "1e-2",
    "0e3",
    "-1.5e+10",
    "-.3e3",
    "inf",
    "-inf",
    "nan",
    "1_000",
    "-5_000",
])
def test_valid_numbers(value):
    result = NumberParser(value).interpret()

    assert result is not None
    assert isinstance(result.mantissa, list)


@pytest.mark.parametrize("value", [
    "",
    "+",
    "-",
    ".",
    ",",
    "01",
    "00",
    "0123",
    "+.",
    "-.",
    "e10",
    "1e",
    "1e+",
    "1e-",
    "abc",
    "1abc",
    "abc1",
    "1 2",
    "1.2.3",
    "-1-2-3",
    "00e3",
    "_5",
    "5__0"
    "5_"
])
def test_invalid_numbers(value):
    with pytest.raises(SystemExit):
        NumberParser(value).interpret()


def test_random_numbers():
    getcontext().prec = 10000

    for _ in range(1000):
        value = BF_to_str(random_BF())

        try:
            parsed = NumberParser(value).interpret()
        except SystemExit:
            try:
                Decimal(value.replace(',', '.'))
                pytest.fail(f"Decimal распарсил '{value}', а твой парсер нет")
            except:
                continue

        your_string = BF_to_str(parsed)
        decimal_string = format(Decimal(value.replace(',', '.')), 'f')

        assert your_string[:10000] == decimal_string[:10000], (
            f"\nЧисло: {value}\n"
            f"Ваша строка: {your_string[:200]}...\n"
            f"Decimal:     {decimal_string[:200]}..."
        )