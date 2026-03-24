from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_database_exists,
    get_database_properties,
    list_all_databases,
    count_transient_databases,
    filter_databases_by_retention
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_database = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_database_exists,
        get_database_properties,
        list_all_databases,
        count_transient_databases,
        filter_databases_by_retention
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
