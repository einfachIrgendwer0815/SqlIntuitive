from sqlIntuitive import sqlGeneration, exceptions

import pytest

def test_A_gen_insert():
    assert sqlGeneration.gen_insert("TestA", {"colA":"val1", "colB": 123, "colC": True}) == "INSERT INTO TestA (colA, colB, colC) VALUES (val1, 123, True);"
    assert sqlGeneration.gen_insert(" Test B", {"colA":"val1", "colB": 123, "colC": True}) == "INSERT INTO TestB (colA, colB, colC) VALUES (val1, 123, True);"

def test_B_gen_insert():
    with pytest.raises(exceptions.DictionaryEmptyException):
        sqlGeneration.gen_insert("TestB", {})

def test_C_gen_insert():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_insert("", {"colA": "val1"})

    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_insert(" ", {"colA": "val1"})

def test_D_gen_delete():
    assert sqlGeneration.gen_delete("TestD", {"colXY": "ABC", "id": 12345}) == "DELETE FROM TestD WHERE colXY='ABC' AND id=12345;"
    assert sqlGeneration.gen_delete("TestD", {"colXY": "ABC", "id": 12345}, 'OR') == "DELETE FROM TestD WHERE colXY='ABC' OR id=12345;"
    assert sqlGeneration.gen_delete("TestD ") == "DELETE FROM TestD;"
    assert sqlGeneration.gen_delete("TestD") == "DELETE FROM TestD;"
    assert sqlGeneration.gen_delete("T es tD", {"colXY": "ABC", "id": 12345}) == "DELETE FROM TestD WHERE colXY='ABC' AND id=12345;"
    assert sqlGeneration.gen_delete("T es tD", {"colXY": "ABC", "id": 12345}, 'OR') == "DELETE FROM TestD WHERE colXY='ABC' OR id=12345;"
    assert sqlGeneration.gen_delete("T es tD") == "DELETE FROM TestD;"
    assert sqlGeneration.gen_delete("T es tD ") == "DELETE FROM TestD;"

def test_E_gen_delete():
    with pytest.raises(exceptions.InvalidTableNameException):
        sqlGeneration.gen_delete("")
        sqlGeneration.gen_delete("", {"col": "val"})
        sqlGeneration.gen_delete("", {"col": "val"}, "OR")
        sqlGeneration.gen_delete(" ")
        sqlGeneration.gen_delete(" ", {"col": "val"})
        sqlGeneration.gen_delete(" ", {"col": "val"}, "OR")
