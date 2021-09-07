from sqlIntuitive import exceptions

import string
import re

INVALID_CHARS = ['!', '"', '#', r'\$', '%', '&', "'", r'\(', r'\)', r'\*', r'\+', ',', '-', '/', ':', ';', '<', '=', '>', r'\?', '@', r'\[', r'\\', r'\]', r'\^', '_', '`', r'\{', r'\|', r'\}', '~', ' ', '\n', '\t']

def check_validName(text, raises=None):
    for char in INVALID_CHARS:
        if re.match(f'.*{char}.*', text, re.I):
            print(char)
            return False

    return True

def gen_insert(tablename, column_values):
    if check_validName(tablename) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

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
    if check_validName(tablename) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

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
    if check_validName(dbName) == False:
        raise exceptions.InvalidDatabaseNameException("Databasename contains invalid characters.")

    if len(dbName) == 0:
        raise exceptions.InvalidDatabaseNameException("Databasename invalid.")

    text = f'CREATE DATABASE {dbName};'

    return text

def gen_create_table(tableName, columns):
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")


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
