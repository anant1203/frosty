from snowflake.snowpark.functions import col
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvinformationschema import InformationSchemaLoadHistory


class Database:
    def __get__(self, instance, owner):
        return instance._database

    def __set__(self, instance, value):
        from src.validation import ValidateObject as vo
        from src.validation import ValidateValue as vv

        vv.required_attribute_check(value, instance.parent.__class__.__name__, self.__class__.__name__)
        if vo.database_exist(instance.session, database_name=value):
            instance._database = value

    def __delete__(self, instance):
        del instance._database


class Schema:
    def __get__(self, instance, owner):
        return instance._schema

    def __set__(self, instance, value):
        from src.validation import ValidateObject as vo
        from src.validation import ValidateValue as vv

        vv.required_attribute_check(value, instance.parent.__class__.__name__, self.__class__.__name__)
        if vo.schema_exist(instance.session, instance._database, schema_name=value):
            instance._schema = value

    def __delete__(self, instance):
        del instance._schema


class LoadHistoryAttr:
    database = Database()
    schema = Schema()


class LoadHistory:
    def __init__(self, session):
        self.col = InformationSchemaLoadHistory().columns
        self.view = self.col._view
        self.session = session

    def use_database(self, db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def set_database(self, value):
        self.use_database(value)

    def get_load_status_of_table(self, database_name, schema_name, table_name):
        self.set_database(database_name)
        df = self.session.table(self.view).filter(
            (col(self.col._schema_name) == schema_name.upper()) & (col(self.col._table_name) == table_name.upper())
        ).select(col(self.col._status))
        res = df.collect()
        return res[0][0]

    def get_load_history_of_table(self, database_name, schema_name, table_name):
        self.set_database(database_name)
        df = self.session.table(self.view).filter(
            (col(self.col._schema_name) == schema_name.upper()) & (col(self.col._table_name) == table_name.upper())
        ).select(
            col(self.col._schema_name),
            col(self.col._file_name),
            col(self.col._table_name),
            col(self.col._last_load_time),
            col(self.col._status),
            col(self.col._row_count),
            col(self.col._row_parsed),
            col(self.col._first_error_message),
            col(self.col._first_error_line_number),
            col(self.col._first_error_character_position),
            col(self.col._first_error_col_name),
            col(self.col._error_count),
            col(self.col._error_limit)
        )
        res = df.collect()
        return res

    def get_load_errors_of_table(self, database_name, schema_name, table_name):
        self.set_database(database_name)
        df = self.session.table(self.view).filter(
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._table_name) == table_name.upper()) &
            (col(self.col._error_count) > 0)
        ).select(
            col(self.col._file_name),
            col(self.col._last_load_time),
            col(self.col._status),
            col(self.col._first_error_message),
            col(self.col._first_error_line_number),
            col(self.col._first_error_character_position),
            col(self.col._first_error_col_name),
            col(self.col._error_count),
            col(self.col._error_limit)
        )
        res = df.collect()
        return res

    def get_most_recent_load_of_table(self, database_name, schema_name, table_name):
        self.set_database(database_name)
        df = self.session.table(self.view).filter(
            (col(self.col._schema_name) == schema_name.upper()) & (col(self.col._table_name) == table_name.upper())
        ).sort(col(self.col._last_load_time).desc()).select(
            col(self.col._file_name),
            col(self.col._last_load_time),
            col(self.col._status),
            col(self.col._row_count),
            col(self.col._row_parsed),
            col(self.col._first_error_message),
            col(self.col._error_count)
        ).limit(1)
        res = df.collect()
        return res

    def get_row_counts_of_table(self, database_name, schema_name, table_name):
        self.set_database(database_name)
        df = self.session.table(self.view).filter(
            (col(self.col._schema_name) == schema_name.upper()) & (col(self.col._table_name) == table_name.upper())
        ).select(
            col(self.col._file_name),
            col(self.col._last_load_time),
            col(self.col._row_count),
            col(self.col._row_parsed)
        )
        res = df.collect()
        return res

    def get_failed_loads_of_table(self, database_name, schema_name, table_name):
        self.set_database(database_name)
        df = self.session.table(self.view).filter(
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._table_name) == table_name.upper()) &
            (col(self.col._status) == "LOAD_FAILED")
        ).select(
            col(self.col._file_name),
            col(self.col._last_load_time),
            col(self.col._status),
            col(self.col._first_error_message),
            col(self.col._first_error_line_number),
            col(self.col._first_error_character_position),
            col(self.col._first_error_col_name),
            col(self.col._error_count),
            col(self.col._error_limit),
            col(self.col._row_count),
            col(self.col._row_parsed)
        )
        res = df.collect()
        return res
