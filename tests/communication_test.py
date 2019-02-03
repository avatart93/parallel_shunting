

from src import evaluator
from src import client
from src import server


EXPRESSIONS_PATH = "../data/test/communication_in.txt"
LOGS_PATH = "../data/test/communication_tmp.txt"
TEMPLATE_PATH = "../data/test/communication_out.txt"


def test_asynchronous_communication():
    """ Tests the communication between the client and server by comparing the log file produced with
     an expected template. Will raise an exception if any differences are detected. This test only works
      when working asynchronously (no children in server). """

    # Serve the shunting yard function.
    server_instance = server.Server()
    server_instance.launch(evaluator.shunting_yard)

    # Establish communication with the server.
    client_instance = client.Client()
    client_instance.open_channel()

    client_instance.process_batch(EXPRESSIONS_PATH, LOGS_PATH, False)

    # Close communication by both sides.
    client_instance.close_channel()
    server_instance.kill()

    logs_fd = open(LOGS_PATH)
    template_fd = open(TEMPLATE_PATH)

    # If last position didn't changed means we reach EOF.
    last_position = None
    while template_fd.tell() != last_position:
        last_position = template_fd.tell()

        assert template_fd.readline() == logs_fd.readline()

    # Make sure the logs file isn't bigger than the template.
    logs_fd.readline()
    assert template_fd.tell() == logs_fd.tell()

    # Always close file descriptors.
    logs_fd.close()
    template_fd.close()


def main():

    test_asynchronous_communication()

    print()
    print("Operations batch computed correctly.")


if __name__ == "__main__":
    main()
