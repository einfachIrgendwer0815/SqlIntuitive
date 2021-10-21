from sqlIntuitive import exceptions

import string
import re

INVALID_CHARS = ['!', '"', '#', r'\$', '%', '&', "'", r'\(', r'\)', r'\*', r'\+', ',', '-', '/', ':', ';', '<', '=', '>', r'\?', '@', r'\[', r'\\', r'\]', r'\^', '_', '`', r'\{', r'\|', r'\}', '~', ' ', '\n', '\t']

def check_validName(text: str) -> bool:
    for char in INVALID_CHARS:
        if re.match(f'.*{char}.*', text, re.I):
            return False

    return True

def gen_select(tableName: str, columns: list = [], conditions: dict = {}, conditionCombining: str = "AND", placeholder: str = '?') -> tuple:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    if len(columns) == 0:
        columns = ('*')

    text = 'SELECT '
    text += ', '.join(columns)

    text += f' FROM {tableName}'

    column_values_ordered = []

    if len(conditions) > 0:
        text += ' WHERE '

        conditionTexts = []
        for column in conditions.keys():
            conditionTexts.append(f'{column}={placeholder}')
            column_values_ordered.append(conditions[column])

        text += f' {conditionCombining} '.join(conditionTexts)

    text += ';'

    return text, column_values_ordered

def gen_insert(tablename: str, column_values: dict, placeholder: str = "?") -> tuple:
    if check_validName(tablename) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tablename) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    if len(column_values) == 0:
        raise exceptions.DictionaryEmptyException("No columns set.")

    column_values_ordered = []

    text = f'INSERT INTO {tablename} ('

    text += ', '.join([f'{column}' for column in column_values.keys()])

    text += ') VALUES ('

    value_texts = []
    for column in column_values.keys():
        value_texts.append(f'{placeholder}')
        column_values_ordered.append(column_values[column])

    text += ', '.join(value_texts)

    text += ');'

    return text, column_values_ordered

def gen_update(tableName: str, newValues: dict, conditions: dict = {}, conditionCombining: str = "AND", placeholder: str = "?") -> tuple:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    if len(newValues) == 0:
        raise exceptions.DictionaryEmptyException("No values to change specified.")

    column_values_ordered = []

    text = f'UPDATE {tableName} SET '

    setTexts = []
    for column in newValues.keys():
        setText = f'{column}={placeholder}'
        setTexts.append(setText)

        column_values_ordered.append(newValues[column])

    text += ', '.join(setTexts)

    if len(conditions) > 0:
        text += ' WHERE '

        conditionTexts = []
        for column in conditions.keys():
            conditionText = f'{column}={placeholder}'
            conditionTexts.append(conditionText)

            column_values_ordered.append(conditions[column])

        text += f' {conditionCombining} '.join(conditionTexts)

    text += ';'

    return text, column_values_ordered

def gen_delete(tablename: str, conditions: dict = {}, conditionCombining: str = "AND", placeholder: str = "?") -> tuple:
    if check_validName(tablename) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tablename) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    column_values_ordered = []
    text = f'DELETE FROM {tablename}'

    if len(conditions) > 0:
        text += ' WHERE '

        conditionsText = []

        for column in conditions.keys():
            condition_text = f'{column}={placeholder}'
            conditionsText.append(condition_text)

            column_values_ordered.append(conditions[column])

        text += f' {conditionCombining} '.join(conditionsText)

    text += ';'

    return text, column_values_ordered

def gen_create_db(dbName: str) -> str:
    if check_validName(dbName) == False:
        raise exceptions.InvalidDatabaseNameException("Databasename contains invalid characters.")

    if len(dbName) == 0:
        raise exceptions.InvalidDatabaseNameException("Databasename invalid.")

    text = f'CREATE DATABASE {dbName};'

    return text

def gen_drop_db(dbName: str) -> str:
    if check_validName(dbName) == False:
        raise exceptions.InvalidDatabaseNameException("Databasename contains invalid characters.")

    if len(dbName) == 0:
        raise exceptions.InvalidDatabaseNameException("Databasename invalid.")

    text = f'DROP DATABASE {dbName};'

    return text

def gen_create_table(tableName: str, columns: dict, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> str:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(columns) == 0:
        raise exceptions.DictionaryEmptyException("No columns set.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    for primary in primaryKeys:
        if primary not in columns.keys():
            raise exceptions.InvalidPrimaryKeyColumn(f'{primary} not in columns.')

    for foreign in foreignKeys.keys():
        if foreign not in columns.keys():
            raise exceptions.InvalidForeignKeyColumn(f'{foreign} not in columns')

    for unique in uniqueColumns:
        if unique not in columns.keys():
            raise exceptions.InvalidUniqueColumn(f'{unique} not in columns')

    for named in namedForeignKeys.keys():
        if named not in columns.keys():
            raise exceptions.InvalidForeignKeyColumn(f'{named} not in columns')

        if type(namedForeignKeys[named]) != dict or 'name' not in namedForeignKeys[named].keys() or 'reference' not in namedForeignKeys[named].keys():
            raise exceptions.InvalidNamedForeignKeyDictionary(f'Values for column {named} are not defined')

    text = 'CREATE TABLE '
    if safeMode:
        text += 'IF NOT EXISTS '

    text += f'{tableName} ('

    columnTexts = []

    for column in columns.keys():
        columnText = f'{column} {columns[column]}'

        columnTexts.append(columnText)

    if len(primaryKeys) > 0:
        primaryText = 'PRIMARY KEY ('
        primarySubTexts = []

        for primary in primaryKeys:
            primarySubTexts.append(str(primary))

        primaryText += ','.join(primarySubTexts)
        primaryText += ')'

        columnTexts.append(primaryText)

    for foreign in foreignKeys.keys():
        foreignText = f'FOREIGN KEY ({foreign}) REFERENCES {foreignKeys[foreign]}'

        columnTexts.append(foreignText)

    for foreign in namedForeignKeys.keys():
        foreignText = f'CONSTRAINT {namedForeignKeys[foreign]["name"]} FOREIGN KEY ({foreign}) REFERENCES {namedForeignKeys[foreign]["reference"]}'

        columnTexts.append(foreignText)

    for unique in uniqueColumns:
        uniqueText = f'UNIQUE ({unique})'

        columnTexts.append(uniqueText)

    text += ', '.join(columnTexts)

    text += ');'

    return text

def gen_drop_table(tableName: str) -> str:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename invalid.")

    text = f'DROP TABLE {tableName};'

    return text
