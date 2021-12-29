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
        raise exceptions.InvalidType(f'{type(conditions)} is not a dict')

    if type(combinations) != list:
        raise exceptions.InvalidType(f'{type(combinations)} is not a list')

    if type(defaultCombination) != CombinationTypes:
        try:
            defaultCombination = CombinationTypes(defaultCombination)
        except ValueError:
            raise exceptions.NotACombinationType(f'{type(defaultCombination)} is not a combination type')

    if type(defaultComparison) != ComparisonTypes:
        try:
            defaultComparison = ComparisonTypes(defaultComparison)
        except ValueError:
            raise exceptions.NotAComparisonType(f'{type(defaultComparison)} is not a comparison type')

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
                raise exceptions.NoValue(f'no value for column {column}')

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
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

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
        raise exceptions.InvalidType(f"{mode} is not an instance of class 'Count_avg_sum_modes'")

    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Table name contains invalid characters.")
    elif len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Table name empty.")

    if not isinstance(column, str):
        raise exceptions.InvalidType(f"{column} is not an instance of class 'str'")

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

def gen_update(tableName: str, newValues: dict, conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = "?") -> tuple:
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

        conditionText, conditionValues = gen_conditions(conditions, combinations=combinations, defaultCombination=conditionCombining, defaultComparison=conditionComparison, placeholder=placeholder)

        text += conditionText
        column_values_ordered += conditionValues

    text += ';'

    return text, column_values_ordered

def gen_delete(tableName: str, conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO, placeholder: str = "?") -> tuple:
    if check_validName(tableName) == False:
        raise exceptions.InvalidTableNameException("Tablename contains invalid characters.")

    if len(tableName) == 0:
        raise exceptions.InvalidTableNameException("Tablename empty.")

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

def gen_create_table(tableName: str, columns: dict, *, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> str:
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
