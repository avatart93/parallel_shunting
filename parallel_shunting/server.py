
import multiprocessing
import socket
import time

from parallel_shunting import tools
from parallel_shunting import children
from parallel_shunting import buffer


class Server:

    def __init__(self):

        self._server = None

    def launch(self, func, logs_path=None, verbose=False, log_exchange=True, children_count=5):
        """ Creates a process to serve the 'func' and starts it. It will create 'children'
         processes to fulfill request. """

        # Define log file path for server with unique name.
        date_time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        logs_name = "server_{0}.txt".format(date_time_stamp)

        answer = tools.verify_dir(logs_path, like='dir', append=logs_name)
        if answer == "Invalid path.":
            return "Wrong 'logs_path' provided, can't find the directory, please verify these and try again."
        logs_path = answer

        # Hosts the serve function and passes func as its parameter.
        self._server = multiprocessing.Process(name='server',
                                               target=Server._serve,
                                               args=[func, logs_path, verbose, log_exchange, children_count])
        self._server.start()

    @staticmethod
    def _serve(func, logs_path, verbose, log_exchange, children_count, port=65432):
        """ It's ran in a different server process, that will launch 'children' processes to serve
        'func'. Any data received by this server will be passed as a parameter to an available child
         process and the result will be then sent back to the client. """

        children_handler = children.ChildrenHandler(children_count, func)

        # Open a file descriptor for logs if one was provided.
        server_log_fd = open(logs_path, 'w') if logs_path is not None else None

        tools.manage_message(server_log_fd, verbose, "Server started.")
        tools.manage_message(server_log_fd, verbose, "Listening through port {0}.".format(port))
        tools.manage_message(server_log_fd, verbose, "Serving function {0}.".format(func.__name__))

        # Create the socket and start listening.
        channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        channel.bind(('127.0.0.1', port))
        channel.listen(1)

        while True:

            # Accept any connection attempt, only one at a time though.
            connection, address = channel.accept()

            tools.manage_message(server_log_fd, verbose, "Connected by {0}.".format(address))

            buffer_handler = buffer.BufferHandler()

            closed_receive = False
            pending_lines = []

            # Process all data lines sent by client.
            while True:

                pending_lines.extend(buffer_handler.receive(connection))

                # Something to process can be processed.
                if len(pending_lines) > 0 and children_handler.can_send():
                    received_line = pending_lines.pop(0)

                    if received_line == "End":
                        closed_receive = True

                    else:
                        children_handler.send(received_line)

                        if log_exchange:
                            tools.manage_message(server_log_fd, verbose, "Received -> {0}".format(received_line))

                children_handler.update_receiving()

                # Something to receive.
                if children_handler.can_receive():
                    line_to_send = children_handler.receive()

                    buffer_handler.send(connection, line_to_send)

                    if log_exchange:
                        tools.manage_message(server_log_fd, verbose, "Reply -> {0}".format(line_to_send))

                # All done.
                if closed_receive and not children_handler.working() and not children_handler.can_receive():

                    buffer_handler.send(connection, "End\n")

                    tools.manage_message(server_log_fd, verbose, "Requests of {0} fulfilled.".format(address))
                    server_log_fd.flush()

                    connection.close()

                    break

    def kill(self):
        """ Kills the process serving. """

        self._server.terminate()
        self._server.join()  # To give time to the object to update its status.
