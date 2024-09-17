'''
Test for io_utils.py

usage:
    python test_io_utils.py [--tests TESTS] [--all]

    --tests
        specify which tests to run
        (valid : 1, 2, 3, 4, or 5)
        You can specify multiple tests as follows:
        --tests 1 3 5

    --all
        run all tests

Examples:

    python test_io_utils.py --tests 2
        --> run test case 2
    python test_io_utils.py --tests 5 1 3
        --> run test cases 5, 1, and 3 (in that order)
    python test_io_utils.py --all
        --> run all test cases
'''

import sys
import os
import shutil
import argparse
sys.path.append("..")
import io_utils
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
a = os.path.abspath(os.path.join(SCRIPT_DIR, "a.txt"))
b = os.path.abspath(os.path.join(SCRIPT_DIR, "b.txt"))
c = os.path.abspath(os.path.join(SCRIPT_DIR, "c.txt"))
mydir = os.path.abspath(os.path.join(SCRIPT_DIR, "mydir"))


def print_testcase(test_case_str, test_case_num):
    print("\n\n ======== TEST # {} ========".format(test_case_num))
    print("\n Description:\n\n" + test_case_str)
    print("\n====================\n\n")


def print_step(step_str):
    print(step_str)


def test_setup():
    print("\n\n ------ TEST SETUP -----------")
    # run test teardown, in case last test failed
    print("\nFirst, call teardown, in case last test failed...")
    test_teardown()

    print("\nSetup: Touch files a.txt, b.txt, and c.txt in current directory")
    Path(a).touch()
    Path(b).touch()
    Path(c).touch()
    print("\n\n -------- END TEST SETUP --------")


def test_teardown():
    print("\n\n ------- TEST TEARDOWN -----")
    print("(1) Remove mydir if still exists")
    if os.path.exists(mydir) and os.path.isdir(mydir):
        shutil.rmtree(mydir)

    def rmfile(myfile):
        if os.path.exists(myfile) and os.path.isfile(myfile):
            os.remove(myfile)

    print("(2) Remove files a,b, and c if still exists")
    rmfile(a)
    rmfile(b)
    rmfile(c)
    print("\n\n -------- END TEST TEARDOWN ------")


def main(args):

    valid_tests = ["1", "2", "3", "4", "5"]

    parser = argparse.ArgumentParser(
        description='Test cases for io_utils.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--tests', choices=valid_tests,
                        default=[], nargs='+',
                        help="Tests to run. Call as many i.e. --tests 3 5")
    parser.add_argument('-a', '--all', default=False,
                        action="store_true", help="Run all tests")
    args = parser.parse_args(args)

    test_list = args.tests
    if args.all:
        test_list = valid_tests

    if not test_list:
        raise Exception("\n\nDidn't select any tests!"
                        "\nRun again with --tests or "
                        "--all to run all tests")

    # test setup
    test_setup()

    # run the tests
    for test in test_list:
        match test:
            case "1":
                testcase_1()
            case "2":
                testcase_2()
            case "3":
                testcase_3()
            case "4":
                testcase_4()
            case "5":
                testcase_5()

    # test teardown
    test_teardown()


def testcase_1():
    print_testcase("Test function: 'copy_file'\n"
                   "1. Create directory mydir in current directory\n"
                   "2. Copy a, b, and c into mydir individually, "
                   "specifiying they are files", 1)

    print_step("Create 'mydir' in current dir")
    io_utils.createPath(mydir)

    print_step("Copy a, b, and c into mydir individually, "
               "specifying they are files")
    io_utils.copy_file(a, mydir)
    io_utils.copy_file(b, mydir)
    io_utils.copy_file(c, mydir)

    print_step("Remove directory 'midir")
    shutil.rmtree(mydir)


def testcase_2():
    print_testcase("Test function: 'copy_files'\n"
                   "1. Create directory mydir in current directory\n"
                   "2. Copy a, b, and c into mydir individually "
                   "as a list of files", 2)

    print_step("Create 'mydir' in current dir")
    io_utils.createPath(mydir)

    print_step("Copy a, b, and c into mydir individually, "
               "without specifying they are files")
    io_utils.copy_files([a, b, c], mydir)

    print_step("Remove directory 'midir")
    shutil.rmtree(mydir)


def testcase_3():
    print_testcase("Test function: 'copy_path'\n"
                   "1. Create directory mydir in current directory\n"
                   "2. Copy a, b, and c into mydir individually without "
                   "specifying if they are dirs of files", 3)

    print_step("Create 'mydir' in current dir")
    mydir = os.path.abspath(os.path.join(SCRIPT_DIR, "mydir"))
    io_utils.createPath(mydir)

    print_step("Copy a, b, and c into mydir individually, "
               "without specifying they are files")
    io_utils.copy_files([a, b, c], mydir)

    print_step("Remove directory 'midir")
    shutil.rmtree(mydir)


def testcase_4():
    print_testcase("Test function: 'copy_paths'\n"
                   "1. Create directory mydir in current directory\n"
                   "2. Copy a, b, and c into mydir as list of paths, without "
                   "specifying if they are dirs of files", 4)

    print_step("Create 'mydir' in current dir")
    mydir = os.path.abspath(os.path.join(SCRIPT_DIR, "mydir"))
    io_utils.createPath(mydir)

    print_step("Copy a, b, c as list of paths, "
               "without specifying if they are files or dirs")
    io_utils.copy_paths([a, b, c], mydir)

    print_step("Remove directory 'midir")
    shutil.rmtree(mydir)


def testcase_5():
    print_testcase("Test function: 'copy_file'\n"
                   "1. Create directory mydir in current directory\n"
                   "2. Copy a into mydir\n"
                   "3. Try to copy a again, and see it fails\n"
                   "4. Try to copy a again, this time with force=True, "
                   "and see it succeeds", 5)

    print_step("Create 'mydir' in current dir")
    io_utils.createPath(mydir)

    print_step("Copy a into mydir")
    io_utils.copy_file(a, mydir)

    print_step("Copy a again, and make sure it fails")
    try:
        io_utils.copy_file(a, mydir)
        print("copy_file didn't fail!! I shouldn't be here!")
    except FileExistsError as e:
        print("copy_file failed, as expected. Error message:" + str(e))

    print_step("Copy a again, but with force option")
    io_utils.copy_file(a, mydir, force=True)

    print_step("Remove directory 'midir")
    shutil.rmtree(mydir)


if __name__ == "__main__":
    main(sys.argv[1:])
