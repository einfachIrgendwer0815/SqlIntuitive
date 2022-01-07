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
    SQL_COUNT_AVG_SUM = nextPowerOf2()

    SQL_PRIMARY_KEYS = nextPowerOf2()
    SQL_FOREIGN_KEYS = nextPowerOf2()
    SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT = nextPowerOf2()
    SQL_UNIQUE = nextPowerOf2()

    SQL_STORED_PROCEDURES = nextPowerOf2()

    # Addon features
    ADDON_CUSTOM_DATA_TYPE = nextPowerOf2()

    # GROUPS
    GROUP_SQL = SQL_CREATE_TABLE | SQL_DROP_TABLE | SQL_INSERT_INTO | SQL_UPDATE | SQL_DELETE_FROM | SQL_SELECT_FROM | SQL_PRIMARY_KEYS | SQL_FOREIGN_KEYS | SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT | SQL_UNIQUE | SQL_COUNT_AVG_SUM | SQL_STORED_PROCEDURES
    GROUP_ADDON = ADDON_CUSTOM_DATA_TYPE

    # all
    ALL = GROUP_SQL | GROUP_ADDON

def or_values(features: list):
    value = 0
    for feature in features:
        value = value | feature.value

    return value

def isSupported(feature: Features, supported: int) -> bool:
    if (supported & feature.value) == feature.value:
        return True
    return False

def ifSupported(feature: Features):

    def decorator(func):
        def replaceFunc(self, *args, **kwargs):
            supported = False
            name = self.__class__.__name__
            supports = self.__class__.SUPPORTS

            if isSupported(feature, supports):
                supported = True

            if supported:
                return func(self, *args, **kwargs)
            else:
                if EXCEPTION_IF_NOT_SUPPORTED:
                    raise NotSupported(feature.name, name)
                else:
                    return None


        return replaceFunc

    return decorator
