from .informationschema import InformationSchema

class PipeUsageHistoryColumnList:
    _fn=InformationSchema._pipe_usage_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _pipe_id="PIPE_ID"
    _pipe_name="PIPE_NAME"
    _credits_used="CREDITS_USED"
    _bytes_inserted="BYTES_INSERTED"
    _files_inserted="FILES_INSERTED"

class InformationSchemaPipeUsageHistory:
    def __init__(self):
        self.columns=PipeUsageHistoryColumnList()
