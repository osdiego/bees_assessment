'''
Simple functions to exemplify how to build a documentation automatically using pdoc
'''


def addition(num1: float, num2: float = 0) -> float:
    '''Adds two numbers

    Args:
        num1 (float): the first number
        num2 (float, optional): the second number. Defaults to 0.

    Returns:
        float: the result of the sum operation
    '''

    return (num1+num2)


def mult(num1: float, num2: float = 1) -> float:
    '''Multiplies two numbers

    Args:
        `num1` (float): The first number.
        `num2` (float, optional): The second number. Defaults to `1`.

    Returns:
        float: The result of the **multiplication** process
    '''

    return (num1*num2)
