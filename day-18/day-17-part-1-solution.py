# --- Day 18: Operation Order ---


def parse_expression(expression : str) -> list:
    """Parses the input expression and returns a list, where all the different
    elements of the expression (integers, operators) are separate items in a list.
    """
    parsed_expression = []
    for item in expression.split(" "):
        if item == "+":
            parsed_expression.append(item)
        elif item == "*":
            parsed_expression.append(item)
        elif item[0] == "(":
            idx = 0
            while item[idx+1] == "(":  # check for nested parentheses
                parsed_expression.append(item[idx])
                idx += 1
            parsed_expression.append(item[idx])
            parsed_expression.append(int(item[idx+1:]))
        elif item[-1] == ")":
            idx = -1
            while item[idx-1] == ")":  # check for nested parentheses
                idx -= 1
            parsed_expression.append(int(item[:idx]))
            for _ in range(idx, 0, 1):
                parsed_expression.append(")")
        else:
            parsed_expression.append(int(item))
  
    return parsed_expression


def get_solution(expression : str) -> int:
    """Parses the input mathematical expression and returns the solution using
    the new "left to right" precedence rules for the + and * operations.
    """
    # first parse the expression
    parsed_expression = parse_expression(expression=expression)

    # then, go through and evaluate any parentheses
    while "(" in parsed_expression:
        expression_without_parentheses = []
        idx = 0
        while idx < len(parsed_expression):
            item = parsed_expression[idx]
            if item == "(":
                # look for 1) the closed parentheses and/or 2) any nested parentheses
                end_idx = idx + 1
                while parsed_expression[end_idx] != ")":
                    # check for nested parentheses, in which case we must evaluate
                    # the innermost one first
                    if parsed_expression[end_idx] == "(":
                        for outer_parentheses_idx in range(idx, end_idx):
                            expression_without_parentheses.append(parsed_expression[outer_parentheses_idx])
                        idx = end_idx
                    end_idx += 1
                # evaluate the innermost parentheses
                parentheses_expression = parsed_expression[idx+1:end_idx]
                parentheses_expression_solution = evaluate_expression(expression=parentheses_expression)
                expression_without_parentheses.append(parentheses_expression_solution)
                idx = end_idx + 1
            else:
                expression_without_parentheses.append(item)
                idx += 1
        parsed_expression = expression_without_parentheses

    # finally, evaluate the remaining expression
    solution = evaluate_expression(expression=parsed_expression)
    
    return solution


def evaluate_expression(expression : list) -> int:
    """Loops over the items in the expression and applies the operations from
    left to right.
    """
    solution = expression[0]
    for idx, item in enumerate(expression[1:]):
        if item == "+":
            solution += expression[idx+2]
        elif item == "*":
            solution *= expression[idx+2]
        else:
            pass

    return solution


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        math_expressions = input_data.read().split("\n")[:-1]  # throw away the last empty item

    # find the solution to each expression in `math_expressions` using the different precedence rules
    solutions = []
    for expression in math_expressions:
        solutions.append(get_solution(expression=expression))

    # the answer to the puzzle is the sum of all the values which the the expressions
    # in `math_expressions` evaluate to
    answer = sum(solutions)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
