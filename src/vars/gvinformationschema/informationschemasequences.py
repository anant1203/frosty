from .informationschema import InformationSchema

class SequencesColumnList:
    _view=InformationSchema._sequences_view
    _sequence_catalog="SEQUENCE_CATALOG"
    _sequence_schema="SEQUENCE_SCHEMA"
    _sequence_name="SEQUENCE_NAME"
    _sequence_owner="SEQUENCE_OWNER"
    _data_type="DATA_TYPE"
    _numeric_precision="NUMERIC_PRECISION"
    _numeric_precision_radix="NUMERIC_PRECISION_RADIX"
    _numeric_scale="NUMERIC_SCALE"
    _start_value="START_VALUE"
    _minimum_value="MINIMUM_VALUE"
    _maximum_value="MAXIMUM_VALUE"
    _increment="INCREMENT"
    _cycle_option="CYCLE_OPTION"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaSequences:
    def __init__(self):
        self.columns=SequencesColumnList()
