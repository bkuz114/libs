# Overview

This folder holds unittests that should be run with the `pytest` utility.

# Install pytest

Before running any tests, start a virtualenv as follows:

`virtualenv venv && source ./venv/Scripts/activate && pip install -r requirements.txt`

This will install `pytest`, as well as any other pip modules required for unit tests in this directory.

# Example test runs

- Run all test files in this dir:

  `pytest`

  This will find all `.py` files prefixed with `test_` and run all tests within them -- i.e., all functions in those files that are prefixed with `test_`

- Run a specific test file in this dir:

  `pytest FILENAME`

  This will run the `.py` file `FILENAME`, and will run all tests within it -- i.e., all functions in `FILENAME` that are prefixed with `test_`

- Run a specific test within a specific test file:

  `pytest FILENAME -k 'TESTNAME`

  This will run the function `TESTNAME` within the `.py` file `FILENAME`

- Run a specific set of tests within specific test file:

  `pytest FILENAME -k `TESTNAME1 or TESTNAME2 or .... TESTNAMEN`

  This would run the functions `TESTNAME1`, `TESTNAME2`, ... `TESTNAMEN` within the `.py` file `FILENAME`

- To display `print` statments when running tests: provide `-s` flag

- The args in `pytest.ini` will be added to any `pytest` invocations.
