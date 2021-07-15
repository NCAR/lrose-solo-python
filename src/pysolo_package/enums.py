from enum import Enum

class Where(Enum):
    ABOVE = 0
    BELOW = 1
    BETWEEN = 2
    
class Logical(Enum):
    AND = 0
    OR = 1
    XOR = 2
