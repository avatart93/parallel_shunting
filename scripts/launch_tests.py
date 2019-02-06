

from parallel_shunting import tests


EXPRESSIONS_PATH = "../data/scripts/communication_in.txt"
RESULTS_PATH = "../data/scripts/communication_tmp.txt"
TEMPLATE_PATH = "../data/scripts/communication_out.txt"


def main():

    tests.test_add()
    tests.test_subtract()
    tests.test_multiply()
    tests.test_divide()

    print("All operations tests finished correctly.")

    tests.test_shunting_yard()

    print("All expressions were computed correctly.")

    print("Testing asynchronous work.")

    for run_index in range(10):

        answer = tests.test_asynchronous_communication(EXPRESSIONS_PATH, RESULTS_PATH, TEMPLATE_PATH)

        if answer is None:
            print("{0} -> Operations batch computed correctly.".format(run_index + 1))
        else:
            print("Error detected: {0}".format(answer))

    print("All done.")


if __name__ == "__main__":

    main()
