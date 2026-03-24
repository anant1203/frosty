
from snowflake.snowpark.functions import col
import sys
import os 

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaColumn
class Columns:
    def __init__(self,session):
        self.col = InformationSchemaColumn().columns
        self.session = session

    def column_exist_in_table(self,database_name,schema_name,table_name,column_name):
        df=self.session.table(self.col._view).select(col(self.col._column_name))\
            .filter((col(self.col._table_catalog)==database_name.upper()) \
                    & (col(self.col._table_schema)==schema_name.upper())\
                    & (col(self.col._table_name)==table_name.upper())\
                    & (col(self.col._column_name)==column_name.upper()))
        res=df.collect()

        if len(res)==0:
            return False
        elif len(res)>0:
            return True
        
    def get_all_columns_of_a_table(self,database_name,schema_name,table_name):
        """
        Returns:
            All columns of a table in a list.
        """
        lst=[]
        df=self.session.table(self.col._view)\
            .select(col(self.col._column_name))\
            .filter((col(self.col._table_catalog)==database_name.upper())\
                    & (col(self.col._table_schema)==schema_name.upper())\
                    & (col(self.col._table_name)==table_name.upper()))
        res=df.collect()
        for i in res:
            lst.append(i[0])
        return lst

    def _base_filter(self,database_name,schema_name,table_name):
        return (col(self.col._table_catalog)==database_name.upper())\
                & (col(self.col._table_schema)==schema_name.upper())\
                & (col(self.col._table_name)==table_name.upper())

    def _base_filter_col(self,database_name,schema_name,table_name,column_name):
        return self._base_filter(database_name,schema_name,table_name)\
                & (col(self.col._column_name)==column_name.upper())

    def _get_single_value(self,column_attr,database_name,schema_name,table_name,column_name):
        res=self.session.table(self.col._view)\
            .select(col(column_attr))\
            .filter(self._base_filter_col(database_name,schema_name,table_name,column_name))\
            .collect()
        if res:
            return res[0][0]
        return None

    def get_column_data_type(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._data_type,database_name,schema_name,table_name,column_name)

    def get_column_ordinal_position(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._ordinal_position,database_name,schema_name,table_name,column_name)

    def get_column_default(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._column_default,database_name,schema_name,table_name,column_name)

    def is_column_nullable(self,database_name,schema_name,table_name,column_name):
        val=self._get_single_value(self.col._is_nullable,database_name,schema_name,table_name,column_name)
        if val is None:
            return None
        return val=='YES'

    def get_column_character_max_length(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._character_maximum_length,database_name,schema_name,table_name,column_name)

    def get_column_character_octet_length(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._character_octet_length,database_name,schema_name,table_name,column_name)

    def get_column_numeric_precision(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._numeric_precision,database_name,schema_name,table_name,column_name)

    def get_column_numeric_precision_radix(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._numeric_precision_radix,database_name,schema_name,table_name,column_name)

    def get_column_numeric_scale(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._numeric_scale,database_name,schema_name,table_name,column_name)

    def is_column_identity(self,database_name,schema_name,table_name,column_name):
        val=self._get_single_value(self.col._is_identity,database_name,schema_name,table_name,column_name)
        if val is None:
            return None
        return val=='YES'

    def get_column_identity_generation(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._identity_generation,database_name,schema_name,table_name,column_name)

    def get_column_identity_start(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._identity_start,database_name,schema_name,table_name,column_name)

    def get_column_identity_increment(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._identity_increment,database_name,schema_name,table_name,column_name)

    def get_column_identity_ordered(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._identity_ordered,database_name,schema_name,table_name,column_name)

    def get_column_comment(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._comment,database_name,schema_name,table_name,column_name)

    def get_column_data_type_alias(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._data_type_alias,database_name,schema_name,table_name,column_name)

    def get_column_schema_evolution_record(self,database_name,schema_name,table_name,column_name):
        return self._get_single_value(self.col._schema_evolution_record,database_name,schema_name,table_name,column_name)

    def get_columns_with_data_types(self,database_name,schema_name,table_name):
        res=self.session.table(self.col._view)\
            .select(col(self.col._column_name),col(self.col._data_type))\
            .filter(self._base_filter(database_name,schema_name,table_name))\
            .collect()
        return [{"column_name":r[0],"data_type":r[1]} for r in res]

    def get_nullable_columns(self,database_name,schema_name,table_name):
        res=self.session.table(self.col._view)\
            .select(col(self.col._column_name))\
            .filter(self._base_filter(database_name,schema_name,table_name)\
                    & (col(self.col._is_nullable)=='YES'))\
            .collect()
        return [r[0] for r in res]

    def get_identity_columns(self,database_name,schema_name,table_name):
        res=self.session.table(self.col._view)\
            .select(col(self.col._column_name))\
            .filter(self._base_filter(database_name,schema_name,table_name)\
                    & (col(self.col._is_identity)=='YES'))\
            .collect()
        return [r[0] for r in res]

    def get_column_count(self,database_name,schema_name,table_name):
        res=self.session.table(self.col._view)\
            .filter(self._base_filter(database_name,schema_name,table_name))\
            .count()
        return res

    def get_column_detail(self,database_name,schema_name,table_name,column_name):
        res=self.session.table(self.col._view)\
            .filter(self._base_filter_col(database_name,schema_name,table_name,column_name))\
            .collect()
        if not res:
            return None
        r=res[0]
        c=self.col
        return {
            "data_type":r[c._data_type],
            "is_nullable":r[c._is_nullable],
            "ordinal_position":r[c._ordinal_position],
            "column_default":r[c._column_default],
            "character_maximum_length":r[c._character_maximum_length],
            "numeric_precision":r[c._numeric_precision],
            "numeric_scale":r[c._numeric_scale],
            "is_identity":r[c._is_identity],
            "comment":r[c._comment],
            "data_type_alias":r[c._data_type_alias],
            "schema_evolution_record":r[c._schema_evolution_record],
        }

    def get_all_column_details(self,database_name,schema_name,table_name):
        res=self.session.table(self.col._view)\
            .filter(self._base_filter(database_name,schema_name,table_name))\
            .collect()
        c=self.col
        return [{
            "column_name":r[c._column_name],
            "data_type":r[c._data_type],
            "is_nullable":r[c._is_nullable],
            "ordinal_position":r[c._ordinal_position],
            "column_default":r[c._column_default],
            "character_maximum_length":r[c._character_maximum_length],
            "numeric_precision":r[c._numeric_precision],
            "numeric_scale":r[c._numeric_scale],
            "is_identity":r[c._is_identity],
            "comment":r[c._comment],
            "data_type_alias":r[c._data_type_alias],
            "schema_evolution_record":r[c._schema_evolution_record],
        } for r in res]
