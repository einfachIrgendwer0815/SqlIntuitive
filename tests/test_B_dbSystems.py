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

    assert mydb.dbCon == None

    mydb.close_connection()

    assert mydb.connect_to_db() == True

    cursor = mydb.get_cursor()

    assert cursor != None

    mydb.close_connection()
