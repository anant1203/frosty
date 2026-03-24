from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_schemas_in_database,
    is_existing_schema,
    get_schema,
    get_schemas_by_owner,
    get_transient_schemas,
    get_deleted_schemas,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_schemata = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_schemas_in_database,
        is_existing_schema,
        get_schema,
        get_schemas_by_owner,
        get_transient_schemas,
        get_deleted_schemas,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
