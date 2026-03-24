

import json

from validation import ValidateObject as vo

class Session:
    def __get__(self,instance,owner):
        return instance._session
    
    def __set__(self,instance,value):
        print(instance)
        instance._session = value
    
    def __delete__(self,instance):
        del instance._session

class Database:
    def __get__(self,instance,owner):
        return instance._database
    
    def __set__(self,instance,value):
        if vo.database_exist(value):
            instance._database = value
    
    def __delete__(self,instance):
        del instance._database

class Schema:
    def __get__(self,instance,owner):
        return instance._schema
    
    def __set__(self,instance,value):
        if vo.schema_exist(database_name=instance._database, schema_name=value):
            instance._schema = value
    
    def __delete__(self,instance):
        del instance._schema

class Name:
    def __get__(self,instance,owner):
        return instance._name
    
    def __set__(self,instance,value):
        print(instance)
        instance._name = value
    
    def __delete__(self,instance):
        del instance._name


class PipeStatusAttr:
    session = Session()
    database = Database()
    schema = Schema()
    name = Name()



class PipeStatus:
    def __init__(self):
        self.attr = PipeStatusAttr()

    def set_session(self,value):
        self.attr.session = value

    def set_database(self,value):
        self.attr.database = value

    def set_schema(self,value):
        self.attr.schema = value

    def set_name(self,value):
        self.attr.name = value

    def convert_to_json(self,status):
        for inner_qry in status:
            for json_string in inner_qry:
                json_data = json.loads(json_string)
        return json_data


    def get_status(self,*largs):
        qry = f" SELECT SYSTEM$PIPE_STATUS( '{self.attr.database}.{self.attr.schema}.{self.attr.name}') "
        status = self.attr.session.sql(qry).collect()
        status = self.convert_to_json(status)
        if len(largs) == 0:
            return status
        elif len(largs) != 0:
            result = {}
            for key in largs:
                result[key] = status[key]
            return result

            
