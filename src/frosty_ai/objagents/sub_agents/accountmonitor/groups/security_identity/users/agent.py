from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_user,
    get_all_active_users,
    get_disabled_users,
    is_existing_user,
    get_users_by_default_role,
    get_users_by_default_warehouse,
    get_users_not_logged_in_since,
    get_user_last_login,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_users = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_user,
        get_all_active_users,
        get_disabled_users,
        is_existing_user,
        get_users_by_default_role,
        get_users_by_default_warehouse,
        get_users_not_logged_in_since,
        get_user_last_login,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
