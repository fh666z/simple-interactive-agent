from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """
    Add a and b.
    
    Args:
        a (int): first integer to be added
        b (int): second integer to be added

    Return:
        int: sum of a and b
    """
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b

@tool
def calculate_tip(total_bill: float, tip_percentage: float) -> float:
    """Calculate the tip for a given total bill and tip percentage."""
    return total_bill * (tip_percentage / 100)


# List of all tools
tools = [add, subtract, multiply]

# Map tool names to tool functions for manual invocation
tool_map = {t.name: t for t in tools}
