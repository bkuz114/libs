"""
Test for io_utils.py

usage:
    virtualenv venv && source ./venv/Scripts/activate && pip install -r requirements.txt
    pytest io_utils.py [-k 'TEST_A or TEST_B or ... TEST_N']

Examples:

    1. Run all tests
        pytest io_utils.py

    2. Run test_1 only
        pytest io_utils.py -k 'test_1'

    3. Run test_1 and test_2 only
        pytest io_utils.py -k 'test_1 or test_2'
"""

import sys
import os
import shutil
from stat import S_IREAD, S_IRGRP, S_IROTH
from pathlib import Path
sys.path.append("..")
import io_utils  # noqa: E402

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
a = os.path.abspath(os.path.join(SCRIPT_DIR, "a.txt"))
b = os.path.abspath(os.path.join(SCRIPT_DIR, "b.txt"))
c = os.path.abspath(os.path.join(SCRIPT_DIR, "c.txt"))
mydir = os.path.abspath(os.path.join(SCRIPT_DIR, "mydir"))


def setup_module():
    print("\nTEST SETUP")
    print("Touch files a.txt, b.txt, and c.txt in current directory")
    Path(a).touch()
    Path(b).touch()
    Path(c).touch()


def teardown_module():
    print("\nTEST TEARDOWN")
    print("(1) Remove mydir if still exists")
    if os.path.exists(mydir) and os.path.isdir(mydir):
        io_utils.remove(mydir)

    def rmfile(myfile):
        if os.path.exists(myfile) and os.path.isfile(myfile):
            os.remove(myfile)

    print("(2) Remove files a,b, and c if still exists")
    rmfile(a)
    rmfile(b)
    rmfile(c)


def test_1():
    print("Test function: 'copy_file'\n"
          "1. Create directory mydir in current directory\n"
          "2. Copy a, b, and c into mydir individually, "
          "specifiying they are files")

    print("Create 'mydir' in current dir")
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Copy a, b, and c into mydir individually, "
          "specifying they are files")
    io_utils.copy_file(a, mydir)
    io_utils.copy_file(b, mydir)
    io_utils.copy_file(c, mydir)
    assert os.path.exists(os.path.join(mydir, a))
    assert os.path.exists(os.path.join(mydir, b))
    assert os.path.exists(os.path.join(mydir, c))

    print("Remove directory 'midir")
    shutil.rmtree(mydir)
    assert not os.path.isdir(mydir)


def test_2():
    print("Test function: 'copy_files'\n"
          "1. Create directory mydir in current directory\n"
          "2. Copy a, b, and c into mydir individually "
          "as a list of files")

    print("Create 'mydir' in current dir")
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Copy a, b, and c into mydir individually, "
          "without specifying they are files")
    io_utils.copy_files([a, b, c], mydir)
    assert os.path.exists(os.path.join(mydir, a))
    assert os.path.exists(os.path.join(mydir, b))
    assert os.path.exists(os.path.join(mydir, c))

    print("Remove directory 'midir")
    shutil.rmtree(mydir)
    assert not os.path.isdir(mydir)


def test_3():
    print("Test function: 'copy_path'\n"
          "1. Create directory mydir in current directory\n"
          "2. Copy a, b, and c into mydir individually without "
          "specifying if they are dirs of files")

    print("Create 'mydir' in current dir")
    mydir = os.path.abspath(os.path.join(SCRIPT_DIR, "mydir"))
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Copy a, b, and c into mydir individually, "
          "without specifying they are files")
    io_utils.copy_path(a, mydir)
    io_utils.copy_path(b, mydir)
    io_utils.copy_path(c, mydir)
    assert os.path.exists(os.path.join(mydir, a))
    assert os.path.exists(os.path.join(mydir, b))
    assert os.path.exists(os.path.join(mydir, c))

    print("Remove directory 'midir")
    shutil.rmtree(mydir)
    assert not os.path.isdir(mydir)


def test_4():
    print("Test function: 'copy_paths'\n"
          "1. Create directory mydir in current directory\n"
          "2. Copy a, b, and c into mydir as list of paths, without "
          "specifying if they are dirs of files")

    print("Create 'mydir' in current dir")
    mydir = os.path.abspath(os.path.join(SCRIPT_DIR, "mydir"))
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Copy a, b, c as list of paths, "
          "without specifying if they are files or dirs")
    io_utils.copy_paths([a, b, c], mydir)
    assert os.path.exists(os.path.join(mydir, a))
    assert os.path.exists(os.path.join(mydir, b))
    assert os.path.exists(os.path.join(mydir, c))

    print("Remove directory 'midir")
    shutil.rmtree(mydir)
    assert not os.path.isdir(mydir)


def test_5():
    print("Test function: 'copy_file'\n"
          "1. Create directory mydir in current directory\n"
          "2. Copy a into mydir\n"
          "3. Try to copy a again, and see it fails\n"
          "4. Try to copy a again, this time with force=True, "
          "and see it succeeds")

    print("Create 'mydir' in current dir")
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Copy a into mydir")
    io_utils.copy_file(a, mydir)
    assert os.path.exists(os.path.join(mydir, a))

    print("Copy a again, and make sure it fails")
    try:
        io_utils.copy_file(a, mydir)
        assert False
    except FileExistsError as e:
        print("copy_file failed, as expected. Error message:" + str(e))

    print("Copy a again, but with force option")
    io_utils.copy_file(a, mydir, force=True)
    assert os.path.exists(os.path.join(mydir, a))

    print("Remove directory 'midir")
    shutil.rmtree(mydir)
    assert not os.path.isdir(mydir)


def test_6():
    print("Test functions: 'createPath' and 'remove'\n"
          "1. Create directory mydir in current directory\n"
          "2. Remove the directory "
          "and see it succeeds")

    print("Create 'mydir' in current dir")
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Remove directory 'midir")
    io_utils.remove(mydir)
    assert not os.path.isdir(mydir)


def test_7():
    print("Test function: 'remove'\n"
          "1. Create directory mydir in current directory\n"
          "2. Make mydir readonly\n"
          "3. Try to remove with shutil and ensure failure\n"
          "4. Try to remove with 'remove' and ensure success,\n"
          "   even though it's read only")

    print("Create 'mydir' in current dir")
    io_utils.createPath(mydir)
    assert os.path.isdir(mydir)

    print("Make 'mydir' readonly")
    os.chmod(mydir, S_IREAD | S_IRGRP | S_IROTH)

    print("Try to remove with shutil and make sure fails due "
          "to read only permissions")
    try:
        shutil.rmtree(mydir)
        assert False
    except PermissionError as e:
        print("shutil.rmtree failed on permission error, as expected. "
              "Error message:" + str(e))

    print("Remove directory via 'remove' function; "
          "should succeed even with RO perms")
    io_utils.remove(mydir)
    assert not os.path.isdir(mydir)
