
import socket


DEFAULT_INPUT_PATH = "../data/src/operations.txt"
DEFAULT_OUTPUT_PATH = "../data/src/results.txt"


class Client:

    def __init__(self):

        self._channel = None

    def open_channel(self, host='127.0.0.1', port=65432):
        """ Creates a socket and connects it to the server at 'host':'port'. """

        self._channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._channel.connect((host, port))

    def close_channel(self):
        """ Closes the connection to the server. """

        self._channel.close()

    def exchange(self, data):
        """ Sends data to be processed by the server. """

        self._channel.send(str(data).encode())
        data = self._channel.recv(1024)
        return data.decode()

    def process_batch(self, in_path, out_path=None, verbose=True):
        """ Receives a file pointed by 'in_path' containing math expressions and computes the result for
         each one. Can save the results in a file pointed by 'out_path' if one is given. If 'verbose',
          the results will be printed out, regardless of the presence of an 'out_path'. """

        operations_fd = open(in_path)
        logs_fd = open(out_path, 'w') if out_path is not None else None

        # If last position didn't changed means we reach EOF.
        last_position = None
        while operations_fd.tell() != last_position:
            last_position = operations_fd.tell()

            expression = operations_fd.readline()  # Read one line at a time to support big files.

            # Clean it.
            expression = expression.replace(' ', '')
            expression = expression.rstrip('\n')

            if expression == '':  # Ignore empty lines if present.
                continue

            result = self.exchange(expression)
            answer = "{0}={1}".format(expression, result)

            if verbose:
                print(answer)

            if logs_fd is not None:
                logs_fd.write(answer + '\n')

        # Always close file descriptors.
        operations_fd.close()
        if logs_fd is not None:
            logs_fd.close()


def main():

    # Compute math expressions in operations.txt (default configuration)

    client_instance = Client()
    client_instance.open_channel()

    client_instance.process_batch(DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH, False)

    client_instance.close_channel()

    print("Computations finished.")


if __name__ == "__main__":

    main()
