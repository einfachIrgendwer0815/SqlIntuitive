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
