

from src import client


EXPRESSIONS_PATH = "../data/test/client_in.txt"
LOGS_PATH = "../data/test/client_tmp.txt"
TEMPLATE_PATH = "../data/test/client_out.txt"


def test_client_asynchronous():
    """ Tests the client script by comparing the log file with an expected template, will raise an
     exception if any differences are detected. This test only works when working asynchronously. """

    client.process_operations_batch(EXPRESSIONS_PATH, LOGS_PATH, verbose=False)

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

    test_client_asynchronous()

    print()
    print("Operations batch computed.")


if __name__ == "__main__":
    main()
