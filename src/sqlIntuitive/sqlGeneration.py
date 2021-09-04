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
