class SqlIntuitiveException(Exception):
    def __str__(self):
        return "An overall exception was raised inside the modul 'sqlIntuitive'."
