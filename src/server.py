

import multiprocessing
import socket


class Server:

    @staticmethod
    def launch(func, daemon=True):

        server = multiprocessing.Process(name='server', target=Server.serve, args=[func])
        server.daemon = daemon

        server.start()
        print("Server started with pid = {0}.".format(server.pid))

    @staticmethod
    def serve(func, port=65432):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
            channel.bind(('127.0.0.1', port))
            channel.listen(3)

            connection, address = channel.accept()
            print("Connected by {0}".format(address))

            while True:

                data = connection.recv(1024).decode()
                if not data:
                    break
                result = str(func(data))
                connection.send(result.encode())
