from sqlIntuitive import exceptions
from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes
from enum import Enum, auto

import string
import re

INVALID_CHARS = ['!', '"', '#', r'\$', '%', '&', "'", r'\(', r'\)', r'\*', r'\+', ',', '-', '/', ':', ';', '<', '=', '>', r'\?', '@', r'\[', r'\\', r'\]', r'\^', '_', '`', r'\{', r'\|', r'\}', '~', ' ', '\n', '\t']

class Count_avg_sum_modes(Enum):
    COUNT = auto()
    AVG = auto()
    SUM = auto()

def check_validName(text: str) -> bool:
    for char in INVALID_CHARS:
        if re.match(f'.*{char}.*', text, re.I):
            return False

    return True

def gen_conditions(conditions: dict = {}, combinations: list = [], *, defaultCombination: CombinationTypes = CombinationTypes.AND, defaultComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = "?") -> tuple:
    if type(conditions) != dict:
        raise exceptions.InvalidType(conditions, dict)

    if type(combinations) != list:
        raise exceptions.InvalidType(combinations, list)

    if type(defaultCombination) != CombinationTypes:
        try:
            defaultCombination = CombinationTypes(defaultCombination)
        except ValueError:
            raise exceptions.NotACombinationType(type(defaultCombination))

    if type(defaultComparison) != ComparisonTypes:
        try:
            defaultComparison = ComparisonTypes(defaultComparison)
        except ValueError:
            raise exceptions.NotAComparisonType(type(defaultComparison))

    combinations = combinations.copy()
    combinations_new = []

    for combination in combinations:
        if type(combination) != CombinationTypes:
            try:
                combination = CombinationTypes(combination)
            except ValueError:
                raise exceptions.NotACombinationType(f'{type(combination)} is not a combination type')
        combinations_new.append(combination)

    combinations = combinations_new
    del combinations_new

    conditionTexts = []
    values_ordered = []

    text = ""

    for column in conditions.keys():
        if type(conditions[column]) == dict:
            if 'value' not in conditions[column].keys():
                raise exceptions.NoValue(column)

            if 'comparison' in conditions[column].keys():
                comparison = conditions[column]['comparison']
                if type(comparison) != ComparisonTypes:
                    try:
                        comparison = ComparisonTypes(comparison)
                    except ValueError:
                        raise exceptions.NotAComparisonType(f'{type(conditions[column]["comparison"])} is not a comparison type.')

                conditionTexts.append(f'{column}{comparison.value}{placeholder}')
                values_ordered.append(conditions[column]["value"])

            else:
                conditionTexts.append(f'{column}{defaultComparison.value}{placeholder}')
                values_ordered.append(conditions[column]["value"])
        else:
            conditionTexts.append(f'{column}{defaultComparison.value}{placeholder}')
            values_ordered.append(conditions[column])

    diff = len(conditionTexts) - 1 - len(combinations)
    if diff > 0:
        combinations += [ defaultCombination for _ in range(diff) ]

    for index in range(len(conditionTexts)):
        if index != 0:
            text += ' '

        text += f'{conditionTexts[index]}'

        if index < len(conditionTexts)-1:
            text += f' {combinations[index].value}'

    return text, values_ordered

def gen_select(tableName: str, columns: list = [], conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = '?') -> tuple:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException()

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

    if len(columns) == 0:
        columns = ('*')

    text = 'SELECT '
    if distinct:
        text += 'DISTINCT '

    text += ', '.join(columns)

    text += f' FROM {tableName}'

    column_values_ordered = []

    if len(conditions) > 0:
        text += ' WHERE '

        conditionText, conditionValues = gen_conditions(conditions, combinations=combinations, defaultCombination=conditionCombining, defaultComparison=conditionComparison, placeholder=placeholder)

        text += conditionText
        column_values_ordered += conditionValues

    text += ';'

    return text, column_values_ordered

def gen_count(tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = '?') -> tuple:
    return gen_count_avg_sum(mode=Count_avg_sum_modes.COUNT, tableName=tableName, column=column, conditions=conditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=placeholder)

def gen_avg(tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = '?') -> tuple:
    return gen_count_avg_sum(mode=Count_avg_sum_modes.AVG, tableName=tableName, column=column, conditions=conditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=placeholder)

def gen_sum(tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = '?') -> tuple:
    return gen_count_avg_sum(mode=Count_avg_sum_modes.SUM, tableName=tableName, column=column, conditions=conditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=placeholder)

def gen_count_avg_sum(mode: Count_avg_sum_modes, tableName: str, column: str, conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = '?') -> tuple:
    if not isinstance(mode, Count_avg_sum_modes):
        raise exceptions.InvalidType(mode, Count_avg_sum_modes)

    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException()
    elif len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

    if not isinstance(column, str):
        raise exceptions.InvalidType(column, str)

    if len(column) == 0:
        column = "*"

    text = "SELECT "

    if mode == Count_avg_sum_modes.COUNT:
        text += "COUNT"
    elif mode == Count_avg_sum_modes.AVG:
        text += "AVG"
    elif mode == Count_avg_sum_modes.SUM:
        text += "SUM"

    text += '('
    if distinct:
        text += 'DISTINCT '

    text += f"{column}) FROM {tableName}"

    column_values_ordered = []
    if len(conditions) > 0:
        text += ' WHERE '

        conditionText, conditionValues = gen_conditions(conditions, combinations=combinations, defaultCombination=conditionCombining, defaultComparison=conditionComparison, placeholder=placeholder)

        text += conditionText
        column_values_ordered += conditionValues

    text += ';'

    return text, column_values_ordered

def gen_insert(tablename: str, column_values: dict, *, placeholder: str = "?") -> tuple:
    if check_validName(tablename) == False:
        raise exceptions.InvalidTableNameException()

    if len(tablename) == 0:
        raise exceptions.InvalidTableNameException()

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

def gen_update(tableName: str, newValues: dict, conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = "?") -> tuple:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException()

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

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

        conditionText, conditionValues = gen_conditions(conditions, combinations=combinations, defaultCombination=conditionCombining, defaultComparison=conditionComparison, placeholder=placeholder)

        text += conditionText
        column_values_ordered += conditionValues

    text += ';'

    return text, column_values_ordered

def gen_delete(tableName: str, conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = "?") -> tuple:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException()

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

    column_values_ordered = []
    text = f'DELETE FROM {tableName}'

    if len(conditions) > 0:
        text += ' WHERE '

        conditionText, conditionValues = gen_conditions(conditions, combinations=combinations, defaultCombination=conditionCombining, defaultComparison=conditionComparison, placeholder=placeholder)

        text += conditionText
        column_values_ordered += conditionValues

    text += ';'

    return text, column_values_ordered

def gen_create_db(dbName: str) -> str:
    if check_validName(dbName) == False:
        raise exceptions.InvalidDatabaseNameException()

    if len(dbName) == 0:
        raise exceptions.InvalidDatabaseNameException()

    text = f'CREATE DATABASE {dbName};'

    return text

def gen_drop_db(dbName: str) -> str:
    if check_validName(dbName) == False:
        raise exceptions.InvalidDatabaseNameException()

    if len(dbName) == 0:
        raise exceptions.InvalidDatabaseNameException()

    text = f'DROP DATABASE {dbName};'

    return text

def gen_create_table(tableName: str, columns: dict, *, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> str:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException()

    if len(columns) == 0:
        raise exceptions.DictionaryEmptyException("No columns set.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

    for primary in primaryKeys:
        if primary not in columns.keys():
            raise exceptions.InvalidPrimaryKeyColumn(primary)

    for foreign in foreignKeys.keys():
        if foreign not in columns.keys():
            raise exceptions.InvalidForeignKeyColumn(foreign)

    for unique in uniqueColumns:
        if unique not in columns.keys():
            raise exceptions.InvalidUniqueColumn(unique)

    for named in namedForeignKeys.keys():
        if named not in columns.keys():
            raise exceptions.InvalidForeignKeyColumn(named)

        if type(namedForeignKeys[named]) != dict or 'name' not in namedForeignKeys[named].keys() or 'reference' not in namedForeignKeys[named].keys():
            raise exceptions.InvalidNamedForeignKeyDictionary(named)

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
        raise exceptions.InvalidTableNameException()

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException()

    text = f'DROP TABLE {tableName};'

    return text

def gen_create_stored_procedure(procedureName: str, sql_statement: str, parameters: dict = {}) -> str:
    if not isinstance(procedureName, str):
        raise exceptions.InvalidType(procedureName, str)

    if not isinstance(sql_statement, str):
        raise exceptions.InvalidType(sql_statement, str)

    if not isinstance(parameters, dict):
        raise exceptions.InvalidType(parameters, dict)
    else:
        for parameter in parameters:
            if not isinstance(parameter, str) or not isinstance(parameters[parameter], str):
                raise exceptions.InvalidType("Dictionary key and/or value", str)

    text = f"CREATE PROCEDURE {procedureName}"

    if len(parameters) > 0:
        text += ' ' + ', '.join([f'@{key} {parameters[key]}' for key in parameters])

    text += f"\nAS\n{sql_statement}\nGO;"

    return text

def gen_exec_procedure(procedureName: str, parameters: dict = {}, placeholder: str = '?') -> tuple:
    if not isinstance(procedureName, str):
        raise exceptions.InvalidType(procedureName, str)

    if not isinstance(parameters, dict):
        raise exceptions.InvalidType(parameters, dict)

    text = f"EXEC {procedureName}"

    values_ordered = []
    if len(parameters) > 0:
        text += ' '

        paramList = []
        for key in parameters:
            paramList.append(f'@{key}=?')
            values_ordered.append(parameters[key])

        text += ', '.join(paramList)

    text += ";"

    return text, values_ordered

def gen_drop_procedure(procedureName: str) -> str:
    if not isinstance(procedureName, str):
        raise exceptions.InvalidType(procedureName, str)

    return f"DROP PROCEDURE {procedureName};"
