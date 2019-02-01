
from src import operations


ERROR_THRESHOLD = 1e-3


def test_add():
    assert operations.add(1, 2) - 3 < ERROR_THRESHOLD
    assert operations.add(-1, 2) - 1 < ERROR_THRESHOLD
    assert operations.add(-1, -2) - -3 < ERROR_THRESHOLD
    assert operations.add(0, 1) - 1 < ERROR_THRESHOLD


def test_subtract():
    assert operations.subtract(1, 2) - -1 < ERROR_THRESHOLD
    assert operations.subtract(-1, 2) - -3 < ERROR_THRESHOLD
    assert operations.subtract(-1, -2) - 1 < ERROR_THRESHOLD
    assert operations.subtract(0, 1) - -1 < ERROR_THRESHOLD


def test_multiply():
    assert operations.multiply(1, 2) - 2 < ERROR_THRESHOLD
    assert operations.multiply(-1, 2) - -2 < ERROR_THRESHOLD
    assert operations.multiply(-1, -2) - 2 < ERROR_THRESHOLD
    assert operations.multiply(0, 1) - 0 < ERROR_THRESHOLD


def test_divide():
    assert operations.divide(2, 1) - 2 < ERROR_THRESHOLD
    assert operations.divide(0, 2) - 0 < ERROR_THRESHOLD
    assert operations.divide(1, -2) - -0.5 < ERROR_THRESHOLD
    assert operations.divide(4, 3) - 1.333 < ERROR_THRESHOLD


def main():

    test_add()
    test_subtract()
    test_multiply()
    test_divide()

    print("All operations tests finished correctly.")


if __name__ == "__main__":
    main()
