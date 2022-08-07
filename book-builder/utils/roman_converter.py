import sys
import re

'''
int to roman:
    https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals

roman to int:
    https://stackoverflow.com/questions/19308177/converting-roman-numerals-to-integers-in-python

is_roman:
    https://dev.to/alexdjulin/a-python-regex-to-validate-roman-numerals-2g99

if all else fails:
    pip install roman
    https://pypi.org/project/roman/
    (but it has an issue on Windows...)
'''

ROMAN = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
    (  10, "X"),
    (   9, "IX"),
    (   5, "V"),
    (   4, "IV"),
    (   1, "I"),
]

def is_roman(num):

    pattern = re.compile(r"""
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE | re.IGNORECASE)

    if re.match(pattern, num):
        return True

    return False

def int_to_roman(number):
    if int(number) <= 0:
        return None

    result = ""
    for (arabic, roman) in ROMAN:
        (factor, number) = divmod(number, arabic)
        result += roman * factor
    return result

def roman_to_int(s):
    if not is_roman(s):
        return None

    d = {'m': 1000, 'd': 500, 'c': 100, 'l': 50, 'x': 10, 'v': 5, 'i': 1}
    n = [d[i] for i in s.lower() if i in d]
    return sum([i if i>=n[min(j+1, len(n)-1)] else -i for j,i in enumerate(n)])

def main(args):
    num = args[0]
    res = None
    if num.isdigit():
        res = int_to_roman(int(num))
    else:
        res = roman_to_int(num)
    print(res)

if __name__ == "__main__":
    main(sys.argv[1:])
