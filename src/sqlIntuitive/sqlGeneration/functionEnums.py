from enum import Enum, auto
from sqlIntuitive.sqlGeneration import standard, mysql, sqlite

class Standard(Enum):
    SELECT_FROM = standard.gen_select
    SELECT_COUNT = standard.gen_count
    SELECT_AVG = standard.gen_avg
    SELECT_SUM = standard.gen_sum
    SELECT_JOIN = standard.gen_select_join
    INSERT_INTO = standard.gen_insert
    UPDATE = standard.gen_update
    DELETE_FROM = standard.gen_delete
    CREATE_DB = standard.gen_create_db
    DROP_DB = standard.gen_drop_db
    CREATE_TABLE = standard.gen_create_table
    DROP_TABLE = standard.gen_drop_table
    ALTER_TABLE_ADD = standard.gen_alter_table_add
    ALTER_TABLE_DROP = standard.gen_alter_table_drop
    ALTER_TABLE_MODIFY = standard.gen_alter_table_modify
    CREATE_STORED_PROCEDURE = standard.gen_create_stored_procedure
    EXEC_PROCEDURE = standard.gen_exec_procedure
    DROP_PROCEDURE = standard.gen_drop_procedure

class MySQL(Standard):
    CREATE_STORED_PROCEDURE = mysql.gen_create_stored_procedure
    EXEC_PROCEDURE = mysql.gen_exec_procedure
    ALTER_TABLE_MODIFY = mysql.gen_alter_table_modify

class SqLite(Standard):
    ALTER_TABLE_RENAME_TABLE = sqlite.gen_alter_table_rename_table
    ALTER_TABLE_RENAME_COLUMN = sqlite.gen_alter_table_rename_column
