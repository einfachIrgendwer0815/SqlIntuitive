from enum import Enum, auto
from sqlIntuitive import sqlGeneration

class Standard(Enum):
    SELECT_FROM = sqlGeneration.standard.gen_select
    SELECT_COUNT = sqlGeneration.standard.gen_count
    SELECT_AVG = sqlGeneration.standard.gen_avg
    SELECT_SUM = sqlGeneration.standard.gen_sum
    SELECT_JOIN = sqlGeneration.standard.gen_select_join
    INSERT_INTO = sqlGeneration.standard.gen_insert
    UPDATE = sqlGeneration.standard.gen_update
    DELETE_FROM = sqlGeneration.standard.gen_delete
    CREATE_DB = sqlGeneration.standard.gen_create_db
    DROP_DB = sqlGeneration.standard.gen_drop_db
    CREATE_TABLE = sqlGeneration.standard.gen_create_table
    DROP_TABLE = sqlGeneration.standard.gen_drop_table
    ALTER_TABLE_ADD = sqlGeneration.standard.gen_alter_table_add
    ALTER_TABLE_DROP = sqlGeneration.standard.gen_alter_table_drop
    ALTER_TABLE_MODIFY = sqlGeneration.standard.gen_alter_table_modify
    CREATE_STORED_PROCEDURE = sqlGeneration.standard.gen_create_stored_procedure
    EXEC_PROCEDURE = sqlGeneration.standard.gen_exec_procedure
    DROP_PROCEDURE = sqlGeneration.standard.gen_drop_procedure

class MySQL(Standard):
    CREATE_STORED_PROCEDURE = sqlGeneration.mysql.gen_create_stored_procedure
    EXEC_PROCEDURE = sqlGeneration.mysql.gen_exec_procedure
    ALTER_TABLE_MODIFY = sqlGeneration.mysql.gen_alter_table_modify

class SqLite(Standard):
    ALTER_TABLE_RENAME_TABLE = sqlGeneration.sqlite.gen_alter_table_rename_table
    ALTER_TABLE_RENAME_COLUMN = sqlGeneration.sqlite.gen_alter_table_rename_column
