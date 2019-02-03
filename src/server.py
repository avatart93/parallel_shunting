
import multiprocessing
import socket
import time

from src import tools


CONNECTION_LOGS_DIR = "../data/logs/"


class Server:

    def __init__(self):

        self._server = None

    def launch(self, func, logs_path=None, verbose=False, log_exchange=True):
        """ Creates a daemon process to serve the 'func' and starts it. """

        # Define log file path for server with unique name.
        date_time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        logs_name = "server_{0}.txt".format(date_time_stamp)

        answer = tools.verify_dir(logs_path, like='dir', append=logs_name)
        if answer == "Invalid path.":
            return "Wrong 'logs_path' provided, can't find the directory, please verify these and try again."
        logs_path = answer

        # Hosts the serve function and passes func as its parameter.
        self._server = multiprocessing.Process(name='server',
                                               target=Server.serve,
                                               args=[func, logs_path, verbose, log_exchange])
        self._server.daemon = True
        self._server.start()

    @staticmethod
    def serve(func, logs_path, verbose, log_exchange, port=65432):
        """ This function is launched in a daemon process and serves the 'func' provided. Any data
         received by the server will be passed as a parameter to 'func' and the result will be then
          return to the client. """

        # Open a file descriptor for logs if one was provided.
        server_log_fd = open(logs_path, 'w') if logs_path is not None else None

        tools.manage_message(server_log_fd, verbose, "Server started.")
        tools.manage_message(server_log_fd, verbose, "Listening through port {0}.".format(port))
        tools.manage_message(server_log_fd, verbose, "Serving function {0}.".format(func.__name__))

        # Create the socket and start listening.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
            channel.bind(('127.0.0.1', port))
            channel.listen(3)

            while True:

                # Accept any connection attempt, only one at a time though.
                connection, address = channel.accept()

                tools.manage_message(server_log_fd, verbose, "Connected by {0}.".format(address))

                while True:

                    # Fulfill all the requests until connection is closed by the client.
                    data = connection.recv(1024).decode()

                    # Client closed connection, logged too.
                    if not data:
                        tools.manage_message(server_log_fd, verbose, "{0} closed connection.".format(address))
                        if server_log_fd is not None:
                            server_log_fd.flush()
                        break

                    result = str(func(data))
                    connection.send(result.encode())

                    # Log exchange between client and server.
                    if log_exchange:
                        tools.manage_message(server_log_fd, verbose, "Received -> {0}.".format(data))
                        tools.manage_message(server_log_fd, verbose, "Reply -> {0}.".format(result))

    def kill(self):
        """ Kills the process serving. """

        self._server.terminate()
        self._server.join()  # To give time to the object to update its status.


def main():

    # Serve the shunting yard function (default configuration).

    from src import evaluator

    server_instance = Server()
    answer = server_instance.launch(evaluator.shunting_yard, CONNECTION_LOGS_DIR, False)

    if answer is None:
        print("Serving -> Function: Shunting Yard, Port: 65432")
        while True:
            pass
    else:
        print("Error detected: {0}".format(answer))


if __name__ == "__main__":

    main()
