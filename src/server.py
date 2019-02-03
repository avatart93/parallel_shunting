

import multiprocessing
import socket


class Server:

    def __init__(self):

        self._sever = None

    def launch(self, func):
        """ Creates a daemon process to serve the 'func' and starts it. """

        # Hosts the serve function and passes func as its parameter.
        self._sever = multiprocessing.Process(name='server', target=Server.serve, args=[func])
        self._sever.daemon = True

        self._sever.start()
        print("Server started with pid = {0}.".format(self._sever.pid))

    @staticmethod
    def serve(func, port=65432):
        """ This function is launched in a daemon process and serves the 'func' provided. Any data
         received by the server will be passed as a parameter to 'func' and the result will be then
          return to the client. """

        # Create the socket and start listening.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
            channel.bind(('127.0.0.1', port))
            channel.listen(3)

            while True:

                # Accept any connection attempt, only one at a time though.
                connection, address = channel.accept()
                print("Connected by {0}".format(address))

                while True:

                    # Fulfill all the requests until connection is closed by the client.
                    data = connection.recv(1024).decode()
                    if not data:
                        break
                    result = str(func(data))
                    connection.send(result.encode())

    def kill(self):
        """ Kills the process serving. """

        self._sever.terminate()

        self._sever.join()  # To give time to the object to update its status.


def main():

    # Serve the shunting yard function (default configuration).

    from src import evaluator

    server_instance = Server()
    server_instance.launch(evaluator.shunting_yard)

    print("Serving -> Function: Shunting Yard, Port: 65432")

    while True:
        pass


if __name__ == "__main__":

    main()
