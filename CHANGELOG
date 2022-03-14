# Changelog

A full list of all changes ordered by the version they were made in.

---

## 0.9.0 - Join

- added sql generators for INNER, LEFT, RIGHT and FULL JOIN
- added 'select ... join' command


## 0.8.0 - Alter table commands

- added enums of available sql generation functions per dbSystem
- added 'alter table' commands
- added 'alter table rename' command for sqlite
- added \_\_main\_\_.py
- added long_description_content_type field (\_\_init\_\_.py)

## 0.7.1 - CursorNotNone

- added raising CursorNotNone exception if cursor is none when trying to execute database operations


## 0.7.0 - Support tracker, select command enhancement, ...

- included version, author and license information to the main \_\_init\_\_.py
- added support tracker to prevent db systems to execute unsupported operations from base db system
- enhanced select_from generator with select_count, select_avg and select_sum
- added 'DISTINCT' option to select operations
- remade and improved exceptions

##### Breaking changes
- made a variety of parameters keyword-only wich concerns the modules sqlGeneration and dbSystems
- moved sqlGeneration.py to sqlGeneration/standard: only db systems and sqlGeneration are concerned


## 0.6.0 - Sqlite support

- added further metadata to setup.py
- created MANIFEST.in
- sqlite is now supported:
	- added base db system all other db systems inherit from


## 0.5.0 - Custom data types

- introduced custom data types
- annotated functions to give type hints


## 0.4.2

- added naming constraits of a foreign key


## 0.4.1

- replaced pytest.raises with assertRaises from unittest
- fixed primary key bug that generated invalid SQL


## 0.4.0

- converted test-cases into 'unittest.TestCase's
- added primary and foreign key constraits
- added unique contrait
- custom exceptions got a hierarchy


## 0.3.2

- added importing sub-modules recursivly in all \_\_init\_\_.py files


## 0.3.0

- added MySql db system with connect_to_dn(), close_connection(), get_cursor()
- MySQL db system got functions to process db actions
- renamed test files to order their execution
- create_table() got the option to use "IF NOT EXISTS"
- no longer directly inserting values into SQL statements -> added parameter for defining a placeholder (default: '?')
- introduced SQL generator select
- new requirement: mysql-connector-python


## 0.2.2

- introduced the following SQL generators:
	- drop_table
	- drop_db


## 0.2.1

- minimum python version set to 3.8 or newer


## 0.2.0

- added setup.py
- introduced the following SQL generators:
	- insert_into
	- delete_from
	- create_table
	- update
- added sqlGeneration.check_validName() wich checks whether a string is a valid name for a database table
