from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_all_active_roles,
    is_existing_role,
    get_role,
    get_roles_by_owner,
    get_deleted_roles,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_roles = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_all_active_roles,
        is_existing_role,
        get_role,
        get_roles_by_owner,
        get_deleted_roles,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
