from .informationschema import InformationSchema

class ServicesColumnList:
    _view=InformationSchema._services_view
    _service_catalog="SERVICE_CATALOG"
    _service_schema="SERVICE_SCHEMA"
    _service_name="SERVICE_NAME"
    _service_owner="SERVICE_OWNER"
    _dns_name="DNS_NAME"
    _min_instances="MIN_INSTANCES"
    _max_instances="MAX_INSTANCES"
    _compute_pool="COMPUTE_POOL"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaServices:
    def __init__(self):
        self.columns=ServicesColumnList()
