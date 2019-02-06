
from parallel_shunting import client


DEFAULT_INPUT_PATH = "../data/scripts/operations.txt"
DEFAULT_OUTPUT_PATH = "../data/scripts/results.txt"
CONNECTION_LOGS_DIR = "../data/logs/"


def main():

    # Compute math expressions in operations.txt (default configuration)

    client_instance = client.Client()
    client_instance.open_channel(logs_path=CONNECTION_LOGS_DIR)

    answer = client_instance.process_batch(DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH, verbose=False)

    client_instance.close_channel()

    if answer is None:
        print("Computations finished.")
    else:
        print("Error detected: {0}".format(answer))


if __name__ == "__main__":

    main()
