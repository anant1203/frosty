from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_all_active_databases,
    is_existing_database,
    get_database,
    get_databases_by_owner,
    get_transient_databases,
    get_deleted_databases,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_databases = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_all_active_databases,
        is_existing_database,
        get_database,
        get_databases_by_owner,
        get_transient_databases,
        get_deleted_databases,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
