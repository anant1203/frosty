from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_table_exists,
    list_tables_in_schema,
    get_table_properties,
    count_transient_tables,
    filter_tables_by_size,
    get_tables_by_type
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_table = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_table_exists,
        list_tables_in_schema,
        get_table_properties,
        count_transient_tables,
        filter_tables_by_size,
        get_tables_by_type
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
