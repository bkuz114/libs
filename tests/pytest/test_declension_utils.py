"""
Test for test_declension_utils.py

usage:
    virtualenv venv && source ./venv/Scripts/activate && pip install -r requirements.txt
    pytest test_declension_utils.py [-k 'TEST_A or TEST_B or ... TEST_N']

Examples:

    1. Run all tests
        pytest test_declension_utils.py

    2. Run test_mark_string only
        pytest test_declension_utils.py -k 'test_mark_string'

    3. Run test_mark_string and test_mark_sentence_1
        pytest test_declension_utils.py -k 'test_mark_string or test_mark_sentence_1'

    4. Run all the test_mark_sentence_* tests
        pytest test_declension_utils.py -k 'test_mark_sentence'
"""

import sys
sys.path.append("../..")
import declension_utils as marker  # noqa: E402


def test_mark_string():
    """ test mark_string function """

    print("\nTest 'mark_string' function")

    sentence1 = "{[Иван*а] сын.}"
    sentence2 = "{папа [Бор*и].}"
    html_str = '''
<html>
    <head></head>
    <body>
        {}
        <br>
        {}
    </body>
</html>
'''.format(sentence1, sentence2)
    print("Original string:")
    print(html_str)

    print("Mark-up string in <span> tags")
    marked = marker.mark_string(
            html_str, "{", "}", "[", "]", "[[", "]]", "*")

    expected = html_str.replace(
            sentence1, "<span>Иван</span><span>а</span> сын.")
    expected = expected.replace(
            sentence2, "папа <span>Бор</span><span>и</span>.")

    print("Marked up string:")
    print(marked)
    assert marked == expected


def test_mark_sentence_1():
    """ test mark_sentence, NO padding <span> with &nbsp; """

    print("\nTest 'mark_sentence' function")

    # the sentence to markup
    sentence = "[Иван*а] сын."
    print("Original sentence:")
    print(sentence)

    # expected markup of sentence
    expected = "<span>Иван</span><span>а</span> сын."

    print("Mark up the sentence by calling mark_sentence")
    # mark up the sentence
    marked = marker.mark_sentence(
            sentence,
            "[", "]", "[[", "]]", "*",
            False, False)

    print("Marked up sentence:")
    print(marked)
    assert marked == expected


def test_mark_sentence_2():
    """ test mark_sentence, padding <span> with &nbsp; """

    print("\nTest 'mark_sentence' function, padding <span> with &nbsp;")

    # the sentence to markup
    sentence = "[Иван*а] сын."
    print("Original sentence:")
    print(sentence)

    # expected markup of sentence
    expected = "<span>Иван</span><span>а</span>&nbsp;сын."

    print("Mark up the sentence by calling mark_sentence")
    # mark up the sentence
    marked = marker.mark_sentence(
            sentence,
            "[", "]", "[[", "]]", "*",
            False, True)

    print("Marked up sentence:")
    print(marked)
    assert marked == expected
