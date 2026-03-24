from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_schema_exists,
    list_all_schemas,
    get_schema_properties,
    count_transient_schemas,
    filter_schemas_by_retention
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_schema = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_schema_exists,
        list_all_schemas,
        get_schema_properties,
        count_transient_schemas,
        filter_schemas_by_retention
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
