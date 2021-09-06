from sqlIntuitive import exceptions

import re

def gen_insert(tablename, column_values):
    tablename = re.sub(' ', '', tablename)

    if len(tablename) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    if len(column_values) == 0:
        raise exceptions.DictionaryEmptyException("No columns set.")

    text = f'INSERT INTO {tablename} ('

    text += ', '.join([f'{column}' for column in column_values.keys()])

    text += ') VALUES ('

    text += ', '.join([f'{column_values[column]}' for column in column_values.keys()])

    text += ');'

    return text

def gen_delete(tablename, conditions={}, conditionCombining="AND"):
    tablename = re.sub(' ', '', tablename)

    if len(tablename) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    text = f'DELETE FROM {tablename}'

    if len(conditions) > 0:
        text += ' WHERE '

        conditionsText = []

        for column in conditions.keys():
            condition_text = f'{column}='

            prefix = ''
            if type(conditions[column]) == str:
                prefix = '\''

            condition_text += f'{prefix}{conditions[column]}{prefix}'

            conditionsText.append(condition_text)

        text += f' {conditionCombining} '.join(conditionsText)

    text += ';'

    return text

def gen_create_db(dbName):
    dbName = re.sub(' ', '', dbName)

    if len(dbName) == 0:
        raise exceptions.InvalidDatabaseNameException("Databasename invalid.")

    text = f'CREATE DATABASE {dbName};'

    return text

def gen_create_table(tableName, columns):
    tableName = re.sub(' ', '', tableName)

    if len(columns) == 0:
        raise exceptions.DictionaryEmptyException("No columns set.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

    text = f'CREATE TABLE {tableName} ('

    columnTexts = []

    for column in columns.keys():
        columnText = f'{column} {columns[column]}'

        columnTexts.append(columnText)

    text += ', '.join(columnTexts)

    text += ');'

    return text
