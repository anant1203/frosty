from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_column_exists,
    list_columns_in_table,
    get_column_properties,
    get_column_count,
    get_nullable_columns,
    get_all_column_details,
    get_identity_columns
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_column = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_column_exists,
        list_columns_in_table,
        get_column_properties,
        get_column_count,
        get_nullable_columns,
        get_all_column_details,
        get_identity_columns
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
