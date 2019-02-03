

from src import evaluator
from src import client
from src import server


EXPRESSIONS_PATH = "../data/test/communication_in.txt"
LOGS_PATH = "../data/test/communication_tmp.txt"
TEMPLATE_PATH = "../data/test/communication_out.txt"


def test_asynchronous_communication():
    """ Tests the communication between the client and server comparing the log file produced with an
     expected template, will raise an exception if any differences are detected. This test only works
      when working asynchronously (no children in server). """

    server.Server.launch(evaluator.shunting_yard)  # Serve the shunting yard function.

    # Instance and connect the client.
    client_instance = client.Client()
    client_instance.open_channel()

    client_instance.process_batch(EXPRESSIONS_PATH, LOGS_PATH, True)

    client_instance.close_channel()

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
    print("Operations batch computed.")


if __name__ == "__main__":
    main()
