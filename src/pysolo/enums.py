from enum import Enum

# Used by threshold_field, set_bad_flags, bad_flags_logic
class Where(Enum):
    ABOVE = 0
    BELOW = 1
    BETWEEN = 2
    
# Used by bad_flags_logic
class Logical(Enum):
    AND = 0
    OR = 1
    XOR = 2
