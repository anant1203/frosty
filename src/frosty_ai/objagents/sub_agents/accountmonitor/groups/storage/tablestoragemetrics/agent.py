from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_storage_metrics_for_table,
    get_storage_metrics_for_schema,
    get_storage_metrics_for_database,
    get_deleted_tables,
    get_tables_with_failsafe_bytes,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_table_storage_metrics = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_storage_metrics_for_table,
        get_storage_metrics_for_schema,
        get_storage_metrics_for_database,
        get_deleted_tables,
        get_tables_with_failsafe_bytes,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
