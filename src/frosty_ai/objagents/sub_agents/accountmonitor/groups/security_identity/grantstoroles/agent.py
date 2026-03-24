from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_grants_for_role,
    get_grants_by_privilege,
    get_grants_on_object,
    get_grants_with_grant_option,
    get_active_grants_for_role,
    get_grants_by_grantor,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_grants_to_roles = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_grants_for_role,
        get_grants_by_privilege,
        get_grants_on_object,
        get_grants_with_grant_option,
        get_active_grants_for_role,
        get_grants_by_grantor,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
