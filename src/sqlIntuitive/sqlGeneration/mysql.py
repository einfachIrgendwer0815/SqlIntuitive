from sqlIntuitive import exceptions

def gen_create_stored_procedure(procedureName: str, sql_statement: str, delimiter: str, parameters: dict = {}) -> str:
    if not isinstance(procedureName, str):
        raise exceptions.InvalidType(f"'{procedureName}' is not an instance of 'str'")

    if not isinstance(sql_statement, str):
        raise exceptions.InvalidType(f"'{sql_statement}' is not an instance of 'str'")

    if not isinstance(delimiter, str):
        raise exceptions.InvalidType(f"'{delimiter}' is not an instance of 'str'")

    if not isinstance(parameters, dict):
        raise exceptions.InvalidType(f"'{parameters}' is not an instance of 'dict'")
    else:
        for parameter in parameters:
            if not isinstance(parameter, str) or not isinstance(parameters[parameter], str):
                raise exceptions.InvalidType(f"Dictionary of parameters key and value must be strings")

    text = f"DELIMITER {delimiter}\nCREATE PROCEDURE {procedureName} ("

    if len(parameters) > 0:
        text += ', '.join([f'IN {key} {parameters[key]}' for key in parameters])

    text += f")\nBEGIN\n{sql_statement}\nEND{delimiter}\nDELIMITER ;"

    return text

def gen_exec_procedure(procedureName: str, parameters: list = [], placeholder: str = '?') -> tuple:
    if not isinstance(procedureName, str):
        raise exceptions.InvalidType(f"'{procedureName}' is not an instance of 'str'")

    if not isinstance(parameters, list):
        raise exceptions.InvalidType(f"'{parameters}' is not an instance of 'list'")

    text = f"CALL {procedureName} ("

    values_ordered = []
    if len(parameters) > 0:
        paramList = ['?' for _ in range(len(parameters))]
        for parameter in parameters:
            values_ordered.append(parameter)

        text += ', '.join(paramList)

    text += ");"

    return text, values_ordered
