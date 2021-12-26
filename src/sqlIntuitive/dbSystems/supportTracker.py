from enum import Enum
from sqlIntuitive.exceptions import NotSupported

EXCEPTION_IF_NOT_SUPPORTED = True

def reuseLastReturn(func):
    lastReturn = None

    def replaceFunc(*args, **kwargs):
        nonlocal lastReturn

        newReturn = func(lastReturn, *args, **kwargs)
        lastReturn = newReturn

        return newReturn

    return replaceFunc

@reuseLastReturn
def nextPowerOf2(lastReturn: int):
    if lastReturn == None: return 1

    return 2 * lastReturn

class Features(Enum):
    # SQL language features
    SQL_CREATE_TABLE = nextPowerOf2()
    SQL_DROP_TABLE = nextPowerOf2()
    SQL_INSERT_INTO = nextPowerOf2()
    SQL_UPDATE = nextPowerOf2()
    SQL_DELETE_FROM = nextPowerOf2()
    SQL_SELECT_FROM = nextPowerOf2()

    SQL_PRIMARY_KEYS = nextPowerOf2()
    SQL_FOREIGN_KEYS = nextPowerOf2()
    SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT = nextPowerOf2()
    SQL_UNIQUE = nextPowerOf2()

    # Addon features
    ADDON_CUSTOM_DATA_TYPE = nextPowerOf2()

    # GROUPS
    GROUP_SQL = SQL_CREATE_TABLE | SQL_DROP_TABLE | SQL_INSERT_INTO | SQL_UPDATE | SQL_DELETE_FROM | SQL_SELECT_FROM | SQL_PRIMARY_KEYS | SQL_FOREIGN_KEYS | SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT | SQL_UNIQUE
    GROUP_ADDON = ADDON_CUSTOM_DATA_TYPE

    # all
    ALL = GROUP_SQL | GROUP_ADDON

def or_values(features: list):
    value = 0
    for feature in features:
        value = value | feature.value

    return value

MYSQL_SUPPORTS = or_values([
    Features.SQL_CREATE_TABLE,
    Features.SQL_DROP_TABLE,
    Features.SQL_INSERT_INTO,
    Features.SQL_UPDATE,
    Features.SQL_DELETE_FROM,
    Features.SQL_SELECT_FROM,
    Features.SQL_PRIMARY_KEYS,
    Features.SQL_FOREIGN_KEYS,
    Features.SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT,
    Features.SQL_UNIQUE,
    Features.ADDON_CUSTOM_DATA_TYPE
    ])

SQLITE_SUPPORTS = or_values([
    Features.SQL_CREATE_TABLE,
    Features.SQL_DROP_TABLE,
    Features.SQL_INSERT_INTO,
    Features.SQL_UPDATE,
    Features.SQL_DELETE_FROM,
    Features.SQL_SELECT_FROM,
    Features.SQL_PRIMARY_KEYS,
    Features.SQL_FOREIGN_KEYS,
    Features.SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT,
    Features.SQL_UNIQUE,
    Features.ADDON_CUSTOM_DATA_TYPE
    ])

def isSupported(feature: Features, supported: int):
    if (supported & feature.value) == feature.value:
        return True
    return False

def ifSupported(feature: Features):

    def decorator(func):
        print(func)
        def replaceFunc(self, *args, **kwargs):
            print(self.__class__.__name__)

            supported = False
            if (name := self.__class__.__name__) == 'MySqlDbSystem':
                if isSupported(feature, MYSQL_SUPPORTS):
                    supported = True
            elif name == 'SqliteDbSystem':
                if isSupported(feature, SQLITE_SUPPORTS):
                    supported = True

            if supported:
                return func(self, *args, **kwargs)
            else:
                if EXCEPTION_IF_NOT_SUPPORTED:
                    raise NotSupported(f'{feature.name} is not supported in {self.__class__.__name__}')
                else:
                    return None


        return replaceFunc

    return decorator
