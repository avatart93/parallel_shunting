
import re


OPERATORS_ORDER = {'+': 0, '-': 0, '*': 1, '/': 1}


def greater_order(operator_a, operator_b):
    return OPERATORS_ORDER[operator_a] >= OPERATORS_ORDER[operator_b]


def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_correct_expression(expression_string):
    """ Will return true if the string contains a valid mathematical expressions. """

    # TODO: Actually verify the expression.
    return True


def compute_one_operation(numbers_stack, operators_stack):

    right_operand = numbers_stack.pop()
    left_operand = numbers_stack.pop()

    operator = operators_stack.pop()

    # TODO: Get rid of eval.
    numbers_stack.append(eval("{0} {1} {2}".format(left_operand, operator, right_operand)))


def shunting_yard(expression_string):
    """ Receives a mathematical expressions as a string and solves it using stacks to rearrange the
    order of the operations. """

    if not is_correct_expression(expression_string):
        print("Invalid expression: {0}.".format(expression_string))
        return None

    numbers_stack = []
    operators_stack = []

    tokens = re.findall("[+\-*/]|\d+", expression_string)
    for token in tokens:

        if is_number(token):
            current_number = int(token)
            numbers_stack.append(current_number)

        else:  # Operator
            current_operator = token

            last_operator = operators_stack[-1] if len(operators_stack) > 0 else None
            while last_operator is not None and greater_order(last_operator, current_operator):
                compute_one_operation(numbers_stack, operators_stack)
                last_operator = operators_stack[-1] if len(operators_stack) > 0 else None

            operators_stack.append(current_operator)

    while len(operators_stack) > 0:
        compute_one_operation(numbers_stack, operators_stack)

    return numbers_stack[0]
