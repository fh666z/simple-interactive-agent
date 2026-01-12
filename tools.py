from langchain_core.tools import tool


@tool
def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Use this tool when you need to calculate the sum of two numbers.
    
    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    
    Example:
        add(3, 5) returns 8
        add(2.5, 1.5) returns 4.0
    """
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """
    Subtract one number from another.
    
    Use this tool when you need to find the difference between two numbers.
    Calculates a minus b.
    
    Args:
        a (float): The number to subtract from (minuend).
        b (float): The number to subtract (subtrahend).

    Returns:
        float: The result of a minus b.
    
    Example:
        subtract(10, 4) returns 6
        subtract(5.5, 2.5) returns 3.0
    """
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together.
    
    Use this tool when you need to calculate the product of two numbers.
    
    Args:
        a (float): The first number (multiplicand).
        b (float): The second number (multiplier).

    Returns:
        float: The product of a and b.
    
    Example:
        multiply(6, 7) returns 42
        multiply(2.5, 4) returns 10.0
    """
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """
    Divide one number by another.
    
    Use this tool when you need to calculate the quotient of two numbers.
    Calculates a divided by b.
    
    Args:
        a (float): The number to be divided (dividend).
        b (float): The number to divide by (divisor). Must not be zero.

    Returns:
        float: The result of a divided by b.
    
    Example:
        divide(20, 4) returns 5.0
        divide(7, 2) returns 3.5
    """
    return a / b


@tool
def calculate_tip(total_bill: float, tip_percentage: float) -> float:
    """
    Calculate the tip amount for a bill.
    
    Use this tool when you need to calculate how much tip to leave
    based on a total bill amount and a desired tip percentage.
    
    Args:
        total_bill (float): The total bill amount in dollars.
        tip_percentage (float): The tip percentage (e.g., 15 for 15%, 20 for 20%).

    Returns:
        float: The tip amount in dollars.
    
    Example:
        calculate_tip(50, 20) returns 10.0 (20% tip on a $50 bill)
        calculate_tip(85.50, 18) returns 15.39 (18% tip on an $85.50 bill)
    """
    return total_bill * (tip_percentage / 100)


# List of all tools
tools = [add, subtract, multiply, divide, calculate_tip]

# Map tool names to tool functions for manual invocation
tool_map = {t.name: t for t in tools}
