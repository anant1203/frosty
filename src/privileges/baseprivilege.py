import sys
import os 

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))


from src.vars import Privilege as priv
from src.exception.privilegeexception import InvalidObject
class ObjectType:
    def __get__(self,instance,owner):
        return instance._object_type
    
    def __set__(self,instance,value):
        instance.parent.logger.info(f"setting {self.__class__.__name__} : {value}")
        if value not in priv._allowed_object_type:
            raise InvalidObject(value)
        instance._object_type = value

    def __delete__(self,instance):
        del instance._object_type

class ObjectIdentifier:
    def __get__(self,instance,owner):
        return instance._object_identifier
    
    def __set__(self,instance,value):
        instance.parent.logger.info(f"setting {self.__class__.__name__} : {value}")
        instance._object_identifier = value

    def __delete__(self,instance):
        del instance._object_identifier

class BasePrivilegeAttrs:
    def __init__(self,parent):
        self.parent = parent
    object_type=ObjectType()
    object_identifier=ObjectIdentifier()

class BasePrivilege:
    def __init__(self,session,logger):
        self.session=session
        self.logger=logger
        self.attr=BasePrivilegeAttrs(self)

    def set_object_type(self,val):
        self.attr.object_type=val
    
    def set_object_identifier(self,val):
        self.attr.object_identifier=val

    @classmethod
    def grant_priv_on_obj_to_rl(cls,cls_inst,object_type,object_identifier,privilege_type,role) -> str:
        cls_inst.logger.debug(f"inside to grant {privilege_type} privilege to role {role}")
        qry = f"GRANT {privilege_type} ON {object_type} {object_identifier} TO ROLE {role}"
        #cls_inst.session.sql(qry).collect()
        cls_inst.logger.debug("privilege granted")
        return qry

    @classmethod
    def grant_rl_to_rl(cls,cls_inst,role1,role2):
        qry = f"GRANT ROLE {role1} to ROLE {role2}"
        return qry
        
    
    @classmethod
    def grant_rl_to_usr(cls,cls_inst,role,user):
        qry = f"GRANT ROLE {role} to USER {user}"
        return qry  
        

    def get_allowed_privileges(self) -> list:
        self.logger.info(f"fetching allowed privileges for {self.attr.object_type}")
        allowed_privileges=priv._allowed_privileges[self.attr.object_type]
        self.logger.info(f"allowed privileges for {self.attr.object_type} : {allowed_privileges}")
        return allowed_privileges
    

        