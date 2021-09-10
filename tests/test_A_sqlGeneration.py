from sqlIntuitive import sqlGeneration, exceptions

import pytest

import random, string

def test_A_gen_insert():
    assert sqlGeneration.gen_insert("TestA", {"colA":"val1", "colB": 123, "colC": True}) == ("INSERT INTO TestA (colA, colB, colC) VALUES (?, ?, ?);", ['val1', 123, True])

def test_B_gen_insert():
    with pytest.raises(exceptions.DictionaryEmptyException):
        sqlGeneration.gen_insert("TestB", {})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_insert(" Test B", {"colA":"val1", "colB": 123, "colC": True})

def test_C_gen_insert():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_insert("", {"colA": "val1"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_insert(" ", {"colA": "val1"})

def test_D_gen_delete():
    assert sqlGeneration.gen_delete("TestD", {"colXY": "ABC", "id": 12345}) == ("DELETE FROM TestD WHERE colXY=? AND id=?;", ['ABC', 12345])
    assert sqlGeneration.gen_delete("TestD", {"colXY": "ABC", "id": 12345}, 'OR') == ("DELETE FROM TestD WHERE colXY=? OR id=?;", ['ABC', 12345])
    assert sqlGeneration.gen_delete("TestD") == ("DELETE FROM TestD;", [])

def test_E_gen_delete():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("")

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("", {"col": "val"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("", {"col": "val"}, "OR")

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete(" ")

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete(" ", {"col": "val"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete(" ", {"col": "val"}, "OR")

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("TestD ")

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("T es tD", {"colXY": "ABC", "id": 12345})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("T es tD", {"colXY": "ABC", "id": 12345}, 'OR')

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("T es tD")

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("T es tD ")

def test_F_gen_create_db():
    assert sqlGeneration.gen_create_db("TestF")

def test_G_gen_create_db():
    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db("")

    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db(" ")

    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db("   ")

    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db(" Tes tF ")

    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db(" TestF")

    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db("TestF ")

    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_create_db(" Tes   tF ")

def test_H_gen_create_table():
    assert sqlGeneration.gen_create_table("TestH", {"col1": "int"}, safeMode=False) == "CREATE TABLE TestH (col1 int);"
    assert sqlGeneration.gen_create_table("TestH", {"col1": "int"}, safeMode=True) == "CREATE TABLE IF NOT EXISTS TestH (col1 int);"
    assert sqlGeneration.gen_create_table("TestH", {"col1": "int"}) == "CREATE TABLE IF NOT EXISTS TestH (col1 int);"
    assert sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, safeMode=False) == "CREATE TABLE TestH (col1 int, xyz char);"
    assert sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, safeMode=True) == "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char);"
    assert sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}) == "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char);"

def test_I_gen_create_table():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_create_table("", {"id": "int"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_create_table("  ", {"id": "int"})

    with pytest.raises(exceptions.DictionaryEmptyException):
        sqlGeneration.gen_create_table("TestI", {})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_create_table("Tes t H", {"col1": "int"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_create_table(" T  es tH", {"col1": "int"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_create_table("Te stH", {"col1": "int", "xyz": "char"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_create_table("Te stH  ", {"col1": "int", "xyz": "char"})

def test_J_INVALID_CHARS():
    assert sqlGeneration.INVALID_CHARS == ['!', '"', '#', r'\$', '%', '&', "'", r'\(', r'\)', r'\*', r'\+', ',', '-', '/', ':', ';', '<', '=', '>', r'\?', '@', r'\[', r'\\', r'\]', r'\^', '_', '`', r'\{', r'\|', r'\}', '~', ' ', '\n', '\t']

def test_K_check_validName():
    chars = string.ascii_letters + string.digits

    for i in range(10):
        for char in sqlGeneration.INVALID_CHARS:
            text = [random.choice(chars) for _ in range(random.randint(10,100))]

            text[random.randint(0, len(text)-1)] = char

            text = ''.join(text)

            assert sqlGeneration.check_validName(text) == False

def test_L_check_validName():
    chars = string.ascii_letters + string.digits

    for _ in range(50):
        text = ''.join([random.choice(chars) for _ in range(70)])

        assert sqlGeneration.check_validName(text) == True

def test_M_gen_update():
    assert sqlGeneration.gen_update("TableA", {"col1": "val1"}) == ("UPDATE TableA SET col1=?;", ['val1'])
    assert sqlGeneration.gen_update("TableA", {"col1": True}) == ("UPDATE TableA SET col1=?;", [True])
    assert sqlGeneration.gen_update("TableA", {"col1": 42}) == ("UPDATE TableA SET col1=?;", [42])

    assert sqlGeneration.gen_update("TableA", {"col1": "val1"}, {'col5': 'hello'}) == ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', 'hello'])
    assert sqlGeneration.gen_update("TableA", {"col1": "val1"}, {'col5': True}) == ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', True])
    assert sqlGeneration.gen_update("TableA", {"col1": "val1"}, {'col5': 42}) == ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', 42])

    assert sqlGeneration.gen_update("TableA", {"col1": True}, {'col5': 'hello'}) == ("UPDATE TableA SET col1=? WHERE col5=?;", [True, 'hello'])
    assert sqlGeneration.gen_update("TableA", {"col1": True}, {'col5': True}) == ("UPDATE TableA SET col1=? WHERE col5=?;", [True, True])
    assert sqlGeneration.gen_update("TableA", {"col1": True}, {'col5': 42}) == ("UPDATE TableA SET col1=? WHERE col5=?;", [True, 42])

    assert sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 'hello'}) == ("UPDATE TableA SET col1=? WHERE col5=?;", [42, 'hello'])
    assert sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': True}) == ("UPDATE TableA SET col1=? WHERE col5=?;", [42, True])
    assert sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 42}) == ("UPDATE TableA SET col1=? WHERE col5=?;", [42, 42])

    assert sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 42, "colB": "welt"}, "OR") == ("UPDATE TableA SET col1=? WHERE col5=? OR colB=?;", [42, 42, 'welt'])
    assert sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 42, "colB": "welt"}) == ("UPDATE TableA SET col1=? WHERE col5=? AND colB=?;", [42, 42, 'welt'])

def test_N_gen_update():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_update("T abl e", {"col1": "val1"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_update("", {"col1": "val1"})

    with pytest.raises(exceptions.DictionaryEmptyException):
        sqlGeneration.gen_update("TableXY", {})

def test_O_gen_drop_db():
    assert sqlGeneration.gen_drop_db("DbA") == 'DROP DATABASE DbA;'

def test_P_gen_drop_db():
    with pytest.raises(exceptions.InvalidDatabaseNameException):
        sqlGeneration.gen_drop_db("")

def test_Q_gen_drop_table():
    assert sqlGeneration.gen_drop_table("TableA") == 'DROP TABLE TableA;'

def test_R_gen_drop_table():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_drop_table("")
