
import socket
import os
import time

from parallel_shunting import tools
from parallel_shunting import buffer


DEFAULT_INPUT_PATH = "../data/scripts/operations.txt"
DEFAULT_OUTPUT_PATH = "../data/scripts/results.txt"
CONNECTION_LOGS_DIR = "../data/logs/"


class Client:
    """ This class holds all the functionality required to: send lines of data from a file to a server,
     receive the answers and store them in log. """

    def __init__(self):

        self._channel = None
        self._log_fd = None
        self._verbose = None
        self._log_exchange = None

    def open_channel(self, host='127.0.0.1', port=65432, logs_path=None, verbose=False, log_exchange=True):
        """ Creates a socket and connects it to the server at 'host':'port'. """

        # Define log file path for client with unique name.
        date_time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        logs_name = "client_{0}.txt".format(date_time_stamp)

        answer = tools.verify_dir(logs_path, like='dir', append=logs_name)
        if answer == "Invalid path.":
            return "Wrong 'logs_path' provided, can't find the directory, please verify these and try again."
        logs_path = answer

        # Open a file descriptor for logs if one was provided.
        self._log_fd = open(logs_path, 'w') if logs_path is not None else None

        self._verbose = verbose
        self._log_exchange = log_exchange

        self._channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._channel.connect((host, port))

        tools.manage_message(self._log_fd, self._verbose, "Client started.")
        tools.manage_message(self._log_fd, self._verbose, "Connected to {0} through port {1}.".format(host, port))

    def close_channel(self):
        """ Closes the connection to the server. """

        tools.manage_message(self._log_fd, self._verbose, "Client closed.")

        # Always close file descriptors.
        if self._log_fd is not None:
            self._log_fd.flush()
            self._log_fd.close()

        self._channel.close()

    def process_batch(self, in_path, out_path=None, verbose=True):
        """ Receives a file pointed by 'in_path' containing lines of data and sends each one to the
        server. Can save each answer from the server in a file pointed by 'out_path' if one is given.
         If 'verbose', the results will be printed out, independent of the presence of an 'out_path'. """

        # Verify that in_path points to a file.
        if not os.path.isfile(in_path):
            return "Wrong 'in_path' provided, can't find the file, please verify these and try again."

        # Verify that out_path belongs to an existing directory.
        answer = tools.verify_dir(out_path, like='file')
        if answer == "Invalid path.":
            return "Wrong 'out_path' provided, can't find the directory, please verify these and try again."
        out_path = answer

        in_fd = open(in_path, 'r')
        out_fd = open(out_path, 'w') if out_path is not None else None

        buffer_handler = buffer.BufferHandler()

        closed_send = False
        closed_receive = False

        last_position = None

        while True:

            line_to_send = None

            if in_fd.tell() != last_position:
                last_position = in_fd.tell()
                line_to_send = in_fd.readline()  # Read one line at a time to support big files.

                # Ignore empty lines if present.
                if line_to_send.rstrip('\n') == '':
                    line_to_send = None

            elif not closed_send:  # Reach EOF for the first time.
                buffer_handler.send(self._channel, "End\n")
                closed_send = True

            # Something to send.
            if line_to_send is not None:
                buffer_handler.send(self._channel, line_to_send)

                if self._log_exchange:
                    tools.manage_message(self._log_fd, self._verbose, "Send -> {0}".format(line_to_send))

            received_lines = buffer_handler.receive(self._channel)

            # Something received.
            for received_line in received_lines:

                if received_line == "End":
                    closed_receive = True
                    break

                # Show or store results obtained according to the user's preferences.
                tools.manage_message(out_fd, verbose, received_line, False)

                if self._log_exchange:
                    tools.manage_message(self._log_fd, self._verbose, "Received -> {0}".format(received_line))

            if closed_receive:
                break

        # Always close file descriptors.
        in_fd.close()
        if out_fd is not None:
            out_fd.close()


def main():

    # Compute math expressions in operations.txt (default configuration)

    client_instance = Client()
    client_instance.open_channel(logs_path=CONNECTION_LOGS_DIR)

    answer = client_instance.process_batch(DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH, verbose=False)

    client_instance.close_channel()

    if answer is None:
        print("Computations finished.")
    else:
        print("Error detected: {0}".format(answer))


if __name__ == "__main__":

    main()
