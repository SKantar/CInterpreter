"""
This module file supports basic functions from math.h library
"""

from ..utils.utils import definition
import math

@definition(return_type='double', arg_types=['double'])
def sqrt(a):
    return math.sqrt(a)