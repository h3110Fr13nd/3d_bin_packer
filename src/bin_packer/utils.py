# utils.py

from typing import Union
import math

# Precision to retain in factored_integer()
FACTOR = 5

def factored_integer(value: Union[int, float]) -> int:
    """
    Factor a number by FACTOR and round to the nearest whole number.
    
    Args:
        value (Union[int, float]): The number to be factored
        
    Returns:
        int: The factored and rounded number
        
    Example:
        >>> factored_integer(1.23456)
        123456
        >>> factored_integer(1.23454)
        123454
    """
    return round(value * (10 ** FACTOR))