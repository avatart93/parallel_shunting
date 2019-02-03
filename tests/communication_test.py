
from src import evaluator
from src import client
from src import server


EXPRESSIONS_PATH = "../data/test/communication_in.txt"
RESULTS_PATH = "../data/test/communication_tmp.txt"
TEMPLATE_PATH = "../data/test/communication_out.txt"
CONNECTION_LOGS_DIR = "../data/logs/"


def test_asynchronous_communication():
    """ Tests the communication between the client and server by comparing the log file produced with
     an expected template. Will raise an exception if any differences are detected. This test only works
      when working asynchronously (no children in server). """

    # Serve the shunting yard function.
    server_instance = server.Server()
    answer = server_instance.launch(evaluator.shunting_yard, CONNECTION_LOGS_DIR)
    if answer is not None:
        return answer

    # Establish communication with the server.
    client_instance = client.Client()
    answer = client_instance.open_channel(logs_path=CONNECTION_LOGS_DIR, verbose=False)
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

    logs_fd = open(RESULTS_PATH, 'r')
    template_fd = open(TEMPLATE_PATH, 'r')

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

    answer = test_asynchronous_communication()

    if answer is None:
        print("Operations batch computed correctly.")
    else:
        print("Error detected: {0}".format(answer))


if __name__ == "__main__":
    main()
