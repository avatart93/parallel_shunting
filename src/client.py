
import socket

from src import evaluator


HOST = '127.0.0.1'  # The server's IP address.
PORT = 65432  # The server's port.


def process_operations_batch(in_path, out_path=None, verbose=True):
    """ Receives a file pointed by 'in_path' containing math expressions and computes the result for
     each one. Can save the results in a file pointed by 'out_path' if one is given. If 'verbose',
      the results will be printed out, regardless of the presence of an 'out_path'. """

    operations_fd = open(in_path)
    logs_fd = open(out_path, 'w') if out_path is not None else None

    # If last position didn't changed means we reach EOF.
    last_position = None
    while operations_fd.tell() != last_position:
        last_position = operations_fd.tell()

        expression = operations_fd.readline() # Read one line at a time to support big files.

        # Clean it.
        expression = expression.replace(' ', '')
        expression = expression.rstrip('\n')

        if expression == '':  # Ignore empty lines if present.
            continue

        result = evaluator.shunting_yard(expression)
        answer = "{0}={1}".format(expression, result)

        if verbose:
            print(answer)

        if logs_fd is not None:
            logs_fd.write(answer + '\n')

    # Always close file descriptors.
    operations_fd.close()
    if logs_fd is not None:
        logs_fd.close()


def client():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
        channel.connect((HOST, PORT))

        while True:

            channel.send("Hello world!".encode())
            data = channel.recv(1024)

            print("Received {0}".format(data.decode()))


def main():

    client()


if __name__ == "__main__":

    main()
