from enum import Enum, auto

class NameAsValue(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class Standard(NameAsValue):
    SELECT_FROM = auto()
    SELECT_COUNT = auto()
    SELECT_AVG = auto()
    SELECT_SUM = auto()
    INSERT_INTO = auto()
    UPDATE = auto()
    DELETE_FROM = auto()
    CREATE_DB = auto()
    DROP_DB = auto()
    CREATE_TABLE = auto()
    DROP_TABLE = auto()
    ALTER_TABLE_ADD = auto()
    ALTER_TABLE_DROP = auto()
    ALTER_TABLE_MODIFY = auto()
    CREATE_STORED_PROCEDURE = auto()
    EXEC_PROCEDURE = auto()
    DROP_PROCEDURE = auto()

class MySQL(NameAsValue):
    CREATE_STORED_PROCEDURE = auto()
    EXEC_PROCEDURE = auto()
    ALTER_TABLE_MODIFY = auto()

class SqLite(NameAsValue):
    ALTER_TABLE_RENAME = auto()
