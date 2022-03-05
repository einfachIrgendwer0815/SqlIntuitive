from sqlIntuitive import exceptions
from sqlIntuitive.sqlGeneration.standard import check_validName

def gen_alter_table_rename_table(tableName: str, newTableName: str) -> str:
    if check_validName(tableName) == False or len(tableName) == 0 or check_validName(newTableName) == False or len(newTableName) == 0:
        raise exceptions.InvalidTableNameException()

    text = f"ALTER TABLE {tableName} RENAME TO {newTableName};"

    return text

def gen_alter_table_rename_column(tableName: str, columnName: str, newColumnName: str) -> str:
    if check_validName(tableName) == False or len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

    text = f"ALTER TABLE {tableName} RENAME COLUMN {columnName} TO {newColumnName};"

    return text
