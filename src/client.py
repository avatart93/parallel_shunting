
import socket


EXPRESSIONS_PATH = "../data/test/communication_in.txt"


class Client:

    def __init__(self):

        self._channel = None

    def open_channel(self, host='127.0.0.1', port=65432):

        self._channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._channel.connect((host, port))

    def close_channel(self):

        self._channel.close()

    def exchange(self, data):

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
