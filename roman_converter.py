import sys
import re

'''
Basic roman numeral <--> integer converter.
Needed because roman py package fails on Windows.

usage:
    1. on cmd:
        python roman_converter.py 5 --> prints V
        python roman_converter.py X --> prints 10
    2. in .py file
        import roman_converter
        roman_converter.int_to_roman(5) --> returns "V"
        roman_converter.roman_to_int("X") --> returns 10

----------------------
int to roman:
    https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
roman to int:
    https://stackoverflow.com/questions/19308177/converting-roman-numerals-to-integers-in-python
is_roman:
    https://dev.to/alexdjulin/a-python-regex-to-validate-roman-numerals-2g99
is_digit:
    https://stackoverflow.com/questions/28279732/how-to-type-negative-number-with-isdigit
if all else fails:
    pip install roman
    https://pypi.org/project/roman/
    (but it fails on Windows..., hence why I've made this)
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

'''
return True if n is an integer;
False otherwise. (needed because
python's isdigit() doesn't work
for negative numbers)
'''
def is_digit(n):
    try:
        int(n) # throws err if number isn't digit
        return True
    except ValueError:
        return  False

def int_to_roman(number):
    if int(number) <= 0:
        raise ValueError("Can't convert {} to roman numeral; there is no roman numeral for it".format(number))
        return None

    result = ""
    for (arabic, roman) in ROMAN:
        (factor, number) = divmod(number, arabic)
        result += roman * factor
    return result

def roman_to_int(s):
    if not is_roman(s):
        raise ValueError("{} is not a valid roman numeral".format(s))

    d = {'m': 1000, 'd': 500, 'c': 100, 'l': 50, 'x': 10, 'v': 5, 'i': 1}
    n = [d[i] for i in s.lower() if i in d]
    return sum([i if i>=n[min(j+1, len(n)-1)] else -i for j,i in enumerate(n)])

def main(args):
    num = args[0]
    res = None
    if is_digit(num):
        res = int_to_roman(int(num))
    else:
        res = roman_to_int(num)
    print(res)

if __name__ == "__main__":
    main(sys.argv[1:])
