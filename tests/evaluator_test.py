
from src import evaluator


ERROR_THRESHOLD = 1e-3


def test_shunting_yard():
    """ Tests the shunting yard algorithm, will raise an exception if any of the test cases fails. """

    case_1 = "38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77"
    case_2 = "57 + 87 - 24 * 27 / 8 + 53 - 87 * 6 * 60 - 30"
    case_3 = "63 * 23 - 91 - 17 * 45 + 63 * 52 - 50"
    case_4 = "47 - 88 + 32 - 71 * 39 * 68"
    case_5 = "43 * 47 - 75 + 94 * 35 - 60 + 55 + 8"
    case_6 = "49 - 97 + 17 + 31 / 37 + 82"
    case_7 = "74 - 36 - 96 + 32 + 2 + 26"
    case_8 = "43 - 45 - 66 - 52 - 6"
    case_9 = "41 / 50 + 53 + 40"
    case_10 = "40 * 76 + 97 - 90 * 52"
    case_11 = "62 - 42 + 7 - 74 / 88"
    case_12 = "66 - 11 / 5 / 58 + 18 - 58 - 88 + 97"
    case_13 = "36 / 48 * 21 - 36 + 69 + 26 + 35 + 49 + 7"
    case_14 = "58 * 10 - 19 - 59"
    case_15 = "63 / 68 * 86 - 62 - 32"

    assert evaluator.shunting_yard(case_1) - eval(case_1) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_2) - eval(case_2) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_3) - eval(case_3) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_4) - eval(case_4) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_5) - eval(case_5) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_6) - eval(case_6) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_7) - eval(case_7) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_8) - eval(case_8) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_9) - eval(case_9) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_10) - eval(case_10) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_11) - eval(case_11) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_12) - eval(case_12) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_13) - eval(case_13) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_14) - eval(case_14) < ERROR_THRESHOLD
    assert evaluator.shunting_yard(case_15) - eval(case_15) < ERROR_THRESHOLD


def main():

    test_shunting_yard()

    print("All expressions were computed correctly.")


if __name__ == "__main__":
    main()
