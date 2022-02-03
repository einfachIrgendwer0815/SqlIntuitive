from enum import Enum, auto

class Standard(Enum):
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
    CREATE_STORED_PROCEDURE = auto()
    EXEC_PROCEDURE = auto()
    DROP_PROCEDURE = auto()

class MySQL(Enum):
    CREATE_STORED_PROCEDURE = auto()
    EXEC_PROCEDURE = auto()
