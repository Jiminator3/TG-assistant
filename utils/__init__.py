from sqlalchemy import Integer, String, TIMESTAMP


def get_db_options(options: list):
    if len(options) > 2:
        return {'options': options[2]}
    else:
        return None


def get_db_types(string_type):
    if string_type == "Integer":
        return Integer
    elif string_type == "String":
        return String
    elif string_type == "TIMESTAMP":
        return TIMESTAMP
