
import os
import time
import random
import pkg_resources
import tempfile

from parallel_shunting import operations
from parallel_shunting import evaluator
from parallel_shunting import client
from parallel_shunting import server


EXPRESSIONS_PATH = pkg_resources.resource_filename('data', "scripts/communication_in.txt")
TEMPLATE_PATH = pkg_resources.resource_filename('data', "scripts/communication_out.txt")

ERROR_THRESHOLD = 1e-3
MAX_DELAYED_SECONDS = 1


def delayed_shunting_yard(expression):
    """ Adds some sleep time to really test the asynchronous work. """

    time.sleep(random.random() * MAX_DELAYED_SECONDS)

    return evaluator.shunting_yard(expression)


def test_asynchronous_communication(in_path, out_path, template_path, logs_path=None):
    """ Tests the communication between the client and server by comparing the log file produced with
     an expected template. Will raise an exception if any differences are detected. This test only works
      when working asynchronously (no children in server). """

    # Serve the shunting yard function.
    server_instance = server.Server()
    answer = server_instance.launch(delayed_shunting_yard, logs_path=logs_path)
    if answer is not None:
        return answer

    time.sleep(1)  # On Linux you have to give some time to the server to get up.

    # Establish communication with the server.
    client_instance = client.Client()
    answer = client_instance.open_channel(logs_path=logs_path)
    if answer is not None:
        server_instance.kill()
        return answer

    answer = client_instance.process_batch(in_path, out_path, False)

    # Close communication by both sides.
    client_instance.close_channel()
    server_instance.kill()

    # Verify after closing connections cause I had to close them either way.
    if answer is not None:
        return answer

    assert os.stat(out_path).st_size == os.stat(template_path).st_size


def test_shunting_yard():
    """ Tests the shunting yard algorithm, will raise an exception if any of the test cases fails. """

    case_1 = "38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77"
    case_2 = "57 + 87 - 24 * 27 / 8 + 53 - 87 * 6 * 60 - 30"
    case_3 = "63 * 23 - 91 - 17 * 45 + 63 * 52 - 50"
    case_4 = "47 - 88 + 32 - 71 * 39 * 68"
    case_5 = "43 * 47 - 75 + 94 * 35 - 60 + 55 + 8"
    case_6 = "49 - 97 + 17 + 31 / 37 + 82"
    case_7 = "74 - 36 - 96 + 32 + 2 + 26"
    case_8 = "43 - 45 - 66 - 52 - 6"
    case_9 = "41 / 50 + 53 + 40"
    case_10 = "40 * 76 + 97 - 90 * 52"
    case_11 = "62 - 42 + 7 - 74 / 88"
    case_12 = "66 - 11 / 5 / 58 + 18 - 58 - 88 + 97"
    case_13 = "36 / 48 * 21 - 36 + 69 + 26 + 35 + 49 + 7"
    case_14 = "58 * 10 - 19 - 59"
    case_15 = "63 / 68 * 86 - 62 - 32"

    assert evaluator.shunting_yard(case_1) - eval(case_1) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_2) - eval(case_2) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_3) - eval(case_3) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_4) - eval(case_4) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_5) - eval(case_5) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_6) - eval(case_6) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_7) - eval(case_7) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_8) - eval(case_8) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_9) - eval(case_9) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_10) - eval(case_10) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_11) - eval(case_11) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_12) - eval(case_12) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_13) - eval(case_13) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_14) - eval(case_14) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_15) - eval(case_15) < ERROR_THRESHOLD


def test_add():
    """ Tests the add operation, will raise an exception if any of the test cases fails. """

    assert operations.add(1, 2) - 3 < ERROR_THRESHOLD
    assert operations.add(-1, 2) - 1 < ERROR_THRESHOLD
    assert operations.add(-1, -2) - -3 < ERROR_THRESHOLD
    assert operations.add(0, 1) - 1 < ERROR_THRESHOLD


def test_subtract():
    """ Tests the subtract operation, will raise an exception if any of the test cases fails. """

    assert operations.subtract(1, 2) - -1 < ERROR_THRESHOLD
    assert operations.subtract(-1, 2) - -3 < ERROR_THRESHOLD
    assert operations.subtract(-1, -2) - 1 < ERROR_THRESHOLD
    assert operations.subtract(0, 1) - -1 < ERROR_THRESHOLD


def test_multiply():
    """ Tests the multiply operation, will raise an exception if any of the test cases fails. """

    assert operations.multiply(1, 2) - 2 < ERROR_THRESHOLD
    assert operations.multiply(-1, 2) - -2 < ERROR_THRESHOLD
    assert operations.multiply(-1, -2) - 2 < ERROR_THRESHOLD
    assert operations.multiply(0, 1) - 0 < ERROR_THRESHOLD


def test_divide():
    """ Tests the divide operation, will raise an exception if any of the test cases fails. """

    assert operations.divide(2, 1) - 2 < ERROR_THRESHOLD
    assert operations.divide(0, 2) - 0 < ERROR_THRESHOLD
    assert operations.divide(1, -2) - -0.5 < ERROR_THRESHOLD
    assert operations.divide(4, 3) - 1.333 < ERROR_THRESHOLD


def main():

    test_add()
    test_subtract()
    test_multiply()
    test_divide()

    print("All operations tests finished correctly.")

    test_shunting_yard()

    print("All expressions were computed correctly.")

    print("Testing asynchronous work.")

    for run_index in range(10):

        temp_fd, temp_path = tempfile.mkstemp()
        os.close(temp_fd)
        answer = test_asynchronous_communication(EXPRESSIONS_PATH, temp_path, TEMPLATE_PATH)
        os.remove(temp_path)

        if answer is None:
            print("{0} -> Operations batch computed correctly.".format(run_index + 1))
        else:
            print("Error detected: {0}".format(answer))

    print("All done.")


if __name__ == "__main__":

    main()
