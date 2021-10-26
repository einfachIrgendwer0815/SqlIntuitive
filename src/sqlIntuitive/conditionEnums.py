from enum import Enum

class ComparisonTypes(Enum):
    EQUAL_TO = "="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUAL_TO = ">="
    LESS_THAN_OR_EQUAL_TO = "<="
    NOT_EQUAL_TO = "!="

class CombinationTypes(Enum):
    AND = "AND"
    OR = "OR"
