
# This operations will be used to avoid the usage of 'eval' by the Shunting Yard Algorithm.


def get_math_func(operator):
    """ Returns the function to apply given a basic math operator. """

    if operator == '+':
        return add
    elif operator == '-':
        return subtract
    elif operator == '*':
        return multiply
    else:  # '/':
        return divide


def add(a, b):
    """ Returns the result of adding the parameters. """

    return a + b


def subtract(a, b):
    """ Returns the result of subtracting the first parameter by the second. """

    return a - b


def multiply(a, b):
    """ Returns the result of multiplying the parameters. """

    return a * b


def divide(a, b):
    """ Returns the result of dividing the first parameter by the second. """

    return a / b
