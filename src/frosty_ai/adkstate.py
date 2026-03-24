import logging

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logging.getLogger(__name__).setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

class ADKState:
    def __init__(self):
        self.state_dict={}

    def add_state(self,key,value=None):
        if isinstance(key,str):
            if value==None:
                self.state_dict[key]=""
            else:
                self.state_dict[key]=value
        else:
            return "key must be string"

    def add_user_state(self,key,value=None):
        if isinstance(key,str):
            key = f'user:{key}'
            if value==None:
                self.state_dict[key]=""
            else:
                self.state_dict[key]=value

    def add_app_state(self,key,value=None):
        if isinstance(key,str):
            key = f'app:{key}'
            if value==None:
                self.state_dict[key]=""
            else:
                self.state_dict[key]=value

    def add_temp_state(self,key,value=None):
        logger.debug("INSIDE BASE CLASS TEMP STATE ")
        if isinstance(key,str):
            key = f'temp:{key}'
            if value==None:
                self.state_dict[key]=""
                logger.debug(" TEMP state initialized with key %s and empty string ",key)
            else:
                self.state_dict[key]=value
                logger.debug(" TEMP state initialized with key %s and value %s",key,value)


class SnowflakeState(ADKState):
    def __init__(self,user_name,snowflake_user_name,user_password,account_identifier,
                 authenticator=None,role=None,warehouse=None,database=None):
        super().__init__()
        self.user_name=user_name
        self.snowflake_user_name=snowflake_user_name
        self.user_password=user_password
        self.account_identifier=account_identifier
        self.authenticator=authenticator
        self.role=role
        self.warehouse=warehouse
        self.database=database

    def __init_user_state(self):
        self.add_user_state(key='USER_NAME',value=self.user_name)
        self.add_user_state(key="SNOWFLAKE_USER_NAME", value=self.snowflake_user_name)
        self.add_user_state(key="USER_PASSWORD",value=self.user_password)
        self.add_user_state(key="QUERIES_EXECUTED",value=[])
        self.add_user_state(key="AUTHENTICATOR",value=self.authenticator)
        self.add_user_state(key="ROLE",value=self.role)

    def __init_app_state(self):
        import os as _os
        self.add_app_state(key='ACCOUNT_IDENTIFIER',value=self.account_identifier)
        self.add_app_state(key='LOGGER',value=logger.name)
        self.add_app_state(key='TASKS_PERFORMED',value=[])
        self.add_app_state(key='AUTO_GENERATE_COMMENTS')
        self.add_app_state(key='INFRASTRUCTURE_SNAPSHOT',value=[])
        self.add_app_state(key='RESEARCH_RESULTS',value={})
        self.add_app_state(key='WAREHOUSE',value=self.warehouse)
        self.add_app_state(key='DATABASE',value=self.database)
        self.add_app_state(key='USE_SKILLS',value=_os.environ.get("USE_SKILLS","true").lower()!="false")

    def init_snowflake_state(self):
        logger.debug(" INSIDE TO SET SNOWFLAKE STATE")
        logger.debug(" setting USER state")
        self.__init_user_state()
        logger.debug(" setting APP state")
        self.__init_app_state()
