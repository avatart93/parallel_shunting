
import os
import time
import random

from src import evaluator
from src import client
from src import server


EXPRESSIONS_PATH = "../data/tests/communication_in.txt"
RESULTS_PATH = "../data/tests/communication_tmp.txt"
TEMPLATE_PATH = "../data/tests/communication_out.txt"
CONNECTION_LOGS_DIR = "../data/logs/"

MAX_DELAYED_SECONDS = 1


def delayed_shunting_yard(expression):
    """ Adds some sleep time to really test the asynchronous work. """

    time.sleep(random.random() * MAX_DELAYED_SECONDS)

    return evaluator.shunting_yard(expression)


def test_asynchronous_communication():
    """ Tests the communication between the client and server by comparing the log file produced with
     an expected template. Will raise an exception if any differences are detected. This test only works
      when working asynchronously (no children in server). """

    # Serve the shunting yard function.
    server_instance = server.Server()
    answer = server_instance.launch(delayed_shunting_yard)
    if answer is not None:
        return answer

    # Establish communication with the server.
    client_instance = client.Client()
    answer = client_instance.open_channel()
    if answer is not None:
        server_instance.kill()
        return answer

    answer = client_instance.process_batch(EXPRESSIONS_PATH, RESULTS_PATH, False)

    # Close communication by both sides.
    client_instance.close_channel()
    server_instance.kill()

    # Verify after closing connections cause I had to close them either way.
    if answer is not None:
        return answer

    assert os.stat(RESULTS_PATH).st_size == os.stat(TEMPLATE_PATH).st_size


def main():

    for run_index in range(10):

        answer = test_asynchronous_communication()

        if answer is None:
            print("{0} -> Operations batch computed correctly.".format(run_index + 1))
        else:
            print("Error detected: {0}".format(answer))


if __name__ == "__main__":
    main()
