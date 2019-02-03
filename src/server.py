

import socket


HOST = '127.0.0.1'  # Localhost.
PORT = 65432  # Port to listen on.


def server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
        channel.bind((HOST, PORT))
        channel.listen(3)

        connection, address = channel.accept()
        print("Connected by {0}".format(address))

        while True:

            data = connection.recv(1024)
            connection.send(data)


def main():

    server()


if __name__ == "__main__":

    main()
