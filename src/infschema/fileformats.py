import sys 
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaFileFormat
class FileFormats:
    def __init__(self,session):
        self.col = InformationSchemaFileFormat().columns
        self.session = session
    
    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_file_format(self,db_name,schema_name,file_format_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._file_format_catalog) == db_name.upper()) & (col(self.col._file_format_schema) == schema_name.upper()) & (col(self.col._file_format_name) == file_format_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return False
        elif len(res) > 0:
            return True
        
    def is_new_file_format(self,db_name,schema_name,file_format_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._file_format_catalog) == db_name.upper()) & (col(self.col._file_format_schema) == schema_name.upper()) & (col(self.col._file_format_name) == file_format_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return True
        elif len(res) > 0:
            return False

    def get_all_file_formats_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._file_format_catalog) == db_name.upper()) & (col(self.col._file_format_schema) == schema_name.upper())).select(col(self.col._file_format_name),col(self.col._file_format_type)).collect()
        return df

    def get_file_format_details(self,db_name,schema_name,file_format_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._file_format_catalog) == db_name.upper()) & (col(self.col._file_format_schema) == schema_name.upper()) & (col(self.col._file_format_name) == file_format_name.upper())).select(
            col(self.col._file_format_name),
            col(self.col._file_format_owner),
            col(self.col._file_format_type),
            col(self.col._record_delimiter),
            col(self.col._field_delimiter),
            col(self.col._skip_header),
            col(self.col._date_format),
            col(self.col._time_format),
            col(self.col._timestamp_format),
            col(self.col._binary_format),
            col(self.col._escape),
            col(self.col._escape_unenclosed_field),
            col(self.col._trim_space),
            col(self.col._field_optionally_enclosed_by),
            col(self.col._null_if),
            col(self.col._compression),
            col(self.col._error_on_column_count_mismatch),
            col(self.col._created),
            col(self.col._last_altered),
            col(self.col._comment)
        ).collect()
        return df

    def get_file_formats_by_type(self,db_name,schema_name,format_type):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._file_format_catalog) == db_name.upper()) & (col(self.col._file_format_schema) == schema_name.upper()) & (col(self.col._file_format_type) == format_type.upper())).select(col(self.col._file_format_name)).collect()
        return df

    def get_file_formats_by_owner(self,db_name,schema_name,owner):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._file_format_catalog) == db_name.upper()) & (col(self.col._file_format_schema) == schema_name.upper()) & (col(self.col._file_format_owner) == owner.upper())).select(col(self.col._file_format_name),col(self.col._file_format_type)).collect()
        return df