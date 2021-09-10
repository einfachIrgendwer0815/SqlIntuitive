from sqlIntuitive import dbSystems

import pytest

import json

with open('tests/mysql_testserver_login.json', 'r') as file:
    mysql_login = json.load(file)

def test_A_connect_to_db__close_connection():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )

    assert mydb.connect_to_db() == True
    assert mydb.dbCon != None
    assert mydb.dbCon.is_connected()

    mydb.close_connection()

    assert mydb.dbCon.is_connected() == False

def test_B_close_connection():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )

    assert mydb.dbCon == None

    mydb.close_connection()

    assert mydb.connect_to_db() == True

    mydb.close_connection()

    mydb.close_connection() # No close happens, but no error should appear.

def test_C_get_cursor():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True

    assert mydb.cursor == None

    mydb.create_cursor()

    assert mydb.cursor != None

    mydb.close_connection()

def test_D_create_table():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True
    mydb.create_cursor()
    assert mydb.cursor != None

    mydb.create_table("TestA", {"name":"varchar(50)","id": "int primary key"})

def test_E_drop_table():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True
    mydb.create_cursor()
    assert mydb.cursor != None

    mydb.drop_table("TestA")

def test_F_insert_into():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True
    mydb.create_cursor()
    assert mydb.cursor != None

    mydb.insert_into("TableB", {"col1": 'Test', "col2": 42, "col3": True})
    mydb.insert_into("TableB", {"col1": 'Test', "col2": 84, "col3": True})

def test_G_update():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True
    mydb.create_cursor()
    assert mydb.cursor != None

    mydb.update("TableB", {"col3": False, "col2": 43}, {"col2": 42})

def test_H_select_from():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True
    mydb.create_cursor()
    assert mydb.cursor != None

    mydb.select_from("TableB")

def test_I_delete():
    mydb = dbSystems.MySqlDbSystem(
        host=mysql_login["host"],
        database=mysql_login["database"],
        username=mysql_login["username"],
        password=mysql_login["password"],
    )
    assert mydb.connect_to_db() == True
    mydb.create_cursor()
    assert mydb.cursor != None

    mydb.delete_from("TableB", {"col2": 84})
    mydb.delete_from("TableB")
