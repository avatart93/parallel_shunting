
import re
from src import operations


OPERATORS_PRECEDENCE = {'+': 0, '-': 0, '*': 1, '/': 1}


def greater_or_equal_precedence(operator_a, operator_b):
    """ Lets you know if the first operator has greater or equal precedence than the second one. """

    return OPERATORS_PRECEDENCE[operator_a] >= OPERATORS_PRECEDENCE[operator_b]


def is_number(string):
    """ Given a string, lets you know if it can parsed into an integer. """

    try:
        int(string)
        return True
    except ValueError:
        return False


def is_correct_expression(expression_string):
    """ Will return true if the string contains a valid mathematical expressions. """

    return re.fullmatch("(\d+[+\-*/])+\d+", expression_string) is not None


def compute_one_operation(numbers_stack, operators_stack):
    """ Will extract one operator, compute it over the last two numbers and append the result. """

    operator = operators_stack.pop()

    right_operand = numbers_stack.pop()
    left_operand = numbers_stack.pop()

    math_func = operations.get_math_func(operator)
    result = math_func(left_operand, right_operand)

    numbers_stack.append(result)


def shunting_yard(expression_string):
    """ Receives a mathematical expressions as a string and solves it using stacks to rearrange the
    order of the operations. """

    expression_string = expression_string.replace(' ', '')
    if not is_correct_expression(expression_string):
        print("Invalid expression: {0}.".format(expression_string))
        return None

    numbers_stack = []
    operators_stack = []

    tokens = re.findall("\d+|[+\-*/]", expression_string)
    for token in tokens:

        if is_number(token):
            current_number = int(token)
            numbers_stack.append(current_number)

        else:  # Operator
            current_operator = token

            last_operator = operators_stack[-1] if len(operators_stack) > 0 else None
            while last_operator is not None and greater_or_equal_precedence(last_operator, current_operator):
                compute_one_operation(numbers_stack, operators_stack)
                last_operator = operators_stack[-1] if len(operators_stack) > 0 else None

            operators_stack.append(current_operator)

    while len(operators_stack) > 0:
        compute_one_operation(numbers_stack, operators_stack)

    return numbers_stack[0]
