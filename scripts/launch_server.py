
from parallel_shunting import server


CONNECTION_LOGS_DIR = "../data/logs/"


def main():

    # Serve the shunting yard function (default configuration).

    from parallel_shunting import evaluator

    server_instance = server.Server()
    answer = server_instance.launch(evaluator.shunting_yard, CONNECTION_LOGS_DIR, False)

    if answer is None:
        print("Serving -> Function: Shunting Yard, Port: 65432")
        while True:
            pass
    else:
        print("Error detected: {0}".format(answer))


if __name__ == "__main__":

    main()
