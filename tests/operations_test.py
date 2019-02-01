
from src import operations


def test_add():
    assert operations.add(1, 2) == 3
    assert operations.add(-1, 2) == 1
    assert operations.add(-1, -2) == -3
    assert operations.add(0, 1) == 1


def test_subtract():
    assert operations.subtract(1, 2) == -1
    assert operations.subtract(-1, 2) == -3
    assert operations.subtract(-1, -2) == 1
    assert operations.subtract(0, 1) == -1


def test_multiply():
    assert operations.multiply(1, 2) == 2
    assert operations.multiply(-1, 2) == -2
    assert operations.multiply(-1, -2) == 2
    assert operations.multiply(0, 1) == 0


def test_divide():
    assert operations.divide(2, 1) - 2 < 1e-2
    assert operations.divide(0, 2) - 0 < 1e-2
    assert operations.divide(1, -2) - -0.5 < 1e-2
    assert operations.divide(4, 3) - 1.33 < 1e-2


def main():

    test_add()
    test_subtract()
    test_multiply()
    test_divide()

    print("All operations tests finished correctly.")


if __name__ == "__main__":
    main()
